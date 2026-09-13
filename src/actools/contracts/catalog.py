"""Single version catalog, strict dispatch and typed contract construction."""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from .canonical import canonical_json_bytes
from .configuration import (
    ConfigurationError,
    contract_schema_validator,
    load_contract_resource,
    parse_json_bytes,
    resolve_configuration,
    validate_contract_limits,
)
from .errors import ContractError, ContractVersionError
from .graph import requirement_graph_model, validate_requirement_graph
from .models import (
    ActorRequirement,
    ArtifactReference,
    ArtifactResult,
    AuthenticatedActor,
    Authentication,
    BackupCapture,
    BackupCommit,
    BackupCommitStatus,
    BackupConstituent,
    BackupEncryption,
    BackupRepository,
    BackupSet,
    CleanupObligation,
    CleanupRecord,
    CollectionAttempt,
    CollectorIdentity,
    CommitChecks,
    CommandError,
    CommandIdentity,
    CommandOutcome,
    CommandResult,
    ConstituentReceipt,
    ContextDigests,
    ContractCatalog,
    ContractCompatibility,
    ContractRegistration,
    Coverage,
    CoveragePair,
    Delivery,
    DeliveryStatus,
    DependencyIdentity,
    DiagnosticContext,
    DiagnosticEvidence,
    DiagnosticResult,
    Disruption,
    DurableOperationOutcome,
    EffectRecord,
    EvidenceProvenance,
    EvidenceReference,
    EvidenceState,
    Finding,
    FindingStatus,
    GateEvaluation,
    GateImpact,
    GateState,
    HandlerIdentity,
    HistoryCoverage,
    Integrity,
    InventoryResult,
    IrreversibleBoundary,
    JournalError,
    MigrationEdge,
    NextAction,
    OperationAttempt,
    OperationDeadlines,
    OperationJournal,
    OperationResult,
    Plan,
    PlannedCheck,
    PlannedEffect,
    PlanReview,
    PlatformProfile,
    Postcondition,
    PresentationMetadata,
    ProtectedResources,
    QualificationReceipt,
    Reconciliation,
    RecoveryRequirement,
    ReleaseArtifact,
    ReleaseManifest,
    ReleaseVerification,
    RequestIdentity,
    ResourceLock,
    RestoreProof,
    RestoreProofStatus,
    Retention,
    RunState,
    SafeNextActionRegistration,
    SecurityFloor,
    Severity,
    StageState,
    StateFingerprint,
    Target,
    VerificationResult,
    VersionEdge,
    VersionResult,
    to_primitive,
)

CATALOG_RESOURCE = "contract-catalog-1.0.0.json"
CATALOG_SCHEMA_RESOURCE = "contract-catalog-1.0.0.schema.json"
SCHEMA_VERSION = "1.0.0"
MAX_GRAPH_AGGREGATE_NODES = 32_768


def _pointer(parts: list[object]) -> str:
    if not parts:
        return "/"
    return "/" + "/".join(
        str(part).replace("~", "~0").replace("/", "~1") for part in parts
    )


def _schema_reason(error: Any) -> str:
    return {
        "additionalProperties": "unknown_property",
        "required": "required_field_missing",
        "format": "invalid_format",
        "minimum": "value_out_of_range",
        "maximum": "value_out_of_range",
        "minLength": "value_out_of_range",
        "maxLength": "value_out_of_range",
        "minItems": "value_out_of_range",
        "maxItems": "value_out_of_range",
        "const": "unsupported_value",
        "enum": "unsupported_value",
        "type": "wrong_type",
        "uniqueItems": "duplicate_array_value",
        "pattern": "invalid_value_syntax",
        "oneOf": "contract_shape_mismatch",
    }.get(getattr(error, "validator", None), "schema_validation_failed")


def _validate_against_schema(
    family: str, document: Mapping[str, Any], schema_resource: str
) -> None:
    try:
        schema = load_contract_resource("schemas", schema_resource)
        if not isinstance(schema, Mapping):
            raise ContractError(family, "/", "schema_resource_invalid")
        validator = contract_schema_validator(schema)
        errors = sorted(
            validator.iter_errors(document),
            key=lambda item: _pointer(list(item.absolute_path)),
        )
    except ConfigurationError as exc:
        raise ContractError(family, exc.path, exc.reason) from None
    if not errors:
        return
    error = errors[0]
    path = list(error.absolute_path)
    if (
        error.validator == "required"
        and isinstance(error.validator_value, list)
        and isinstance(error.instance, dict)
    ):
        missing = [name for name in error.validator_value if name not in error.instance]
        if missing:
            path.append(missing[0])
    raise ContractError(family, _pointer(path), _schema_reason(error))


def _catalog_model(document: Mapping[str, Any]) -> ContractCatalog:
    return ContractCatalog(
        schema_version=document["schema_version"],
        catalog_id=document["catalog_id"],
        profile=document["profile"],
        json_schema_dialect=document["json_schema_dialect"],
        canonicalization=document["canonicalization"],
        action_vocabulary=tuple(document["action_vocabulary"]),
        diagnostic_formats=tuple(document["diagnostic_formats"]),
        safe_next_actions=tuple(
            SafeNextActionRegistration(**item) for item in document["safe_next_actions"]
        ),
        contracts=tuple(
            ContractRegistration(
                family=item["family"],
                owner=item["owner"],
                schema_version=item["schema_version"],
                schema_resource=item["schema_resource"],
                policy_resource=item["policy_resource"],
                reader_versions=tuple(item["reader_versions"]),
                writer_version=item["writer_version"],
                migration_edges=tuple(
                    MigrationEdge(**edge) for edge in item["migration_edges"]
                ),
                field_groups=tuple(item["field_groups"]),
                artifact_boundary=item["artifact_boundary"],
                mutation_authority=item["mutation_authority"],
            )
            for item in document["contracts"]
        ),
    )


def _validate_catalog_semantics(document: Mapping[str, Any]) -> None:
    contracts = document["contracts"]
    families = [item["family"] for item in contracts]
    expected = {
        "configuration",
        "plan",
        "operation-journal",
        "requirement-graph",
        "release-manifest",
        "diagnostic-evidence",
        "backup-set",
        "command-result",
        "contract-catalog",
    }
    if len(families) != len(set(families)) or set(families) != expected:
        raise ContractError("contract-catalog", "/contracts", "catalog_family_inventory_mismatch")
    for index, item in enumerate(contracts):
        if item["writer_version"] not in item["reader_versions"]:
            raise ContractError(
                "contract-catalog",
                f"/contracts/{index}/writer_version",
                "catalog_writer_not_readable",
            )
        expected_schema = f"{item['family']}-1.0.0.schema.json"
        if item["schema_resource"] != expected_schema:
            raise ContractError(
                "contract-catalog",
                f"/contracts/{index}/schema_resource",
                "catalog_schema_identity_mismatch",
            )
        if item["migration_edges"]:
            raise ContractError(
                "contract-catalog",
                f"/contracts/{index}/migration_edges",
                "catalog_unimplemented_migration",
            )


def load_contract_catalog() -> ContractCatalog:
    """Load and validate the only packaged contract/version registry."""
    try:
        document = load_contract_resource("policies", CATALOG_RESOURCE)
    except ConfigurationError as exc:
        raise ContractError("contract-catalog", exc.path, exc.reason) from None
    if not isinstance(document, Mapping):
        raise ContractError("contract-catalog", "/", "root_must_be_object")
    _validate_against_schema("contract-catalog", document, CATALOG_SCHEMA_RESOURCE)
    _validate_catalog_semantics(document)
    return _catalog_model(document)


def registration_for(family: str) -> ContractRegistration:
    """Return the immutable catalog registration for *family*."""
    catalog = load_contract_catalog()
    for registration in catalog.contracts:
        if registration.family == family:
            return registration
    raise ContractError("contract-catalog", "/contracts", "unknown_contract_family")


def canonical_contract_bytes(value: object) -> bytes:
    """Return canonical bytes for a document or immutable owned model."""
    if isinstance(value, Mapping):
        primitive: object = copy.deepcopy(dict(value))
    else:
        primitive = to_primitive(value)
    return canonical_json_bytes(primitive)


def canonical_contract_digest(value: object) -> str:
    """Return the RFC 8785 SHA-256 identity used by the contracts."""
    import hashlib

    return hashlib.sha256(canonical_contract_bytes(value)).hexdigest()


def _target(item: Mapping[str, Any]) -> Target:
    return Target(**item)


def _artifact(item: Mapping[str, Any]) -> ArtifactReference:
    return ArtifactReference(**item)


def _evidence_reference(item: Mapping[str, Any]) -> EvidenceReference:
    return EvidenceReference(**item)


def _plan_model(document: Mapping[str, Any]) -> Plan:
    request = document["request"]
    protected = document["protected_resources"]
    disruption = document["disruption"]
    recovery = document["recovery"]
    review = document["review"]
    return Plan(
        schema_version=document["schema_version"],
        canonicalization=document["canonicalization"],
        plan_id=document["plan_id"],
        operation_id=document["operation_id"],
        action=document["action"],
        request=RequestIdentity(**request),
        actor_requirements=tuple(
            ActorRequirement(**item) for item in document["actor_requirements"]
        ),
        target=_target(document["target"]),
        protected_resources=ProtectedResources(
            tuple(protected["source_ids"]), tuple(protected["destination_ids"])
        ),
        fingerprints=tuple(
            StateFingerprint(**item) for item in document["fingerprints"]
        ),
        collected_at=document["collected_at"],
        expires_at=document["expires_at"],
        context_digests=ContextDigests(**document["context_digests"]),
        required_capabilities=tuple(document["required_capabilities"]),
        effects=tuple(PlannedEffect(**item) for item in document["effects"]),
        disruption=Disruption(**disruption),
        preconditions=tuple(
            PlannedCheck(**item) for item in document["preconditions"]
        ),
        postconditions=tuple(
            PlannedCheck(**item) for item in document["postconditions"]
        ),
        recovery=RecoveryRequirement(**recovery),
        irreversible_boundaries=tuple(
            IrreversibleBoundary(**item)
            for item in document["irreversible_boundaries"]
        ),
        review=PlanReview(**review),
    )


def _operation_model(document: Mapping[str, Any]) -> OperationJournal:
    error = document["error"]
    return OperationJournal(
        schema_version=document["schema_version"],
        journal_id=document["journal_id"],
        operation_id=document["operation_id"],
        plan_id=document["plan_id"],
        plan_digest=document["plan_digest"],
        state=StageState(document["state"]),
        actor=AuthenticatedActor(**document["actor"]),
        protected_target_ids=tuple(document["protected_target_ids"]),
        locks=tuple(ResourceLock(**item) for item in document["locks"]),
        predecessor_generation=document["predecessor_generation"],
        target_generation=document["target_generation"],
        intent_at=document["intent_at"],
        attempts=tuple(
            OperationAttempt(
                attempt_id=item["attempt_id"],
                effect_id=item["effect_id"],
                state=StageState(item["state"]),
                started_at=item["started_at"],
                finished_at=item["finished_at"],
                deadline_at=item["deadline_at"],
            )
            for item in document["attempts"]
        ),
        deadlines=OperationDeadlines(**document["deadlines"]),
        handler=HandlerIdentity(**document["handler"]),
        expected_postconditions=tuple(
            Postcondition(**item) for item in document["expected_postconditions"]
        ),
        evidence_refs=tuple(
            _evidence_reference(item) for item in document["evidence_refs"]
        ),
        error=None if error is None else JournalError(**error),
        reconciliation=Reconciliation(**document["reconciliation"]),
        cleanup_obligations=tuple(
            CleanupObligation(**item) for item in document["cleanup_obligations"]
        ),
    )


def _release_model(document: Mapping[str, Any]) -> ReleaseManifest:
    return ReleaseManifest(
        schema_version=document["schema_version"],
        release_id=document["release_id"],
        release_version=document["release_version"],
        source_commit=document["source_commit"],
        artifacts=tuple(ReleaseArtifact(**item) for item in document["artifacts"]),
        dependencies=tuple(
            DependencyIdentity(**item) for item in document["dependencies"]
        ),
        license_references=tuple(document["license_references"]),
        sbom_references=tuple(document["sbom_references"]),
        platform_profiles=tuple(
            PlatformProfile(**item) for item in document["platform_profiles"]
        ),
        contract_compatibility=tuple(
            ContractCompatibility(
                family=item["family"],
                reader_versions=tuple(item["reader_versions"]),
                writer_version=item["writer_version"],
            )
            for item in document["contract_compatibility"]
        ),
        schema_update_edges=tuple(
            VersionEdge(**item) for item in document["schema_update_edges"]
        ),
        recovery_edges=tuple(
            VersionEdge(**item) for item in document["recovery_edges"]
        ),
        upgrade_edges=tuple(
            VersionEdge(**item) for item in document["upgrade_edges"]
        ),
        requirement_graph_digest=document["requirement_graph_digest"],
        configuration_template_digest=document["configuration_template_digest"],
        security_floor=SecurityFloor(**document["security_floor"]),
        verification=ReleaseVerification(**document["verification"]),
        qualification_receipts=tuple(
            QualificationReceipt(**item)
            for item in document["qualification_receipts"]
        ),
    )


def _diagnostic_model(document: Mapping[str, Any]) -> DiagnosticEvidence:
    provenance = document["provenance"]
    coverage = document["coverage"]
    return DiagnosticEvidence(
        schema_version=document["schema_version"],
        evidence_id=document["evidence_id"],
        run_id=document["run_id"],
        target=_target(document["target"]),
        host_id=document["host_id"],
        boot_id=document["boot_id"],
        collector=CollectorIdentity(**document["collector"]),
        context=DiagnosticContext(
            release_digest=document["context"]["release_digest"],
            configuration_digest=document["context"]["configuration_digest"],
            policy_id=document["context"]["policy_id"],
            policy_version=document["context"]["policy_version"],
            capability_ids=tuple(document["context"]["capability_ids"]),
        ),
        captured_at=document["captured_at"],
        evaluated_at=document["evaluated_at"],
        valid_until=document["valid_until"],
        run_state=RunState(document["run_state"]),
        findings=tuple(
            Finding(
                control_id=item["control_id"],
                check_version=item["check_version"],
                policy_id=item["policy_id"],
                selected=item["selected"],
                required=item["required"],
                applicable=item["applicable"],
                prerequisite_ids=tuple(item["prerequisite_ids"]),
                expected_id=item["expected_id"],
                observed_id=item["observed_id"],
                evidence_state=EvidenceState(item["evidence_state"]),
                status=FindingStatus(item["status"]),
                severity=Severity(item["severity"]),
                blocking=item["blocking"],
                evidence_refs=tuple(
                    _evidence_reference(reference)
                    for reference in item["evidence_refs"]
                ),
                error_ids=tuple(item["error_ids"]),
                remedy_id=item["remedy_id"],
                exception_id=item["exception_id"],
                gate_impact=GateImpact(item["gate_impact"]),
            )
            for item in document["findings"]
        ),
        coverage=CoveragePair(
            selected=Coverage(
                numerator=coverage["selected"]["numerator"],
                denominator=coverage["selected"]["denominator"],
                gap_ids=tuple(coverage["selected"]["gap_ids"]),
            ),
            full_required_policy=Coverage(
                numerator=coverage["full_required_policy"]["numerator"],
                denominator=coverage["full_required_policy"]["denominator"],
                gap_ids=tuple(coverage["full_required_policy"]["gap_ids"]),
            ),
        ),
        gates=tuple(
            GateEvaluation(
                policy_id=item["policy_id"],
                gate_state=GateState(item["gate_state"]),
                blocking_finding_ids=tuple(item["blocking_finding_ids"]),
                coverage_gap_ids=tuple(item["coverage_gap_ids"]),
            )
            for item in document["gates"]
        ),
        attempts=tuple(
            CollectionAttempt(**item) for item in document["attempts"]
        ),
        artifact_refs=tuple(_artifact(item) for item in document["artifact_refs"]),
        effects=tuple(EffectRecord(**item) for item in document["effects"]),
        cleanup=tuple(CleanupRecord(**item) for item in document["cleanup"]),
        provenance=EvidenceProvenance(
            source_kind=provenance["source_kind"],
            source_reference=provenance["source_reference"],
            authentication=Authentication(**provenance["authentication"]),
            integrity=Integrity(**provenance["integrity"]),
            context_matched=provenance["context_matched"],
            freshness_valid=provenance["freshness_valid"],
            presentation_only=provenance["presentation_only"],
        ),
    )


def _history(item: Mapping[str, Any]) -> HistoryCoverage:
    return HistoryCoverage(
        applicable=item["applicable"],
        status=item["status"],
        from_timestamp=item["from"],
        until=item["until"],
        gap_ids=tuple(item["gap_ids"]),
    )


def _backup_model(document: Mapping[str, Any]) -> BackupSet:
    commit = document["commit"]
    proof = document["restore_proof"]
    return BackupSet(
        schema_version=document["schema_version"],
        set_id=document["set_id"],
        site_id=document["site_id"],
        environment_id=document["environment_id"],
        protected_source_id=document["protected_source_id"],
        capture=BackupCapture(**document["capture"]),
        release_reference=document["release_reference"],
        configuration_reference=document["configuration_reference"],
        constituents=tuple(
            BackupConstituent(**item) for item in document["constituents"]
        ),
        repository=BackupRepository(**document["repository"]),
        encryption=BackupEncryption(**document["encryption"]),
        file_history_coverage=_history(document["file_history_coverage"]),
        pitr_coverage=_history(document["pitr_coverage"]),
        constituent_receipts=tuple(
            ConstituentReceipt(**item) for item in document["constituent_receipts"]
        ),
        verification_results=tuple(
            VerificationResult(**item) for item in document["verification_results"]
        ),
        commit=BackupCommit(
            status=BackupCommitStatus(commit["status"]),
            committed_at=commit["committed_at"],
            manifest_digest=commit["manifest_digest"],
            checks=CommitChecks(**commit["checks"]),
        ),
        retention=Retention(**document["retention"]),
        restore_proof=RestoreProof(
            status=RestoreProofStatus(proof["status"]),
            receipt_id=proof["receipt_id"],
            verified_at=proof["verified_at"],
            historical_coverage_status=proof["historical_coverage_status"],
        ),
    )


def _command_payload(item: Mapping[str, Any]):
    kind = item["kind"]
    if kind == "version":
        return VersionResult(**item)
    if kind == "artifact":
        return ArtifactResult(**item)
    if kind == "diagnostic":
        return DiagnosticResult(
            kind=kind,
            evidence_reference=item["evidence_reference"],
            policy_id=item["policy_id"],
            gate_state=GateState(item["gate_state"]),
            selected_coverage_complete=item["selected_coverage_complete"],
            full_required_coverage_complete=item["full_required_coverage_complete"],
        )
    if kind == "operation":
        return OperationResult(
            kind=kind,
            journal_reference=item["journal_reference"],
            durable_state=StageState(item["durable_state"]),
            reconciliation_required=item["reconciliation_required"],
        )
    return InventoryResult(**item)


def _command_model(document: Mapping[str, Any]) -> CommandResult:
    operation = document["operation_outcome"]
    delivery = document["delivery"]
    presentation = document["presentation"]
    return CommandResult(
        schema_version=document["schema_version"],
        command=CommandIdentity(**document["command"]),
        run_id=document["run_id"],
        operation_id=document["operation_id"],
        target=_target(document["target"]),
        run_state=RunState(document["run_state"]),
        outcome=CommandOutcome(document["outcome"]),
        started_at=document["started_at"],
        finished_at=document["finished_at"],
        result=_command_payload(document["result"]),
        operation_outcome=(
            None
            if operation is None
            else DurableOperationOutcome(
                durable_state=StageState(operation["durable_state"]),
                recorded=operation["recorded"],
                journal_reference=operation["journal_reference"],
                reconciliation_required=operation["reconciliation_required"],
            )
        ),
        delivery=Delivery(
            status=DeliveryStatus(delivery["status"]),
            stdout_document_count=delivery["stdout_document_count"],
            artifact_reference=(
                None
                if delivery["artifact_reference"] is None
                else _artifact(delivery["artifact_reference"])
            ),
            error_id=delivery["error_id"],
        ),
        errors=tuple(CommandError(**item) for item in document["errors"]),
        evidence_refs=tuple(
            _evidence_reference(item) for item in document["evidence_refs"]
        ),
        next_actions=tuple(NextAction(**item) for item in document["next_actions"]),
        presentation=PresentationMetadata(
            format=presentation["format"],
            rendered_at=presentation["rendered_at"],
            artifact_reference=(
                None
                if presentation["artifact_reference"] is None
                else _artifact(presentation["artifact_reference"])
            ),
            admission_authority=presentation["admission_authority"],
            creates_evidence=presentation["creates_evidence"],
            collects_evidence=presentation["collects_evidence"],
        ),
    )


def _validate_plan_semantics(document: Mapping[str, Any]) -> None:
    if document["action"] != document["request"]["action"]:
        raise ContractError("plan", "/request/action", "plan_request_action_mismatch")
    if document["expires_at"] <= document["collected_at"]:
        raise ContractError("plan", "/expires_at", "plan_expiry_not_after_collection")
    disruption = document["disruption"]
    if disruption["maximum_seconds"] < disruption["expected_seconds"]:
        raise ContractError(
            "plan", "/disruption/maximum_seconds", "plan_disruption_bound_invalid"
        )
    if document["recovery"]["checkpoint_required"] and document["recovery"][
        "checkpoint_id"
    ] is None:
        raise ContractError(
            "plan", "/recovery/checkpoint_id", "plan_checkpoint_identity_required"
        )
    effect_ids = [item["effect_id"] for item in document["effects"]]
    if len(effect_ids) != len(set(effect_ids)):
        raise ContractError("plan", "/effects", "plan_duplicate_effect_id")
    irreversible = {
        item["effect_id"] for item in document["effects"] if item["irreversible"]
    }
    boundary_ids = {
        item["effect_id"] for item in document["irreversible_boundaries"]
    }
    if irreversible != boundary_ids:
        raise ContractError(
            "plan",
            "/irreversible_boundaries",
            "plan_irreversible_boundary_mismatch",
        )


def _validate_operation_semantics(document: Mapping[str, Any]) -> None:
    if document["target_generation"] < document["predecessor_generation"]:
        raise ContractError(
            "operation-journal",
            "/target_generation",
            "journal_generation_regression",
        )
    attempt_ids = [item["attempt_id"] for item in document["attempts"]]
    if len(attempt_ids) != len(set(attempt_ids)):
        raise ContractError(
            "operation-journal", "/attempts", "journal_duplicate_attempt_id"
        )
    if document["state"] == StageState.SUCCEEDED.value:
        if document["error"] is not None or any(
            item["required"] and item["state"] != "satisfied"
            for item in document["expected_postconditions"]
        ):
            raise ContractError(
                "operation-journal",
                "/state",
                "journal_success_without_postconditions",
            )
    if document["reconciliation"]["required"] != (
        document["reconciliation"]["classification"] != "not-needed"
    ):
        raise ContractError(
            "operation-journal",
            "/reconciliation",
            "journal_reconciliation_mismatch",
        )


def _validate_release_semantics(document: Mapping[str, Any]) -> None:
    for field, identity in (
        ("artifacts", "artifact_id"),
        ("dependencies", "name"),
        ("contract_compatibility", "family"),
        ("qualification_receipts", "receipt_id"),
    ):
        identifiers = [item[identity] for item in document[field]]
        if len(identifiers) != len(set(identifiers)):
            raise ContractError(
                "release-manifest", f"/{field}", "release_duplicate_identity"
            )
    for index, item in enumerate(document["contract_compatibility"]):
        if item["writer_version"] not in item["reader_versions"]:
            raise ContractError(
                "release-manifest",
                f"/contract_compatibility/{index}/writer_version",
                "release_writer_not_readable",
            )
    advertised = any(item["advertised"] for item in document["platform_profiles"])
    if advertised and not any(
        item["result"] == "pass" for item in document["qualification_receipts"]
    ):
        raise ContractError(
            "release-manifest",
            "/platform_profiles",
            "release_advertised_without_qualification",
        )


_VALID_FINDING_STATES = {
    FindingStatus.PASS.value,
    FindingStatus.FAIL.value,
    FindingStatus.WARN.value,
}
_INCOMPLETE_EVIDENCE_STATES = {
    EvidenceState.MISSING.value,
    EvidenceState.STALE.value,
    EvidenceState.INACCESSIBLE.value,
    EvidenceState.MALFORMED.value,
    EvidenceState.UNSUPPORTED.value,
    EvidenceState.INCONCLUSIVE.value,
}


def _validate_diagnostic_semantics(document: Mapping[str, Any]) -> None:
    if not (
        document["captured_at"]
        <= document["evaluated_at"]
        <= document["valid_until"]
    ):
        raise ContractError(
            "diagnostic-evidence", "/evaluated_at", "evidence_time_order_invalid"
        )
    findings = document["findings"]
    control_ids = [item["control_id"] for item in findings]
    if len(control_ids) != len(set(control_ids)):
        raise ContractError(
            "diagnostic-evidence", "/findings", "evidence_duplicate_control_id"
        )
    for index, item in enumerate(findings):
        evidence_state = item["evidence_state"]
        status = item["status"]
        path = f"/findings/{index}/status"
        if item["policy_id"] != document["context"]["policy_id"]:
            raise ContractError(
                "diagnostic-evidence", path, "finding_policy_identity_mismatch"
            )
        if evidence_state == EvidenceState.VALID.value and status not in _VALID_FINDING_STATES:
            raise ContractError(
                "diagnostic-evidence", path, "valid_evidence_status_mismatch"
            )
        if evidence_state in _INCOMPLETE_EVIDENCE_STATES and status != FindingStatus.UNKNOWN.value:
            raise ContractError(
                "diagnostic-evidence", path, "missing_evidence_cannot_pass"
            )
        if evidence_state == EvidenceState.SKIPPED.value and status != FindingStatus.SKIPPED.value:
            raise ContractError(
                "diagnostic-evidence", path, "skipped_evidence_status_mismatch"
            )
        if (
            evidence_state == EvidenceState.NOT_APPLICABLE_PROVEN.value
            and status != FindingStatus.NOT_APPLICABLE.value
        ):
            raise ContractError(
                "diagnostic-evidence", path, "applicability_evidence_status_mismatch"
            )
        if item["applicable"] != (status != FindingStatus.NOT_APPLICABLE.value):
            raise ContractError(
                "diagnostic-evidence", path, "finding_applicability_status_mismatch"
            )
        if evidence_state in {
            EvidenceState.VALID.value,
            EvidenceState.NOT_APPLICABLE_PROVEN.value,
        } and not item["evidence_refs"]:
            raise ContractError(
                "diagnostic-evidence", path, "finding_evidence_reference_required"
            )
        if evidence_state == EvidenceState.VALID.value and item["observed_id"] is None:
            raise ContractError(
                "diagnostic-evidence", path, "finding_observation_required"
            )
        if evidence_state != EvidenceState.VALID.value and item["observed_id"] is not None:
            raise ContractError(
                "diagnostic-evidence", path, "finding_observation_state_mismatch"
            )
        if item["blocking"] and status not in {
            FindingStatus.FAIL.value,
            FindingStatus.WARN.value,
        }:
            raise ContractError(
                "diagnostic-evidence", path, "finding_blocking_status_mismatch"
            )
        if status in {
            FindingStatus.PASS.value,
            FindingStatus.NOT_APPLICABLE.value,
        } and item["severity"] != Severity.NONE.value:
            raise ContractError(
                "diagnostic-evidence", path, "finding_severity_status_mismatch"
            )

    assessed = _VALID_FINDING_STATES
    for coverage_name, predicate in (
        ("selected", lambda item: item["selected"] and item["applicable"]),
        (
            "full_required_policy",
            lambda item: item["required"] and item["applicable"],
        ),
    ):
        coverage = document["coverage"][coverage_name]
        covered = [item for item in findings if predicate(item)]
        gaps = set(coverage["gap_ids"])
        expected_gaps = {
            item["control_id"] for item in covered if item["status"] not in assessed
        }
        expected_numerator = sum(item["status"] in assessed for item in covered)
        if gaps != expected_gaps:
            raise ContractError(
                "diagnostic-evidence",
                f"/coverage/{coverage_name}/gap_ids",
                "coverage_gap_inventory_mismatch",
            )
        if (
            coverage["numerator"] != expected_numerator
            or coverage["denominator"] != len(covered)
        ):
            raise ContractError(
                "diagnostic-evidence",
                f"/coverage/{coverage_name}",
                "coverage_fraction_invalid",
            )

    gate_policy_ids = [item["policy_id"] for item in document["gates"]]
    if len(gate_policy_ids) != len(set(gate_policy_ids)):
        raise ContractError(
            "diagnostic-evidence", "/gates", "gate_duplicate_policy"
        )
    context_gate = None
    for index, gate in enumerate(document["gates"]):
        if not set(gate["blocking_finding_ids"]) <= set(control_ids) or not set(
            gate["coverage_gap_ids"]
        ) <= set(control_ids):
            raise ContractError(
                "diagnostic-evidence",
                f"/gates/{index}",
                "gate_unknown_finding",
            )
        if gate["policy_id"] == document["context"]["policy_id"]:
            context_gate = (index, gate)
    if context_gate is None:
        raise ContractError(
            "diagnostic-evidence", "/gates", "gate_context_policy_missing"
        )

    gate_index, gate = context_gate
    expected_blockers = {
        item["control_id"]
        for item in findings
        if item["applicable"] and item["selected"] and item["blocking"]
    }
    expected_gaps = set(document["coverage"]["full_required_policy"]["gap_ids"])
    if (
        set(gate["blocking_finding_ids"]) != expected_blockers
        or set(gate["coverage_gap_ids"]) != expected_gaps
    ):
        raise ContractError(
            "diagnostic-evidence",
            f"/gates/{gate_index}",
            "gate_finding_inventory_mismatch",
        )
    expected_state = (
        GateState.BLOCKED.value
        if expected_blockers or expected_gaps
        else GateState.PASS.value
    )
    if (
        gate["gate_state"] != GateState.NOT_EVALUATED.value
        and gate["gate_state"] != expected_state
    ):
        raise ContractError(
            "diagnostic-evidence",
            f"/gates/{gate_index}/gate_state",
            "gate_disposition_mismatch",
        )
    for finding_index, finding in enumerate(findings):
        expected_impact = (
            GateImpact.NOT_EVALUATED.value
            if gate["gate_state"] == GateState.NOT_EVALUATED.value
            else (
                GateImpact.BLOCKS.value
                if finding["blocking"]
                else GateImpact.DOES_NOT_BLOCK.value
            )
        )
        if finding["gate_impact"] != expected_impact:
            raise ContractError(
                "diagnostic-evidence",
                f"/findings/{finding_index}/gate_impact",
                "finding_gate_impact_mismatch",
            )

    if document["run_state"] == RunState.COMPLETE.value and any(
        item["status"] in {
            FindingStatus.UNKNOWN.value,
            FindingStatus.SKIPPED.value,
        }
        for item in findings
    ):
        raise ContractError(
            "diagnostic-evidence", "/run_state", "run_state_coverage_mismatch"
        )
    attempt_ids = [item["attempt_id"] for item in document["attempts"]]
    if len(attempt_ids) != len(set(attempt_ids)):
        raise ContractError(
            "diagnostic-evidence", "/attempts", "attempt_duplicate_identity"
        )
    known_control_ids = set(control_ids)
    if any(
        item["control_id"] not in known_control_ids for item in document["attempts"]
    ):
        raise ContractError(
            "diagnostic-evidence", "/attempts", "attempt_unknown_control"
        )


def _validate_backup_semantics(document: Mapping[str, Any]) -> None:
    constituents = {item["constituent_id"]: item for item in document["constituents"]}
    if len(constituents) != len(document["constituents"]):
        raise ContractError("backup-set", "/constituents", "backup_duplicate_constituent")
    receipts = {
        item["constituent_id"]: item for item in document["constituent_receipts"]
    }
    if len(receipts) != len(document["constituent_receipts"]):
        raise ContractError(
            "backup-set", "/constituent_receipts", "backup_duplicate_receipt"
        )
    if not set(receipts) <= set(constituents):
        raise ContractError(
            "backup-set", "/constituent_receipts", "backup_receipt_unknown_constituent"
        )
    commit = document["commit"]
    if commit["status"] == BackupCommitStatus.COMMITTED.value:
        missing = [
            constituent_id
            for constituent_id, item in constituents.items()
            if item["required"]
            and (
                constituent_id not in receipts
                or receipts[constituent_id]["status"] != "complete"
                or not receipts[constituent_id]["digest_verified"]
            )
        ]
        if missing:
            raise ContractError(
                "backup-set", "/commit/status", "backup_commit_incomplete_constituents"
            )
        if not all(commit["checks"].values()):
            raise ContractError(
                "backup-set", "/commit/checks", "backup_commit_checks_incomplete"
            )
    proof = document["restore_proof"]
    if proof["status"] == RestoreProofStatus.NOT_RUN.value and (
        proof["receipt_id"] is not None or proof["verified_at"] is not None
    ):
        raise ContractError(
            "backup-set", "/restore_proof", "backup_restore_proof_not_run_mismatch"
        )
    if proof["status"] != RestoreProofStatus.NOT_RUN.value and (
        proof["receipt_id"] is None or proof["verified_at"] is None
    ):
        raise ContractError(
            "backup-set", "/restore_proof", "backup_restore_proof_identity_missing"
        )


def _validate_command_semantics(document: Mapping[str, Any]) -> None:
    if document["finished_at"] < document["started_at"]:
        raise ContractError(
            "command-result", "/finished_at", "command_time_order_invalid"
        )
    command = document["command"]
    presentation = document["presentation"]
    if command["format"] != presentation["format"]:
        raise ContractError(
            "command-result", "/presentation/format", "presentation_format_mismatch"
        )
    if command["format"] == "html":
        if command["name"] not in {"audit", "doctor"}:
            raise ContractError(
                "command-result", "/command/format", "html_command_not_supported"
            )
        presentation_artifact = presentation["artifact_reference"]
        delivery_artifact = document["delivery"]["artifact_reference"]
        if document["delivery"]["status"] == DeliveryStatus.DELIVERED.value:
            if (
                presentation_artifact is None
                or presentation_artifact["media_type"] != "text/html"
                or delivery_artifact != presentation_artifact
            ):
                raise ContractError(
                    "command-result",
                    "/presentation/artifact_reference",
                    "html_artifact_required",
                )
        elif presentation_artifact is not None or delivery_artifact is not None:
            raise ContractError(
                "command-result",
                "/presentation/artifact_reference",
                "undelivered_html_artifact_forbidden",
            )
    allowed_next = {item.action_id for item in load_contract_catalog().safe_next_actions}
    if any(item["action_id"] not in allowed_next for item in document["next_actions"]):
        raise ContractError(
            "command-result", "/next_actions", "unowned_next_action"
        )
    delivery = document["delivery"]
    if delivery["status"] == DeliveryStatus.FAILED.value and delivery["error_id"] is None:
        raise ContractError(
            "command-result", "/delivery/error_id", "delivery_error_identity_required"
        )
    error_ids = [item["error_id"] for item in document["errors"]]
    if len(error_ids) != len(set(error_ids)):
        raise ContractError("command-result", "/errors", "command_duplicate_error_id")
    if (
        delivery["status"] == DeliveryStatus.FAILED.value
        and delivery["error_id"] not in set(error_ids)
    ):
        raise ContractError(
            "command-result", "/delivery/error_id", "delivery_error_record_missing"
        )
    if (
        delivery["status"] != DeliveryStatus.FAILED.value
        and delivery["error_id"] is not None
    ):
        raise ContractError(
            "command-result", "/delivery/error_id", "delivery_error_state_mismatch"
        )
    operation = document["operation_outcome"]
    if operation is not None and operation["recorded"] and document["operation_id"] is None:
        raise ContractError(
            "command-result", "/operation_id", "recorded_operation_identity_required"
        )
    result = document["result"]
    if (result["kind"] == "operation") != (operation is not None):
        raise ContractError(
            "command-result", "/operation_outcome", "operation_outcome_shape_mismatch"
        )
    if operation is not None:
        if document["operation_id"] is None or any(
            result[field] != operation[field]
            for field in (
                "journal_reference",
                "durable_state",
                "reconciliation_required",
            )
        ):
            raise ContractError(
                "command-result",
                "/operation_outcome",
                "operation_outcome_identity_mismatch",
            )
        expected_outcome = {
            StageState.SUCCEEDED.value: CommandOutcome.SUCCEEDED.value,
            StageState.FAILED.value: CommandOutcome.FAILED.value,
            StageState.BLOCKED.value: CommandOutcome.BLOCKED.value,
            StageState.INTERRUPTED.value: CommandOutcome.INTERRUPTED.value,
            StageState.PENDING.value: CommandOutcome.NOT_EVALUATED.value,
            StageState.RUNNING.value: CommandOutcome.NOT_EVALUATED.value,
        }[operation["durable_state"]]
        if document["outcome"] != expected_outcome:
            raise ContractError(
                "command-result", "/outcome", "operation_outcome_status_mismatch"
            )


def _validate_semantics(family: str, document: Mapping[str, Any]) -> None:
    validators = {
        "contract-catalog": _validate_catalog_semantics,
        "requirement-graph": validate_requirement_graph,
        "plan": _validate_plan_semantics,
        "operation-journal": _validate_operation_semantics,
        "release-manifest": _validate_release_semantics,
        "diagnostic-evidence": _validate_diagnostic_semantics,
        "backup-set": _validate_backup_semantics,
        "command-result": _validate_command_semantics,
    }
    validator = validators.get(family)
    if validator is not None:
        validator(document)


def _build_model(family: str, document: Mapping[str, Any]):
    builders = {
        "contract-catalog": _catalog_model,
        "requirement-graph": requirement_graph_model,
        "plan": _plan_model,
        "operation-journal": _operation_model,
        "release-manifest": _release_model,
        "diagnostic-evidence": _diagnostic_model,
        "backup-set": _backup_model,
        "command-result": _command_model,
    }
    return builders[family](document)


def validate_contract_document(family: str, value: Mapping[str, Any]):
    """Validate a detached document and return its immutable typed model."""
    registration = registration_for(family)
    try:
        validate_contract_limits(
            value,
            max_aggregate_nodes=(
                MAX_GRAPH_AGGREGATE_NODES
                if family == "requirement-graph"
                else 4_096
            ),
        )
    except ConfigurationError as exc:
        raise ContractError(family, exc.path, exc.reason) from None
    document = copy.deepcopy(dict(value))
    version = document.get("schema_version")
    if version not in registration.reader_versions:
        raise ContractVersionError(family, "/schema_version", "unsupported_schema_version")
    if family == "configuration":
        try:
            return resolve_configuration(document)
        except ConfigurationError as exc:
            raise ContractError(family, exc.path, exc.reason) from None
    _validate_against_schema(family, document, registration.schema_resource)
    _validate_semantics(family, document)
    return _build_model(family, document)


def parse_contract_bytes(family: str, data: bytes):
    """Strictly parse JSON bytes, reject unknown versions, and build a model."""
    try:
        value = parse_json_bytes(
            data,
            max_aggregate_nodes=(
                MAX_GRAPH_AGGREGATE_NODES
                if family == "requirement-graph"
                else 4_096
            ),
        )
    except ConfigurationError as exc:
        raise ContractError(family, exc.path, exc.reason) from None
    if not isinstance(value, Mapping):
        raise ContractError(family, "/", "root_must_be_object")
    return validate_contract_document(family, value)


def load_packaged_contract(family: str):
    """Load a catalog-owned packaged policy document for *family*."""
    registration = registration_for(family)
    if registration.policy_resource is None:
        raise ContractError(family, "/", "contract_has_no_packaged_policy")
    try:
        value = load_contract_resource("policies", registration.policy_resource)
    except ConfigurationError as exc:
        raise ContractError(family, exc.path, exc.reason) from None
    if not isinstance(value, Mapping):
        raise ContractError(family, "/", "root_must_be_object")
    return validate_contract_document(family, value)
