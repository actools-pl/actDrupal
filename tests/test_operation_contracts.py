from __future__ import annotations

import copy
import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from actools.contracts.catalog import load_contract_catalog, validate_contract_document
from actools.contracts.errors import ContractError
from actools.contracts.models import (
    BackupCommitStatus,
    BackupSet,
    BackupTransport,
    CommandOutcome,
    CommandResult,
    DeliveryStatus,
    OperationJournal,
    Plan,
    RestoreProofStatus,
    StageState,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/contracts"


def _fixture(kind: str, family: str) -> dict:
    path = FIXTURES / kind / f"{family}-1.0.0.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("filename", "family", "reason"),
    [
        (
            "plan-executable-command-1.0.0.json",
            "plan",
            "unknown_property",
        ),
        (
            "plan-unsupported-version-2.0.0.json",
            "plan",
            "unsupported_schema_version",
        ),
        (
            "presentation-forged-admission-1.0.0.json",
            "command-result",
            "unsupported_value",
        ),
    ],
)
def test_fixed_invalid_operation_contracts_fail_closed(
    filename: str, family: str, reason: str
) -> None:
    value = json.loads((FIXTURES / "invalid" / filename).read_text(encoding="utf-8"))
    with pytest.raises(ContractError) as exc:
        validate_contract_document(family, value)
    assert exc.value.reason == reason


def test_plan_is_descriptive_closed_and_immutable() -> None:
    value = _fixture("valid", "plan")
    model = validate_contract_document("plan", value)
    assert isinstance(model, Plan)
    assert model.action == model.request.action == "deployment.install"
    assert model.actor_requirements[0].authenticated_actor_required is True
    assert model.review.review_identity == "review-install-alpha"
    assert "command" not in value
    assert "argv" not in value
    with pytest.raises(FrozenInstanceError):
        model.action = "deployment.update"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("mutate", "reason"),
    [
        (
            lambda value: value["request"].__setitem__("action", "deployment.update"),
            "plan_request_action_mismatch",
        ),
        (
            lambda value: value["recovery"].update(
                {"checkpoint_required": True, "checkpoint_id": None}
            ),
            "plan_checkpoint_identity_required",
        ),
        (
            lambda value: value["effects"][0].__setitem__("irreversible", True),
            "plan_irreversible_boundary_mismatch",
        ),
    ],
)
def test_plan_cross_field_invariants_reject_without_mutating_input(
    mutate, reason: str
) -> None:
    value = _fixture("valid", "plan")
    mutate(value)
    before = copy.deepcopy(value)
    with pytest.raises(ContractError) as exc:
        validate_contract_document("plan", value)
    assert exc.value.reason == reason
    assert value == before


def test_plan_omission_and_wrong_types_are_not_defaulted_or_coerced() -> None:
    missing = _fixture("valid", "plan")
    del missing["disruption"]
    with pytest.raises(ContractError) as exc:
        validate_contract_document("plan", missing)
    assert exc.value.reason == "required_field_missing"

    wrong_type = _fixture("valid", "plan")
    wrong_type["disruption"]["maximum_seconds"] = "120"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("plan", wrong_type)
    assert exc.value.reason == "wrong_type"


def test_plan_uses_calendar_valid_utc_and_the_fifteen_minute_window() -> None:
    boundary = _fixture("valid", "plan")
    assert validate_contract_document("plan", boundary).expires_at == (
        "2026-09-13T10:15:00Z"
    )

    overlong = _fixture("valid", "plan")
    overlong["expires_at"] = "2026-09-13T10:15:00.000000001Z"
    overlong["review"]["expires_at"] = overlong["expires_at"]
    with pytest.raises(ContractError) as exc:
        validate_contract_document("plan", overlong)
    assert exc.value.reason == "plan_validity_window_exceeded"

    review_outside = _fixture("valid", "plan")
    review_outside["review"]["reviewed_at"] = "2026-09-13T09:59:59Z"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("plan", review_outside)
    assert exc.value.reason == "plan_review_interval_outside_validity"

    impossible = _fixture("valid", "plan")
    impossible["collected_at"] = "2026-02-29T10:00:00Z"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("plan", impossible)
    assert exc.value.reason == "invalid_format"


def test_successful_journal_has_durable_identity_and_satisfied_postconditions() -> None:
    model = validate_contract_document(
        "operation-journal", _fixture("valid", "operation-journal")
    )
    assert isinstance(model, OperationJournal)
    assert model.state == StageState.SUCCEEDED
    assert model.predecessor_generation == 7
    assert model.target_generation == 8
    assert all(
        not postcondition.required or postcondition.state == "satisfied"
        for postcondition in model.expected_postconditions
    )
    assert model.reconciliation.required is False
    assert tuple(attempt.state for attempt in model.attempts) == (
        StageState.FAILED,
        StageState.SUCCEEDED,
    )


def test_journal_cannot_claim_success_with_missing_proof_or_regressed_generation() -> None:
    missing = _fixture("valid", "operation-journal")
    missing["expected_postconditions"][0]["state"] = "unknown"
    missing["expected_postconditions"][0]["evidence_id"] = None
    with pytest.raises(ContractError) as exc:
        validate_contract_document("operation-journal", missing)
    assert exc.value.reason == "journal_success_without_postconditions"

    regressed = _fixture("valid", "operation-journal")
    regressed["target_generation"] = regressed["predecessor_generation"] - 1
    with pytest.raises(ContractError) as exc:
        validate_contract_document("operation-journal", regressed)
    assert exc.value.reason == "journal_generation_regression"


def test_succeeded_journal_requires_unique_resolvable_postcondition_proof() -> None:
    missing_only = _fixture("valid", "operation-journal")
    missing_only["expected_postconditions"][0]["evidence_id"] = None
    with pytest.raises(ContractError) as exc:
        validate_contract_document("operation-journal", missing_only)
    assert exc.value.reason == "journal_success_without_postconditions"

    dangling = _fixture("valid", "operation-journal")
    dangling["expected_postconditions"][0]["evidence_id"] = "evidence-missing"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("operation-journal", dangling)
    assert exc.value.reason == "journal_postcondition_evidence_missing"

    removed = _fixture("valid", "operation-journal")
    removed["evidence_refs"] = []
    with pytest.raises(ContractError) as exc:
        validate_contract_document("operation-journal", removed)
    assert exc.value.reason == "journal_postcondition_evidence_missing"

    duplicate = _fixture("valid", "operation-journal")
    duplicate["evidence_refs"].append(copy.deepcopy(duplicate["evidence_refs"][0]))
    with pytest.raises(ContractError) as exc:
        validate_contract_document("operation-journal", duplicate)
    assert exc.value.reason == "journal_duplicate_evidence_reference"


def test_backup_commit_and_later_restore_proof_are_distinct_states() -> None:
    model = validate_contract_document("backup-set", _fixture("valid", "backup-set"))
    assert isinstance(model, BackupSet)
    assert model.commit.status == BackupCommitStatus.COMMITTED
    assert model.commit.checks.constituents_complete is True
    assert model.repository.transport == BackupTransport.REST
    assert model.restore_proof.status == RestoreProofStatus.NOT_RUN
    assert model.restore_proof.receipt_id is None
    assert model.restore_proof.verified_at is None


def test_backup_commit_requires_every_required_receipt_and_commit_check() -> None:
    missing = _fixture("valid", "backup-set")
    missing["constituent_receipts"].pop()
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", missing)
    assert exc.value.reason == "backup_commit_incomplete_constituents"

    unchecked = _fixture("valid", "backup-set")
    unchecked["commit"]["checks"]["repository_verified"] = False
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", unchecked)
    assert exc.value.reason == "unsupported_value"


def test_backup_commit_owns_complete_single_site_inventory_and_verification() -> None:
    removed = _fixture("valid", "backup-set")
    removed["constituents"] = [
        item for item in removed["constituents"] if item["kind"] != "private-files"
    ]
    removed["constituent_receipts"] = [
        item
        for item in removed["constituent_receipts"]
        if item["constituent_id"] != "private-files"
    ]
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", removed)
    assert exc.value.reason == "backup_commit_mandatory_constituent_missing"

    demoted = _fixture("valid", "backup-set")
    demoted["constituents"][0]["required"] = False
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", demoted)
    assert exc.value.reason == "backup_commit_mandatory_constituent_missing"

    duplicate_kind = _fixture("valid", "backup-set")
    duplicate_kind["constituents"][-1]["kind"] = "private-files"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", duplicate_kind)
    assert exc.value.reason == "backup_duplicate_constituent_kind"

    duplicate_id = _fixture("valid", "backup-set")
    duplicate_id["constituents"][-1]["constituent_id"] = (
        duplicate_id["constituents"][0]["constituent_id"]
    )
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", duplicate_id)
    assert exc.value.reason == "backup_duplicate_constituent"

    bad_digest_receipt = _fixture("valid", "backup-set")
    bad_digest_receipt["constituent_receipts"][0]["digest_verified"] = False
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", bad_digest_receipt)
    assert exc.value.reason == "backup_commit_incomplete_constituents"

    failed_verification = _fixture("valid", "backup-set")
    failed_verification["verification_results"][0]["status"] = "fail"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", failed_verification)
    assert exc.value.reason == "backup_commit_verification_missing_or_failed"

    missing_verification = _fixture("valid", "backup-set")
    missing_verification["verification_results"].pop(0)
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", missing_verification)
    assert exc.value.reason == "backup_commit_verification_missing_or_failed"

    duplicate_receipt_id = _fixture("valid", "backup-set")
    duplicate_receipt_id["constituent_receipts"][1]["receipt_id"] = (
        duplicate_receipt_id["constituent_receipts"][0]["receipt_id"]
    )
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", duplicate_receipt_id)
    assert exc.value.reason == "backup_duplicate_receipt_identity"

    duplicate_check_id = _fixture("valid", "backup-set")
    duplicate_check_id["verification_results"][1]["check_id"] = (
        duplicate_check_id["verification_results"][0]["check_id"]
    )
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", duplicate_check_id)
    assert exc.value.reason == "backup_duplicate_verification"

    contradictory_snapshot = _fixture("valid", "backup-set")
    contradictory_snapshot["verification_results"][-1]["status"] = "unknown"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", contradictory_snapshot)
    assert exc.value.reason == "backup_commit_verification_missing_or_failed"


def test_backup_transport_is_the_selected_rest_backend_only() -> None:
    unsupported = _fixture("valid", "backup-set")
    unsupported["repository"]["transport"] = "restic-sftp"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("backup-set", unsupported)
    assert exc.value.reason == "unsupported_value"


def test_operation_outcome_survives_independent_delivery_failure() -> None:
    model = validate_contract_document(
        "command-result", _fixture("valid", "command-result")
    )
    assert isinstance(model, CommandResult)
    assert model.outcome == CommandOutcome.SUCCEEDED
    assert model.operation_outcome is not None
    assert model.operation_outcome.durable_state == StageState.SUCCEEDED
    assert model.operation_outcome.recorded is True
    assert model.delivery.status == DeliveryStatus.FAILED
    assert model.delivery.stdout_document_count == 1
    assert model.next_actions[0].action_id == "retry.delivery"


def test_html_is_an_artifact_format_only_for_audit_and_doctor() -> None:
    html = _fixture("valid", "command-result")
    html["command"].update({"name": "doctor", "format": "html"})
    html["operation_id"] = None
    html["result"] = {
        "kind": "diagnostic",
        "evidence_reference": "evidence://store/doctor-001",
        "policy_id": "doctor-default",
        "gate_state": "pass",
        "selected_coverage_complete": True,
        "full_required_coverage_complete": True,
    }
    html["operation_outcome"] = None
    html["delivery"].update(
        {
            "status": "delivered",
            "artifact_reference": {
                "artifact_id": "diagnostic-report-html",
                "media_type": "text/html",
                "digest": "9" * 64,
                "source": "artifact://diagnostics/report-html",
            },
            "error_id": None,
        }
    )
    html["errors"] = []
    html["next_actions"] = []
    html["presentation"].update(
        {
            "format": "html",
            "artifact_reference": copy.deepcopy(
                html["delivery"]["artifact_reference"]
            ),
        }
    )
    model = validate_contract_document("command-result", html)
    assert model.presentation.artifact_reference is not None
    assert model.presentation.artifact_reference.media_type == "text/html"
    assert model.presentation.admission_authority == "none"
    assert model.presentation.creates_evidence is False
    assert model.presentation.collects_evidence is False

    forbidden = copy.deepcopy(html)
    forbidden["command"]["name"] = "apply"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("command-result", forbidden)
    assert exc.value.reason == "html_command_not_supported"

    no_artifact = copy.deepcopy(html)
    no_artifact["presentation"]["artifact_reference"] = None
    with pytest.raises(ContractError) as exc:
        validate_contract_document("command-result", no_artifact)
    assert exc.value.reason == "html_artifact_required"

    failed_delivery = copy.deepcopy(html)
    failed_delivery["delivery"].update(
        {
            "status": "failed",
            "artifact_reference": None,
            "error_id": "report-delivery-failed",
        }
    )
    failed_delivery["presentation"]["artifact_reference"] = None
    failed_delivery["errors"] = [
        {
            "error_id": "report-delivery-failed",
            "source": "delivery",
            "message_id": "destination-publication-failed",
            "evidence_reference": None,
        }
    ]
    model = validate_contract_document("command-result", failed_delivery)
    assert model.outcome == CommandOutcome.SUCCEEDED
    assert model.delivery.status == DeliveryStatus.FAILED


def test_command_result_uses_owned_safe_actions_and_one_stdout_document() -> None:
    value = _fixture("valid", "command-result")
    value["next_actions"][0]["action_id"] = "shell.retry"
    with pytest.raises(ContractError):
        validate_contract_document("command-result", value)

    value = _fixture("valid", "command-result")
    value["delivery"]["stdout_document_count"] = 2
    with pytest.raises(ContractError) as exc:
        validate_contract_document("command-result", value)
    assert exc.value.reason == "unsupported_value"


@pytest.mark.parametrize(
    "documentation_id",
    ["docs:unowned", "docs:operation-inspection"],
)
def test_command_result_requires_the_complete_catalog_guidance_tuple(
    documentation_id: str,
) -> None:
    value = _fixture("valid", "command-result")
    value["next_actions"][0]["documentation_id"] = documentation_id
    with pytest.raises(ContractError) as exc:
        validate_contract_document("command-result", value)
    assert exc.value.reason == "unowned_next_action"


def test_every_registered_guidance_tuple_round_trips() -> None:
    for registration in load_contract_catalog().safe_next_actions:
        value = _fixture("valid", "command-result")
        value["next_actions"] = [
            {
                "action_id": registration.action_id,
                "source": registration.source,
                "documentation_id": registration.documentation_id,
            }
        ]
        validate_contract_document("command-result", value)


def test_command_timestamp_order_uses_exact_fractional_utc_instants() -> None:
    later_fraction = _fixture("valid", "command-result")
    later_fraction["started_at"] = "2026-09-13T10:00:00Z"
    later_fraction["finished_at"] = "2026-09-13T10:00:00.1Z"
    assert validate_contract_document("command-result", later_fraction).finished_at == (
        "2026-09-13T10:00:00.1Z"
    )

    equivalent = _fixture("valid", "command-result")
    equivalent["started_at"] = "2026-09-13T10:00:00Z"
    equivalent["finished_at"] = "2026-09-13T10:00:00.0Z"
    validate_contract_document("command-result", equivalent)

    reversed_fraction = _fixture("valid", "command-result")
    reversed_fraction["started_at"] = "2026-09-13T10:00:00.1Z"
    reversed_fraction["finished_at"] = "2026-09-13T10:00:00Z"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("command-result", reversed_fraction)
    assert exc.value.reason == "command_time_order_invalid"

    leap_day = _fixture("valid", "command-result")
    leap_day["started_at"] = "2028-02-29T10:00:00Z"
    leap_day["finished_at"] = "2028-02-29T10:00:01Z"
    validate_contract_document("command-result", leap_day)

    impossible = _fixture("valid", "command-result")
    impossible["started_at"] = "2026-02-29T10:00:00Z"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("command-result", impossible)
    assert exc.value.reason == "invalid_format"


def test_operation_result_and_durable_outcome_cannot_disagree() -> None:
    value = _fixture("valid", "command-result")
    value["result"]["durable_state"] = "failed"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("command-result", value)
    assert exc.value.reason == "operation_outcome_identity_mismatch"
