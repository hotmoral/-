"""M3 V1 reference FIFO BFS over the frozen M2 public state kernel.

Shortest distance and search diagnostics are reference facts, not player rules
or difficulty metrics. Execution failures propagate outside SolveResultV1.
"""

from collections import deque
from dataclasses import dataclass
from enum import Enum

from reference.m2_state_model import (
    ActionV1, ChainStateV1, PuzzleInstanceV1, apply_action, is_solved,
    legal_actions, validate_goal, validate_state,
)


class SolveStatusV1(Enum):
    SOLVED = "SOLVED"
    UNSOLVABLE = "UNSOLVABLE"
    INCOMPLETE = "INCOMPLETE"


@dataclass(frozen=True, slots=True)
class SearchBudgetV1:
    max_expanded_states: int | None = None

    def __post_init__(self) -> None:
        value = self.max_expanded_states
        if value is not None and (type(value) is not int or value < 0):
            raise ValueError("Expansion budget must be None or an exact nonnegative int")


@dataclass(frozen=True, slots=True)
class SolveResultV1:
    status: SolveStatusV1
    shortest_distance: int | None
    actions: tuple[ActionV1, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.status, SolveStatusV1):
            raise ValueError("Invalid solve status")
        actions = tuple(self.actions)
        if not all(isinstance(action, ActionV1) for action in actions):
            raise ValueError("Witness must contain M2 ActionV1 values")
        object.__setattr__(self, "actions", actions)
        if self.status is SolveStatusV1.SOLVED:
            if (type(self.shortest_distance) is not int or self.shortest_distance < 0
                    or len(actions) != self.shortest_distance):
                raise ValueError("SOLVED requires exact distance matching witness length")
        elif self.shortest_distance is not None or actions:
            raise ValueError("Non-SOLVED requires null distance and empty witness")


@dataclass(frozen=True, slots=True)
class SearchDiagnosticsV1:
    discovered_state_count: int
    expanded_state_count: int

    def __post_init__(self) -> None:
        if (type(self.discovered_state_count) is not int
                or type(self.expanded_state_count) is not int
                or not 0 <= self.expanded_state_count <= self.discovered_state_count
                or self.discovered_state_count < 1):
            raise ValueError("Invalid discovered/expanded counts")


@dataclass(frozen=True, slots=True)
class SolveRunV1:
    result: SolveResultV1
    diagnostics: SearchDiagnosticsV1

    def __post_init__(self) -> None:
        if not isinstance(self.result, SolveResultV1) or not isinstance(self.diagnostics, SearchDiagnosticsV1):
            raise ValueError("SolveRun requires validated result and diagnostics")
        counts = self.diagnostics
        if self.result.status is SolveStatusV1.UNSOLVABLE:
            if counts.discovered_state_count != counts.expanded_state_count:
                raise ValueError("UNSOLVABLE requires complete frontier exhaustion")
        elif counts.discovered_state_count <= counts.expanded_state_count:
            raise ValueError("SOLVED/INCOMPLETE require an unexpanded discovered state")


def _reconstruct(state: ChainStateV1, parents) -> tuple[ActionV1, ...]:
    actions = []
    while parents[state] is not None:
        state, action = parents[state]
        actions.append(action)
    return tuple(reversed(actions))


def solve_puzzle(instance: PuzzleInstanceV1,
                 budget: SearchBudgetV1 | None = None) -> SolveRunV1:
    if not isinstance(instance, PuzzleInstanceV1):
        raise TypeError("Expected a valid M2 PuzzleInstanceV1")
    if budget is not None and not isinstance(budget, SearchBudgetV1):
        raise TypeError("Expected SearchBudgetV1 or None")
    validate_state(instance.board, instance.chain, instance.initial_state)
    validate_goal(instance.board, instance.goal)
    limit = None if budget is None else budget.max_expanded_states
    initial = instance.initial_state
    if is_solved(instance.goal, initial):
        return SolveRunV1(SolveResultV1(SolveStatusV1.SOLVED, 0, ()),
                          SearchDiagnosticsV1(1, 0))

    parents = {initial: None}
    frontier = deque(((initial, 0),))
    expanded = 0
    while frontier:
        if limit is not None and expanded >= limit:
            return SolveRunV1(SolveResultV1(SolveStatusV1.INCOMPLETE, None, ()),
                              SearchDiagnosticsV1(len(parents), expanded))
        state, depth = frontier.popleft()
        expanded += 1
        for action in legal_actions(instance.board, instance.chain, state):
            transition = apply_action(instance.board, instance.chain, state, action)
            if not transition.accepted:
                raise RuntimeError("M2 apply_action rejected an M2 enumerated legal action")
            successor = transition.next_state
            if successor in parents:
                continue
            parents[successor] = (state, action)
            if is_solved(instance.goal, successor):
                return SolveRunV1(
                    SolveResultV1(SolveStatusV1.SOLVED, depth + 1,
                                  _reconstruct(successor, parents)),
                    SearchDiagnosticsV1(len(parents), expanded),
                )
            frontier.append((successor, depth + 1))
    return SolveRunV1(SolveResultV1(SolveStatusV1.UNSOLVABLE, None, ()),
                      SearchDiagnosticsV1(len(parents), expanded))
