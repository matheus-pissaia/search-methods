from GameState import goal_state
from utils import index_to_row_and_col


# Uniform cost heuristic - always returns 0
def h_zero(_board: list[int]) -> int:
    return 0


# Non-admissible heuristic - returns the number of misplaced tiles multiplied
# by 3, leading to an overestimation in some cases.
def h_misplaced_x3(board: list[int]) -> int:
    return (
        sum(1 for i, tile in enumerate(board) if tile != 0 and tile != goal_state[i])
        * 3
    )


# Admissible heuristic - returns the number of misplaced tiles
def h_misplaced(board: list[int]) -> int:
    return sum(1 for i, tile in enumerate(board) if tile != 0 and tile != goal_state[i])


# Precomputed goal positions for Manhattan distance
_GOAL_POSITIONS = {tile: index_to_row_and_col(i) for i, tile in enumerate(goal_state)}


# Admissible heuristic - returns the sum of the Manhattan distances between
# each tile and its goal position
def h_manhattan(board: list[int]) -> int:
    distance = 0
    for i, tile in enumerate(board):
        if tile == 0:
            continue
        curr_row, curr_col = index_to_row_and_col(i)
        goal_row, goal_col = _GOAL_POSITIONS[tile]
        distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance


HEURISTICS = [
    ("Uniform Cost", h_zero),
    ("A* Non-admissible", h_misplaced_x3),
    ("A* Misplaced Tiles", h_misplaced),
    ("A* Manhattan", h_manhattan),
]
