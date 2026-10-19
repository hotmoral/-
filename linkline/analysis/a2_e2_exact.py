"""A2 E2 exact N=2/3 domain census over frozen M2/M3/A2-B semantics.

This module performs complete finite-domain execution only. It reports exact
counts and boundaries; it does not assign final H1-H8 lifecycle classifications,
human difficulty, or production parameters.
"""
from collections import defaultdict, deque
from itertools import combinations

from reference.m2_state_model import (
    ActionV1,
    BoardSpecV1,
    ChainSpecV1,
    ChainStateV1,
    apply_action,
    legal_actions,
    validate_state,
)
from analysis.a2_cognitive import (
    ct3_nonincreasing_proximity,
    ct3_relational_one_side,
    ct6_solution_space_summary,
    exact_goal_distance,
    proximity,
    representation_key,
)

E2_VERSION = "1.0.0"


def _enumerate_states(n: int, length: int):
    board, chain = BoardSpecV1(n), ChainSpecV1(length)
    found = set()

    def walk(path, used):
        if len(path) == length:
            state = ChainStateV1(path)
            validate_state(board, chain, state)
            found.add(state.path)
            return
        for cell in board.neighbors(path[-1]):
            if cell not in used:
                walk(path + (cell,), used | {cell})

    for cell in range(n * n):
        walk((cell,), {cell})
    return tuple(sorted(found))


def _graph(n: int, length: int):
    board, chain = BoardSpecV1(n), ChainSpecV1(length)
    paths = _enumerate_states(n, length)
    index = {path: i for i, path in enumerate(paths)}
    rows = []
    for path in paths:
        state = ChainStateV1(path)
        row = []
        for action in legal_actions(board, chain, state):
            result = apply_action(board, chain, state, action)
            if not result.accepted:
                raise RuntimeError("M2 enumerated action was rejected")
            row.append(((action.source_cell, action.destination_cell), index[result.next_state.path]))
        rows.append(tuple(row))
    return board, chain, paths, index, tuple(rows)


def _component_count(edges) -> int:
    seen = set()
    count = 0
    for start in range(len(edges)):
        if start in seen:
            continue
        count += 1
        seen.add(start)
        stack = [start]
        while stack:
            node = stack.pop()
            for _, other in edges[node]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
    return count


def _ct1_signature(board, chain, path, pair):
    state = ChainStateV1(path)
    result = apply_action(board, chain, state, ActionV1(*pair))
    return result.accepted, result.next_state.path


def _representation_stats(kind, n, length, board, chain, paths):
    groups = defaultdict(list)
    for path in paths:
        groups[representation_key(kind, n, length, path)].append(path)

    multi = 0
    collisions = 0
    common_accepted = 0
    for key, group in groups.items():
        if len(group) < 2:
            continue
        multi += 1
        endpoint_pair = key[1]
        candidates = tuple(
            (source, destination)
            for source in endpoint_pair
            for destination in board.neighbors(source)
        )
        for first, second in combinations(group, 2):
            pair_collision = False
            pair_common = False
            for action in candidates:
                left = _ct1_signature(board, chain, first, action)
                right = _ct1_signature(board, chain, second, action)
                if left != right:
                    pair_collision = True
                    if left[0] and right[0]:
                        pair_common = True
            collisions += int(pair_collision)
            common_accepted += int(pair_common)
    return multi, collisions, common_accepted


def _reachable_footprints(paths, edges, start, horizon):
    seen = {start: 0}
    queue = deque((start,))
    values = set()
    while queue:
        node = queue.popleft()
        depth = seen[node]
        values.add(tuple(sorted(paths[node])))
        if depth == horizon:
            continue
        for _, other in edges[node]:
            if other not in seen:
                seen[other] = depth + 1
                queue.append(other)
    return values


def _h7_stats(paths, edges):
    count = 0
    minimum_horizon = None
    for root, row in enumerate(edges):
        if len(row) < 2:
            continue
        for (_, first), (_, second) in combinations(row, 2):
            excluded = {
                tuple(sorted(paths[root])),
                tuple(sorted(paths[first])),
                tuple(sorted(paths[second])),
            }
            for horizon in range(1, 5):
                left = _reachable_footprints(paths, edges, first, horizon)
                right = _reachable_footprints(paths, edges, second, horizon)
                if (left ^ right) - excluded:
                    count += 1
                    minimum_horizon = horizon if minimum_horizon is None else min(minimum_horizon, horizon)
                    break
    return count, minimum_horizon


def _targets(n: int):
    return tuple(combinations(range(n * n), 2))


def _domain_row(n: int, length: int):
    board, chain, paths, index, edges = _graph(n, length)
    goal_pairs = _targets(n)

    r1 = _representation_stats("R1", n, length, board, chain, paths)
    r2 = _representation_stats("R2", n, length, board, chain, paths)
    h7_count, h7_min = _h7_stats(paths, edges)

    solvable = 0
    max_distance = 0
    h3l = h3s = h4 = h8 = 0
    ct6_branch = ct6_convergence = 0
    ct6_multi_path = ct6_multi_goal = ct6_mandatory = 0

    for targets in goal_pairs:
        distances = [exact_goal_distance(n, length, path, targets) for path in paths]
        for root, path in enumerate(paths):
            distance = distances[root]
            if distance is None:
                continue
            solvable += 1
            max_distance = max(max_distance, distance)

            observations = []
            for action, other in edges[root]:
                observations.append(
                    (action, other, proximity(n, paths[other], targets), distances[other])
                )

            if any(
                left[2] == right[2] and left[3] != right[3]
                for left, right in combinations(observations, 2)
            ):
                h3l += 1

            if distance > 0:
                restricted = ct3_nonincreasing_proximity(n, length, path, targets)
                if not restricted["restrictedComplete"]:
                    raise RuntimeError("E2 H3-S unexpectedly hit an exact-search cap")
                if restricted["restrictedSolutionExists"] is False:
                    h3s += 1

                one_side = ct3_relational_one_side(n, length, path, targets)
                if not one_side["restrictedComplete"]:
                    raise RuntimeError("E2 H4 unexpectedly hit an exact-search cap")
                if one_side["restrictedSolutionExists"] is False:
                    h4 += 1

            ct6 = ct6_solution_space_summary(n, length, path, targets)
            if not ct6["complete"]:
                raise RuntimeError("E2 CT6 unexpectedly hit an exact-search cap")
            if ct6["branchStates"]:
                ct6_branch += 1
            if ct6["convergenceStates"]:
                ct6_convergence += 1
            if ct6["shortestPathCount"] > 1:
                ct6_multi_path += 1
            if len(ct6["nearestSolvedStates"]) > 1:
                ct6_multi_goal += 1
            if ct6["mandatoryInternalStates"]:
                ct6_mandatory += 1

            if distance > 0 and ct6["mandatoryInternalStates"]:
                mandatory = {tuple(item) for item in ct6["mandatoryInternalStates"]}
                found = False
                for left, right in combinations(observations, 2):
                    if left[2] != right[2]:
                        continue
                    left_short = left[3] == distance - 1
                    right_short = right[3] == distance - 1
                    if left_short == right_short:
                        continue
                    chosen = paths[left[1] if left_short else right[1]]
                    if tuple(chosen) in mandatory:
                        found = True
                        break
                if found:
                    h8 += 1

    return {
        "N": n,
        "L": length,
        "canonicalStates": len(paths),
        "directedEdges": sum(len(row) for row in edges),
        "components": _component_count(edges),
        "goalPairs": len(goal_pairs),
        "puzzleInstances": len(paths) * len(goal_pairs),
        "solvablePuzzleInstances": solvable,
        "maxShortestDistance": max_distance,
        "r1MultiStateGroups": r1[0],
        "r1Ct1CollisionPairs": r1[1],
        "r1CommonAcceptedCollisionPairs": r1[2],
        "r2MultiStateGroups": r2[0],
        "r2Ct1CollisionPairs": r2[1],
        "r2CommonAcceptedCollisionPairs": r2[2],
        "h3lInstances": h3l,
        "h3sRestrictedFailures": h3s,
        "h4RestrictedFailures": h4,
        "h7BranchPairs": h7_count,
        "h8OptimizationInstances": h8,
        "ct6BranchInstances": ct6_branch,
        "ct6ConvergenceInstances": ct6_convergence,
        "ct6MultipleShortestPathInstances": ct6_multi_path,
        "ct6MultipleNearestSolvedInstances": ct6_multi_goal,
        "ct6MandatoryInternalInstances": ct6_mandatory,
    }, h7_min


def _first(rows, field):
    for row in rows:
        if row[field]:
            return {"N": row["N"], "L": row["L"]}
    return None


def build_e2_summary():
    rows = []
    h7_horizons = {}
    for n in (2, 3):
        for length in range(2, n * n + 1):
            row, horizon = _domain_row(n, length)
            rows.append(row)
            h7_horizons[(n, length)] = horizon

    h2_first = _first(rows, "r2Ct1CollisionPairs")
    if h2_first is not None:
        matching = next(row for row in rows if row["N"] == h2_first["N"] and row["L"] == h2_first["L"])
        h2_first = {
            **h2_first,
            "kind": (
                "COMMON_ACCEPTED"
                if matching["r2CommonAcceptedCollisionPairs"]
                else "REJECTED_ACTION_IDENTITY"
            ),
        }

    h7_first = _first(rows, "h7BranchPairs")
    if h7_first is not None:
        h7_first = {
            **h7_first,
            "successorHorizon": h7_horizons[(h7_first["N"], h7_first["L"])],
        }

    return {
        "schemaVersion": 1,
        "domains": rows,
        "boundaries": {
            "H1": {
                "firstCt1Collision": _first(rows, "r1Ct1CollisionPairs"),
                "firstCommonAcceptedCollision": _first(rows, "r1CommonAcceptedCollisionPairs"),
            },
            "H2": {
                "firstCt1Collision": h2_first,
                "commonAcceptedCollisionInE2": any(
                    row["r2CommonAcceptedCollisionPairs"] for row in rows
                ),
            },
            "H3-L": {"firstInstance": _first(rows, "h3lInstances")},
            "H3-S": {
                "firstRestrictedFailure": _first(rows, "h3sRestrictedFailures"),
                "e2FailureCount": sum(row["h3sRestrictedFailures"] for row in rows),
            },
            "H4": {
                "restrictedFailuresInE2": sum(row["h4RestrictedFailures"] for row in rows)
            },
            "H7": {"firstBranchPair": h7_first},
            "H8": {"firstOptimizationInstance": _first(rows, "h8OptimizationInstances")},
        },
    }
