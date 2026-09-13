"""Immutable typed models generated from the CP-003 closed contract schemas."""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import StrEnum
from typing import TypeAlias


class DecisionStatus(StrEnum):
    ACCEPTED = "accepted"
    ACCEPTED_WITH_DEFERRED_SCOPE = "accepted-with-deferred-scope"
    CHANGED = "changed"
    DEFERRED = "deferred"
    CONDITIONAL = "conditional"


class ImplementationStatus(StrEnum):
    NOT_IMPLEMENTED = "not-implemented"
    PARTIAL = "partial"
    IMPLEMENTED = "implemented"


class NodeKind(StrEnum):
    FEATURE = "feature"
    WORK_PACKAGE = "work-package"
    GATE = "gate"
    UX_REQUIREMENT = "ux-requirement"
    SECURITY_REFINEMENT = "security-refinement"
    SECURITY_CASE = "security-case"


class MappingStatus(StrEnum):
    RESOLVED = "resolved"
    PARTIAL = "partial"
    UNRESOLVED = "unresolved"


class RuntimeEvidenceStatus(StrEnum):
    NOT_EVALUATED = "not-evaluated"
    PASS = "pass"
    FAIL = "fail"
    UNKNOWN = "unknown"
    STALE = "stale"


class ApplicabilityPredicate(StrEnum):
    ALWAYS = "always"
    WHEN_SELECTED = "when-selected"
    WHEN_ENABLED = "when-enabled"
    FUTURE_DECISION = "future-decision"


class StageState(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"
    INTERRUPTED = "interrupted"


class RunState(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    ERROR = "error"


class FindingStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"
    UNKNOWN = "UNKNOWN"
    SKIPPED = "SKIPPED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class Severity(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"
    NONE = "none"


class GateState(StrEnum):
    PASS = "pass"
    BLOCKED = "blocked"
    NOT_EVALUATED = "not_evaluated"


class EvidenceState(StrEnum):
    VALID = "valid"
    MISSING = "missing"
    STALE = "stale"
    INACCESSIBLE = "inaccessible"
    MALFORMED = "malformed"
    UNSUPPORTED = "unsupported"
    INCONCLUSIVE = "inconclusive"
    SKIPPED = "skipped"
    NOT_APPLICABLE_PROVEN = "not-applicable-proven"


class GateImpact(StrEnum):
    BLOCKS = "blocks"
    DOES_NOT_BLOCK = "does-not-block"
    NOT_EVALUATED = "not-evaluated"


class CommandOutcome(StrEnum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"
    INTERRUPTED = "interrupted"
    NOT_EVALUATED = "not-evaluated"


class DeliveryStatus(StrEnum):
    DELIVERED = "delivered"
    FAILED = "failed"
    NOT_REQUESTED = "not-requested"


class BackupCommitStatus(StrEnum):
    UNCOMMITTED = "uncommitted"
    COMMITTED = "committed"
    FAILED = "failed"


class RestoreProofStatus(StrEnum):
    NOT_RUN = "not-run"
    PASS = "pass"
    FAIL = "fail"
    STALE = "stale"


@dataclass(frozen=True, slots=True)
class Target:
    installation_id: str
    site_id: str
    environment_id: str


@dataclass(frozen=True, slots=True)
class ArtifactReference:
    artifact_id: str
    media_type: str
    digest: str
    source: str


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    evidence_id: str
    digest: str
    source: str
    trust: str


@dataclass(frozen=True, slots=True)
class MigrationEdge:
    from_version: str
    to_version: str
    migration_id: str


@dataclass(frozen=True, slots=True)
class ContractRegistration:
    family: str
    owner: str
    schema_version: str
    schema_resource: str
    policy_resource: str | None
    reader_versions: tuple[str, ...]
    writer_version: str
    migration_edges: tuple[MigrationEdge, ...]
    field_groups: tuple[str, ...]
    artifact_boundary: str
    mutation_authority: str


@dataclass(frozen=True, slots=True)
class SafeNextActionRegistration:
    action_id: str
    documentation_id: str
    source: str


@dataclass(frozen=True, slots=True)
class ContractCatalog:
    schema_version: str
    catalog_id: str
    profile: str
    json_schema_dialect: str
    canonicalization: str
    action_vocabulary: tuple[str, ...]
    diagnostic_formats: tuple[str, ...]
    safe_next_actions: tuple[SafeNextActionRegistration, ...]
    contracts: tuple[ContractRegistration, ...]


@dataclass(frozen=True, slots=True)
class RuntimeEvidence:
    status: RuntimeEvidenceStatus
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Applicability:
    predicate: ApplicabilityPredicate
    capability_id: str | None
    mapping_status: MappingStatus


@dataclass(frozen=True, slots=True)
class TestMapping:
    status: MappingStatus
    acceptance_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ContractMapping:
    status: MappingStatus
    authority_ids: tuple[str, ...]
    secret_ids: tuple[str, ...]
    endpoint_ids: tuple[str, ...]
    resource_ids: tuple[str, ...]
    action_ids: tuple[str, ...]
    handler_ids: tuple[str, ...]
    schema_ids: tuple[str, ...]
    schema_update_ids: tuple[str, ...]
    probe_ids: tuple[str, ...]
    recovery_constituent_ids: tuple[str, ...]
    disable_behavior: str
    rollback_behavior: str
    support_profiles: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RequirementNode:
    id: str
    kind: NodeKind
    title: str
    parent_feature_ids: tuple[str, ...]
    parent_mapping_status: MappingStatus
    source_refs: tuple[str, ...]
    decision_status: DecisionStatus
    decision_detail: str
    implementation_status: ImplementationStatus
    advertised_support: bool
    runtime_evidence: RuntimeEvidence
    applicability: Applicability
    owner_ids: tuple[str, ...]
    dependency_ids: tuple[str, ...]
    dependency_mapping_status: MappingStatus
    refines_ids: tuple[str, ...]
    supersedes_ids: tuple[str, ...]
    relationship_mapping_status: MappingStatus
    test_mapping: TestMapping
    contract_mapping: ContractMapping
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RequirementCounts:
    feature: int
    work_package: int
    gate: int
    ux_requirement: int
    security_refinement: int
    security_case: int
    total: int


@dataclass(frozen=True, slots=True)
class RequirementGraph:
    schema_version: str
    graph_id: str
    profile: str
    architecture_version: str
    architecture_sha256: str
    expected_counts: RequirementCounts
    nodes: tuple[RequirementNode, ...]


@dataclass(frozen=True, slots=True)
class RequestIdentity:
    request_id: str
    schema_version: str
    action: str
    digest: str


@dataclass(frozen=True, slots=True)
class ActorRequirement:
    authority_id: str
    authenticated_actor_required: bool
    approval_required: bool


@dataclass(frozen=True, slots=True)
class ProtectedResources:
    source_ids: tuple[str, ...]
    destination_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class StateFingerprint:
    resource_id: str
    digest: str
    generation: int
    relevance: str


@dataclass(frozen=True, slots=True)
class ContextDigests:
    release: str
    configuration: str
    policy: str


@dataclass(frozen=True, slots=True)
class PlannedEffect:
    effect_id: str
    effect_type: str
    resource_id: str
    description: str
    irreversible: bool


@dataclass(frozen=True, slots=True)
class Disruption:
    level: str
    expected_seconds: int
    maximum_seconds: int
    description: str


@dataclass(frozen=True, slots=True)
class PlannedCheck:
    check_id: str
    description: str
    evidence_required: bool


@dataclass(frozen=True, slots=True)
class RecoveryRequirement:
    checkpoint_required: bool
    checkpoint_id: str | None
    rollback_strategy: str
    description: str


@dataclass(frozen=True, slots=True)
class IrreversibleBoundary:
    effect_id: str
    description: str
    acknowledgement_id: str


@dataclass(frozen=True, slots=True)
class PlanReview:
    required: bool
    review_identity: str
    reviewed_plan_digest: str
    reviewed_at: str
    expires_at: str


@dataclass(frozen=True, slots=True)
class Plan:
    schema_version: str
    canonicalization: str
    plan_id: str
    operation_id: str
    action: str
    request: RequestIdentity
    actor_requirements: tuple[ActorRequirement, ...]
    target: Target
    protected_resources: ProtectedResources
    fingerprints: tuple[StateFingerprint, ...]
    collected_at: str
    expires_at: str
    context_digests: ContextDigests
    required_capabilities: tuple[str, ...]
    effects: tuple[PlannedEffect, ...]
    disruption: Disruption
    preconditions: tuple[PlannedCheck, ...]
    postconditions: tuple[PlannedCheck, ...]
    recovery: RecoveryRequirement
    irreversible_boundaries: tuple[IrreversibleBoundary, ...]
    review: PlanReview


@dataclass(frozen=True, slots=True)
class AuthenticatedActor:
    subject_id: str
    authentication_method: str
    authentication_reference: str


@dataclass(frozen=True, slots=True)
class ResourceLock:
    lock_id: str
    resource_id: str
    owner_operation_id: str
    acquired_at: str


@dataclass(frozen=True, slots=True)
class OperationAttempt:
    attempt_id: str
    effect_id: str
    state: StageState
    started_at: str
    finished_at: str | None
    deadline_at: str


@dataclass(frozen=True, slots=True)
class OperationDeadlines:
    operation_deadline_at: str
    lock_deadline_at: str
    safety_deadline_at: str


@dataclass(frozen=True, slots=True)
class HandlerIdentity:
    handler_id: str
    version: str
    release_digest: str


@dataclass(frozen=True, slots=True)
class Postcondition:
    check_id: str
    required: bool
    state: str
    evidence_id: str | None


@dataclass(frozen=True, slots=True)
class JournalError:
    error_id: str
    source: str
    message_id: str
    evidence_id: str | None


@dataclass(frozen=True, slots=True)
class Reconciliation:
    classification: str
    required: bool
    reason_id: str


@dataclass(frozen=True, slots=True)
class CleanupObligation:
    cleanup_id: str
    resource_id: str
    state: str
    deadline_at: str | None


@dataclass(frozen=True, slots=True)
class OperationJournal:
    schema_version: str
    journal_id: str
    operation_id: str
    plan_id: str
    plan_digest: str
    state: StageState
    actor: AuthenticatedActor
    protected_target_ids: tuple[str, ...]
    locks: tuple[ResourceLock, ...]
    predecessor_generation: int
    target_generation: int
    intent_at: str
    attempts: tuple[OperationAttempt, ...]
    deadlines: OperationDeadlines
    handler: HandlerIdentity
    expected_postconditions: tuple[Postcondition, ...]
    evidence_refs: tuple[EvidenceReference, ...]
    error: JournalError | None
    reconciliation: Reconciliation
    cleanup_obligations: tuple[CleanupObligation, ...]


@dataclass(frozen=True, slots=True)
class ReleaseArtifact:
    artifact_id: str
    kind: str
    digest: str
    source: str


@dataclass(frozen=True, slots=True)
class DependencyIdentity:
    name: str
    version: str
    digest: str
    license_id: str


@dataclass(frozen=True, slots=True)
class PlatformProfile:
    profile: str
    os: str
    architecture: str
    runtime_backend: str
    advertised: bool


@dataclass(frozen=True, slots=True)
class ContractCompatibility:
    family: str
    reader_versions: tuple[str, ...]
    writer_version: str


@dataclass(frozen=True, slots=True)
class VersionEdge:
    from_version: str
    to_version: str
    edge_id: str
    classification: str


@dataclass(frozen=True, slots=True)
class SecurityFloor:
    policy_id: str
    policy_version: str
    digest: str


@dataclass(frozen=True, slots=True)
class ReleaseVerification:
    signature_scheme: str
    signature_reference: str
    trust_root_reference: str
    verified_at: str


@dataclass(frozen=True, slots=True)
class QualificationReceipt:
    receipt_id: str
    gate_id: str
    target: str
    result: str
    digest: str


@dataclass(frozen=True, slots=True)
class ReleaseManifest:
    schema_version: str
    release_id: str
    release_version: str
    source_commit: str
    artifacts: tuple[ReleaseArtifact, ...]
    dependencies: tuple[DependencyIdentity, ...]
    license_references: tuple[str, ...]
    sbom_references: tuple[str, ...]
    platform_profiles: tuple[PlatformProfile, ...]
    contract_compatibility: tuple[ContractCompatibility, ...]
    schema_update_edges: tuple[VersionEdge, ...]
    recovery_edges: tuple[VersionEdge, ...]
    upgrade_edges: tuple[VersionEdge, ...]
    requirement_graph_digest: str
    configuration_template_digest: str
    security_floor: SecurityFloor
    verification: ReleaseVerification
    qualification_receipts: tuple[QualificationReceipt, ...]


@dataclass(frozen=True, slots=True)
class CollectorIdentity:
    collector_id: str
    version: str
    identity: str
    source_kind: str


@dataclass(frozen=True, slots=True)
class DiagnosticContext:
    release_digest: str
    configuration_digest: str
    policy_id: str
    policy_version: str
    capability_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Finding:
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
    status: FindingStatus
    severity: Severity
    blocking: bool
    evidence_refs: tuple[EvidenceReference, ...]
    error_ids: tuple[str, ...]
    remedy_id: str | None
    exception_id: str | None
    gate_impact: GateImpact


@dataclass(frozen=True, slots=True)
class Coverage:
    numerator: int
    denominator: int
    gap_ids: tuple[str, ...]

    @property
    def complete(self) -> bool:
        return self.denominator > 0 and self.numerator == self.denominator


@dataclass(frozen=True, slots=True)
class CoveragePair:
    selected: Coverage
    full_required_policy: Coverage


@dataclass(frozen=True, slots=True)
class GateEvaluation:
    policy_id: str
    gate_state: GateState
    blocking_finding_ids: tuple[str, ...]
    coverage_gap_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CollectionAttempt:
    attempt_id: str
    control_id: str
    collector_id: str
    started_at: str
    finished_at: str
    state: str
    error_id: str | None


@dataclass(frozen=True, slots=True)
class EffectRecord:
    effect_id: str
    effect_class: str
    target_id: str
    authorized: bool
    outcome: str


@dataclass(frozen=True, slots=True)
class CleanupRecord:
    effect_id: str
    required: bool
    outcome: str
    evidence_id: str | None


@dataclass(frozen=True, slots=True)
class Authentication:
    state: str
    reference: str | None


@dataclass(frozen=True, slots=True)
class Integrity:
    algorithm: str
    digest: str
    verified: bool


@dataclass(frozen=True, slots=True)
class EvidenceProvenance:
    source_kind: str
    source_reference: str
    authentication: Authentication
    integrity: Integrity
    context_matched: bool
    freshness_valid: bool
    presentation_only: bool


@dataclass(frozen=True, slots=True)
class DiagnosticEvidence:
    schema_version: str
    evidence_id: str
    run_id: str
    target: Target
    host_id: str
    boot_id: str
    collector: CollectorIdentity
    context: DiagnosticContext
    captured_at: str
    evaluated_at: str
    valid_until: str
    run_state: RunState
    findings: tuple[Finding, ...]
    coverage: CoveragePair
    gates: tuple[GateEvaluation, ...]
    attempts: tuple[CollectionAttempt, ...]
    artifact_refs: tuple[ArtifactReference, ...]
    effects: tuple[EffectRecord, ...]
    cleanup: tuple[CleanupRecord, ...]
    provenance: EvidenceProvenance


@dataclass(frozen=True, slots=True)
class BackupCapture:
    started_at: str
    completed_at: str
    boundary_id: str
    database_consistency: str
    files_consistency: str


@dataclass(frozen=True, slots=True)
class BackupConstituent:
    constituent_id: str
    kind: str
    required: bool
    size_bytes: int
    digest: str


@dataclass(frozen=True, slots=True)
class BackupRepository:
    repository_id: str
    snapshot_id: str
    transport: str
    availability_verified_at: str


@dataclass(frozen=True, slots=True)
class BackupEncryption:
    scheme: str
    key_id: str
    key_generation: int
    key_present_on_source: bool


@dataclass(frozen=True, slots=True)
class HistoryCoverage:
    applicable: bool
    status: str
    from_timestamp: str | None
    until: str | None
    gap_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ConstituentReceipt:
    constituent_id: str
    receipt_id: str
    status: str
    captured_at: str
    digest_verified: bool


@dataclass(frozen=True, slots=True)
class VerificationResult:
    check_id: str
    status: str
    verified_at: str
    evidence_id: str


@dataclass(frozen=True, slots=True)
class CommitChecks:
    constituents_complete: bool
    authenticated_manifest: bool
    repository_verified: bool
    snapshot_reference_verified: bool


@dataclass(frozen=True, slots=True)
class BackupCommit:
    status: BackupCommitStatus
    committed_at: str | None
    manifest_digest: str
    checks: CommitChecks


@dataclass(frozen=True, slots=True)
class Retention:
    classification: str
    protected_until: str
    maintenance_authority_id: str


@dataclass(frozen=True, slots=True)
class RestoreProof:
    status: RestoreProofStatus
    receipt_id: str | None
    verified_at: str | None
    historical_coverage_status: str


@dataclass(frozen=True, slots=True)
class BackupSet:
    schema_version: str
    set_id: str
    site_id: str
    environment_id: str
    protected_source_id: str
    capture: BackupCapture
    release_reference: str
    configuration_reference: str
    constituents: tuple[BackupConstituent, ...]
    repository: BackupRepository
    encryption: BackupEncryption
    file_history_coverage: HistoryCoverage
    pitr_coverage: HistoryCoverage
    constituent_receipts: tuple[ConstituentReceipt, ...]
    verification_results: tuple[VerificationResult, ...]
    commit: BackupCommit
    retention: Retention
    restore_proof: RestoreProof


@dataclass(frozen=True, slots=True)
class CommandIdentity:
    name: str
    format: str


@dataclass(frozen=True, slots=True)
class VersionResult:
    kind: str
    version: str
    source_commit: str


@dataclass(frozen=True, slots=True)
class ArtifactResult:
    kind: str
    contract_family: str
    contract_version: str
    contract_reference: str
    digest: str


@dataclass(frozen=True, slots=True)
class DiagnosticResult:
    kind: str
    evidence_reference: str
    policy_id: str
    gate_state: GateState
    selected_coverage_complete: bool
    full_required_coverage_complete: bool


@dataclass(frozen=True, slots=True)
class OperationResult:
    kind: str
    journal_reference: str
    durable_state: StageState
    reconciliation_required: bool


@dataclass(frozen=True, slots=True)
class InventoryResult:
    kind: str
    catalog_reference: str
    item_count: int


CommandPayload: TypeAlias = (
    VersionResult | ArtifactResult | DiagnosticResult | OperationResult | InventoryResult
)


@dataclass(frozen=True, slots=True)
class DurableOperationOutcome:
    durable_state: StageState
    recorded: bool
    journal_reference: str
    reconciliation_required: bool


@dataclass(frozen=True, slots=True)
class Delivery:
    status: DeliveryStatus
    stdout_document_count: int
    artifact_reference: ArtifactReference | None
    error_id: str | None


@dataclass(frozen=True, slots=True)
class CommandError:
    error_id: str
    source: str
    message_id: str
    evidence_reference: str | None


@dataclass(frozen=True, slots=True)
class NextAction:
    action_id: str
    source: str
    documentation_id: str


@dataclass(frozen=True, slots=True)
class PresentationMetadata:
    format: str
    rendered_at: str
    artifact_reference: ArtifactReference | None
    admission_authority: str
    creates_evidence: bool
    collects_evidence: bool


@dataclass(frozen=True, slots=True)
class CommandResult:
    schema_version: str
    command: CommandIdentity
    run_id: str
    operation_id: str | None
    target: Target
    run_state: RunState
    outcome: CommandOutcome
    started_at: str
    finished_at: str
    result: CommandPayload
    operation_outcome: DurableOperationOutcome | None
    delivery: Delivery
    errors: tuple[CommandError, ...]
    evidence_refs: tuple[EvidenceReference, ...]
    next_actions: tuple[NextAction, ...]
    presentation: PresentationMetadata


ContractModel: TypeAlias = (
    ContractCatalog
    | RequirementGraph
    | Plan
    | OperationJournal
    | ReleaseManifest
    | DiagnosticEvidence
    | BackupSet
    | CommandResult
)


def to_primitive(value: object) -> object:
    """Convert an owned model to its schema-shaped JSON value."""
    if isinstance(value, StrEnum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {
            ("from" if isinstance(value, HistoryCoverage) and item.name == "from_timestamp" else item.name): to_primitive(
                getattr(value, item.name)
            )
            for item in fields(value)
        }
    if isinstance(value, tuple):
        return [to_primitive(item) for item in value]
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    raise TypeError("value is not an owned contract model")
