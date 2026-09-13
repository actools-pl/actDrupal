"""Deterministic pure diagnostic evaluation and admission predicates."""

from __future__ import annotations

from dataclasses import dataclass, replace

from .errors import EvaluationError
from .models import (
    Coverage,
    CoveragePair,
    EvidenceProvenance,
    EvidenceReference,
    EvidenceState,
    Finding,
    FindingStatus,
    GateEvaluation,
    GateImpact,
    GateState,
    RunState,
    Severity,
)


@dataclass(frozen=True, slots=True)
class ControlEvaluationInput:
    """One policy control and its already-collected, non-executable observation."""

    control_id: str
    check_version: str
    policy_id: str
    selected: bool
    required: bool
    applicable: bool
    prerequisite_ids: tuple[str, ...]
    expected_id: str
    observed_id: str | None
    evidence_state: EvidenceState
    observed_status: FindingStatus | None
    severity: Severity
    blocking: bool
    evidence_refs: tuple[EvidenceReference, ...] = ()
    error_ids: tuple[str, ...] = ()
    remedy_id: str | None = None
    exception_id: str | None = None


@dataclass(frozen=True, slots=True)
class DiagnosticEvaluation:
    run_state: RunState
    findings: tuple[Finding, ...]
    coverage: CoveragePair
    gate: GateEvaluation
    exit_code: int


@dataclass(frozen=True, slots=True)
class AdmissionVerification:
    """Facts established outside presentation by a future trusted evidence reader."""

    source_reference: str
    verified_digest: str
    authenticated_source: bool
    digest_verified: bool
    context_matched: bool
    freshness_valid: bool


_ASSESSED = {
    FindingStatus.PASS,
    FindingStatus.FAIL,
    FindingStatus.WARN,
}
_SATISFIED_PREREQUISITES = {
    FindingStatus.PASS,
    FindingStatus.NOT_APPLICABLE,
}
_PREREQUISITE_ERROR_ID = "prerequisite-not-satisfied"


def _finding_status(item: ControlEvaluationInput) -> tuple[FindingStatus, bool]:
    if item.evidence_state == EvidenceState.NOT_APPLICABLE_PROVEN:
        if item.applicable:
            raise EvaluationError("applicable control cannot use not-applicable proof")
        if item.observed_status is not None:
            raise EvaluationError("not-applicable control cannot carry an observed status")
        if not item.evidence_refs:
            raise EvaluationError("not-applicable status requires applicability proof")
        return FindingStatus.NOT_APPLICABLE, False

    effective_applicable = True
    if not item.applicable:
        if item.evidence_state not in {
            EvidenceState.MISSING,
            EvidenceState.STALE,
            EvidenceState.INACCESSIBLE,
            EvidenceState.MALFORMED,
            EvidenceState.UNSUPPORTED,
            EvidenceState.INCONCLUSIVE,
            EvidenceState.SKIPPED,
        }:
            raise EvaluationError("non-applicability requires explicit proof")

    if item.evidence_state == EvidenceState.VALID:
        if item.observed_status not in _ASSESSED:
            raise EvaluationError("valid evidence requires PASS, FAIL or WARN")
        if item.observed_id is None or not item.evidence_refs:
            raise EvaluationError("valid evidence requires observation proof")
        return item.observed_status, effective_applicable
    if item.observed_status is not None:
        raise EvaluationError("incomplete evidence cannot carry a factual status")
    if item.evidence_state == EvidenceState.SKIPPED:
        return FindingStatus.SKIPPED, effective_applicable
    return FindingStatus.UNKNOWN, effective_applicable


def _coverage(findings: tuple[Finding, ...], *, selected: bool) -> Coverage:
    eligible = tuple(
        item
        for item in findings
        if item.applicable and (item.selected if selected else item.required)
    )
    assessed = tuple(item for item in eligible if item.status in _ASSESSED)
    gaps = tuple(sorted(item.control_id for item in eligible if item.status not in _ASSESSED))
    return Coverage(len(assessed), len(eligible), gaps)


def _dependency_order(
    controls: tuple[ControlEvaluationInput, ...],
) -> tuple[ControlEvaluationInput, ...]:
    by_id = {item.control_id: item for item in controls}
    for item in controls:
        prerequisites = item.prerequisite_ids
        if len(prerequisites) != len(set(prerequisites)):
            raise EvaluationError("prerequisite identifiers must be unique")
        if item.control_id in prerequisites:
            raise EvaluationError("control cannot depend on itself")
        if any(prerequisite_id not in by_id for prerequisite_id in prerequisites):
            raise EvaluationError("prerequisite control is unknown")

    state: dict[str, int] = {}
    ordered: list[ControlEvaluationInput] = []

    def visit(control_id: str) -> None:
        marker = state.get(control_id, 0)
        if marker == 1:
            raise EvaluationError("prerequisite cycle is not permitted")
        if marker == 2:
            return
        state[control_id] = 1
        item = by_id[control_id]
        for prerequisite_id in sorted(item.prerequisite_ids):
            visit(prerequisite_id)
        state[control_id] = 2
        ordered.append(item)

    for control_id in sorted(by_id):
        visit(control_id)
    return tuple(ordered)


def _blocks_gate(item: Finding) -> bool:
    return (
        item.applicable
        and item.blocking
        and (item.required or item.selected)
    )


def evaluate_diagnostics(
    controls: tuple[ControlEvaluationInput, ...],
    *,
    policy_id: str,
    gate_requested: bool = True,
    engine_error: bool = False,
) -> DiagnosticEvaluation:
    """Evaluate controls with fixed 3 > 2 > 1 > 0 diagnostic precedence."""
    if not controls:
        raise EvaluationError("zero-control inventory cannot be evaluated")
    identifiers = [item.control_id for item in controls]
    if len(identifiers) != len(set(identifiers)):
        raise EvaluationError("control identifiers must be unique")
    if any(item.policy_id != policy_id for item in controls):
        raise EvaluationError("control policy identity mismatch")

    resolved: dict[
        str,
        tuple[
            FindingStatus,
            bool,
            EvidenceState,
            str | None,
            tuple[str, ...],
            bool,
        ],
    ] = {}
    for item in _dependency_order(controls):
        status, effective_applicable = _finding_status(item)
        if item.blocking and status not in {FindingStatus.FAIL, FindingStatus.WARN}:
            raise EvaluationError("only factual FAIL or WARN may be blocking")
        if (
            status in {FindingStatus.PASS, FindingStatus.NOT_APPLICABLE}
            and item.severity != Severity.NONE
        ):
            raise EvaluationError("PASS and NOT_APPLICABLE severity must be none")

        evidence_state = item.evidence_state
        observed_id = item.observed_id
        error_ids = tuple(sorted(item.error_ids))
        blocking = item.blocking
        if effective_applicable and any(
            resolved[prerequisite_id][0] not in _SATISFIED_PREREQUISITES
            for prerequisite_id in item.prerequisite_ids
        ):
            status = FindingStatus.UNKNOWN
            error_ids = tuple(sorted({*error_ids, _PREREQUISITE_ERROR_ID}))
            blocking = False
        resolved[item.control_id] = (
            status,
            effective_applicable,
            evidence_state,
            observed_id,
            error_ids,
            blocking,
        )

    gate_active = gate_requested and not engine_error
    preliminary: list[Finding] = []
    for item in sorted(controls, key=lambda control: control.control_id):
        (
            status,
            effective_applicable,
            evidence_state,
            observed_id,
            error_ids,
            blocking,
        ) = resolved[item.control_id]
        preliminary.append(
            Finding(
                control_id=item.control_id,
                check_version=item.check_version,
                policy_id=item.policy_id,
                selected=item.selected,
                required=item.required,
                applicable=effective_applicable,
                prerequisite_ids=tuple(sorted(item.prerequisite_ids)),
                expected_id=item.expected_id,
                observed_id=observed_id,
                observed_status=item.observed_status,
                evidence_state=evidence_state,
                status=status,
                severity=item.severity,
                blocking=blocking,
                evidence_refs=tuple(item.evidence_refs),
                error_ids=error_ids,
                remedy_id=item.remedy_id,
                exception_id=item.exception_id,
                gate_impact=GateImpact.NOT_EVALUATED,
            )
        )

    immutable_preliminary = tuple(preliminary)
    blocker_ids = {
        item.control_id for item in immutable_preliminary if _blocks_gate(item)
    }
    findings: list[Finding] = []
    for item in immutable_preliminary:
        findings.append(
            replace(
                item,
                gate_impact=(
                    GateImpact.NOT_EVALUATED
                    if not gate_active
                    else (
                        GateImpact.BLOCKS
                        if item.control_id in blocker_ids
                        else GateImpact.DOES_NOT_BLOCK
                    )
                ),
            )
        )

    immutable_findings = tuple(findings)
    selected_coverage = _coverage(immutable_findings, selected=True)
    full_coverage = _coverage(immutable_findings, selected=False)
    if full_coverage.denominator == 0:
        raise EvaluationError("required-policy denominator cannot be zero")
    coverage = CoveragePair(selected_coverage, full_coverage)
    blockers = tuple(sorted(blocker_ids))

    has_incomplete_observation = any(
        item.status in {FindingStatus.UNKNOWN, FindingStatus.SKIPPED}
        for item in immutable_findings
    )
    run_state = (
        RunState.ERROR
        if engine_error
        else RunState.PARTIAL
        if has_incomplete_observation
        else RunState.COMPLETE
    )
    if not gate_active:
        gate_state = GateState.NOT_EVALUATED
    elif full_coverage.gap_ids or blockers:
        gate_state = GateState.BLOCKED
    else:
        gate_state = GateState.PASS
    gate = GateEvaluation(
        policy_id=policy_id,
        gate_state=gate_state,
        blocking_finding_ids=blockers if gate_active else (),
        coverage_gap_ids=full_coverage.gap_ids if gate_active else (),
    )

    if engine_error:
        exit_code = 3
    elif full_coverage.gap_ids:
        exit_code = 2
    elif blockers:
        exit_code = 1
    else:
        exit_code = 0
    return DiagnosticEvaluation(run_state, immutable_findings, coverage, gate, exit_code)


def evidence_is_admissible(
    provenance: EvidenceProvenance,
    verification: AdmissionVerification | None = None,
) -> bool:
    """Require independent source verification; a model or digest alone is never enough."""
    if verification is None or provenance.presentation_only:
        return False
    return (
        provenance.authentication.state == "authenticated"
        and provenance.integrity.verified
        and provenance.context_matched
        and provenance.freshness_valid
        and verification.source_reference == provenance.source_reference
        and verification.verified_digest == provenance.integrity.digest
        and verification.authenticated_source
        and verification.digest_verified
        and verification.context_matched
        and verification.freshness_valid
    )
