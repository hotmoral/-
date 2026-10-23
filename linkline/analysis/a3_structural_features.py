"""A3 structural difficulty-feature analyzer over frozen Linkline mechanics.

This module computes A3F01-A3F12 structural descriptors only. It does not
assign human difficulty, production tiers, or calibration weights and does not
consume test-owned Golden expected data.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from typing import Iterable

from analysis.a2_cognitive import proximity
from reference.m2_state_model import (
    ActionV1,
    BoardSpecV1,
    ChainSpecV1,
    ChainStateV1,
    GoalSpecV1,
    PuzzleInstanceV1,
    apply_action,
    hash_puzzle_instance,
    is_solved,
    legal_actions,
)
from reference.m3_solver import SolveStatusV1, solve_puzzle


ANALYZER_VERSION = "1.0.0"
FEATURE_SCHEMA_VERSION = "0.1"
MECHANIC_BASELINE = "a2-v1.0.0"

EXACT = "STRUCTURAL_MEASURED_EXACT"
BOUNDED = "STRUCTURAL_MEASURED_BOUNDED"
INCOMPLETE = "STRUCTURAL_INCOMPLETE"
OUTSIDE = "OUTSIDE_A3_B0_DOMAIN"

FEATURE_NAMES = (
    "shortestDistance",
    "shortestActionSequenceCount",
    "shortestDagStateCount",
    "mandatoryInternalStateCount",
    "initialLegalActionCount",
    "initialShortestActionCount",
    "initialPositiveRegretActionCount",
    "initialMeanRegret",
    "initialMaxRegret",
    "shortestMinProximityUpSteps",
    "shortestMinProximityUpMagnitude",
    "shortestMinRelationalSideSwitches",
)


def _positive_cap(value: int) -> int:
    if type(value) is not int or value < 1:
        raise ValueError("state_cap must be a positive integer")
    return value


def _state(values: Iterable[int]) -> ChainStateV1:
    return ChainStateV1(tuple(values))


def _instance(n: int, length: int, state, targets) -> PuzzleInstanceV1:
    return PuzzleInstanceV1(
        BoardSpecV1(n),
        ChainSpecV1(length),
        GoalSpecV1(*targets),
        _state(state),
    )


def _exact_goal_distance(n: int, length: int, state, targets) -> int | None:
    run = solve_puzzle(_instance(n, length, state, targets))
    if run.result.status is SolveStatusV1.SOLVED:
        return run.result.shortest_distance
    if run.result.status is SolveStatusV1.UNSOLVABLE:
        return None
    raise RuntimeError("Unbudgeted frozen M3 returned INCOMPLETE")


@dataclass(frozen=True)
class _ShortestActionGraph:
    complete: bool
    shortest_distance: int
    depths: dict
    edges: dict
    goals: frozenset


def _shortest_action_graph_known_distance(
    n: int,
    length: int,
    initial,
    targets,
    shortest_distance: int,
    *,
    state_cap: int,
) -> _ShortestActionGraph:
    """Build the complete shortest action graph when the cap permits.

    The exact shortest distance is supplied by frozen M3. This builder preserves
    action identity/multiplicity and fails closed if state_cap prevents complete
    enumeration through depth D.
    """
    state_cap = _positive_cap(state_cap)
    board = BoardSpecV1(n)
    chain = ChainSpecV1(length)
    goal = GoalSpecV1(*targets)
    root = _state(initial)

    depths = {root: 0}
    raw_edges = defaultdict(list)
    queue = deque((root,))
    complete = True

    while queue:
        state = queue.popleft()
        depth = depths[state]
        if depth >= shortest_distance:
            continue

        for action in legal_actions(board, chain, state):
            transition = apply_action(board, chain, state, action)
            if not transition.accepted:
                raise RuntimeError("M2 rejected an M2-enumerated legal action")
            successor = transition.next_state
            next_depth = depth + 1
            if next_depth > shortest_distance:
                continue

            previous = depths.get(successor)
            if previous is None:
                if len(depths) >= state_cap:
                    complete = False
                    break
                depths[successor] = next_depth
                if next_depth < shortest_distance:
                    queue.append(successor)

            if depths.get(successor) == next_depth:
                raw_edges[state].append((action, successor))
        if not complete:
            break

    if not complete:
        return _ShortestActionGraph(False, shortest_distance, depths, {}, frozenset())

    goals = frozenset(
        state
        for state, depth in depths.items()
        if depth == shortest_distance and is_solved(goal, state)
    )
    if not goals:
        raise RuntimeError("Exact M3 distance has no goal in completed shortest-depth graph")

    can_reach = set(goals)
    for depth in range(shortest_distance - 1, -1, -1):
        for state, state_depth in tuple(depths.items()):
            if state_depth != depth:
                continue
            if any(successor in can_reach for _, successor in raw_edges.get(state, ())):
                can_reach.add(state)

    if root not in can_reach:
        raise RuntimeError("Completed graph cannot connect root to exact shortest goal")

    edges = {
        state: tuple(
            (action, successor)
            for action, successor in raw_edges.get(state, ())
            if successor in can_reach and depths[successor] == depths[state] + 1
        )
        for state in can_reach
    }
    return _ShortestActionGraph(True, shortest_distance, depths, edges, goals)


def _path_counts(graph: _ShortestActionGraph, root: ChainStateV1):
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


def _mandatory_count(graph: _ShortestActionGraph, root: ChainStateV1) -> int:
    total, prefix, suffix = _path_counts(graph, root)
    return sum(
        1
        for state in graph.edges
        if 0 < graph.depths[state] < graph.shortest_distance
        and prefix.get(state, 0) * suffix.get(state, 0) == total
    )


def _proximity_costs(graph: _ShortestActionGraph, n: int, targets, root: ChainStateV1):
    ordered = sorted(
        graph.edges,
        key=lambda state: (graph.depths[state], state.path),
        reverse=True,
    )
    min_steps = {}
    min_magnitude = {}
    for state in ordered:
        if state in graph.goals:
            min_steps[state] = 0
            min_magnitude[state] = 0
            continue
        current = proximity(n, state.path, targets)
        step_values = []
        magnitude_values = []
        for _, successor in graph.edges[state]:
            following = proximity(n, successor.path, targets)
            step_values.append(
                (1 if following > current else 0) + min_steps[successor]
            )
            magnitude_values.append(
                max(0, following - current) + min_magnitude[successor]
            )
        min_steps[state] = min(step_values)
        min_magnitude[state] = min(magnitude_values)
    return min_steps[root], min_magnitude[root]


def _relational_switch_cost(graph: _ShortestActionGraph, root: ChainStateV1) -> int:
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


def _feature(status: str, value=None) -> dict:
    row = {"status": status}
    if status != INCOMPLETE:
        row["value"] = value
    return row


def analyze_structural_features(
    n: int,
    length: int,
    initial,
    targets,
    *,
    state_cap: int = 100_000,
) -> dict:
    state_cap = _positive_cap(state_cap)
    instance = _instance(n, length, initial, targets)
    root = instance.initial_state
    solve = solve_puzzle(instance)

    base = {
        "mechanicBaseline": MECHANIC_BASELINE,
        "puzzleFingerprint": hash_puzzle_instance(instance),
        "featureSchemaVersion": FEATURE_SCHEMA_VERSION,
        "analyzerVersion": ANALYZER_VERSION,
        "computationConfig": {"stateCap": state_cap},
        "canonicalInitial": list(root.path),
        "targets": [instance.goal.t0, instance.goal.t1],
    }

    if solve.result.status is SolveStatusV1.UNSOLVABLE or (
        solve.result.status is SolveStatusV1.SOLVED
        and solve.result.shortest_distance == 0
    ):
        base["domainStatus"] = OUTSIDE
        base["features"] = {
            name: _feature(OUTSIDE, None) for name in FEATURE_NAMES
        }
        return base

    if solve.result.status is not SolveStatusV1.SOLVED:
        raise RuntimeError("Unbudgeted frozen M3 returned INCOMPLETE")

    distance = solve.result.shortest_distance
    if distance is None or distance < 1:
        raise RuntimeError("In-domain puzzle requires positive exact distance")

    board = instance.board
    chain = instance.chain
    initial_actions = legal_actions(board, chain, root)
    if not initial_actions:
        raise RuntimeError("Solvable unsolved state has no legal action")

    regrets = []
    shortest_initial = 0
    for action in initial_actions:
        successor = apply_action(board, chain, root, action).next_state
        successor_distance = _exact_goal_distance(
            n,
            length,
            successor.path,
            (instance.goal.t0, instance.goal.t1),
        )
        if successor_distance is None:
            raise RuntimeError("Reversible solvable root produced unsolvable successor")
        regret = 1 + successor_distance - distance
        if regret < 0:
            raise RuntimeError("Negative regret violates exact shortest distance")
        regrets.append(regret)
        if regret == 0:
            shortest_initial += 1

    mean_regret = Fraction(sum(regrets), len(regrets))

    graph = _shortest_action_graph_known_distance(
        n,
        length,
        root.path,
        (instance.goal.t0, instance.goal.t1),
        distance,
        state_cap=state_cap,
    )

    features = {
        "shortestDistance": _feature(EXACT, distance),
        "initialLegalActionCount": _feature(EXACT, len(initial_actions)),
        "initialShortestActionCount": _feature(EXACT, shortest_initial),
        "initialPositiveRegretActionCount": _feature(
            EXACT, sum(value > 0 for value in regrets)
        ),
        "initialMeanRegret": _feature(
            EXACT,
            {
                "numerator": mean_regret.numerator,
                "denominator": mean_regret.denominator,
            },
        ),
        "initialMaxRegret": _feature(EXACT, max(regrets)),
    }

    graph_feature_names = (
        "shortestActionSequenceCount",
        "shortestDagStateCount",
        "mandatoryInternalStateCount",
        "shortestMinProximityUpSteps",
        "shortestMinProximityUpMagnitude",
        "shortestMinRelationalSideSwitches",
    )

    if not graph.complete:
        for name in graph_feature_names:
            features[name] = _feature(INCOMPLETE)
    else:
        total_paths, _, _ = _path_counts(graph, root)
        min_steps, min_magnitude = _proximity_costs(
            graph,
            n,
            (instance.goal.t0, instance.goal.t1),
            root,
        )
        features.update(
            {
                "shortestActionSequenceCount": _feature(EXACT, total_paths),
                "shortestDagStateCount": _feature(EXACT, len(graph.edges)),
                "mandatoryInternalStateCount": _feature(
                    EXACT, _mandatory_count(graph, root)
                ),
                "shortestMinProximityUpSteps": _feature(EXACT, min_steps),
                "shortestMinProximityUpMagnitude": _feature(EXACT, min_magnitude),
                "shortestMinRelationalSideSwitches": _feature(
                    EXACT, _relational_switch_cost(graph, root)
                ),
            }
        )

    # Emit in canonical feature order.
    base["domainStatus"] = "IN_DOMAIN"
    base["features"] = {name: features[name] for name in FEATURE_NAMES}
    return base


def exact_feature_values(
    n: int,
    length: int,
    initial,
    targets,
    *,
    state_cap: int = 100_000,
) -> dict:
    profile = analyze_structural_features(
        n,
        length,
        initial,
        targets,
        state_cap=state_cap,
    )
    if profile["domainStatus"] != "IN_DOMAIN":
        raise ValueError("Puzzle is outside A3-B0 feature domain")

    values = {}
    for name in FEATURE_NAMES:
        row = profile["features"][name]
        if row["status"] != EXACT:
            raise RuntimeError(f"Feature {name} is not exact under current guard")
        values[name] = row["value"]
    return values


def normalized_profile_fingerprint(profile: dict) -> str:
    encoded = json.dumps(profile, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded).hexdigest()
