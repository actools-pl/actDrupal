from __future__ import annotations

import copy
import json
from dataclasses import replace
from pathlib import Path

import pytest

from actools.contracts.catalog import validate_contract_document
from actools.contracts.errors import ContractError, EvaluationError
from actools.contracts.evaluation import (
    AdmissionVerification,
    ControlEvaluationInput,
    evaluate_diagnostics,
    evidence_is_admissible,
)
from actools.contracts.models import (
    DiagnosticEvidence,
    EvidenceReference,
    EvidenceState,
    FindingStatus,
    GateImpact,
    GateState,
    RunState,
    Severity,
)

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "tests/fixtures/contracts/valid"


def _control(
    control_id: str,
    *,
    evidence_state: EvidenceState = EvidenceState.VALID,
    observed_status: FindingStatus | None = FindingStatus.PASS,
    severity: Severity = Severity.NONE,
    blocking: bool = False,
    selected: bool = True,
    required: bool = True,
    applicable: bool = True,
) -> ControlEvaluationInput:
    evidence_refs = (
        (
            EvidenceReference(
                evidence_id=f"evidence-{control_id}",
                digest="a" * 64,
                source=f"evidence://store/{control_id}",
                trust="authenticated",
            ),
        )
        if evidence_state
        in {EvidenceState.VALID, EvidenceState.NOT_APPLICABLE_PROVEN}
        else ()
    )
    return ControlEvaluationInput(
        control_id=control_id,
        check_version="1.0.0",
        policy_id="community-baseline",
        selected=selected,
        required=required,
        applicable=applicable,
        prerequisite_ids=(),
        expected_id=f"expected-{control_id}",
        observed_id=(
            None if observed_status is None else f"observed-{control_id}"
        ),
        evidence_state=evidence_state,
        observed_status=observed_status,
        severity=severity,
        blocking=blocking,
        evidence_refs=evidence_refs,
    )


def test_factual_failure_plus_missing_proof_preserves_both_and_exit_precedence() -> None:
    controls = (
        _control(
            "control-firewall",
            observed_status=FindingStatus.FAIL,
            severity=Severity.HIGH,
            blocking=True,
        ),
        _control(
            "control-backup",
            evidence_state=EvidenceState.MISSING,
            observed_status=None,
            severity=Severity.MEDIUM,
        ),
    )
    result = evaluate_diagnostics(controls, policy_id="community-baseline")
    findings = {item.control_id: item for item in result.findings}

    assert result.run_state == RunState.PARTIAL
    assert findings["control-firewall"].status == FindingStatus.FAIL
    assert findings["control-backup"].status == FindingStatus.UNKNOWN
    assert result.coverage.selected.numerator == 1
    assert result.coverage.selected.denominator == 2
    assert result.coverage.selected.gap_ids == ("control-backup",)
    assert result.coverage.full_required_policy == result.coverage.selected
    assert result.gate.gate_state == GateState.BLOCKED
    assert result.gate.blocking_finding_ids == ("control-firewall",)
    assert result.gate.coverage_gap_ids == ("control-backup",)
    assert result.exit_code == 2


def test_exit_codes_have_fixed_engine_coverage_gate_success_precedence() -> None:
    clean = (_control("control-clean"),)
    blocking = (
        _control(
            "control-blocking",
            observed_status=FindingStatus.FAIL,
            severity=Severity.CRITICAL,
            blocking=True,
        ),
    )
    incomplete = (
        _control(
            "control-incomplete",
            evidence_state=EvidenceState.INACCESSIBLE,
            observed_status=None,
            severity=Severity.HIGH,
        ),
    )

    assert evaluate_diagnostics(clean, policy_id="community-baseline").exit_code == 0
    assert (
        evaluate_diagnostics(blocking, policy_id="community-baseline").exit_code
        == 1
    )
    assert (
        evaluate_diagnostics(incomplete, policy_id="community-baseline").exit_code
        == 2
    )
    engine = evaluate_diagnostics(
        incomplete, policy_id="community-baseline", engine_error=True
    )
    assert engine.exit_code == 3
    assert engine.run_state == RunState.ERROR
    assert engine.gate.gate_state == GateState.NOT_EVALUATED


def test_missing_or_incomplete_proof_cannot_become_pass() -> None:
    invalid = (
        _control(
            "control-invalid",
            evidence_state=EvidenceState.MISSING,
            observed_status=FindingStatus.PASS,
        ),
    )
    with pytest.raises(EvaluationError):
        evaluate_diagnostics(invalid, policy_id="community-baseline")

    document = json.loads(
        (VALID / "diagnostic-evidence-1.0.0.json").read_text(encoding="utf-8")
    )
    document["findings"][0]["evidence_state"] = "missing"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("diagnostic-evidence", document)
    assert exc.value.reason == "missing_evidence_cannot_pass"


def test_not_applicable_requires_proof_and_is_excluded_from_denominators() -> None:
    controls = (
        _control("control-required"),
        _control(
            "control-na",
            evidence_state=EvidenceState.NOT_APPLICABLE_PROVEN,
            observed_status=None,
            applicable=False,
        ),
    )
    result = evaluate_diagnostics(controls, policy_id="community-baseline")
    findings = {item.control_id: item for item in result.findings}
    assert findings["control-na"].status == FindingStatus.NOT_APPLICABLE
    assert result.coverage.selected.numerator == 1
    assert result.coverage.selected.denominator == 1
    assert result.coverage.full_required_policy.denominator == 1
    assert result.exit_code == 0

    unproved = (
        _control(
            "control-na",
            evidence_state=EvidenceState.VALID,
            observed_status=FindingStatus.PASS,
            applicable=False,
        ),
    )
    with pytest.raises(EvaluationError):
        evaluate_diagnostics(unproved, policy_id="community-baseline")


def test_selected_and_full_required_coverage_are_independent() -> None:
    controls = (
        _control("control-required"),
        _control(
            "control-optional",
            evidence_state=EvidenceState.MISSING,
            observed_status=None,
            severity=Severity.INFO,
            required=False,
        ),
    )
    result = evaluate_diagnostics(controls, policy_id="community-baseline")
    assert result.coverage.selected.numerator == 1
    assert result.coverage.selected.denominator == 2
    assert result.coverage.selected.complete is False
    assert result.coverage.full_required_policy.numerator == 1
    assert result.coverage.full_required_policy.denominator == 1
    assert result.coverage.full_required_policy.complete is True
    assert result.gate.gate_state == GateState.PASS
    assert result.run_state == RunState.PARTIAL
    assert result.exit_code == 0


def test_unrequested_gate_is_explicitly_not_evaluated() -> None:
    controls = (
        _control(
            "control-failure",
            observed_status=FindingStatus.FAIL,
            severity=Severity.HIGH,
            blocking=True,
        ),
    )
    result = evaluate_diagnostics(
        controls, policy_id="community-baseline", gate_requested=False
    )
    assert result.gate.gate_state == GateState.NOT_EVALUATED
    assert result.findings[0].gate_impact == GateImpact.NOT_EVALUATED
    assert result.exit_code == 1


def test_evaluation_order_is_deterministic_and_inputs_are_unchanged() -> None:
    controls = (_control("control-zulu"), _control("control-alpha"))
    before = copy.deepcopy(controls)
    first = evaluate_diagnostics(controls, policy_id="community-baseline")
    second = evaluate_diagnostics(tuple(reversed(controls)), policy_id="community-baseline")
    assert tuple(item.control_id for item in first.findings) == (
        "control-alpha",
        "control-zulu",
    )
    assert first == second
    assert controls == before


def test_presentation_or_digest_alone_cannot_create_admission() -> None:
    document = json.loads(
        (VALID / "diagnostic-evidence-1.0.0.json").read_text(encoding="utf-8")
    )
    evidence = validate_contract_document("diagnostic-evidence", document)
    assert isinstance(evidence, DiagnosticEvidence)
    provenance = evidence.provenance
    assert evidence_is_admissible(provenance) is False

    verified = AdmissionVerification(
        source_reference=provenance.source_reference,
        verified_digest=provenance.integrity.digest,
        authenticated_source=True,
        digest_verified=True,
        context_matched=True,
        freshness_valid=True,
    )
    assert evidence_is_admissible(provenance, verified) is True
    assert evidence_is_admissible(
        provenance,
        AdmissionVerification(
            source_reference="evidence://store/caller-edited-copy",
            verified_digest=provenance.integrity.digest,
            authenticated_source=True,
            digest_verified=True,
            context_matched=True,
            freshness_valid=True,
        ),
    ) is False

    caller_rehashed = replace(provenance.integrity, digest="5" * 64)
    assert evidence_is_admissible(
        replace(provenance, integrity=caller_rehashed), verified
    ) is False

    presentation = copy.deepcopy(document)
    presentation["provenance"]["presentation_only"] = True
    with pytest.raises(ContractError) as exc:
        validate_contract_document("diagnostic-evidence", presentation)
    assert exc.value.reason == "unsupported_value"
    assert evidence_is_admissible(
        replace(provenance, presentation_only=True), verified
    ) is False


def test_diagnostic_contract_rejects_a_gate_disposition_lie() -> None:
    document = json.loads(
        (VALID / "diagnostic-evidence-1.0.0.json").read_text(encoding="utf-8")
    )
    document["gates"][0]["gate_state"] = "pass"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("diagnostic-evidence", document)
    assert exc.value.reason == "gate_disposition_mismatch"
