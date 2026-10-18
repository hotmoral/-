"""M2 V1: a single unoriented chain, strict-empty movement, and exact identities.

Only the canonical path is stored in ChainStateV1. Constructors check local
field constraints; validate_state / validate_goal check board-dependent validity.
Movement and mechanical identity have no goal or history argument.
"""

from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable


def _integer(value: int) -> None:
    if type(value) is not int:
        raise ValueError("Expected an integer")


@dataclass(frozen=True, slots=True)
class BoardSpecV1:
    N: int

    def __post_init__(self) -> None:
        validate_board(self)

    def in_bounds(self, cell: int) -> bool:
        return type(cell) is int and 0 <= cell < self.N * self.N

    def cell_id(self, row: int, col: int) -> int:
        _integer(row)
        _integer(col)
        if not (0 <= row < self.N and 0 <= col < self.N):
            raise ValueError("Coordinate outside board")
        return row * self.N + col

    def coordinates(self, cell: int) -> tuple[int, int]:
        if not self.in_bounds(cell):
            raise ValueError("Cell outside board")
        return divmod(cell, self.N)

    def adjacent(self, first: int, second: int) -> bool:
        if not self.in_bounds(first) or not self.in_bounds(second):
            return False
        r1, c1 = self.coordinates(first)
        r2, c2 = self.coordinates(second)
        return abs(r1 - r2) + abs(c1 - c2) == 1

    def neighbors(self, cell: int) -> tuple[int, ...]:
        row, col = self.coordinates(cell)
        return tuple(sorted(
            self.cell_id(r, c)
            for r, c in ((row - 1, col), (row + 1, col),
                         (row, col - 1), (row, col + 1))
            if 0 <= r < self.N and 0 <= c < self.N
        ))


@dataclass(frozen=True, slots=True)
class ChainSpecV1:
    L: int

    def __post_init__(self) -> None:
        _integer(self.L)
        if self.L < 2:
            raise ValueError("L must be at least 2")


@dataclass(frozen=True, slots=True)
class GoalSpecV1:
    t0: int
    t1: int

    def __post_init__(self) -> None:
        _integer(self.t0)
        _integer(self.t1)
        if self.t0 < 0 or self.t1 < 0 or self.t0 == self.t1:
            raise ValueError("Targets must be distinct nonnegative cell IDs")
        first, second = sorted((self.t0, self.t1))
        object.__setattr__(self, "t0", first)
        object.__setattr__(self, "t1", second)


def canonicalize_path(path: Iterable[int]) -> tuple[int, ...]:
    values = tuple(path)
    for value in values:
        _integer(value)
    return min(values, values[::-1])


@dataclass(frozen=True, slots=True)
class ChainStateV1:
    path: tuple[int, ...]

    def __post_init__(self) -> None:
        path = canonicalize_path(self.path)
        if len(path) < 2:
            raise ValueError("A chain state requires at least two cells")
        object.__setattr__(self, "path", path)


@dataclass(frozen=True, slots=True)
class ActionV1:
    source_cell: int
    destination_cell: int

    def __post_init__(self) -> None:
        _integer(self.source_cell)
        _integer(self.destination_cell)


@dataclass(frozen=True, slots=True)
class ApplyResultV1:
    accepted: bool
    next_state: ChainStateV1


@dataclass(frozen=True, slots=True)
class PuzzleInstanceV1:
    board: BoardSpecV1
    chain: ChainSpecV1
    goal: GoalSpecV1
    initial_state: ChainStateV1

    def __post_init__(self) -> None:
        validate_state(self.board, self.chain, self.initial_state)
        validate_goal(self.board, self.goal)


def validate_board(board: BoardSpecV1) -> None:
    _integer(board.N)
    if board.N < 2:
        raise ValueError("N must be at least 2")


def validate_chain_spec(board: BoardSpecV1, chain: ChainSpecV1) -> None:
    validate_board(board)
    _integer(chain.L)
    if not 2 <= chain.L <= board.N * board.N:
        raise ValueError("L must be between 2 and N squared")


def validate_goal(board: BoardSpecV1, goal: GoalSpecV1) -> None:
    validate_board(board)
    if not (board.in_bounds(goal.t0) and board.in_bounds(goal.t1)):
        raise ValueError("Target outside board")
    if goal.t0 == goal.t1:
        raise ValueError("Target cells must differ")


def validate_state(board: BoardSpecV1, chain: ChainSpecV1,
                   state: ChainStateV1) -> None:
    validate_chain_spec(board, chain)
    path = state.path
    if len(path) != chain.L:
        raise ValueError("Path length differs from L")
    if not all(board.in_bounds(cell) for cell in path):
        raise ValueError("Path cell outside board")
    if len(set(path)) != chain.L:
        raise ValueError("Path cells must be distinct")
    if not all(board.adjacent(a, b) for a, b in zip(path, path[1:])):
        raise ValueError("Consecutive path cells must be adjacent")


def occupied(state: ChainStateV1) -> frozenset[int]:
    return frozenset(state.path)


def endpoints(state: ChainStateV1) -> frozenset[int]:
    return frozenset((state.path[0], state.path[-1]))


def _legal(board: BoardSpecV1, state: ChainStateV1, action: ActionV1) -> bool:
    return (action.source_cell in endpoints(state)
            and board.in_bounds(action.destination_cell)
            and board.adjacent(action.source_cell, action.destination_cell)
            and action.destination_cell not in occupied(state))


def is_legal_action(board: BoardSpecV1, chain: ChainSpecV1,
                    state: ChainStateV1, action: ActionV1) -> bool:
    validate_state(board, chain, state)
    return _legal(board, state, action)


def legal_actions(board: BoardSpecV1, chain: ChainSpecV1,
                  state: ChainStateV1) -> tuple[ActionV1, ...]:
    validate_state(board, chain, state)
    cells = occupied(state)
    return tuple(sorted(
        (ActionV1(source, destination)
         for source in endpoints(state)
         for destination in board.neighbors(source)
         if destination not in cells),
        key=lambda action: (action.source_cell, action.destination_cell),
    ))


def apply_action(board: BoardSpecV1, chain: ChainSpecV1,
                 state: ChainStateV1, action: ActionV1) -> ApplyResultV1:
    validate_state(board, chain, state)
    if not _legal(board, state, action):
        return ApplyResultV1(False, state)
    path = state.path
    temporary = path if action.source_cell == path[0] else path[::-1]
    return ApplyResultV1(
        True, ChainStateV1((action.destination_cell,) + temporary[:-1]),
    )


def is_solved(goal: GoalSpecV1, state: ChainStateV1) -> bool:
    return endpoints(state) == frozenset((goal.t0, goal.t1))


def _array(values: Iterable[int]) -> str:
    return "[" + ",".join(str(value) for value in values) + "]"


def serialize_mechanical_configuration(board: BoardSpecV1, chain: ChainSpecV1,
                                       state: ChainStateV1) -> bytes:
    validate_state(board, chain, state)
    return (f'["LL_MECH",1,{board.N},{chain.L},{_array(state.path)}]'
            .encode("utf-8"))


def hash_mechanical_configuration(board: BoardSpecV1, chain: ChainSpecV1,
                                  state: ChainStateV1) -> str:
    return sha256(serialize_mechanical_configuration(board, chain, state)).hexdigest()


def serialize_puzzle_instance(instance: PuzzleInstanceV1) -> bytes:
    validate_state(instance.board, instance.chain, instance.initial_state)
    validate_goal(instance.board, instance.goal)
    targets = _array((instance.goal.t0, instance.goal.t1))
    path = _array(instance.initial_state.path)
    return (f'["LL_INSTANCE",1,{instance.board.N},{instance.chain.L},'
            f'{targets},{path}]').encode("utf-8")


def hash_puzzle_instance(instance: PuzzleInstanceV1) -> str:
    return sha256(serialize_puzzle_instance(instance)).hexdigest()


def serialize_action(action: ActionV1) -> bytes:
    return (f'["LL_ACTION",1,{action.source_cell},{action.destination_cell}]'
            .encode("utf-8"))
