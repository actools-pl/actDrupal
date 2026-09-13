from __future__ import annotations

import copy
import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from actools.contracts.catalog import validate_contract_document
from actools.contracts.errors import ContractError
from actools.contracts.models import (
    BackupCommitStatus,
    BackupSet,
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


def test_backup_commit_and_later_restore_proof_are_distinct_states() -> None:
    model = validate_contract_document("backup-set", _fixture("valid", "backup-set"))
    assert isinstance(model, BackupSet)
    assert model.commit.status == BackupCommitStatus.COMMITTED
    assert model.commit.checks.constituents_complete is True
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


def test_operation_result_and_durable_outcome_cannot_disagree() -> None:
    value = _fixture("valid", "command-result")
    value["result"]["durable_state"] = "failed"
    with pytest.raises(ContractError) as exc:
        validate_contract_document("command-result", value)
    assert exc.value.reason == "operation_outcome_identity_mismatch"
