#!/usr/bin/env python3
"""Public-safe synthetic model for packed-v2 native budget/frontier semantics."""
from collections import defaultdict, deque
from dataclasses import dataclass
import hashlib
import json


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_hash(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class NodeSpec:
    state: str
    terminal: str = "NORMAL"  # NORMAL / SOLVED / INVALID


@dataclass(frozen=True)
class Arc:
    source: str
    target: str
    key: str
    cost: int = 1
    priority: int = 0


class SyntheticPackedV2:
    EXPLORER_VERSION = "2.0.0"
    SEARCH_POLICY = "BFS_SEMANTIC_STATE_FIRST_DISCOVERY_CP2_ORDER_V2"
    BUDGET_VERSION = "2.0.0"
    NODE_VERSION = "2.0.0"
    ARC_VERSION = "2.0.0"
    FRONTIER_VERSION = "2.0.0"

    def __init__(self, nodes, arcs, root="S0"):
        self.root = root
        self.nodes = {}
        for node in nodes:
            if node.state in self.nodes:
                raise ValueError("duplicate node")
            if node.terminal not in {"NORMAL", "SOLVED", "INVALID"}:
                raise ValueError("unknown terminal kind")
            self.nodes[node.state] = node
        if root not in self.nodes:
            raise ValueError("missing root")

        self.adj = defaultdict(list)
        seen_keys = set()
        for arc in arcs:
            if arc.source not in self.nodes or arc.target not in self.nodes:
                raise ValueError("arc references missing node")
            identity = (arc.source, arc.key)
            if identity in seen_keys:
                raise ValueError("duplicate source/opportunity")
            seen_keys.add(identity)
            self.adj[arc.source].append(arc)
        for source in self.adj:
            self.adj[source].sort(
                key=lambda a: (a.priority, a.key, a.target, a.cost)
            )
        self._assert_acyclic()

    def _assert_acyclic(self):
        visiting = set()
        visited = set()

        def visit(state):
            if state in visiting:
                raise ValueError("semantic cycle")
            if state in visited:
                return
            visiting.add(state)
            for arc in self.adj.get(state, ()):  # exact semantic relation
                visit(arc.target)
            visiting.remove(state)
            visited.add(state)

        for state in sorted(self.nodes):
            visit(state)

    @staticmethod
    def _state_hash(state):
        return canonical_hash({"syntheticState": state})

    def _arc_record(self, arc, opportunity_index, generated_ordinal):
        payload = {
            "recordType": "SyntheticPackedSemanticArc",
            "arcVersion": self.ARC_VERSION,
            "sourceState": arc.source,
            "sourceStateHash": self._state_hash(arc.source),
            "targetState": arc.target,
            "targetStateHash": self._state_hash(arc.target),
            "opportunityKey": arc.key,
            "costDelta": arc.cost,
            "sourceOpportunityIndex": opportunity_index,
            "generatedSemanticArcOrdinal": generated_ordinal,
        }
        return {**payload, "semanticArcId": canonical_hash(payload)}

    def _frontier_record(self, state, min_depth, cutoff, inspection, offset, pending):
        return {
            "recordType": "SyntheticPackedFrontierWitness",
            "frontierVersion": self.FRONTIER_VERSION,
            "state": state,
            "stateHash": self._state_hash(state),
            "minimumHumanDepth": min_depth,
            "inspectionStatus": inspection,
            "cutoff": cutoff,
            "nextOpportunityOffset": offset,
            "pendingOpportunityKeys": list(pending),
        }

    def search(self, max_states, max_arcs, max_depth):
        if min(max_states, max_arcs, max_depth) < 0:
            raise ValueError("negative budget")

        config = {
            "recordType": "SyntheticPackedV2Config",
            "budgetVersion": self.BUDGET_VERSION,
            "maxExpandedSemanticStates": max_states,
            "maxGeneratedSemanticArcs": max_arcs,
            "maxDepth": max_depth,
        }
        records = {}
        discovery_order = []
        queue = deque()
        discovery_counter = 0

        def discover(state, depth):
            nonlocal discovery_counter
            if state in records:
                if depth < records[state]["minimumHumanDepth"]:
                    raise AssertionError("first-discovery BFS depth was not minimum")
                return False
            record = {
                "recordType": "SyntheticPackedSemanticStateNode",
                "nodeVersion": self.NODE_VERSION,
                "state": state,
                "stateHash": self._state_hash(state),
                "firstDiscoveryOrdinal": discovery_counter,
                "minimumHumanDepth": depth,
                "inspectionStatus": "UNINSPECTED",
                "classification": "UNINSPECTED",
                "productiveOpportunityKeys": None,
                "outgoingSemanticArcIds": [],
            }
            discovery_counter += 1
            records[state] = record
            discovery_order.append(state)
            queue.append(state)
            return True

        discover(self.root, 0)
        semantic_arcs = []
        frontier = []
        cutoff_causes = []
        solved = []
        stalled = []
        invalid = []
        expanded = 0
        generated = 0
        stop = False

        def add_cause(cause):
            if cause not in cutoff_causes:
                cutoff_causes.append(cause)

        def drain(cutoff):
            while queue:
                state = queue.popleft()
                rec = records[state]
                frontier.append(
                    self._frontier_record(
                        state,
                        rec["minimumHumanDepth"],
                        cutoff,
                        "UNINSPECTED",
                        0,
                        [],
                    )
                )

        while queue and not stop:
            # State budget is consumed by inspection. A queued state at the cap is
            # still discovered, but remains explicitly uninspected.
            if expanded == max_states:
                add_cause("SEMANTIC_STATE_LIMIT")
                drain("STATE_LIMIT")
                break

            state = queue.popleft()
            rec = records[state]
            spec = self.nodes[state]
            rec["inspectionStatus"] = "INSPECTED"
            expanded += 1

            if spec.terminal == "INVALID":
                rec["classification"] = "INVALID"
                rec["productiveOpportunityKeys"] = []
                invalid.append(state)
                continue
            if spec.terminal == "SOLVED":
                rec["classification"] = "SOLVED"
                rec["productiveOpportunityKeys"] = []
                solved.append(state)
                continue

            productive = list(self.adj.get(state, ()))
            rec["productiveOpportunityKeys"] = [arc.key for arc in productive]
            if not productive:
                rec["classification"] = "STALLED"
                stalled.append(state)
                continue

            depth = rec["minimumHumanDepth"]
            if depth == max_depth:
                rec["classification"] = "DEPTH_LIMITED_PRODUCTIVE"
                add_cause("DEPTH_LIMIT")
                frontier.append(
                    self._frontier_record(
                        state,
                        depth,
                        "DEPTH_LIMIT",
                        "INSPECTED",
                        0,
                        [arc.key for arc in productive],
                    )
                )
                continue

            rec["classification"] = "EXPANDABLE"
            for index, arc in enumerate(productive):
                # Equality alone is not a cutoff. A cutoff exists only when the
                # next semantic arc would exceed the budget.
                if generated == max_arcs:
                    add_cause("SEMANTIC_ARC_LIMIT")
                    frontier.append(
                        self._frontier_record(
                            state,
                            depth,
                            "ARC_LIMIT",
                            "INSPECTED",
                            index,
                            [item.key for item in productive[index:]],
                        )
                    )
                    drain("UNVISITED_AFTER_ARC_LIMIT")
                    stop = True
                    break

                arc_record = self._arc_record(arc, index, generated)
                semantic_arcs.append(arc_record)
                rec["outgoingSemanticArcIds"].append(arc_record["semanticArcId"])
                generated += 1
                discover(arc.target, depth + 1)

        initial_invalid = (
            records[self.root]["inspectionStatus"] == "INSPECTED"
            and records[self.root]["classification"] == "INVALID"
        )
        if initial_invalid:
            completeness = "NOT_APPLICABLE"
            conclusion = "INVALID_INPUT"
        else:
            completeness = "COMPLETE" if not frontier else "INCOMPLETE"
            if solved:
                conclusion = "HUMAN_PATH_EXISTS"
            elif completeness == "COMPLETE":
                conclusion = "NO_HUMAN_SOLUTION_PATH_UNDER_PROFILE"
            else:
                conclusion = "UNKNOWN"

        ordered_nodes = [records[state] for state in discovery_order]
        max_min_depth = max((r["minimumHumanDepth"] for r in ordered_nodes), default=0)
        result = {
            "recordType": "SyntheticPackedPathExplorerResultV2",
            "explorerVersion": self.EXPLORER_VERSION,
            "searchPolicyVersion": self.SEARCH_POLICY,
            "budgetVersion": self.BUDGET_VERSION,
            "config": config,
            "rootState": self.root,
            "rootStateHash": self._state_hash(self.root),
            "expandedSemanticStateCount": expanded,
            "generatedSemanticArcCount": generated,
            "distinctSemanticStateCount": len(ordered_nodes),
            "maxMinimumDepthReached": max_min_depth,
            "semanticSearchCompleteness": completeness,
            "cutoffCauses": cutoff_causes,
            "provenanceLanguageStatus": "EXACT_FOR_RECORDED_SEMANTIC_GRAPH",
            "explicitHistoryMaterializationStatus": "NOT_MATERIALIZED",
            "conclusion": conclusion,
            "solvedSemanticStates": solved,
            "stalledSemanticStates": stalled,
            "invalidSemanticStates": invalid,
            "semanticNodes": ordered_nodes,
            "semanticArcs": semantic_arcs,
            "frontier": frontier,
        }
        result["packedV2Identity"] = canonical_hash(result)
        return result

    def enumerate_histories_to(self, search_result, target, max_depth=32):
        by_source = defaultdict(list)
        for arc in search_result["semanticArcs"]:
            by_source[arc["sourceState"]].append(arc)
        for source in by_source:
            by_source[source].sort(key=lambda a: a["sourceOpportunityIndex"])
        out = []

        def visit(state, keys, cost):
            if state == target and keys:
                out.append({"keys": list(keys), "depth": len(keys), "cost": cost})
            if len(keys) >= max_depth:
                return
            for arc in by_source.get(state, ()):  # acyclic by constructor
                visit(
                    arc["targetState"],
                    keys + [arc["opportunityKey"]],
                    cost + arc["costDelta"],
                )

        visit(self.root, [], 0)
        out.sort(key=lambda h: (h["depth"], h["keys"], h["cost"]))
        return out


def legacy_v1_projection_identity(packed_result):
    """Namespace-separation witness only; does not re-prove legacy projection."""
    payload = {
        "recordType": "SyntheticLegacyV1ProjectionIdentity",
        "projectionVersion": "1.0.0",
        "rootStateHash": packed_result["rootStateHash"],
        "generatedOccurrenceEdgeCount": packed_result["generatedSemanticArcCount"],
    }
    return canonical_hash(payload)


def budget_fixture():
    # Root emits exactly six arcs. With max_arcs=6 the cap is reached at the
    # exact end of the root source, so no cutoff exists yet. SOLVED, INVALID,
    # and STALLED children can then be inspected at the cap. The next PRODUCTIVE
    # child becomes ARC_LIMIT only when it actually requests another arc; two
    # later queued states remain UNVISITED_AFTER_ARC_LIMIT in FIFO order.
    nodes = [
        NodeSpec("S0"),
        NodeSpec("SOL", "SOLVED"),
        NodeSpec("BAD", "INVALID"),
        NodeSpec("STALL"),
        NodeSpec("P"),
        NodeSpec("Q1"),
        NodeSpec("Q2"),
        NodeSpec("PX"),
        NodeSpec("PY"),
    ]
    arcs = [
        Arc("S0", "SOL", "A_SOLVED"),
        Arc("S0", "BAD", "B_INVALID"),
        Arc("S0", "STALL", "C_STALLED"),
        Arc("S0", "P", "D_PRODUCTIVE"),
        Arc("S0", "Q1", "E_QUEUE_1"),
        Arc("S0", "Q2", "F_QUEUE_2"),
        Arc("P", "PX", "P_ALPHA"),
        Arc("P", "PY", "P_BETA"),
    ]
    return nodes, arcs


def provenance_fixture():
    # C is reached directly at depth 1 and through A/B at depth 2; C->D has
    # parallel opportunity arcs. This reuses only public-safe synthetic ideas.
    nodes = [
        NodeSpec("S0"), NodeSpec("A"), NodeSpec("B"), NodeSpec("C"),
        NodeSpec("D"), NodeSpec("E"),
    ]
    arcs = [
        Arc("S0", "A", "ROOT_A", 1),
        Arc("S0", "B", "ROOT_B", 2),
        Arc("S0", "C", "ROOT_C_DIRECT", 4),
        Arc("A", "C", "A_C", 5),
        Arc("B", "C", "B_C", 1),
        Arc("C", "D", "C_D_ALPHA", 1),
        Arc("C", "D", "C_D_BETA", 2),
        Arc("D", "E", "D_E", 1),
    ]
    return nodes, arcs
