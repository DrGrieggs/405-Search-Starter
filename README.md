# Search Algorithms in Python: Starter Repository

Starter code and tests for the search algorithms worksheet (Chapter 3, Sections 3.3–3.4). You will implement breadth-first, depth-first, and best-first search, then choose the right one for three problems.

## Setup

You need Python 3.8 or newer.

```
python -m pip install -r requirements.txt
```

## What's here

| File | What you do with it |
| --- | --- |
| `search.py` | The problem and node framework, plus the Romania map. **Parts 1–3:** fill in `breadth_first_search`, `depth_first_search`, and `best_first_search` at the bottom. |
| `problems.py` | **Part 4:** finish the knight and queens formulations, and fill in `solve_ambulance`, `solve_knight`, and `solve_queens` with the search you choose. |
| `ANSWERS.md` | Your written answers: the worksheet questions and your algorithm justifications. |
| `tests/` | The test suite. Don't edit it. |

## Running the tests

Run every test:

```
python -m pytest -v
```

Run one part at a time:

```
python -m pytest tests/test_search.py -v              # Parts 1-3
python -m pytest tests/test_problems.py -v            # Part 4
python -m pytest tests/test_search.py -k bfs -v       # tests whose names contain "bfs"
python -m pytest tests/test_search.py -k depth -v     # depth-first tests
```

All tests fail until you write code; that's expected. Work through them part by part.

To see your algorithms run on the Romania map:

```
python search.py
python problems.py
```

## What the tests check

**`tests/test_search.py` (Parts 1–3)**

- Every search returns a legal path from start to goal with the correct `path_cost`, handles a start that is already the goal, and returns `None` when the goal can't be reached.
- Breadth-first search finds the fewest actions (3 from Arad to Bucharest), even when that isn't the cheapest route.
- Depth-first search terminates on a map with cycles and never returns a path that repeats a state.
- Best-first search with path cost finds the cheapest route (418 miles), uses a late goal test (Sibiu to Bucharest costs 278, not 310), updates `reached` when it finds a cheaper path, and handles ties in the priority queue.

**`tests/test_problems.py` (Part 4)**

- Each formulation's `actions` and `result` behave correctly.
- Each answer meets the problem's requirement: the fastest ambulance route, the fewest knight moves, and a valid queens placement that fits in 1 MB of memory.

The Part 4 tests don't say which algorithm to use. A poor choice shows up as a failing requirement test.

## Tips

- Every test has a 10-second time limit (on macOS and Linux). A timeout usually means a search is looping forever: check your cycle check or `reached` table.
- Python's `heapq` compares tuples item by item. If two entries have the same `f` value it will try to compare the nodes and crash, so push `(f(node), tie_breaker, node)`.
- `path_states(node)` and `node.depth()` are handy for debugging.
