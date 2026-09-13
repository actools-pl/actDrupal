from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from actools.contracts.catalog import (
    canonical_contract_digest,
    load_contract_catalog,
    load_packaged_contract,
    parse_contract_bytes,
    registration_for,
    validate_contract_document,
)
from actools.contracts.configuration import (
    ConfigurationError,
    contract_schema_validator,
    load_contract_resource,
)
from actools.contracts.errors import ContractError, ContractVersionError
from actools.contracts.models import ContractCatalog, RequirementGraph, to_primitive

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/contracts"
SCHEMAS = ROOT / "src/actools/contracts/schemas"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_catalog_is_the_closed_reader_writer_and_action_registry() -> None:
    catalog = load_contract_catalog()
    assert isinstance(catalog, ContractCatalog)
    assert catalog.schema_version == "1.0.0"
    assert catalog.profile == "single-site-production"
    assert catalog.canonicalization == "RFC8785"
    assert catalog.diagnostic_formats == ("human", "json", "markdown", "html")
    assert catalog.action_vocabulary == (
        "host.initialize",
        "host.prepare",
        "deployment.install",
        "configuration.publish",
        "credentials.rotate",
        "service.restart",
        "caddy.reload",
        "maintenance.transition",
        "application.operator",
        "storage.probe",
        "notification.probe",
        "backup.capture",
        "backup.verify",
        "backup.maintain",
        "recovery.rehearse",
        "recovery.restore",
        "recovery.promote",
        "deployment.update",
        "deployment.rollback",
        "management.update",
        "diagnostics.probe",
        "operation.reconcile",
    )
    assert {item.family for item in catalog.contracts} == {
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
    assert all(item.writer_version in item.reader_versions for item in catalog.contracts)
    assert all(item.migration_edges == () for item in catalog.contracts)
    assert to_primitive(catalog) == load_contract_resource(
        "policies", "contract-catalog-1.0.0.json"
    )
    assert registration_for("requirement-graph").policy_resource == (
        "requirement-graph-1.0.0.json"
    )


def test_schema_enumerations_are_exact_catalog_projections() -> None:
    catalog = load_contract_catalog()
    plan_schema = load_contract_resource("schemas", "plan-1.0.0.schema.json")
    result_schema = load_contract_resource(
        "schemas", "command-result-1.0.0.schema.json"
    )
    assert tuple(plan_schema["$defs"]["action"]["enum"]) == (
        catalog.action_vocabulary
    )
    assert tuple(result_schema["$defs"]["command"]["properties"]["format"]["enum"]) == (
        catalog.diagnostic_formats
    )
    assert tuple(
        result_schema["$defs"]["nextAction"]["properties"]["action_id"]["enum"]
    ) == tuple(item.action_id for item in catalog.safe_next_actions)


def test_every_owned_schema_is_draft_2020_12_and_all_objects_are_closed() -> None:
    def objects(value: object):
        if isinstance(value, dict):
            if value.get("type") == "object":
                yield value
            for child in value.values():
                yield from objects(child)
        elif isinstance(value, list):
            for child in value:
                yield from objects(child)

    for path in sorted(SCHEMAS.glob("*.schema.json")):
        schema = _json(path)
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        contract_schema_validator(schema)
        assert all(item.get("additionalProperties") is False for item in objects(schema))


@pytest.mark.parametrize(
    "family",
    [
        "plan",
        "operation-journal",
        "release-manifest",
        "diagnostic-evidence",
        "backup-set",
        "command-result",
    ],
)
def test_valid_fixture_models_round_trip_exactly_through_owned_fields(family: str) -> None:
    document = _json(FIXTURES / "valid" / f"{family}-1.0.0.json")
    model = validate_contract_document(family, document)
    assert to_primitive(model) == document


def test_packaged_graph_round_trips_without_a_second_registry() -> None:
    document = load_contract_resource("policies", "requirement-graph-1.0.0.json")
    graph = load_packaged_contract("requirement-graph")
    assert isinstance(graph, RequirementGraph)
    assert to_primitive(graph) == document


def test_contract_reference_matrix_tracks_every_catalog_registration() -> None:
    reference = (ROOT / "docs/reference/contracts.md").read_text(encoding="utf-8")
    for registration in load_contract_catalog().contracts:
        assert f"| `{registration.family}` |" in reference
        assert f"`{registration.schema_resource}`" in reference


def test_unknown_future_version_rejects_before_and_without_input_mutation() -> None:
    value = _json(FIXTURES / "valid/plan-1.0.0.json")
    value["schema_version"] = "2.0.0"
    before = copy.deepcopy(value)
    with pytest.raises(ContractVersionError) as exc:
        validate_contract_document("plan", value)
    assert exc.value.reason == "unsupported_schema_version"
    assert value == before


def test_strict_json_parser_rejects_duplicate_keys_without_reflecting_values() -> None:
    raw = b'{"schema_version":"1.0.0","schema_version":"2.0.0"}'
    with pytest.raises(ContractError) as exc:
        parse_contract_bytes("plan", raw)
    assert exc.value.reason == "duplicate_json_key"
    assert "2.0.0" not in str(exc.value)


def test_packaged_resource_lookup_rejects_unowned_paths() -> None:
    with pytest.raises(ConfigurationError) as exc:
        load_contract_resource("schemas", "../configuration-1.0.0.schema.json")
    assert exc.value.reason == "contract_resource_name_invalid"


def test_every_significant_plan_group_changes_canonical_identity() -> None:
    value = _json(FIXTURES / "valid/plan-1.0.0.json")
    original = canonical_contract_digest(value)

    mutations = [
        lambda item: item["request"].__setitem__("digest", "0" * 64),
        lambda item: item["actor_requirements"][0].__setitem__(
            "authority_id", "deployment-secondary"
        ),
        lambda item: item["target"].__setitem__("site_id", "site-bravo"),
        lambda item: item["protected_resources"]["destination_ids"].__setitem__(
            0, "resource://site/bravo"
        ),
        lambda item: item["fingerprints"][0].__setitem__("generation", 8),
        lambda item: item.__setitem__("expires_at", "2026-09-13T10:31:00Z"),
        lambda item: item["context_digests"].__setitem__("policy", "0" * 64),
        lambda item: item["required_capabilities"].append("local-storage"),
        lambda item: item["effects"][0].__setitem__(
            "description", "Publish a different reviewed generation."
        ),
        lambda item: item["disruption"].__setitem__("maximum_seconds", 121),
        lambda item: item["preconditions"][0].__setitem__(
            "evidence_required", False
        ),
        lambda item: item["recovery"].__setitem__(
            "rollback_strategy", "qualified-recovery"
        ),
        lambda item: item["review"].__setitem__(
            "review_identity", "review-install-bravo"
        ),
    ]
    digests = set()
    for mutate in mutations:
        candidate = copy.deepcopy(value)
        mutate(candidate)
        digests.add(canonical_contract_digest(candidate))
    assert original not in digests
    assert len(digests) == len(mutations)
