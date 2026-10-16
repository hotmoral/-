#!/usr/bin/env python3
import random

from contract import (
    Arc,
    NodeSpec,
    SyntheticPackedV2,
    budget_fixture,
    canonical_json,
    legacy_v1_projection_identity,
    provenance_fixture,
)

CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def node(result, state):
    for value in result["semanticNodes"]:
        if value["state"] == state:
            return value
    raise AssertionError(f"missing node {state}")


def main():
    budget_nodes, budget_arcs = budget_fixture()
    model = SyntheticPackedV2(budget_nodes, budget_arcs)

    # 1) Deterministic unique-state FIFO first-discovery and semantic-arc order.
    full = model.search(max_states=100, max_arcs=100, max_depth=10)
    check(
        [n["state"] for n in full["semanticNodes"]]
        == ["S0", "SOL", "BAD", "STALL", "P", "Q1", "Q2", "PX", "PY"],
        "unique-state FIFO first-discovery order",
    )
    check(
        [a["opportunityKey"] for a in full["semanticArcs"]]
        == ["A_SOLVED", "B_INVALID", "C_STALLED", "D_PRODUCTIVE", "E_QUEUE_1", "F_QUEUE_2", "P_ALPHA", "P_BETA"],
        "deterministic semantic-arc order",
    )
    check(full["expandedSemanticStateCount"] == 9, "unique states inspected once")
    check(full["generatedSemanticArcCount"] == 8, "semantic arc count")
    check(full["distinctSemanticStateCount"] == 9, "distinct semantic state count")

    # 2) State limit is checked before dequeue/inspection; queued nodes remain uninspected.
    state1 = model.search(max_states=1, max_arcs=100, max_depth=10)
    check(state1["expandedSemanticStateCount"] == 1, "state limit consumes only root inspection")
    check(
        [f["state"] for f in state1["frontier"]]
        == ["SOL", "BAD", "STALL", "P", "Q1", "Q2"],
        "state-limit frontier preserves FIFO queue order",
    )
    check(all(f["cutoff"] == "STATE_LIMIT" for f in state1["frontier"]), "state-limit cutoff kind")
    check(all(f["inspectionStatus"] == "UNINSPECTED" for f in state1["frontier"]), "state-limit entries uninspected")
    check(all(node(state1, f["state"])["classification"] == "UNINSPECTED" for f in state1["frontier"]), "uninspected never serialized as stalled")
    check(state1["semanticSearchCompleteness"] == "INCOMPLETE", "state-limit incomplete")
    check(state1["cutoffCauses"] == ["SEMANTIC_STATE_LIMIT"], "state-limit cause explicit")

    # 3) Arc budget zero at productive root: inspect/enumerate root, emit no arc.
    arc0 = model.search(max_states=100, max_arcs=0, max_depth=10)
    check(arc0["expandedSemanticStateCount"] == 1, "arc-zero still inspects productive root")
    check(arc0["generatedSemanticArcCount"] == 0, "arc-zero emits no semantic arc")
    check(len(arc0["frontier"]) == 1 and arc0["frontier"][0]["state"] == "S0", "arc-zero root frontier")
    check(arc0["frontier"][0]["cutoff"] == "ARC_LIMIT", "arc-zero cutoff kind")
    check(arc0["frontier"][0]["nextOpportunityOffset"] == 0, "arc-zero offset")
    check(
        arc0["frontier"][0]["pendingOpportunityKeys"]
        == ["A_SOLVED", "B_INVALID", "C_STALLED", "D_PRODUCTIVE", "E_QUEUE_1", "F_QUEUE_2"],
        "arc-zero full pending suffix",
    )

    # 4) Mid-source arc cutoff: exact suffix/offset and queued-unvisited FIFO drain.
    mid = model.search(max_states=100, max_arcs=2, max_depth=10)
    check(mid["generatedSemanticArcCount"] == 2, "mid-source arc cap exact")
    check(mid["frontier"][0]["state"] == "S0" and mid["frontier"][0]["cutoff"] == "ARC_LIMIT", "mid-source active cutoff first")
    check(mid["frontier"][0]["nextOpportunityOffset"] == 2, "mid-source offset")
    check(
        mid["frontier"][0]["pendingOpportunityKeys"]
        == ["C_STALLED", "D_PRODUCTIVE", "E_QUEUE_1", "F_QUEUE_2"],
        "mid-source pending suffix exact",
    )
    check(
        [(f["state"], f["cutoff"]) for f in mid["frontier"][1:]]
        == [("SOL", "UNVISITED_AFTER_ARC_LIMIT"), ("BAD", "UNVISITED_AFTER_ARC_LIMIT")],
        "mid-source queued discoveries drained FIFO",
    )
    check(node(mid, "SOL")["classification"] == "UNINSPECTED", "mid-source global stop does not inspect queued solved")

    # 5) Exact end-of-source cap is NOT a cutoff. At cap, terminal states are still inspectable.
    exact_end = model.search(max_states=100, max_arcs=6, max_depth=10)
    check(exact_end["generatedSemanticArcCount"] == 6, "exact-end arc count remains capped")
    check(node(exact_end, "SOL")["classification"] == "SOLVED", "solved inspected while arc count already at cap")
    check(node(exact_end, "BAD")["classification"] == "INVALID", "invalid inspected while arc count already at cap")
    check(node(exact_end, "STALL")["classification"] == "STALLED", "stalled inspected while arc count already at cap")
    check(exact_end["frontier"][0]["state"] == "P", "first later productive state becomes actual arc-limit source")
    check(exact_end["frontier"][0]["cutoff"] == "ARC_LIMIT", "later productive state cutoff kind")
    check(exact_end["frontier"][0]["nextOpportunityOffset"] == 0, "later productive cutoff offset")
    check(exact_end["frontier"][0]["pendingOpportunityKeys"] == ["P_ALPHA", "P_BETA"], "later productive pending suffix")
    check(
        [(f["state"], f["cutoff"]) for f in exact_end["frontier"][1:]]
        == [("Q1", "UNVISITED_AFTER_ARC_LIMIT"), ("Q2", "UNVISITED_AFTER_ARC_LIMIT")],
        "queued-unvisited ordering after actual later arc cutoff",
    )
    check(all(node(exact_end, s)["classification"] == "UNINSPECTED" for s in ["Q1", "Q2"]), "queued unvisited not mislabeled stalled")

    # 6) Depth-bound productive state is inspected/enumerated, emits no arc, and cannot prove no path.
    depth0 = model.search(max_states=100, max_arcs=100, max_depth=0)
    check(depth0["expandedSemanticStateCount"] == 1, "depth-bound root inspected")
    check(depth0["generatedSemanticArcCount"] == 0, "depth-bound root emits no arc")
    check(node(depth0, "S0")["classification"] == "DEPTH_LIMITED_PRODUCTIVE", "depth-bound productive classification")
    check(depth0["frontier"][0]["cutoff"] == "DEPTH_LIMIT", "depth frontier explicit")
    check(depth0["frontier"][0]["pendingOpportunityKeys"] == node(depth0, "S0")["productiveOpportunityKeys"], "depth frontier retains full productive list")
    check(depth0["semanticSearchCompleteness"] == "INCOMPLETE", "depth-bounded search not globally complete")
    check(depth0["cutoffCauses"] == ["DEPTH_LIMIT"], "depth cause distinct from resource cutoff")
    check(depth0["conclusion"] == "UNKNOWN", "productive depth boundary cannot conclude global no path")

    # 7) Solved / stalled / invalid root semantics remain distinct.
    solved = SyntheticPackedV2([NodeSpec("S0", "SOLVED")], []).search(10, 10, 10)
    check(solved["semanticSearchCompleteness"] == "COMPLETE", "solved root complete")
    check(solved["conclusion"] == "HUMAN_PATH_EXISTS", "solved root conclusion")
    stalled = SyntheticPackedV2([NodeSpec("S0")], []).search(10, 10, 10)
    check(node(stalled, "S0")["classification"] == "STALLED", "normal no-op root stalled")
    check(stalled["semanticSearchCompleteness"] == "COMPLETE", "stalled root complete")
    check(stalled["conclusion"] == "NO_HUMAN_SOLUTION_PATH_UNDER_PROFILE", "complete stalled graph supports no-path conclusion")
    invalid = SyntheticPackedV2([NodeSpec("S0", "INVALID")], []).search(10, 10, 10)
    check(invalid["semanticSearchCompleteness"] == "NOT_APPLICABLE", "invalid root completeness")
    check(invalid["conclusion"] == "INVALID_INPUT", "invalid root conclusion")

    # 8) Result dimensions are explicitly separate.
    for result in [full, state1, arc0, mid, exact_end, depth0]:
        check("semanticSearchCompleteness" in result, "semantic completeness field present")
        check("cutoffCauses" in result, "cutoff causes field present")
        check(result["provenanceLanguageStatus"] == "EXACT_FOR_RECORDED_SEMANTIC_GRAPH", "provenance coverage explicit")
        check(result["explicitHistoryMaterializationStatus"] == "NOT_MATERIALIZED", "materialization status explicit")
        check(result["config"]["budgetVersion"] == "2.0.0", "packed budget version explicit")
        check(result["searchPolicyVersion"] == "BFS_SEMANTIC_STATE_FIRST_DISCOVERY_CP2_ORDER_V2", "packed search identity explicit")

    # 9) Reconvergence, cross-depth minimum-depth bookkeeping, and parallel arcs survive packed search.
    p_nodes, p_arcs = provenance_fixture()
    provenance_model = SyntheticPackedV2(p_nodes, p_arcs)
    provenance = provenance_model.search(100, 100, 10)
    check(node(provenance, "C")["minimumHumanDepth"] == 1, "cross-depth node stores true minimum depth")
    c_histories = provenance_model.enumerate_histories_to(provenance, "C")
    check([h["depth"] for h in c_histories] == [1, 2, 2], "implicit cross-depth provenance remains reconstructable")
    check(sorted(h["cost"] for h in c_histories) == [3, 4, 6], "divergent accumulated costs remain reconstructable")
    cd = [a for a in provenance["semanticArcs"] if a["sourceState"] == "C" and a["targetState"] == "D"]
    check(len(cd) == 2, "parallel source-target arcs retained")
    check({a["opportunityKey"] for a in cd} == {"C_D_ALPHA", "C_D_BETA"}, "parallel opportunity identities retained")
    check(provenance["expandedSemanticStateCount"] == 6, "reconverged states expanded once")

    # 10) Packed-v2 identity is a distinct namespace from legacy-v1 projection identity.
    check(full["packedV2Identity"] != legacy_v1_projection_identity(full), "packed v2 identity distinct from legacy v1 projection identity")

    # 11) Construction-order shuffle invariance for both fixtures.
    expected_budget = canonical_json(full)
    expected_provenance = canonical_json(provenance)
    for seed in range(20):
        rng = random.Random(seed)
        n1, a1 = list(budget_nodes), list(budget_arcs)
        rng.shuffle(n1); rng.shuffle(a1)
        candidate = SyntheticPackedV2(n1, a1).search(100, 100, 10)
        check(canonical_json(candidate) == expected_budget, f"budget fixture shuffle invariant {seed}")
        n2, a2 = list(p_nodes), list(p_arcs)
        rng.shuffle(n2); rng.shuffle(a2)
        candidate2 = SyntheticPackedV2(n2, a2).search(100, 100, 10)
        check(canonical_json(candidate2) == expected_provenance, f"provenance fixture shuffle invariant {seed}")

    # 12) Semantic cycles are rejected.
    try:
        SyntheticPackedV2(p_nodes, p_arcs + [Arc("E", "S0", "ILLEGAL_CYCLE")])
        raise AssertionError("cycle should be rejected")
    except ValueError as exc:
        check(str(exc) == "semantic cycle", "cycle rejection")

    # 13) Negative packed budgets reject early.
    for values in [(-1, 0, 0), (0, -1, 0), (0, 0, -1)]:
        try:
            model.search(*values)
            raise AssertionError("negative budget should reject")
        except ValueError as exc:
            check(str(exc) == "negative budget", f"negative budget reject {values}")

    print(
        "PUBLIC_PACKED_V2_BUDGET_FRONTIER_CONTRACT_PASS "
        f"checks={CHECKS} fullStates={full['expandedSemanticStateCount']} "
        f"fullArcs={full['generatedSemanticArcCount']} "
        f"exactEndCutoffSource={exact_end['frontier'][0]['state']} "
        f"crossDepthHistories={len(c_histories)} parallelArcs={len(cd)}"
    )


if __name__ == "__main__":
    main()
