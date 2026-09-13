from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from actools.contracts.catalog import load_packaged_contract, parse_contract_bytes
from actools.contracts.errors import ContractError, RequirementGraphError
from actools.contracts.graph import EXPECTED_NODE_IDS, validate_requirement_graph
from actools.contracts.models import (
    DecisionStatus,
    ImplementationStatus,
    RequirementGraph,
    RuntimeEvidenceStatus,
)

ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE = (
    ROOT
    / "coding/baseline/Actools_Drupal_Community_Rewrite_Architecture_Implementation_v1.5.1.md"
)
POLICY = ROOT / "src/actools/contracts/policies/requirement-graph-1.0.0.json"
INVALID = ROOT / "tests/fixtures/contracts/invalid"


def _document() -> dict:
    return json.loads(POLICY.read_text(encoding="utf-8"))


def test_canonical_graph_has_the_complete_architecture_inventory_and_source() -> None:
    graph = load_packaged_contract("requirement-graph")
    assert isinstance(graph, RequirementGraph)
    assert tuple(node.id for node in graph.nodes) == EXPECTED_NODE_IDS
    assert graph.expected_counts.total == 163
    assert graph.expected_counts.feature == 75
    assert graph.expected_counts.work_package == 25
    assert graph.expected_counts.gate == 22
    assert graph.expected_counts.ux_requirement == 18
    assert graph.expected_counts.security_refinement == 8
    assert graph.expected_counts.security_case == 15
    assert graph.architecture_sha256 == hashlib.sha256(ARCHITECTURE.read_bytes()).hexdigest()


def test_graph_keeps_decision_implementation_support_and_evidence_separate() -> None:
    graph = load_packaged_contract("requirement-graph")
    by_id = {node.id: node for node in graph.nodes}
    assert by_id["F03"].decision_status == DecisionStatus.ACCEPTED
    assert by_id["F03"].implementation_status == ImplementationStatus.PARTIAL
    assert by_id["F03"].advertised_support is False
    assert by_id["F03"].runtime_evidence.status == RuntimeEvidenceStatus.NOT_EVALUATED

    assert by_id["F24"].decision_status == DecisionStatus.DEFERRED
    assert by_id["F24"].implementation_status == ImplementationStatus.NOT_IMPLEMENTED
    assert by_id["F24"].advertised_support is False
    assert by_id["F24"].decision_detail == (
        "Deferred by user: production S3-compatible storage adapter"
    )
    assert by_id["F42"].decision_detail == (
        "Deferred by user: production binary-log recovery capability"
    )
    assert by_id["UX-R16"].decision_status == DecisionStatus.DEFERRED
    assert all(not node.advertised_support for node in graph.nodes)
    assert all(node.owner_ids for node in graph.nodes)


def test_unresolved_exact_mappings_are_data_not_false_support() -> None:
    graph = load_packaged_contract("requirement-graph")
    assert any(node.parent_mapping_status.value == "unresolved" for node in graph.nodes)
    assert any(
        node.dependency_mapping_status.value == "unresolved" for node in graph.nodes
    )
    assert any(node.test_mapping.status.value == "unresolved" for node in graph.nodes)
    assert all(
        not node.advertised_support
        for node in graph.nodes
        if "unresolved"
        in {
            node.parent_mapping_status.value,
            node.dependency_mapping_status.value,
            node.relationship_mapping_status.value,
            node.test_mapping.status.value,
            node.contract_mapping.status.value,
        }
    )


@pytest.mark.parametrize(
    "fixture",
    [
        "graph-duplicate-id-1.0.0.json",
        "graph-unknown-dependency-1.0.0.json",
        "graph-unowned-capability-1.0.0.json",
        "graph-deferred-implemented-1.0.0.json",
    ],
)
def test_fixed_invalid_graphs_are_rejected(fixture: str) -> None:
    with pytest.raises(ContractError):
        parse_contract_bytes("requirement-graph", (INVALID / fixture).read_bytes())


def test_graph_semantics_report_the_four_required_failure_classes() -> None:
    duplicate = json.loads((INVALID / "graph-duplicate-id-1.0.0.json").read_text())
    with pytest.raises(RequirementGraphError) as exc:
        validate_requirement_graph(duplicate)
    assert exc.value.reason == "graph_duplicate_id"

    unknown = json.loads(
        (INVALID / "graph-unknown-dependency-1.0.0.json").read_text()
    )
    with pytest.raises(RequirementGraphError) as exc:
        validate_requirement_graph(unknown)
    assert exc.value.reason == "graph_unknown_reference"

    unowned = json.loads(
        (INVALID / "graph-unowned-capability-1.0.0.json").read_text()
    )
    with pytest.raises(RequirementGraphError) as exc:
        validate_requirement_graph(unowned)
    assert exc.value.reason == "graph_unowned_node"

    deferred = json.loads(
        (INVALID / "graph-deferred-implemented-1.0.0.json").read_text()
    )
    with pytest.raises(RequirementGraphError) as exc:
        validate_requirement_graph(deferred)
    assert exc.value.reason == "graph_deferred_marked_implemented"


def test_canonical_graph_cannot_silently_drop_an_architecture_identifier() -> None:
    document = _document()
    document["nodes"].pop()
    with pytest.raises(RequirementGraphError) as exc:
        validate_requirement_graph(document)
    assert exc.value.reason == "graph_canonical_inventory_mismatch"


def test_canonical_graph_is_bound_to_the_exact_architecture_source() -> None:
    document = _document()
    document["architecture_sha256"] = "0" * 64
    with pytest.raises(RequirementGraphError) as exc:
        validate_requirement_graph(document)
    assert exc.value.reason == "graph_architecture_identity_mismatch"


def test_dependency_cycles_and_partial_support_advertisements_fail_closed() -> None:
    document = _document()
    first, second = copy.deepcopy(document["nodes"][:2])
    first["dependency_ids"] = [second["id"]]
    second["dependency_ids"] = [first["id"]]
    first["dependency_mapping_status"] = "partial"
    second["dependency_mapping_status"] = "partial"
    fixture = copy.deepcopy(document)
    fixture["graph_id"] = "fixture-cycle-1.0.0"
    fixture["nodes"] = [first, second]
    with pytest.raises(RequirementGraphError) as exc:
        validate_requirement_graph(fixture)
    assert exc.value.reason == "graph_dependency_cycle"

    candidate = _document()
    node = next(item for item in candidate["nodes"] if item["id"] == "F03")
    node["advertised_support"] = True
    node["implementation_status"] = "implemented"
    node["runtime_evidence"] = {"status": "pass", "evidence_ids": ["evidence-f03"]}
    node["test_mapping"]["status"] = "resolved"
    node["contract_mapping"]["status"] = "resolved"
    node["contract_mapping"]["support_profiles"] = ["single-site-production"]
    with pytest.raises(RequirementGraphError) as exc:
        validate_requirement_graph(candidate)
    assert exc.value.reason == "graph_unsupported_advertisement"


def test_graph_validation_never_mutates_the_caller_document() -> None:
    document = _document()
    before = copy.deepcopy(document)
    validate_requirement_graph(document)
    assert document == before
