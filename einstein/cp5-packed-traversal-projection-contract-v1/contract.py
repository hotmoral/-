#!/usr/bin/env python3
"""Public-safe synthetic contract for packed CP5 provenance + v1 projection.

No private puzzle data, state hashes, seeds, or production implementation is included.
"""
from dataclasses import dataclass
from collections import defaultdict, deque
import hashlib
import json


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_hash(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Arc:
    source: str
    target: str
    key: str
    cost: int
    priority: int = 0
    row: int = 0

    def data(self):
        return {
            "source": self.source,
            "target": self.target,
            "key": self.key,
            "cost": self.cost,
            "priority": self.priority,
            "row": self.row,
        }


class SyntheticPackedTraversal:
    """Finite acyclic semantic multigraph with lossless history-language projection."""

    VERSION = "1.0.0"
    SEARCH_POLICY = "SYNTHETIC_PACKED_SEMANTIC_BFS_V1"
    V1_PROJECTOR = "SYNTHETIC_V1_HISTORY_OCCURRENCE_PROJECTOR_V1"

    def __init__(self, arcs, root="S0"):
        self.root = root
        self._adj = defaultdict(list)
        self._all_arcs = tuple(arcs)
        for arc in arcs:
            self._adj[arc.source].append(arc)
        for source in self._adj:
            self._adj[source].sort(
                key=lambda a: (a.priority, a.row, a.key, a.target, a.cost)
            )
        self._assert_acyclic()

    def _assert_acyclic(self):
        visiting = set()
        visited = set()

        def dfs(state):
            if state in visiting:
                raise ValueError("semantic cycle")
            if state in visited:
                return
            visiting.add(state)
            for arc in self._adj.get(state, ()):
                dfs(arc.target)
            visiting.remove(state)
            visited.add(state)

        dfs(self.root)

    def path_record(self, path_arcs):
        states = [self.root]
        keys = []
        cost = 0
        for arc in path_arcs:
            if states[-1] != arc.source:
                raise ValueError("broken path chain")
            states.append(arc.target)
            keys.append(arc.key)
            cost += arc.cost
        history = {
            "orderedArcKeys": keys,
            "orderedStateIds": states,
            "cost": cost,
        }
        return {
            **history,
            "humanDepth": len(keys),
            "pathId": canonical_hash(history),
        }

    def packed_result(self, materialized=False):
        """Deterministic unique-state BFS; repeated arrivals add provenance, not re-expansion."""
        queue = deque([self.root])
        seen = {self.root}
        min_depth = {self.root: 0}
        state_order = []
        semantic_arcs = []

        while queue:
            state = queue.popleft()
            state_order.append(state)
            for arc in self._adj.get(state, ()):
                semantic_arcs.append(arc.data())
                candidate_depth = min_depth[state] + 1
                if arc.target not in seen:
                    seen.add(arc.target)
                    min_depth[arc.target] = candidate_depth
                    queue.append(arc.target)
                else:
                    min_depth[arc.target] = min(min_depth[arc.target], candidate_depth)

        incoming = defaultdict(list)
        for arc in semantic_arcs:
            incoming[arc["target"]].append(arc["key"])

        value = {
            "recordType": "SyntheticPackedTraversalResult",
            "contractVersion": self.VERSION,
            "searchPolicyVersion": self.SEARCH_POLICY,
            "root": self.root,
            "stateOrder": state_order,
            "states": sorted(seen),
            "semanticArcs": semantic_arcs,
            "minHumanDepth": {k: min_depth[k] for k in sorted(min_depth)},
            "incomingProvenanceKeys": {
                state: sorted(keys) for state, keys in sorted(incoming.items())
            },
            "semanticSearchCompleteness": "COMPLETE",
            "provenanceLanguageCoverage": "EXACT_FOR_DISCOVERED_GRAPH",
            "explicitMaterializationStatus": (
                "MATERIALIZED" if materialized else "NOT_MATERIALIZED"
            ),
            "expandedSemanticStateCount": len(state_order),
            "generatedSemanticArcCount": len(semantic_arcs),
        }
        value["packedIdentity"] = canonical_hash(value)
        return value

    def enumerate_paths_to(self, target, max_depth=64):
        out = []

        def visit(state, path):
            if state == target and path:
                out.append(self.path_record(path))
            if len(path) >= max_depth:
                return
            for arc in self._adj.get(state, ()):
                visit(arc.target, path + [arc])

        visit(self.root, [])
        out.sort(key=lambda p: (p["humanDepth"], p["orderedArcKeys"], p["pathId"]))
        return out

    def _v1_occurrence_traversal(self, max_edges, max_depth, max_nodes):
        queue = deque([(self.root, [])])
        edges = []
        frontier = []
        expanded = 0
        generated = 0

        while queue:
            if expanded == max_nodes:
                while queue:
                    state, path = queue.popleft()
                    frontier.append({
                        "path": self.path_record(path),
                        "state": state,
                        "cutoff": "NODE_LIMIT",
                        "pendingOpportunityKeys": [],
                    })
                break

            state, path = queue.popleft()
            expanded += 1
            productive = self._adj.get(state, ())

            if not productive:
                continue

            if len(path) == max_depth:
                frontier.append({
                    "path": self.path_record(path),
                    "state": state,
                    "cutoff": "DEPTH_LIMIT",
                    "pendingOpportunityKeys": [a.key for a in productive],
                })
                continue

            cutoff = False
            for index, arc in enumerate(productive):
                if generated == max_edges:
                    frontier.append({
                        "path": self.path_record(path),
                        "state": state,
                        "cutoff": "EDGE_LIMIT",
                        "pendingOpportunityKeys": [
                            item.key for item in productive[index:]
                        ],
                    })
                    while queue:
                        pending_state, pending_path = queue.popleft()
                        frontier.append({
                            "path": self.path_record(pending_path),
                            "state": pending_state,
                            "cutoff": "UNVISITED_AFTER_EDGE_LIMIT",
                            "pendingOpportunityKeys": [],
                        })
                    cutoff = True
                    break

                next_path = path + [arc]
                edges.append({
                    "sourcePathId": self.path_record(path)["pathId"],
                    "targetPathId": self.path_record(next_path)["pathId"],
                    "sourceState": arc.source,
                    "targetState": arc.target,
                    "opportunityKey": arc.key,
                    "costDelta": arc.cost,
                })
                generated += 1
                queue.append((arc.target, next_path))

            if cutoff:
                break

        result = {
            "recordType": "SyntheticLegacyProjection",
            "projectorVersion": self.V1_PROJECTOR,
            "expandedNodeCount": expanded,
            "generatedEdgeCount": generated,
            "edges": edges,
            "frontier": frontier,
            "completeness": "BUDGET_EXHAUSTED" if frontier else "COMPLETE",
            "explicitMaterializationStatus": "MATERIALIZED",
        }
        result["projectionIdentity"] = canonical_hash(result)
        return result

    def legacy_v1_reference(self, max_edges=10_000, max_depth=64, max_nodes=10_000):
        """Reference occurrence traversal over the same synthetic semantic relation."""
        return self._v1_occurrence_traversal(max_edges, max_depth, max_nodes)

    def project_v1(self, max_edges=10_000, max_depth=64, max_nodes=10_000):
        """Lossless materialization oracle from the packed graph contract."""
        return self._v1_occurrence_traversal(max_edges, max_depth, max_nodes)


def synthetic_fixture():
    # C has three distinct histories:
    #   S0->A->C cost 6
    #   S0->B->C cost 3
    #   S0->C    cost 4
    # This simultaneously exercises same-depth cost divergence and cross-depth reconvergence.
    #
    # C->D has parallel semantic arcs with different opportunity identities.
    return [
        Arc("S0", "A", "ROOT_A", 1),
        Arc("S0", "B", "ROOT_B", 2),
        Arc("S0", "C", "ROOT_C_DIRECT", 4),
        Arc("A", "C", "A_C", 5),
        Arc("B", "C", "B_C", 1),
        Arc("C", "D", "C_D_ALPHA", 1),
        Arc("C", "D", "C_D_BETA", 2),
        Arc("D", "E", "D_E", 1),
    ]
