from enum import Enum
from GameState import GameState


# Enum for possible moves, where each move is a tuple of (row, col)
class Move(Enum):
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)


# Dimensions of the board (3x3)
N = 3


# Prints the board in a 3x3 grid
def print_board(board: list[int]):
    for i in range(N):
        print(board[i * N], board[i * N + 1], board[i * N + 2])


def is_valid_move(row: int, col: int) -> bool:
    return 0 <= row < N and 0 <= col < N


# Converts the index in the list to a row and column values
def index_to_row_and_col(index: int) -> tuple[int, int]:
    return index // N, index % N


# Converts row and col to the index in the list
def row_and_col_to_index(row: int, col: int) -> int:
    return (row * N) + col


def solve_puzzle_dfs(board: list[int]):
    stack: list[GameState] = []
    visited: set[tuple] = set()

    visited.add(tuple(board))
    stack.append(GameState(board, board.index(0), 0))

    while stack:
        curr_state = stack.pop()
        empty_index = curr_state.empty_index

        if curr_state.is_goal_state:
            print("Goal state reached at depth", curr_state.depth)
            return

        print(f"Current depth at {curr_state.depth} and state:")
        print_board(curr_state.board)

        for move in Move:
            row, col = index_to_row_and_col(empty_index)

            # Calculate the new row and column from desired move
            new_row, new_col = row + move.value[0], col + move.value[1]

            if is_valid_move(new_row, new_col):
                new_empty_index = row_and_col_to_index(new_row, new_col)

                # Create a copy of the board
                new_board = list(curr_state.board)

                # Swap tiles
                new_board[empty_index], new_board[new_empty_index] = (
                    new_board[new_empty_index],
                    new_board[empty_index],
                )

                new_board_tuple = tuple(new_board)

                if new_board_tuple not in visited:
                    visited.add(new_board_tuple)
                    stack.append(
                        GameState(new_board, new_empty_index, curr_state.depth + 1)
                    )

    print("No solution found")


# Ignore formatting code below for easier reading
# fmt: off
solve_puzzle_dfs([
    1, 2, 3,
    4, 0, 5,
    6, 7, 8
])

# fmt: on
