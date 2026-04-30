goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]


class GameState:
    def __init__(self, board: list[int], empty_index: int, depth: int):
        # Board grid is represented as a one-dimensional list
        self.board: list[int] = board
        # Index of the empty tile (represented as 0)
        self.empty_index: int = empty_index
        # Depth of the current search
        self.depth: int = depth

    @property
    def is_goal_state(self) -> bool:
        return self.board == goal_state
