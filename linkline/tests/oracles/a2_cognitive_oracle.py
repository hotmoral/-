"""A2-A independent cognitive Golden oracle.

This test-only module consumes frozen M2/M3 public semantics and never imports
the future A2 production analyzer.  It recomputes the exact outputs attached
to a compact set of hand-selected representation/strategy microcases.
"""

from collections import deque
from hashlib import sha256
import json

from reference.m2_state_model import (
    ActionV1,
    BoardSpecV1,
    ChainSpecV1,
    ChainStateV1,
    GoalSpecV1,
    PuzzleInstanceV1,
    apply_action,
    endpoints,
    legal_actions,
    occupied,
)
from reference.m3_solver import SolveStatusV1, solve_puzzle


def _action(values):
    return ActionV1(values[0], values[1])


def _state(values):
    return ChainStateV1(tuple(values))


def _instance(n, length, initial, targets):
    return PuzzleInstanceV1(
        BoardSpecV1(n),
        ChainSpecV1(length),
        GoalSpecV1(*targets),
        _state(initial),
    )


def _apply(n, length, state, action):
    board, chain = BoardSpecV1(n), ChainSpecV1(length)
    result = apply_action(board, chain, _state(state), _action(action))
    return {
        "accepted": result.accepted,
        "nextState": list(result.next_state.path),
    }


def _distance(n, length, state, targets):
    run = solve_puzzle(_instance(n, length, state, targets))
    if run.result.status is not SolveStatusV1.SOLVED:
        return None
    return run.result.shortest_distance


def _manhattan(n, first, second):
    r0, c0 = divmod(first, n)
    r1, c1 = divmod(second, n)
    return abs(r0 - r1) + abs(c0 - c1)


def proximity(n, state, targets):
    state = _state(state)
    first, second = state.path[0], state.path[-1]
    t0, t1 = targets
    return min(
        _manhattan(n, first, t0) + _manhattan(n, second, t1),
        _manhattan(n, first, t1) + _manhattan(n, second, t0),
    )


def _replay(n, length, initial, actions):
    board, chain = BoardSpecV1(n), ChainSpecV1(length)
    state = _state(initial)
    for values in actions:
        result = apply_action(board, chain, state, _action(values))
        if not result.accepted:
            raise AssertionError("Literal witness contains an illegal action")
        state = result.next_state
    return state


def _is_solved(state, targets):
    return endpoints(state) == frozenset(targets)


def _proximity_restricted_closure(n, length, initial, targets):
    board, chain = BoardSpecV1(n), ChainSpecV1(length)
    initial_state = _state(initial)
    queue = deque((initial_state,))
    seen = {initial_state}
    while queue:
        state = queue.popleft()
        current = proximity(n, state.path, targets)
        for action in legal_actions(board, chain, state):
            result = apply_action(board, chain, state, action)
            successor = result.next_state
            if proximity(n, successor.path, targets) <= current and successor not in seen:
                seen.add(successor)
                queue.append(successor)
    return seen


def _one_side_context_closure(n, length, initial):
    board, chain = BoardSpecV1(n), ChainSpecV1(length)
    root = _state(initial)
    queue = deque()
    seen = set()
    for action in legal_actions(board, chain, root):
        successor = apply_action(board, chain, root, action).next_state
        context = (successor, action.destination_cell)
        if context not in seen:
            seen.add(context)
            queue.append(context)
    while queue:
        state, active_endpoint = queue.popleft()
        for action in legal_actions(board, chain, state):
            if action.source_cell != active_endpoint:
                continue
            successor = apply_action(board, chain, state, action).next_state
            context = (successor, action.destination_cell)
            if context not in seen:
                seen.add(context)
                queue.append(context)
    return seen


def _footprint_reachable(n, length, initial, footprint, horizon):
    board, chain = BoardSpecV1(n), ChainSpecV1(length)
    root = _state(initial)
    queue = deque(((root, 0),))
    best = {root: 0}
    target = frozenset(footprint)
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


def _literal_cases():
    return [
        {
            "id": "A2G01", "hypothesis": "H1", "evidenceLayer": "L1",
            "task": "CT1", "representation": "R1",
            "status": "EXACT_INFORMATION_INSUFFICIENT", "scope": "EXACT_WITNESS",
            "domain": {"N": 2, "L": 3}, "targets": None,
            "states": [[0, 1, 3], [0, 2, 3]],
            "reducedRepresentation": {"endpoints": [0, 3]},
            "action": [0, 2],
            "provenance": "A1 C1 exact witness revalidated for CT1",
        },
        {
            "id": "A2G02", "hypothesis": "H2", "evidenceLayer": "L1",
            "task": "CT1", "representation": "R2",
            "status": "EXACT_INFORMATION_INSUFFICIENT", "scope": "EXACT_WITNESS",
            "domain": {"N": 4, "L": 9}, "targets": None,
            "states": [
                [0, 1, 2, 6, 5, 4, 8, 9, 10],
                [0, 4, 8, 9, 5, 1, 2, 6, 10],
            ],
            "reducedRepresentation": {
                "endpoints": [0, 10],
                "occupied": [0, 1, 2, 4, 5, 6, 8, 9, 10],
            },
            "action": [10, 11],
            "provenance": "A2 targeted N=4 exact collision",
        },
        {
            "id": "A2G03", "hypothesis": "H3-L", "evidenceLayer": "L1",
            "task": "CT4", "representation": "R4",
            "status": "EXACT_INFORMATION_INSUFFICIENT", "scope": "EXACT_WITNESS",
            "domain": {"N": 3, "L": 3}, "initial": [0, 1, 2],
            "targets": [0, 4],
            "provenance": "A1 C4 / C8-D small-domain exact structure revalidated for CT4",
        },
        {
            "id": "A2G04", "hypothesis": "H3-S", "evidenceLayer": "L2",
            "task": "CT3", "representation": "R4",
            "status": "STRATEGY_RESTRICTION_FAILS", "scope": "EXACT_WITNESS",
            "domain": {"N": 3, "L": 4}, "initial": [0, 1, 2, 5],
            "targets": [0, 1],
            "restriction": {
                "name": "NONINCREASING_ENDPOINT_TARGET_MANHATTAN",
                "rule": "allow successor only when H(next) <= H(current)",
            },
            "unrestrictedWitness": [[5, 8], [1, 4], [4, 3], [3, 0]],
            "provenance": "A1 C4 forced-proximity-sacrifice instance revalidated as CT3 strategy counterexample",
        },
        {
            "id": "A2G05", "hypothesis": "H4", "evidenceLayer": "L2",
            "task": "CT3", "representation": "R5",
            "status": "STRATEGY_RESTRICTION_FAILS", "scope": "EXACT_WITNESS",
            "domain": {"N": 4, "L": 10},
            "initial": [0, 4, 5, 6, 7, 11, 15, 14, 13, 9],
            "targets": [0, 14],
            "restriction": {
                "name": "RELATIONAL_ONE_SIDE_CONTINUATION",
                "rule": "first action unrestricted; thereafter source_cell must equal previous destination_cell",
            },
            "unrestrictedWitness": [
                [0, 1], [13, 12], [12, 8], [8, 9], [9, 10],
                [6, 2], [2, 1], [1, 5], [5, 4], [4, 0],
            ],
            "provenance": "A1 C5 strong exact witness revalidated for CT3 using relational endpoint semantics",
        },
        {
            "id": "A2G06", "hypothesis": "H5", "evidenceLayer": "L1",
            "task": "CT2", "representation": "R3",
            "status": "NOT_REQUIRED_BY_CORE", "scope": "GLOBAL_THEOREM",
            "domain": {"N": 3, "L": 3}, "state": [0, 1, 2],
            "histories": [[], [[0, 3], [1, 2]]],
            "convergedState": [0, 1, 2],
            "provenance": "Frozen M2 current-state sufficiency / A1 theorem T6",
        },
        {
            "id": "A2G07", "hypothesis": "H6", "evidenceLayer": "L2",
            "task": "CT4", "representation": "R3",
            "status": "NOT_REQUIRED_BY_CORE", "scope": "GLOBAL_THEOREM",
            "domain": {"N": 3, "L": 2}, "initial": [0, 1],
            "targets": [0, 3], "detourAction": [1, 2],
            "forcedRecoveryAction": [1, 0],
            "provenance": "Frozen exact reversibility/component invariance with A1 C7-B recovery witness",
        },
        {
            "id": "A2G08", "hypothesis": "H7", "evidenceLayer": "L2",
            "task": "CT4", "representation": "R3",
            "status": "STRUCTURALLY_RELEVANT", "scope": "EXACT_WITNESS",
            "domain": {"N": 3, "L": 2}, "initial": [0, 1],
            "successors": [[0, 3], [1, 2]], "horizon": 2,
            "footprint": [2, 5],
            "exclusions": "initial and immediate-successor occupied footprints excluded",
            "provenance": "A1 C3 bounded-footprint exact witness revalidated for CT4",
        },
        {
            "id": "A2G09", "hypothesis": "H8", "evidenceLayer": "L2",
            "task": "CT5", "representation": "R4+STRUCTURAL_SETUP",
            "status": "STRUCTURALLY_RELEVANT", "scope": "OPTIMIZATION_ONLY",
            "domain": {"N": 3, "L": 3}, "initial": [0, 1, 2],
            "targets": [0, 4],
            "provenance": "A1 C8-D exact shortest-structure witness; validity claim explicitly excluded",
        },
    ]


def golden_payload():
    cases = _literal_cases()

    g1 = cases[0]
    g1["exactResults"] = [
        _apply(2, 3, state, g1["action"]) for state in g1["states"]
    ]

    g2 = cases[1]
    first, second = map(_state, g2["states"])
    if endpoints(first) != endpoints(second) or occupied(first) != occupied(second):
        raise AssertionError("R2 witness does not preserve endpoints/occupancy")
    g2["exactResults"] = [
        _apply(4, 9, state, g2["action"]) for state in g2["states"]
    ]

    g3 = cases[2]
    alternatives = [([0, 3], [1, 0, 3]), ([2, 5], [1, 2, 5])]
    g3["alternatives"] = [
        {
            "action": action,
            "state": state,
            "proximity": proximity(3, state, g3["targets"]),
            "exactGoalDistance": _distance(3, 3, state, g3["targets"]),
        }
        for action, state in alternatives
    ]

    g4 = cases[3]
    unrestricted = solve_puzzle(_instance(3, 4, g4["initial"], g4["targets"]))
    if unrestricted.result.status is not SolveStatusV1.SOLVED:
        raise AssertionError("H3-S unrestricted instance must be solvable")
    final_state = _replay(3, 4, g4["initial"], g4["unrestrictedWitness"])
    if not _is_solved(final_state, g4["targets"]):
        raise AssertionError("H3-S literal witness does not solve the goal")
    sequence = [g4["initial"]]
    current = _state(g4["initial"])
    board, chain = BoardSpecV1(3), ChainSpecV1(4)
    for action_values in g4["unrestrictedWitness"]:
        current = apply_action(board, chain, current, _action(action_values)).next_state
        sequence.append(list(current.path))
    closure = _proximity_restricted_closure(3, 4, g4["initial"], g4["targets"])
    g4["unrestrictedShortestDistance"] = unrestricted.result.shortest_distance
    g4["witnessProximitySequence"] = [
        proximity(3, state, g4["targets"]) for state in sequence
    ]
    g4["restrictedReachableStateCount"] = len(closure)
    g4["restrictedSolutionExists"] = any(
        _is_solved(state, g4["targets"]) for state in closure
    )

    g5 = cases[4]
    unrestricted = solve_puzzle(_instance(4, 10, g5["initial"], g5["targets"]))
    final_state = _replay(4, 10, g5["initial"], g5["unrestrictedWitness"])
    contexts = _one_side_context_closure(4, 10, g5["initial"])
    actions = g5["unrestrictedWitness"]
    g5["unrestrictedShortestDistance"] = unrestricted.result.shortest_distance
    g5["switchFlagsAfterFirst"] = [
        actions[index][0] != actions[index - 1][1]
        for index in range(1, len(actions))
    ]
    g5["restrictedReachableContextCount"] = len(contexts)
    g5["restrictedSolutionExists"] = any(
        _is_solved(state, g5["targets"]) for state, _ in contexts
    )
    if not _is_solved(final_state, g5["targets"]):
        raise AssertionError("H4 literal witness does not solve the goal")

    g6 = cases[5]
    replayed = _replay(3, 3, g6["state"], g6["histories"][1])
    if list(replayed.path) != g6["convergedState"]:
        raise AssertionError("History-equivalence witness does not converge")
    board, chain = BoardSpecV1(3), ChainSpecV1(3)
    root = _state(g6["state"])
    actions = legal_actions(board, chain, root)
    g6["futureLegalActions"] = [
        [action.source_cell, action.destination_cell] for action in actions
    ]
    g6["futureNextStates"] = [
        {
            "action": [action.source_cell, action.destination_cell],
            "nextState": list(apply_action(board, chain, root, action).next_state.path),
        }
        for action in actions
    ]

    g7 = cases[6]
    g7["initialExactGoalDistance"] = _distance(3, 2, g7["initial"], g7["targets"])
    detour = _replay(3, 2, g7["initial"], [g7["detourAction"]])
    g7["detourState"] = list(detour.path)
    g7["detourExactGoalDistance"] = _distance(3, 2, detour.path, g7["targets"])
    recovered = _replay(3, 2, detour.path, [g7["forcedRecoveryAction"]])
    g7["recoveredState"] = list(recovered.path)

    g8 = cases[7]
    g8["reachable"] = [
        _footprint_reachable(3, 2, successor, g8["footprint"], g8["horizon"])
        for successor in g8["successors"]
    ]

    g9 = cases[8]
    g9["shortestDistance"] = _distance(3, 3, g9["initial"], g9["targets"])
    alternatives = [([0, 3], [1, 0, 3]), ([2, 5], [1, 2, 5])]
    g9["alternatives"] = [
        {
            "action": action,
            "state": state,
            "proximity": proximity(3, state, g9["targets"]),
            "exactGoalDistance": _distance(3, 3, state, g9["targets"]),
            "onShortestDag": _distance(3, 3, state, g9["targets"]) == g9["shortestDistance"] - 1,
        }
        for action, state in alternatives
    ]
    g9["mandatoryInternalState"] = [1, 0, 3]
    setup = _state(g9["mandatoryInternalState"])
    board, chain = BoardSpecV1(3), ChainSpecV1(3)
    g9["shortestPathCount"] = sum(
        1 for action in legal_actions(board, chain, setup)
        if _is_solved(apply_action(board, chain, setup, action).next_state, g9["targets"])
    )

    return {"schemaVersion": 1, "cases": cases}


def fingerprint(payload):
    return sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
