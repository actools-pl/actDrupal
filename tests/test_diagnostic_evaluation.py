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
    to_primitive,
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
    prerequisite_ids: tuple[str, ...] = (),
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
        prerequisite_ids=prerequisite_ids,
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


def _serialized_result(
    result, controls: tuple[ControlEvaluationInput, ...]
) -> dict:
    document = json.loads(
        (VALID / "diagnostic-evidence-1.0.0.json").read_text(encoding="utf-8")
    )
    document["run_state"] = result.run_state.value
    document["findings"] = to_primitive(result.findings)
    document["coverage"] = to_primitive(result.coverage)
    document["gates"] = [to_primitive(result.gate)]
    document["attempts"] = [
        {
            "attempt_id": f"attempt-{index}",
            "control_id": control.control_id,
            "collector_id": "host-collector",
            "started_at": "2026-09-13T09:00:00Z",
            "finished_at": "2026-09-13T09:00:01Z",
            "state": "completed",
            "error_id": None,
        }
        for index, control in enumerate(controls, start=1)
    ]
    return document


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


@pytest.mark.parametrize(
    ("selected", "required", "expected_blocks"),
    [
        (True, True, True),
        (True, False, True),
        (False, True, True),
        (False, False, False),
    ],
)
def test_gate_blockers_use_required_or_selected_policy_scope(
    selected: bool, required: bool, expected_blocks: bool
) -> None:
    controls = (
        _control("control-baseline"),
        _control(
            "control-failure",
            observed_status=FindingStatus.FAIL,
            severity=Severity.HIGH,
            blocking=True,
            selected=selected,
            required=required,
        ),
    )
    result = evaluate_diagnostics(controls, policy_id="community-baseline")
    failure = next(
        finding
        for finding in result.findings
        if finding.control_id == "control-failure"
    )
    assert ("control-failure" in result.gate.blocking_finding_ids) is expected_blocks
    assert (failure.gate_impact == GateImpact.BLOCKS) is expected_blocks
    assert result.gate.gate_state == (
        GateState.BLOCKED if expected_blocks else GateState.PASS
    )
    validate_contract_document(
        "diagnostic-evidence", _serialized_result(result, controls)
    )


def test_serialized_gate_cannot_drop_an_unselected_required_blocker() -> None:
    controls = (
        _control(
            "control-required-failure",
            observed_status=FindingStatus.FAIL,
            severity=Severity.HIGH,
            blocking=True,
            selected=False,
        ),
    )
    result = evaluate_diagnostics(controls, policy_id="community-baseline")
    document = _serialized_result(result, controls)
    document["gates"][0].update(
        {
            "gate_state": "pass",
            "blocking_finding_ids": [],
        }
    )
    with pytest.raises(ContractError):
        validate_contract_document("diagnostic-evidence", document)


def test_every_serialized_gate_is_bound_to_owned_policy_evaluation() -> None:
    document = json.loads(
        (VALID / "diagnostic-evidence-1.0.0.json").read_text(encoding="utf-8")
    )
    document["gates"].append(
        {
            "policy_id": "production-admission",
            "gate_state": "pass",
            "blocking_finding_ids": [],
            "coverage_gap_ids": [],
        }
    )
    with pytest.raises(ContractError) as exc:
        validate_contract_document("diagnostic-evidence", document)
    assert exc.value.reason == "gate_without_policy_evaluation"

    document["gates"][-1]["gate_state"] = "not_evaluated"
    validate_contract_document("diagnostic-evidence", document)


def test_zero_required_denominator_and_engine_gate_lies_reject() -> None:
    all_not_applicable = (
        _control(
            "control-na",
            evidence_state=EvidenceState.NOT_APPLICABLE_PROVEN,
            observed_status=None,
            applicable=False,
        ),
    )
    with pytest.raises(EvaluationError):
        evaluate_diagnostics(
            all_not_applicable, policy_id="community-baseline"
        )

    optional_only = (_control("control-optional", required=False),)
    with pytest.raises(EvaluationError):
        evaluate_diagnostics(optional_only, policy_id="community-baseline")

    document = json.loads(
        (VALID / "diagnostic-evidence-1.0.0.json").read_text(encoding="utf-8")
    )
    for finding in document["findings"]:
        finding["required"] = False
    document["coverage"]["full_required_policy"] = {
        "numerator": 0,
        "denominator": 0,
        "gap_ids": [],
    }
    document["gates"][0]["coverage_gap_ids"] = []
    with pytest.raises(ContractError) as exc:
        validate_contract_document("diagnostic-evidence", document)
    assert exc.value.reason == "coverage_required_denominator_empty"

    controls = (_control("control-clean"),)
    result = evaluate_diagnostics(
        controls, policy_id="community-baseline", engine_error=True
    )
    engine = _serialized_result(result, controls)
    validate_contract_document("diagnostic-evidence", engine)
    engine["gates"][0]["gate_state"] = "pass"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("diagnostic-evidence", engine)
    assert exc.value.reason == "gate_disposition_mismatch"


def test_failed_prerequisite_makes_dependent_unknown_without_stopping_peers() -> None:
    controls = (
        _control(
            "control-prerequisite",
            observed_status=FindingStatus.FAIL,
            severity=Severity.HIGH,
            required=False,
        ),
        _control(
            "control-dependent",
            prerequisite_ids=("control-prerequisite",),
        ),
        _control("control-independent"),
    )
    result = evaluate_diagnostics(controls, policy_id="community-baseline")
    findings = {item.control_id: item for item in result.findings}
    assert findings["control-prerequisite"].status == FindingStatus.FAIL
    assert findings["control-dependent"].status == FindingStatus.UNKNOWN
    assert findings["control-dependent"].evidence_state == EvidenceState.VALID
    assert findings["control-dependent"].observed_id == "observed-control-dependent"
    assert findings["control-dependent"].observed_status == FindingStatus.PASS
    assert "prerequisite-not-satisfied" in findings["control-dependent"].error_ids
    assert findings["control-independent"].status == FindingStatus.PASS
    assert result.coverage.full_required_policy.gap_ids == ("control-dependent",)
    assert result.exit_code == 2
    document = _serialized_result(result, controls)
    validate_contract_document("diagnostic-evidence", document)

    forged = copy.deepcopy(document)
    dependent = next(
        finding
        for finding in forged["findings"]
        if finding["control_id"] == "control-dependent"
    )
    dependent.update(
        {
            "status": "PASS",
            "error_ids": [],
            "gate_impact": "does-not-block",
        }
    )
    forged["coverage"]["selected"].update(
        {"numerator": 3, "gap_ids": []}
    )
    forged["coverage"]["full_required_policy"].update(
        {"numerator": 2, "gap_ids": []}
    )
    forged["gates"][0].update(
        {"gate_state": "pass", "coverage_gap_ids": []}
    )
    with pytest.raises(ContractError) as exc:
        validate_contract_document("diagnostic-evidence", forged)
    assert exc.value.reason == "finding_prerequisite_outcome_mismatch"


def test_missing_prerequisite_also_makes_the_dependent_unknown() -> None:
    controls = (
        _control(
            "control-prerequisite",
            evidence_state=EvidenceState.MISSING,
            observed_status=None,
            severity=Severity.MEDIUM,
            required=False,
        ),
        _control(
            "control-dependent",
            prerequisite_ids=("control-prerequisite",),
        ),
    )
    result = evaluate_diagnostics(controls, policy_id="community-baseline")
    findings = {item.control_id: item for item in result.findings}
    assert findings["control-prerequisite"].status == FindingStatus.UNKNOWN
    assert findings["control-dependent"].status == FindingStatus.UNKNOWN
    assert findings["control-dependent"].observed_status == FindingStatus.PASS
    assert result.coverage.full_required_policy.gap_ids == ("control-dependent",)
    assert result.exit_code == 2
    validate_contract_document(
        "diagnostic-evidence", _serialized_result(result, controls)
    )


def test_prerequisite_graph_rejects_unknown_self_and_cycles() -> None:
    invalid_sets = (
        (_control("control-a", prerequisite_ids=("control-missing",)),),
        (_control("control-a", prerequisite_ids=("control-a",)),),
        (_control("control-a", prerequisite_ids=("control-b", "control-b")),
         _control("control-b")),
        (
            _control("control-a", prerequisite_ids=("control-b",)),
            _control("control-b", prerequisite_ids=("control-a",)),
        ),
    )
    for controls in invalid_sets:
        with pytest.raises(EvaluationError):
            evaluate_diagnostics(controls, policy_id="community-baseline")


def test_valid_dependency_is_order_independent_and_substitute_evidence_survives() -> None:
    controls = (
        _control("control-prerequisite"),
        _control(
            "control-dependent",
            prerequisite_ids=("control-prerequisite",),
        ),
    )
    first = evaluate_diagnostics(controls, policy_id="community-baseline")
    second = evaluate_diagnostics(
        tuple(reversed(controls)), policy_id="community-baseline"
    )
    assert first == second
    assert all(item.status == FindingStatus.PASS for item in first.findings)

    document = _serialized_result(first, controls)
    document["attempts"][0].update(
        {"state": "failed", "error_id": "fresh-collection-failed"}
    )
    validate_contract_document("diagnostic-evidence", document)


def test_diagnostic_times_use_calendar_valid_fractional_utc_order() -> None:
    document = json.loads(
        (VALID / "diagnostic-evidence-1.0.0.json").read_text(encoding="utf-8")
    )
    document["captured_at"] = "2026-09-13T09:00:00Z"
    document["evaluated_at"] = "2026-09-13T09:00:00.1Z"
    document["valid_until"] = "2026-09-13T09:00:00.100000001Z"
    validate_contract_document("diagnostic-evidence", document)

    equivalent = copy.deepcopy(document)
    equivalent["captured_at"] = "2026-09-13T09:00:00.0Z"
    validate_contract_document("diagnostic-evidence", equivalent)

    reversed_time = copy.deepcopy(document)
    reversed_time["captured_at"] = "2026-09-13T09:00:00.2Z"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("diagnostic-evidence", reversed_time)
    assert exc.value.reason == "evidence_time_order_invalid"

    impossible = copy.deepcopy(document)
    impossible["evaluated_at"] = "2026-04-31T09:00:00Z"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("diagnostic-evidence", impossible)
    assert exc.value.reason == "invalid_format"

    reversed_attempt = copy.deepcopy(document)
    reversed_attempt["attempts"][0].update(
        {
            "started_at": "2026-09-13T09:00:00.2Z",
            "finished_at": "2026-09-13T09:00:00.1Z",
        }
    )
    with pytest.raises(ContractError) as exc:
        validate_contract_document("diagnostic-evidence", reversed_attempt)
    assert exc.value.reason == "attempt_time_order_invalid"


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
