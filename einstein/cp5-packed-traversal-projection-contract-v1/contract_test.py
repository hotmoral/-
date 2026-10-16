#!/usr/bin/env python3
import copy
import random

from contract import (
    Arc,
    SyntheticPackedTraversal,
    canonical_hash,
    canonical_json,
    synthetic_fixture,
)

CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def main():
    fixture = synthetic_fixture()
    model = SyntheticPackedTraversal(fixture)

    # 1) Packed semantic graph basics.
    packed = model.packed_result(materialized=False)
    check(packed["stateOrder"] == ["S0", "A", "B", "C", "D", "E"], "unique-state BFS order")
    check(packed["expandedSemanticStateCount"] == 6, "unique-state expansion count")
    check(packed["generatedSemanticArcCount"] == 8, "semantic arc count")
    check(packed["minHumanDepth"]["C"] == 1, "cross-depth min depth")
    check(packed["minHumanDepth"]["D"] == 2, "parallel-arc destination min depth")
    check(packed["semanticSearchCompleteness"] == "COMPLETE", "semantic completeness")
    check(packed["provenanceLanguageCoverage"] == "EXACT_FOR_DISCOVERED_GRAPH", "provenance coverage")
    check(packed["explicitMaterializationStatus"] == "NOT_MATERIALIZED", "materialization split")

    # 2) Same state preserves same-depth cost divergence + cross-depth provenance.
    to_c = model.enumerate_paths_to("C")
    check(len(to_c) == 3, "three histories reach C")
    check(sorted(p["humanDepth"] for p in to_c) == [1, 2, 2], "cross-depth histories retained")
    depth2_costs = sorted(p["cost"] for p in to_c if p["humanDepth"] == 2)
    check(depth2_costs == [3, 6], "same-depth divergent costs retained")
    check(sorted(p["cost"] for p in to_c) == [3, 4, 6], "all C costs retained")
    check(len({p["pathId"] for p in to_c}) == 3, "distinct path IDs retained")

    # 3) Parallel arcs remain separate and create distinct histories.
    to_d = model.enumerate_paths_to("D")
    check(len(to_d) == 6, "each C history branches through both parallel arcs")
    suffixes = {p["orderedArcKeys"][-1] for p in to_d}
    check(suffixes == {"C_D_ALPHA", "C_D_BETA"}, "parallel arc identities preserved")
    check(len({p["pathId"] for p in to_d}) == 6, "parallel histories have distinct path IDs")

    # 4) V1 projection exactness under a depth boundary.
    legacy_depth2 = model.legacy_v1_reference(max_edges=100, max_depth=2, max_nodes=100)
    projected_depth2 = model.project_v1(max_edges=100, max_depth=2, max_nodes=100)
    check(canonical_json(projected_depth2) == canonical_json(legacy_depth2), "depth-2 exact v1 projection")
    check(projected_depth2["generatedEdgeCount"] == 7, "depth-2 v1 generated edge count")
    check(len(projected_depth2["frontier"]) == 4, "depth-2 frontier occurrence count")

    # Cross-depth max-depth dominance: only direct C history may continue to D at maxDepth=2.
    generated_keys = [e["opportunityKey"] for e in projected_depth2["edges"]]
    check(generated_keys.count("C_D_ALPHA") == 1, "only min-depth C occurrence extends through alpha")
    check(generated_keys.count("C_D_BETA") == 1, "only min-depth C occurrence extends through beta")
    c_depth_frontier = [
        f for f in projected_depth2["frontier"]
        if f["state"] == "C" and f["cutoff"] == "DEPTH_LIMIT"
    ]
    check(len(c_depth_frontier) == 2, "longer C histories retained at depth boundary")
    check(
        all(f["pendingOpportunityKeys"] == ["C_D_ALPHA", "C_D_BETA"] for f in c_depth_frontier),
        "depth-boundary C histories keep pending semantic choices",
    )

    # 5) Edge-budget cutoff projection exactness and FIFO frontier.
    legacy_edge5 = model.legacy_v1_reference(max_edges=5, max_depth=2, max_nodes=100)
    projected_edge5 = model.project_v1(max_edges=5, max_depth=2, max_nodes=100)
    check(canonical_json(projected_edge5) == canonical_json(legacy_edge5), "edge-5 exact v1 projection")
    check(projected_edge5["generatedEdgeCount"] == 5, "edge budget consumed exactly")
    check(projected_edge5["completeness"] == "BUDGET_EXHAUSTED", "edge cutoff completeness")
    check(projected_edge5["frontier"][0]["cutoff"] == "EDGE_LIMIT", "active cutoff first")
    check(projected_edge5["frontier"][0]["state"] == "C", "direct C is cutoff source")
    check(
        projected_edge5["frontier"][0]["pendingOpportunityKeys"] == ["C_D_ALPHA", "C_D_BETA"],
        "remaining canonical opportunity order preserved",
    )
    check(
        [f["cutoff"] for f in projected_edge5["frontier"][1:]]
        == ["UNVISITED_AFTER_EDGE_LIMIT", "UNVISITED_AFTER_EDGE_LIMIT"],
        "queued histories drained in FIFO order",
    )

    # 6) Construction-order independence.
    expected_packed = canonical_json(packed)
    expected_projection = canonical_json(projected_depth2)
    for seed in range(20):
        shuffled = fixture[:]
        random.Random(seed).shuffle(shuffled)
        candidate = SyntheticPackedTraversal(shuffled)
        check(canonical_json(candidate.packed_result(materialized=False)) == expected_packed, f"packed shuffle {seed}")
        check(canonical_json(candidate.project_v1(max_edges=100, max_depth=2, max_nodes=100)) == expected_projection, f"projection shuffle {seed}")

    # 7) Explicit materialization status is orthogonal to semantic graph identity inputs.
    materialized = model.packed_result(materialized=True)
    check(materialized["explicitMaterializationStatus"] == "MATERIALIZED", "materialization status toggles")
    p1 = copy.deepcopy(packed)
    p2 = copy.deepcopy(materialized)
    p1.pop("packedIdentity")
    p2.pop("packedIdentity")
    p1.pop("explicitMaterializationStatus")
    p2.pop("explicitMaterializationStatus")
    check(canonical_json(p1) == canonical_json(p2), "same semantic graph regardless of materialization state")

    # 8) Canonical hash is deterministic and counters remain integer-valued.
    check(canonical_hash({"b": 2, "a": 1}) == canonical_hash({"a": 1, "b": 2}), "canonical key ordering")
    check(isinstance(packed["expandedSemanticStateCount"], int), "integer semantic-state counter")
    check(isinstance(projected_depth2["generatedEdgeCount"], int), "integer projected-edge counter")

    # 9) Cycle rejection: packed contract must remain acyclic.
    try:
        SyntheticPackedTraversal(fixture + [Arc("E", "S0", "ILLEGAL_CYCLE", 1)])
        raise AssertionError("cycle should be rejected")
    except ValueError as exc:
        check(str(exc) == "semantic cycle", "cycle rejection")

    # 10) V1 identity is deliberately separate from packed identity.
    check(packed["searchPolicyVersion"] != projected_depth2["projectorVersion"], "version boundary explicit")
    check(packed["packedIdentity"] != projected_depth2["projectionIdentity"], "packed and v1 identities differ")

    print(
        "PUBLIC_PACKED_PROVENANCE_PROJECTION_CONTRACT_PASS "
        f"checks={CHECKS} packedStates={packed['expandedSemanticStateCount']} "
        f"semanticArcs={packed['generatedSemanticArcCount']} "
        f"cHistories={len(to_c)} dHistories={len(to_d)}"
    )


if __name__ == "__main__":
    main()
