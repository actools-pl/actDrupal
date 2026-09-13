"""Semantic validation for the single source-owned requirement graph."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from typing import Any

from .errors import RequirementGraphError
from .models import (
    Applicability,
    ApplicabilityPredicate,
    ContractMapping,
    DecisionStatus,
    ImplementationStatus,
    MappingStatus,
    NodeKind,
    RequirementCounts,
    RequirementGraph,
    RequirementNode,
    RuntimeEvidence,
    RuntimeEvidenceStatus,
    TestMapping,
)

CANONICAL_GRAPH_ID = "actools-requirement-graph-1.0.0"
CANONICAL_PROFILE = "single-site-production"
CANONICAL_ARCHITECTURE_VERSION = "1.5.1"
CANONICAL_ARCHITECTURE_SHA256 = (
    "b131f36e316593f93aa9ec41e86c1b918a7b32dec87300188e4fdf0d487dde87"
)


def _numbered(prefix: str, start: int, finish: int) -> tuple[str, ...]:
    return tuple(f"{prefix}{number:02d}" for number in range(start, finish + 1))


EXPECTED_NODE_IDS = (
    *_numbered("F", 1, 75),
    *_numbered("WP", 1, 25),
    *_numbered("G", 1, 22),
    *_numbered("UX-R", 1, 18),
    *_numbered("UXS-", 1, 8),
    *_numbered("UXS-C", 1, 15),
)

EXPECTED_COUNTS = {
    NodeKind.FEATURE: 75,
    NodeKind.WORK_PACKAGE: 25,
    NodeKind.GATE: 22,
    NodeKind.UX_REQUIREMENT: 18,
    NodeKind.SECURITY_REFINEMENT: 8,
    NodeKind.SECURITY_CASE: 15,
}


def _kind_for_id(node_id: str) -> NodeKind | None:
    if node_id.startswith("UXS-C"):
        return NodeKind.SECURITY_CASE
    if node_id.startswith("UXS-"):
        return NodeKind.SECURITY_REFINEMENT
    if node_id.startswith("UX-R"):
        return NodeKind.UX_REQUIREMENT
    if node_id.startswith("WP"):
        return NodeKind.WORK_PACKAGE
    if node_id.startswith("F"):
        return NodeKind.FEATURE
    if node_id.startswith("G"):
        return NodeKind.GATE
    return None


def _as_tuple(value: Any) -> tuple[str, ...]:
    return tuple(value)


def requirement_graph_model(document: Mapping[str, Any]) -> RequirementGraph:
    """Build an immutable model from a schema-valid graph document."""
    count_data = document["expected_counts"]
    nodes: list[RequirementNode] = []
    for item in document["nodes"]:
        runtime = item["runtime_evidence"]
        applicability = item["applicability"]
        tests = item["test_mapping"]
        contract = item["contract_mapping"]
        nodes.append(
            RequirementNode(
                id=item["id"],
                kind=NodeKind(item["kind"]),
                title=item["title"],
                parent_feature_ids=_as_tuple(item["parent_feature_ids"]),
                parent_mapping_status=MappingStatus(item["parent_mapping_status"]),
                source_refs=_as_tuple(item["source_refs"]),
                decision_status=DecisionStatus(item["decision_status"]),
                decision_detail=item["decision_detail"],
                implementation_status=ImplementationStatus(
                    item["implementation_status"]
                ),
                advertised_support=item["advertised_support"],
                runtime_evidence=RuntimeEvidence(
                    RuntimeEvidenceStatus(runtime["status"]),
                    _as_tuple(runtime["evidence_ids"]),
                ),
                applicability=Applicability(
                    ApplicabilityPredicate(applicability["predicate"]),
                    applicability["capability_id"],
                    MappingStatus(applicability["mapping_status"]),
                ),
                owner_ids=_as_tuple(item["owner_ids"]),
                dependency_ids=_as_tuple(item["dependency_ids"]),
                dependency_mapping_status=MappingStatus(
                    item["dependency_mapping_status"]
                ),
                refines_ids=_as_tuple(item["refines_ids"]),
                supersedes_ids=_as_tuple(item["supersedes_ids"]),
                relationship_mapping_status=MappingStatus(
                    item["relationship_mapping_status"]
                ),
                test_mapping=TestMapping(
                    MappingStatus(tests["status"]),
                    _as_tuple(tests["acceptance_ids"]),
                ),
                contract_mapping=ContractMapping(
                    status=MappingStatus(contract["status"]),
                    authority_ids=_as_tuple(contract["authority_ids"]),
                    secret_ids=_as_tuple(contract["secret_ids"]),
                    endpoint_ids=_as_tuple(contract["endpoint_ids"]),
                    resource_ids=_as_tuple(contract["resource_ids"]),
                    action_ids=_as_tuple(contract["action_ids"]),
                    handler_ids=_as_tuple(contract["handler_ids"]),
                    schema_ids=_as_tuple(contract["schema_ids"]),
                    schema_update_ids=_as_tuple(contract["schema_update_ids"]),
                    probe_ids=_as_tuple(contract["probe_ids"]),
                    recovery_constituent_ids=_as_tuple(
                        contract["recovery_constituent_ids"]
                    ),
                    disable_behavior=contract["disable_behavior"],
                    rollback_behavior=contract["rollback_behavior"],
                    support_profiles=_as_tuple(contract["support_profiles"]),
                ),
                evidence_refs=_as_tuple(item["evidence_refs"]),
            )
        )
    return RequirementGraph(
        schema_version=document["schema_version"],
        graph_id=document["graph_id"],
        profile=document["profile"],
        architecture_version=document["architecture_version"],
        architecture_sha256=document["architecture_sha256"],
        expected_counts=RequirementCounts(**count_data),
        nodes=tuple(nodes),
    )


def _assert_no_dependency_cycle(nodes: Mapping[str, Mapping[str, Any]]) -> None:
    state: dict[str, int] = {}

    def visit(node_id: str) -> None:
        marker = state.get(node_id, 0)
        if marker == 1:
            raise RequirementGraphError("/nodes", "graph_dependency_cycle")
        if marker == 2:
            return
        state[node_id] = 1
        for dependency_id in nodes[node_id]["dependency_ids"]:
            visit(dependency_id)
        state[node_id] = 2

    for node_id in nodes:
        visit(node_id)


def validate_requirement_graph(document: Mapping[str, Any]) -> None:
    """Validate cross-node truth and completeness without mutating *document*."""
    raw_nodes = document.get("nodes")
    if not isinstance(raw_nodes, list):
        raise RequirementGraphError("/nodes", "graph_nodes_invalid")

    identifiers = [item.get("id") for item in raw_nodes if isinstance(item, Mapping)]
    duplicate_ids = sorted(
        identifier
        for identifier, count in Counter(identifiers).items()
        if isinstance(identifier, str) and count > 1
    )
    if duplicate_ids:
        raise RequirementGraphError("/nodes", "graph_duplicate_id")

    nodes: dict[str, Mapping[str, Any]] = {}
    for index, item in enumerate(raw_nodes):
        path = f"/nodes/{index}"
        if not isinstance(item, Mapping) or not isinstance(item.get("id"), str):
            raise RequirementGraphError(path, "graph_node_invalid")
        node_id = item["id"]
        nodes[node_id] = item
        if not item.get("owner_ids"):
            raise RequirementGraphError(path, "graph_unowned_node")
        expected_kind = _kind_for_id(node_id)
        if expected_kind is None or item.get("kind") != expected_kind.value:
            raise RequirementGraphError(path, "graph_kind_mismatch")

    known_ids = set(nodes)
    for index, item in enumerate(raw_nodes):
        path = f"/nodes/{index}"
        node_id = item["id"]
        for field in (
            "parent_feature_ids",
            "dependency_ids",
            "refines_ids",
            "supersedes_ids",
        ):
            references = item.get(field)
            if not isinstance(references, list):
                raise RequirementGraphError(path, "graph_reference_list_invalid")
            if any(reference not in known_ids for reference in references):
                raise RequirementGraphError(path, "graph_unknown_reference")
            if node_id in references and field != "parent_feature_ids":
                raise RequirementGraphError(path, "graph_self_reference")
        if any(
            nodes[parent_id].get("kind") != NodeKind.FEATURE.value
            for parent_id in item["parent_feature_ids"]
        ):
            raise RequirementGraphError(path, "graph_parent_not_feature")
        if item["kind"] == NodeKind.FEATURE.value and item["parent_feature_ids"] != [node_id]:
            raise RequirementGraphError(path, "graph_feature_parent_mismatch")
        if (
            item["kind"] != NodeKind.FEATURE.value
            and item.get("parent_mapping_status") == MappingStatus.RESOLVED.value
            and not item["parent_feature_ids"]
        ):
            raise RequirementGraphError(path, "graph_resolved_parent_empty")

        decision = item.get("decision_status")
        implementation = item.get("implementation_status")
        advertised = item.get("advertised_support")
        runtime = item.get("runtime_evidence", {})
        applicability = item.get("applicability", {})
        tests = item.get("test_mapping", {})
        contract = item.get("contract_mapping", {})

        deferred = decision == DecisionStatus.DEFERRED.value or applicability.get(
            "predicate"
        ) == ApplicabilityPredicate.FUTURE_DECISION.value
        if deferred and implementation != ImplementationStatus.NOT_IMPLEMENTED.value:
            raise RequirementGraphError(path, "graph_deferred_marked_implemented")
        if deferred and advertised:
            raise RequirementGraphError(path, "graph_deferred_marked_supported")
        if runtime.get("status") == RuntimeEvidenceStatus.PASS.value and not runtime.get(
            "evidence_ids"
        ):
            raise RequirementGraphError(path, "graph_pass_without_evidence")
        if tests.get("status") == MappingStatus.RESOLVED.value and not tests.get(
            "acceptance_ids"
        ):
            raise RequirementGraphError(path, "graph_resolved_tests_empty")
        if advertised and (
            implementation != ImplementationStatus.IMPLEMENTED.value
            or runtime.get("status") != RuntimeEvidenceStatus.PASS.value
            or tests.get("status") != MappingStatus.RESOLVED.value
            or contract.get("status") != MappingStatus.RESOLVED.value
            or item.get("parent_mapping_status") != MappingStatus.RESOLVED.value
            or item.get("dependency_mapping_status") != MappingStatus.RESOLVED.value
            or item.get("relationship_mapping_status") != MappingStatus.RESOLVED.value
            or applicability.get("mapping_status") != MappingStatus.RESOLVED.value
            or document.get("profile") not in contract.get("support_profiles", [])
        ):
            raise RequirementGraphError(path, "graph_unsupported_advertisement")

    if document.get("graph_id") == CANONICAL_GRAPH_ID:
        if (
            document.get("architecture_version") != CANONICAL_ARCHITECTURE_VERSION
            or document.get("architecture_sha256") != CANONICAL_ARCHITECTURE_SHA256
        ):
            raise RequirementGraphError(
                "/architecture_sha256", "graph_architecture_identity_mismatch"
            )
        if tuple(identifiers) != EXPECTED_NODE_IDS:
            raise RequirementGraphError("/nodes", "graph_canonical_inventory_mismatch")
        counts = Counter(NodeKind(item["kind"]) for item in raw_nodes)
        if any(counts[kind] != expected for kind, expected in EXPECTED_COUNTS.items()):
            raise RequirementGraphError("/nodes", "graph_canonical_count_mismatch")
        declared = document.get("expected_counts")
        if not isinstance(declared, Mapping) or declared.get("total") != len(
            EXPECTED_NODE_IDS
        ):
            raise RequirementGraphError(
                "/expected_counts", "graph_declared_count_mismatch"
            )
    _assert_no_dependency_cycle(nodes)
