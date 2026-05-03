# Dimensions of the board (3x3)
from GameState import GameState

N = 3


# Converts the index in the list to a row and column values
def index_to_row_and_col(index: int) -> tuple[int, int]:
    return index // N, index % N


# Converts row and col to the index in the list
def row_and_col_to_index(row: int, col: int) -> int:
    return (row * N) + col


# Checks if the position is within the board dimensions
def is_valid_position(row: int, col: int) -> bool:
    return 0 <= row < N and 0 <= col < N


# Checks if the given board state is solvable
def is_solvable(board: list[int]) -> bool:
    tiles = [t for t in board if t != 0]
    inversions = sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )
    return inversions % 2 == 0


# Lists the moves made to reach the current state
def reconstruct_path(state: GameState) -> list[str]:
    path = []
    while state.move is not None:
        path.append(state.move.name)
        state = state.parent
    path.reverse()
    return path
