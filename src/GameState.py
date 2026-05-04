from enum import Enum


class Move(Enum):
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)


goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]


class GameState:
    def __init__(self, board, empty_index, depth, parent=None, move=None):
        # Board grid represented as a 1D array
        self.board: list[int] = board
        # Index of the empty tile
        self.empty_index: int = empty_index
        # Search depth of the current state
        self.depth: int = depth
        # Game state parent node
        self.parent: "GameState | None" = parent
        # Move made to reach the current state
        self.move: "Move | None" = move

    @property
    def is_goal_state(self) -> bool:
        return self.board == goal_state
