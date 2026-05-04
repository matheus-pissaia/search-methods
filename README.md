# A* Search — 8-Puzzle Solver

Solves the 8-puzzle using four search algorithm variants and compares their performance.

## Algorithms

| Algorithm | Heuristic | Admissible |
|---|---|---|
| Uniform Cost | h = 0 | — |
| A* Non-admissible | No. misplaced tiles x 3 | No |
| A* Misplaced Tiles | No. misplaced tiles | Yes |
| A* Manhattan | Sum of Manhattan distances | Yes |

## Goal State

```
1 2 3
4 5 6
7 8 _
```

## Project Structure

```
src/
  main.py        # Entry point and A* solver loop
  GameState.py   # Board state representation and moves
  heuristics.py  # All heuristic functions
  utils.py       # Board helpers (solvability, path reconstruction)
output/          # JSON results for each board/algorithm pair
```

## Running

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd src
python main.py
```

The solver runs all four algorithms against five pre-defined boards (Easy, Medium 1, Medium 2, Hard 1, Hard 2) and prints a comparison table:

```
Easy — [1, 2, 3, 0, 4, 6, 7, 5, 8]
+--------------------+---------------+---------------+---------+--------------+
| Algorithm          |   Visited Nodes |   Path Length | Time    |   Max Frontier |
+====================+=================+===============+=========+================+
| Uniform Cost       |              10 |             3 | 0.0001s |              8 |
| A* Non-admissible  |               5 |             3 | 0.0001s |              5 |
| A* Misplaced Tiles |               7 |             3 | 0.0001s |              6 |
| A* Manhattan       |               5 |             3 | 0.0001s |              4 |
+--------------------+-----------------+---------------+---------+----------------+
```

Each run also writes a JSON file to `output/` containing the solution path, visited nodes, and frontier state.

## Output Format

```json
{
  "algorithm": "A* Manhattan",
  "difficulty": "Easy",
  "metrics": {
    "visited_count": 5,
    "path_length": 3,
    "time": "0.0001s",
    "max_frontier_size": 4
  },
  "path": ["LEFT", "DOWN", "RIGHT"],
  "frontier": [[...]],
  "visited": [[...]]
}
```
