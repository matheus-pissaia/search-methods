import heapq
import json
import time
from pathlib import Path

from tabulate import tabulate

from GameState import GameState, Move, goal_state

# Dimensions of the board (3x3)
N = 3


# Converts the index in the list to a row and column values
def index_to_row_and_col(index: int) -> tuple[int, int]:
    return index // N, index % N


# Converts row and col to the index in the list
def row_and_col_to_index(row: int, col: int) -> int:
    return (row * N) + col


def is_valid_move(row: int, col: int) -> bool:
    return 0 <= row < N and 0 <= col < N


def is_solvable(board: list[int]) -> bool:
    tiles = [t for t in board if t != 0]
    inversions = sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )
    return inversions % 2 == 0


def reconstruct_path(state: GameState) -> list[str]:
    path = []
    while state.move is not None:
        path.append(state.move.name)
        state = state.parent
    path.reverse()
    return path


# Precomputed goal positions for Manhattan distance
_GOAL_POSITIONS = {tile: index_to_row_and_col(i) for i, tile in enumerate(goal_state)}


def h_zero(_board: list[int]) -> int:
    return 0


def h_misplaced_x3(board: list[int]) -> int:
    return (
        sum(1 for i, tile in enumerate(board) if tile != 0 and tile != goal_state[i])
        * 3
    )


def h_misplaced(board: list[int]) -> int:
    return sum(1 for i, tile in enumerate(board) if tile != 0 and tile != goal_state[i])


def h_manhattan(board: list[int]) -> int:
    distance = 0
    for i, tile in enumerate(board):
        if tile == 0:
            continue
        curr_row, curr_col = index_to_row_and_col(i)
        goal_row, goal_col = _GOAL_POSITIONS[tile]
        distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance


def solve(board: list[int], heuristic) -> dict | None:
    frontier: list[tuple] = []
    visited: set[tuple] = set()
    node_count = 0
    max_frontier_size = 0

    start = GameState(board, board.index(0), 0)
    heapq.heappush(frontier, (heuristic(board), node_count, start))
    node_count += 1

    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        _, _, curr_state = heapq.heappop(frontier)

        board_tuple = tuple(curr_state.board)
        if board_tuple in visited:
            continue
        visited.add(board_tuple)

        if curr_state.is_goal_state:
            path = reconstruct_path(curr_state)
            return {
                "path": path,
                "visited_count": len(visited),
                "path_length": len(path),
                "max_frontier_size": max_frontier_size,
                "frontier": [list(item[2].board) for item in frontier],
                "visited": [list(b) for b in visited],
            }

        empty_index = curr_state.empty_index
        row, col = index_to_row_and_col(empty_index)

        for move in Move:
            new_row = row + move.value[0]
            new_col = col + move.value[1]
            if not is_valid_move(new_row, new_col):
                continue

            new_empty_index = row_and_col_to_index(new_row, new_col)
            new_board = list(curr_state.board)
            new_board[empty_index], new_board[new_empty_index] = (
                new_board[new_empty_index],
                new_board[empty_index],
            )

            if tuple(new_board) not in visited:
                new_state = GameState(
                    new_board,
                    new_empty_index,
                    curr_state.depth + 1,
                    parent=curr_state,
                    move=move,
                )
                f = new_state.depth + heuristic(new_board)
                heapq.heappush(frontier, (f, node_count, new_state))
                node_count += 1

    return None


ALGORITHMS = [
    ("Uniform Cost", h_zero),
    ("A* Non-admissible", h_misplaced_x3),
    ("A* Misplaced Tiles", h_misplaced),
    ("A* Manhattan", h_manhattan),
]

# fmt: off
BOARDS = {
    "Easy":     [1, 2, 3, 0, 4, 6, 7, 5, 8],
    "Medium 1": [1, 2, 3, 4, 0, 5, 6, 7, 8],
    "Medium 2": [1, 3, 6, 5, 0, 2, 4, 7, 8],
    "Hard 1":   [8, 6, 7, 2, 5, 4, 3, 0, 1],
    "Hard 2":   [6, 4, 7, 8, 5, 0, 3, 2, 1],
}
# fmt: on


def run_all(board: list[int], difficulty: str) -> list[dict]:
    results = []
    for name, heuristic in ALGORITHMS:
        start_time = time.time()
        result = solve(board, heuristic)
        elapsed = time.time() - start_time

        file_key = f"{difficulty.lower()}_{name.lower().replace(' ', '_').replace('*', 'star')}"

        if result is None:
            row = {
                "algorithm": name,
                "visited_count": "N/A",
                "path_length": "N/A",
                "time": f"{elapsed:.4f}s",
                "max_frontier_size": "N/A",
                "path": None,
            }
        else:
            row = {
                "algorithm": name,
                "visited_count": result["visited_count"],
                "path_length": result["path_length"],
                "time": f"{elapsed:.4f}s",
                "max_frontier_size": result["max_frontier_size"],
                "path": result["path"],
            }
            output_dir = Path(__file__).parent.parent / "output"
            output_dir.mkdir(parents=True, exist_ok=True)
            with open(output_dir / f"{file_key}.json", "w") as f:
                json.dump(
                    {
                        "algorithm": name,
                        "difficulty": difficulty,
                        "metrics": {
                            "visited_count": result["visited_count"],
                            "path_length": result["path_length"],
                            "time": f"{elapsed:.4f}s",
                            "max_frontier_size": result["max_frontier_size"],
                        },
                        "path": result["path"],
                        "frontier": result["frontier"],
                        "visited": result["visited"],
                    },
                    f,
                )

        results.append(row)

    return results


def print_table(difficulty: str, board: list[int], results: list[dict]):
    keys = ["algorithm", "visited_count", "path_length", "time", "max_frontier_size"]
    headers = ["Algorithm", "Visited Nodes", "Path Length", "Time", "Max Frontier"]
    rows = [[r[k] for k in keys] for r in results]

    print(f"{difficulty} — {board}")
    print(tabulate(rows, headers=headers, tablefmt="outline"))


def main():
    for difficulty, board in BOARDS.items():
        if not is_solvable(board):
            print(f"{difficulty} — {board}")
            print("  Skipped: board is not solvable.\n")
            continue
        results = run_all(board, difficulty)
        print_table(difficulty, board, results)
        print()


if __name__ == "__main__":
    main()
