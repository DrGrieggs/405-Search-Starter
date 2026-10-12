"""Tests for Part 4: the ambulance, the knight, and the queens.

These tests check your formulations and that each answer meets the problem's
requirements. They don't tell you which algorithm to use; a poor choice
shows up as a wrong answer or a timeout.

Run from the repository folder:  python -m pytest tests/test_problems.py -v
"""

import tracemalloc

import pytest

from search import RouteProblem, path_states
from problems import (city, solve_ambulance, KNIGHT_MOVES, KnightProblem, square_name,
                      solve_knight, QueensProblem, solve_queens)


def queens_attack(state):
    """True if any two queens in state attack each other."""
    for c1, r1 in enumerate(state):
        for c2, r2 in enumerate(state):
            if c1 < c2 and (r1 == r2 or abs(r1 - r2) == c2 - c1):
                return True
    return False


# ---------------------------------------------------------------------------
# Problem A: the ambulance route
# ---------------------------------------------------------------------------

def test_ambulance_route_is_a_real_route():
    node = solve_ambulance()
    states = path_states(node)
    assert states[0] == "Depot" and states[-1] == "Hospital"
    for a, b in zip(states, states[1:]):
        assert b in city[a], f"there is no road from {a} to {b}"


def test_ambulance_route_is_the_fastest():
    node = solve_ambulance()
    assert node.path_cost == 22, (
        f"your route takes {node.path_cost} minutes; a faster one exists")


# ---------------------------------------------------------------------------
# Problem B: the knight's journey
# ---------------------------------------------------------------------------

def test_knight_actions_from_a_corner():
    problem = KnightProblem((0, 0), (7, 7))
    assert sorted(problem.actions((0, 0))) == [(1, 2), (2, 1)]


def test_knight_actions_from_the_middle():
    problem = KnightProblem((0, 0), (7, 7))
    assert sorted(problem.actions((3, 3))) == sorted(KNIGHT_MOVES)


def test_knight_actions_never_leave_the_board():
    problem = KnightProblem((0, 0), (7, 7))
    for col in range(8):
        for row in range(8):
            for action in problem.actions((col, row)):
                c, r = problem.result((col, row), action)
                assert 0 <= c < 8 and 0 <= r < 8, f"{square_name((col, row))} jumps off the board"


def test_knight_result():
    problem = KnightProblem((0, 0), (7, 7))
    assert problem.result((0, 0), (1, 2)) == (1, 2)
    assert problem.result((4, 4), (-2, -1)) == (2, 3)


def test_knight_journey_is_legal():
    node = solve_knight()
    squares = path_states(node)
    assert squares[0] == (0, 0) and squares[-1] == (7, 7)
    for (c1, r1), (c2, r2) in zip(squares, squares[1:]):
        assert (c2 - c1, r2 - r1) in KNIGHT_MOVES, (
            f"{square_name((c1, r1))} to {square_name((c2, r2))} is not a knight move")


def test_knight_journey_uses_fewest_moves():
    node = solve_knight()
    assert node.depth() == 6, f"your journey takes {node.depth()} moves; a shorter one exists"


# ---------------------------------------------------------------------------
# Problem C: the n queens
# ---------------------------------------------------------------------------

def test_queens_first_column_has_every_row():
    assert sorted(QueensProblem(8).actions(())) == list(range(8))


def test_queens_actions_avoid_attacked_rows():
    # A queen in row 0 of column 0 attacks row 0 and (diagonally) row 1 of column 1.
    assert sorted(QueensProblem(8).actions((0,))) == [2, 3, 4, 5, 6, 7]


def test_queens_actions_check_every_earlier_queen():
    # Queens at (col 0, row 0) and (col 1, row 2). In column 2, row 0 is in
    # the same row as the first queen, row 2 is in the same row as the second,
    # and rows 1 and 3 are on the second queen's diagonals.
    assert sorted(QueensProblem(8).actions((0, 2))) == [4, 5, 6, 7]


def test_queens_full_board_has_no_actions():
    assert QueensProblem(4).actions((1, 3, 0, 2)) == []


@pytest.mark.parametrize("n", [1, 4, 5, 8])
def test_queens_solution_is_valid(n):
    node = solve_queens(n)
    assert node is not None, f"{n} queens has a solution"
    assert len(node.state) == n
    assert sorted(node.state) == list(range(n)), "each row should hold exactly one queen"
    assert not queens_attack(node.state), f"queens attack each other in {node.state}"


@pytest.mark.parametrize("n", [2, 3])
def test_queens_with_no_solution_returns_none(n):
    assert solve_queens(n) is None


def test_queens_uses_little_memory():
    # Section 3.4.3: when any solution will do and the space is a tree, a
    # well-chosen search keeps only a small frontier. 10 queens should fit
    # in 1 MB of peak memory; an algorithm that stores every partial board
    # needs several megabytes.
    budget_mb = 1.0
    tracemalloc.start()
    try:
        node = solve_queens(10)
        peak_mb = tracemalloc.get_traced_memory()[1] / 1_000_000
    finally:
        tracemalloc.stop()
    assert node is not None and not queens_attack(node.state)
    assert peak_mb < budget_mb, (
        f"10 queens used {peak_mb:.1f} MB at peak; the budget is {budget_mb} MB")
