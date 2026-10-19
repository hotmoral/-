"""A2 production cognitive analyzer over frozen M2/M3 semantics.

The module computes exact task observations only. It does not assign A2
hypothesis statuses, human-strategy claims, difficulty, or production policy.
Golden expected data is test-owned and never generated here.
"""

from collections import deque
from dataclasses import dataclass
from typing import Iterable

from reference.m2_state_model import (
    ActionV1,
    BoardSpecV1,
    ChainSpecV1,
    ChainStateV1,
    GoalSpecV1,
    PuzzleInstanceV1,
    apply_action,
    endpoints,
    is_solved,
    legal_actions,
    occupied,
)
from reference.m3_solver import SolveStatusV1, solve_puzzle

ANALYZER_VERSION = "1.0.0"


def _positive_cap(value: int, name: str) -> int:
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _state(values: Iterable[int]) -> ChainStateV1:
    return ChainStateV1(tuple(values))


def _action(values: Iterable[int]) -> ActionV1:
    source, destination = tuple(values)
    return ActionV1(source, destination)


def _instance(n: int, length: int, state, targets) -> PuzzleInstanceV1:
    return PuzzleInstanceV1(
        BoardSpecV1(n),
        ChainSpecV1(length),
        GoalSpecV1(*targets),
        _state(state),
    )


def _pair(action: ActionV1) -> list[int]:
    return [action.source_cell, action.destination_cell]


def _manhattan(n: int, first: int, second: int) -> int:
    r0, c0 = divmod(first, n)
    r1, c1 = divmod(second, n)
    return abs(r0 - r1) + abs(c0 - c1)


def proximity(n: int, state, targets) -> int:
    """R4 endpoint-to-target Manhattan descriptor, orientation invariant."""
    path = _state(state).path
    first, second = path[0], path[-1]
    t0, t1 = tuple(targets)
    return min(
        _manhattan(n, first, t0) + _manhattan(n, second, t1),
        _manhattan(n, first, t1) + _manhattan(n, second, t0),
    )


def representation_key(kind: str, n: int, length: int, state, targets=None):
    """Return an exact reduced-representation grouping key for R1-R4.

    R5 is intentionally excluded because it is a strategy restriction, not a
    mechanical representation with persistent endpoint identity.
    """
    path = _state(state).path
    target_key = None if targets is None else tuple(sorted(tuple(targets)))
    endpoint_key = tuple(sorted((path[0], path[-1])))
    if kind == "R1":
        return (target_key, endpoint_key)
    if kind == "R2":
        return (target_key, endpoint_key, tuple(sorted(path)))
    if kind == "R3":
        return (n, length, target_key, path)
    if kind == "R4":
        if targets is None:
            raise ValueError("R4 requires targets")
        return (target_key, proximity(n, path, targets))
    raise ValueError(f"Unsupported representation: {kind}")


def ct1_transition(n: int, length: int, state, action) -> dict:
    board, chain = BoardSpecV1(n), ChainSpecV1(length)
    result = apply_action(board, chain, _state(state), _action(action))
    return {"accepted": result.accepted, "nextState": list(result.next_state.path)}


def ct2_project_sequence(n: int, length: int, initial, actions) -> dict:
    """Project an explicit sequence, stopping at the first rejected action."""
    board, chain = BoardSpecV1(n), ChainSpecV1(length)
    state = _state(initial)
    for index, values in enumerate(actions):
        result = apply_action(board, chain, state, _action(values))
        if not result.accepted:
            return {
                "complete": False,
                "invalidStep": index,
                "finalState": list(state.path),
            }
        state = result.next_state
    return {"complete": True, "invalidStep": None, "finalState": list(state.path)}


def exact_goal_distance(n: int, length: int, state, targets):
    """Consume M3 exact status/distance without redefining solver semantics."""
    run = solve_puzzle(_instance(n, length, state, targets))
    if run.result.status is SolveStatusV1.SOLVED:
        return run.result.shortest_distance
    if run.result.status is SolveStatusV1.UNSOLVABLE:
        return None
    raise RuntimeError("Unbudgeted M3 solve returned INCOMPLETE")


def exact_future(n: int, length: int, state) -> list[dict]:
    board, chain = BoardSpecV1(n), ChainSpecV1(length)
    current = _state(state)
    rows = []
    for action in legal_actions(board, chain, current):
        result = apply_action(board, chain, current, action)
        if not result.accepted:
            raise RuntimeError("M2 rejected an M2-enumerated legal action")
        rows.append({"action": _pair(action), "nextState": list(result.next_state.path)})
    return rows


def _unrestricted_summary(n: int, length: int, initial, targets) -> tuple[bool, int | None]:
    run = solve_puzzle(_instance(n, length, initial, targets))
    if run.result.status is SolveStatusV1.SOLVED:
        return True, run.result.shortest_distance
    if run.result.status is SolveStatusV1.UNSOLVABLE:
        return False, None
    raise RuntimeError("Unbudgeted M3 solve returned INCOMPLETE")


def ct3_nonincreasing_proximity(
    n: int,
    length: int,
    initial,
    targets,
    *,
    state_cap: int = 100_000,
) -> dict:
    """Exact CT3 closure for H(next) <= H(current)."""
    state_cap = _positive_cap(state_cap, "state_cap")
    unrestricted, distance = _unrestricted_summary(n, length, initial, targets)
    board, chain, goal = BoardSpecV1(n), ChainSpecV1(length), GoalSpecV1(*targets)
    root = _state(initial)
    queue = deque((root,))
    seen = {root}
    solved = is_solved(goal, root)
    while queue and not solved:
        state = queue.popleft()
        current_value = proximity(n, state.path, targets)
        for action in legal_actions(board, chain, state):
            successor = apply_action(board, chain, state, action).next_state
            if proximity(n, successor.path, targets) > current_value or successor in seen:
                continue
            if len(seen) >= state_cap:
                return {
                    "unrestrictedSolutionExists": unrestricted,
                    "unrestrictedShortestDistance": distance,
                    "restrictedComplete": False,
                    "restrictedSolutionExists": None,
                    "restrictedReachableStateCount": len(seen),
                }
            seen.add(successor)
            if is_solved(goal, successor):
                solved = True
                break
            queue.append(successor)
    return {
        "unrestrictedSolutionExists": unrestricted,
        "unrestrictedShortestDistance": distance,
        "restrictedComplete": True,
        "restrictedSolutionExists": solved,
        "restrictedReachableStateCount": len(seen),
    }


def ct3_relational_one_side(
    n: int,
    length: int,
    initial,
    targets,
    *,
    context_cap: int = 100_000,
) -> dict:
    """Exact relation-based one-side continuation restriction.

    The first action is unrestricted. Thereafter the next source must equal the
    previous destination. No persistent head/tail identity is introduced.
    """
    context_cap = _positive_cap(context_cap, "context_cap")
    unrestricted, distance = _unrestricted_summary(n, length, initial, targets)
    board, chain, goal = BoardSpecV1(n), ChainSpecV1(length), GoalSpecV1(*targets)
    root = _state(initial)
    if is_solved(goal, root):
        return {
            "unrestrictedSolutionExists": unrestricted,
            "unrestrictedShortestDistance": distance,
            "restrictedComplete": True,
            "restrictedSolutionExists": True,
            "restrictedReachableContextCount": 0,
        }

    seen = set()
    queue = deque()
    for action in legal_actions(board, chain, root):
        successor = apply_action(board, chain, root, action).next_state
        context = (successor, action.destination_cell)
        if context not in seen:
            if len(seen) >= context_cap:
                return {
                    "unrestrictedSolutionExists": unrestricted,
                    "unrestrictedShortestDistance": distance,
                    "restrictedComplete": False,
                    "restrictedSolutionExists": None,
                    "restrictedReachableContextCount": len(seen),
                }
            seen.add(context)
            if is_solved(goal, successor):
                return {
                    "unrestrictedSolutionExists": unrestricted,
                    "unrestrictedShortestDistance": distance,
                    "restrictedComplete": True,
                    "restrictedSolutionExists": True,
                    "restrictedReachableContextCount": len(seen),
                }
            queue.append(context)

    while queue:
        state, active_endpoint = queue.popleft()
        for action in legal_actions(board, chain, state):
            if action.source_cell != active_endpoint:
                continue
            successor = apply_action(board, chain, state, action).next_state
            context = (successor, action.destination_cell)
            if context in seen:
                continue
            if len(seen) >= context_cap:
                return {
                    "unrestrictedSolutionExists": unrestricted,
                    "unrestrictedShortestDistance": distance,
                    "restrictedComplete": False,
                    "restrictedSolutionExists": None,
                    "restrictedReachableContextCount": len(seen),
                }
            seen.add(context)
            if is_solved(goal, successor):
                return {
                    "unrestrictedSolutionExists": unrestricted,
                    "unrestrictedShortestDistance": distance,
                    "restrictedComplete": True,
                    "restrictedSolutionExists": True,
                    "restrictedReachableContextCount": len(seen),
                }
            queue.append(context)

    return {
        "unrestrictedSolutionExists": unrestricted,
        "unrestrictedShortestDistance": distance,
        "restrictedComplete": True,
        "restrictedSolutionExists": False,
        "restrictedReachableContextCount": len(seen),
    }


def ct4_footprint_reachable(n: int, length: int, initial, footprint, horizon: int) -> bool:
    """Whether an exact occupied footprint is reachable within <= horizon moves."""
    if type(horizon) is not int or horizon < 0:
        raise ValueError("horizon must be a nonnegative integer")
    board, chain = BoardSpecV1(n), ChainSpecV1(length)
    root = _state(initial)
    target = frozenset(footprint)
    queue = deque(((root, 0),))
    best = {root: 0}
    while queue:
        state, depth = queue.popleft()
        if occupied(state) == target:
            return True
        if depth == horizon:
            continue
        for action in legal_actions(board, chain, state):
            successor = apply_action(board, chain, state, action).next_state
            next_depth = depth + 1
            if next_depth < best.get(successor, horizon + 1):
                best[successor] = next_depth
                queue.append((successor, next_depth))
    return False


def ct4_continuation_observation(n: int, length: int, initial, targets, action) -> dict:
    """Exact descriptor bundle for one immediate continuation; no value judgment."""
    transition = ct1_transition(n, length, initial, action)
    if not transition["accepted"]:
        return {"accepted": False, "nextState": transition["nextState"]}
    next_state = transition["nextState"]
    root_distance = exact_goal_distance(n, length, initial, targets)
    next_distance = exact_goal_distance(n, length, next_state, targets)
    return {
        "accepted": True,
        "nextState": next_state,
        "proximity": proximity(n, next_state, targets),
        "exactGoalDistance": next_distance,
        "onShortestDag": (
            root_distance is not None
            and next_distance is not None
            and next_distance + 1 == root_distance
        ),
    }


@dataclass(frozen=True)
class _ShortestDag:
    shortest_distance: int
    depths: dict
    edges: dict
    goals: frozenset


def _shortest_dag(n: int, length: int, initial, targets, state_cap: int) -> _ShortestDag | None:
    state_cap = _positive_cap(state_cap, "state_cap")
    board, chain, goal = BoardSpecV1(n), ChainSpecV1(length), GoalSpecV1(*targets)
    root = _state(initial)
    if is_solved(goal, root):
        return _ShortestDag(0, {root: 0}, {root: ()}, frozenset((root,)))

    depths = {root: 0}
    raw_edges = {}
    queue = deque((root,))
    shortest = None
    while queue:
        state = queue.popleft()
        depth = depths[state]
        if shortest is not None and depth >= shortest:
            continue
        row = []
        for action in legal_actions(board, chain, state):
            successor = apply_action(board, chain, state, action).next_state
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
                row.append(successor)
            if is_solved(goal, successor):
                shortest = next_depth if shortest is None else min(shortest, next_depth)
        raw_edges[state] = tuple(row)

    if shortest is None:
        return _ShortestDag(-1, depths, raw_edges, frozenset())

    goals = frozenset(
        state for state, depth in depths.items()
        if depth == shortest and is_solved(goal, state)
    )
    can_reach = set(goals)
    for depth in range(shortest - 1, -1, -1):
        for state, state_depth in tuple(depths.items()):
            if state_depth != depth:
                continue
            if any(successor in can_reach for successor in raw_edges.get(state, ())):
                can_reach.add(state)

    edges = {
        state: tuple(
            successor for successor in raw_edges.get(state, ())
            if successor in can_reach and depths[successor] == depths[state] + 1
        )
        for state in can_reach
    }
    return _ShortestDag(shortest, depths, edges, goals)


def _shortest_dag_metrics(dag: _ShortestDag, initial) -> dict:
    root = _state(initial)
    distance = dag.shortest_distance
    prefix = {state: 0 for state in dag.edges}
    if root in prefix:
        prefix[root] = 1
    ordered = sorted(dag.edges, key=lambda state: (dag.depths[state], state.path))
    indegree = {state: 0 for state in dag.edges}
    for state in ordered:
        for successor in dag.edges[state]:
            prefix[successor] = prefix.get(successor, 0) + prefix[state]
            indegree[successor] = indegree.get(successor, 0) + 1

    suffix = {}
    for state in reversed(ordered):
        if state in dag.goals:
            suffix[state] = 1
        else:
            suffix[state] = sum(suffix[successor] for successor in dag.edges[state])
    total = suffix.get(root, 1 if distance == 0 else 0)

    mandatory = [
        list(state.path)
        for state in ordered
        if 0 < dag.depths[state] < distance
        and prefix.get(state, 0) * suffix.get(state, 0) == total
    ]
    return {
        "shortestPathCount": total,
        "nearestSolvedStates": [list(state.path) for state in sorted(dag.goals, key=lambda item: item.path)],
        "branchStates": [
            list(state.path) for state in ordered
            if dag.depths[state] < distance and len(dag.edges[state]) > 1
        ],
        "convergenceStates": [
            list(state.path) for state in ordered
            if 0 < dag.depths[state] <= distance and indegree.get(state, 0) > 1
        ],
        "mandatoryInternalStates": mandatory,
    }


def ct6_solution_space_summary(
    n: int,
    length: int,
    initial,
    targets,
    *,
    state_cap: int = 100_000,
) -> dict:
    """Exact nearest-solution DAG structure for CT6; meta/advanced only."""
    dag = _shortest_dag(n, length, initial, targets, state_cap)
    if dag is None:
        return {"complete": False}
    if dag.shortest_distance < 0:
        return {
            "complete": True,
            "solvable": False,
            "shortestDistance": None,
            "shortestPathCount": 0,
            "nearestSolvedStates": [],
            "branchStates": [],
            "convergenceStates": [],
            "mandatoryInternalStates": [],
        }
    metrics = _shortest_dag_metrics(dag, initial)
    return {
        "complete": True,
        "solvable": True,
        "shortestDistance": dag.shortest_distance,
        **metrics,
    }


def ct5_shortest_dag_summary(
    n: int,
    length: int,
    initial,
    targets,
    *,
    state_cap: int = 100_000,
) -> dict:
    """CT5 shortest-setup projection; explicitly optimization-only evidence."""
    summary = ct6_solution_space_summary(
        n, length, initial, targets, state_cap=state_cap
    )
    if not summary.get("complete"):
        return {"complete": False}
    if not summary.get("solvable"):
        return {
            "complete": True,
            "solvable": False,
            "shortestDistance": None,
            "shortestPathCount": 0,
            "mandatoryInternalStates": [],
        }
    return {
        "complete": True,
        "solvable": True,
        "shortestDistance": summary["shortestDistance"],
        "shortestPathCount": summary["shortestPathCount"],
        "nearestSolvedStateCount": len(summary["nearestSolvedStates"]),
        "mandatoryInternalStates": summary["mandatoryInternalStates"],
    }
