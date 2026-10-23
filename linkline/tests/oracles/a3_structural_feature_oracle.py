"""Independent A3 structural-feature oracle over frozen M2/M3 mechanics.

This module is test-owned. It does not import the production A3 analyzer and
computes A3F01-A3F12 independently from the production implementation.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from typing import Iterable

from reference.m2_state_model import (
    ActionV1,
    BoardSpecV1,
    ChainSpecV1,
    ChainStateV1,
    GoalSpecV1,
    PuzzleInstanceV1,
    apply_action,
    is_solved,
    legal_actions,
)
from reference.m3_solver import SolveStatusV1, solve_puzzle


ORACLE_VERSION = "1.0.0"
FEATURE_SCHEMA_VERSION = "0.1"


def _state(values: Iterable[int]) -> ChainStateV1:
    return ChainStateV1(tuple(values))


def _instance(n: int, length: int, state, targets) -> PuzzleInstanceV1:
    return PuzzleInstanceV1(
        BoardSpecV1(n),
        ChainSpecV1(length),
        GoalSpecV1(*targets),
        _state(state),
    )


def _manhattan(n: int, first: int, second: int) -> int:
    r0, c0 = divmod(first, n)
    r1, c1 = divmod(second, n)
    return abs(r0 - r1) + abs(c0 - c1)


def proximity(n: int, state, targets) -> int:
    path = _state(state).path
    first, second = path[0], path[-1]
    t0, t1 = tuple(targets)
    return min(
        _manhattan(n, first, t0) + _manhattan(n, second, t1),
        _manhattan(n, first, t1) + _manhattan(n, second, t0),
    )


def exact_goal_distance(n: int, length: int, state, targets) -> int | None:
    run = solve_puzzle(_instance(n, length, state, targets))
    if run.result.status is SolveStatusV1.SOLVED:
        return run.result.shortest_distance
    if run.result.status is SolveStatusV1.UNSOLVABLE:
        return None
    raise RuntimeError("Unbudgeted frozen M3 returned INCOMPLETE")


@dataclass(frozen=True)
class _ShortestActionGraph:
    shortest_distance: int
    depths: dict
    edges: dict
    goals: frozenset


def _shortest_action_graph(
    n: int,
    length: int,
    initial,
    targets,
    *,
    state_cap: int = 100_000,
) -> _ShortestActionGraph | None:
    if type(state_cap) is not int or state_cap < 1:
        raise ValueError("state_cap must be a positive integer")

    board = BoardSpecV1(n)
    chain = ChainSpecV1(length)
    goal = GoalSpecV1(*targets)
    root = _state(initial)

    if is_solved(goal, root):
        return _ShortestActionGraph(0, {root: 0}, {root: ()}, frozenset((root,)))

    depths = {root: 0}
    raw_edges = defaultdict(list)
    queue = deque((root,))
    shortest = None

    while queue:
        state = queue.popleft()
        depth = depths[state]
        if shortest is not None and depth >= shortest:
            continue

        for action in legal_actions(board, chain, state):
            transition = apply_action(board, chain, state, action)
            if not transition.accepted:
                raise RuntimeError("M2 rejected an M2-enumerated legal action")
            successor = transition.next_state
            next_depth = depth + 1
            if shortest is not None and next_depth > shortest:
                continue

            previous = depths.get(successor)
            if previous is None:
                if len(depths) >= state_cap:
                    return None
                depths[successor] = next_depth
                queue.append(successor)

            if depths.get(successor) == next_depth:
                # Preserve action identity/multiplicity even when successors converge.
                raw_edges[state].append((action, successor))

            if is_solved(goal, successor):
                shortest = next_depth if shortest is None else min(shortest, next_depth)

    if shortest is None:
        return _ShortestActionGraph(-1, depths, dict(raw_edges), frozenset())

    goals = frozenset(
        state
        for state, depth in depths.items()
        if depth == shortest and is_solved(goal, state)
    )

    can_reach = set(goals)
    for depth in range(shortest - 1, -1, -1):
        for state, state_depth in tuple(depths.items()):
            if state_depth != depth:
                continue
            if any(successor in can_reach for _, successor in raw_edges.get(state, ())):
                can_reach.add(state)

    edges = {
        state: tuple(
            (action, successor)
            for action, successor in raw_edges.get(state, ())
            if successor in can_reach and depths[successor] == depths[state] + 1
        )
        for state in can_reach
    }
    return _ShortestActionGraph(shortest, depths, edges, goals)


def _shortest_path_counts(graph: _ShortestActionGraph, initial) -> tuple[int, dict, dict]:
    root = _state(initial)
    ordered = sorted(graph.edges, key=lambda state: (graph.depths[state], state.path))

    prefix = defaultdict(int)
    prefix[root] = 1
    for state in ordered:
        for _, successor in graph.edges.get(state, ()):
            prefix[successor] += prefix[state]

    suffix = {}
    for state in reversed(ordered):
        if state in graph.goals:
            suffix[state] = 1
        else:
            suffix[state] = sum(
                suffix[successor] for _, successor in graph.edges.get(state, ())
            )

    return suffix[root], dict(prefix), suffix


def _mandatory_internal_state_count(graph: _ShortestActionGraph, initial) -> int:
    total, prefix, suffix = _shortest_path_counts(graph, initial)
    count = 0
    for state in graph.edges:
        depth = graph.depths[state]
        if depth <= 0 or depth >= graph.shortest_distance:
            continue
        if prefix.get(state, 0) * suffix.get(state, 0) == total:
            count += 1
    return count


def _min_proximity_costs(graph: _ShortestActionGraph, n: int, targets, initial):
    root = _state(initial)
    ordered = sorted(
        graph.edges,
        key=lambda state: (graph.depths[state], state.path),
        reverse=True,
    )

    min_up_steps = {}
    min_up_magnitude = {}
    for state in ordered:
        if state in graph.goals:
            min_up_steps[state] = 0
            min_up_magnitude[state] = 0
            continue

        current_h = proximity(n, state.path, targets)
        step_values = []
        magnitude_values = []
        for _, successor in graph.edges[state]:
            successor_h = proximity(n, successor.path, targets)
            step_values.append(
                (1 if successor_h > current_h else 0) + min_up_steps[successor]
            )
            magnitude_values.append(
                max(0, successor_h - current_h) + min_up_magnitude[successor]
            )
        min_up_steps[state] = min(step_values)
        min_up_magnitude[state] = min(magnitude_values)

    return min_up_steps[root], min_up_magnitude[root]


def _min_relational_switches(graph: _ShortestActionGraph, initial) -> int:
    root = _state(initial)
    if graph.shortest_distance <= 1:
        return 0

    memo = {}

    def best(state: ChainStateV1, previous_destination: int) -> int:
        key = (state, previous_destination)
        if key in memo:
            return memo[key]
        if state in graph.goals:
            return 0

        value = min(
            (0 if action.source_cell == previous_destination else 1)
            + best(successor, action.destination_cell)
            for action, successor in graph.edges[state]
        )
        memo[key] = value
        return value

    return min(
        best(successor, action.destination_cell)
        for action, successor in graph.edges[root]
    )


def feature_values(n: int, length: int, initial, targets, *, state_cap: int = 100_000) -> dict:
    graph = _shortest_action_graph(
        n,
        length,
        initial,
        targets,
        state_cap=state_cap,
    )
    if graph is None:
        raise RuntimeError("Golden oracle state cap reached")
    if graph.shortest_distance <= 0:
        raise ValueError("Golden case must be initially unsolved and solvable")

    root = _state(initial)
    board = BoardSpecV1(n)
    chain = ChainSpecV1(length)
    initial_actions = legal_actions(board, chain, root)

    regrets = []
    shortest_initial = 0
    for action in initial_actions:
        successor = apply_action(board, chain, root, action).next_state
        successor_distance = exact_goal_distance(n, length, successor.path, targets)
        if successor_distance is None:
            raise RuntimeError("Reversible solvable root produced unsolvable successor")
        regret = 1 + successor_distance - graph.shortest_distance
        if regret < 0:
            raise RuntimeError("Negative regret violates shortest-distance semantics")
        regrets.append(regret)
        if regret == 0:
            shortest_initial += 1

    total_paths, _, _ = _shortest_path_counts(graph, root.path)
    mean_regret = Fraction(sum(regrets), len(regrets))
    min_up_steps, min_up_magnitude = _min_proximity_costs(
        graph,
        n,
        targets,
        root.path,
    )

    return {
        "shortestDistance": graph.shortest_distance,
        "shortestActionSequenceCount": total_paths,
        "shortestDagStateCount": len(graph.edges),
        "mandatoryInternalStateCount": _mandatory_internal_state_count(graph, root.path),
        "initialLegalActionCount": len(initial_actions),
        "initialShortestActionCount": shortest_initial,
        "initialPositiveRegretActionCount": sum(value > 0 for value in regrets),
        "initialMeanRegret": {
            "numerator": mean_regret.numerator,
            "denominator": mean_regret.denominator,
        },
        "initialMaxRegret": max(regrets),
        "shortestMinProximityUpSteps": min_up_steps,
        "shortestMinProximityUpMagnitude": min_up_magnitude,
        "shortestMinRelationalSideSwitches": _min_relational_switches(graph, root.path),
    }


def case_payload(case: dict) -> dict:
    values = feature_values(
        case["n"],
        case["length"],
        case["initial"],
        case["targets"],
    )
    return {
        "id": case["id"],
        "n": case["n"],
        "length": case["length"],
        "initial": list(case["initial"]),
        "targets": list(case["targets"]),
        "note": case["note"],
        "expected": values,
    }


def normalized_fingerprint(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded).hexdigest()
