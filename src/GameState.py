from enum import Enum


class Move(Enum):
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)


goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]


class GameState:
    def __init__(self, board, empty_index, depth, parent=None, move=None):
        self.board: list[int] = board
        self.empty_index: int = empty_index
        self.depth: int = depth
        self.parent: "GameState | None" = parent
        self.move: "Move | None" = move

    @property
    def is_goal_state(self) -> bool:
        return self.board == goal_state
