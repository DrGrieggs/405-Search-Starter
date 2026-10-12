"""Part 4: Choose your algorithm.

For each problem: finish its formulation, then fill in its solve_... function
using whichever search from search.py you think fits best. Justify your choice
in ANSWERS.md.
"""

from search import (Problem, RouteProblem, make_graph, path_states,
                    breadth_first_search, depth_first_search,
                    best_first_search, uniform_cost_search)


# ---------------------------------------------------------------------------
# Problem A: The ambulance route
# Reach the Hospital from the Depot as fast as possible.
# Each road is labeled with its travel time in minutes.
# ---------------------------------------------------------------------------

CITY_ROADS = [
    ("Depot", "Bridge", 18), ("Bridge", "Hospital", 17),
    ("Depot", "Market", 4), ("Market", "School", 5),
    ("School", "Library", 3), ("Library", "Park", 4),
    ("Park", "Hospital", 6), ("Market", "Library", 9),
    ("School", "Stadium", 12), ("Stadium", "Hospital", 9),
]
city = make_graph(CITY_ROADS)


def solve_ambulance():
    """Return the goal Node for the ambulance's route from Depot to Hospital."""
    problem = RouteProblem("Depot", "Hospital", city)
    raise NotImplementedError("Problem A: choose a search and return its result")


# ---------------------------------------------------------------------------
# Problem B: The knight's journey
# Fewest knight moves from a1 to h8 on an empty 8 x 8 board.
# A state is (column, row), each 0-7: a1 is (0, 0), h8 is (7, 7).
# An action is one of KNIGHT_MOVES, a (d_column, d_row) offset.
# ---------------------------------------------------------------------------

KNIGHT_MOVES = [(1, 2), (2, 1), (2, -1), (1, -2),
                (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


class KnightProblem(Problem):

    def actions(self, state):
        """Return the moves in KNIGHT_MOVES that keep the knight on the board."""
        raise NotImplementedError("Problem B: implement actions")

    def result(self, state, action):
        """Return the square the knight lands on."""
        raise NotImplementedError("Problem B: implement result")


def square_name(state):
    """(0, 0) -> 'a1', (7, 7) -> 'h8'."""
    column, row = state
    return "abcdefgh"[column] + str(row + 1)


def solve_knight():
    """Return the goal Node for the knight's journey from a1 to h8."""
    problem = KnightProblem((0, 0), (7, 7))
    raise NotImplementedError("Problem B: choose a search and return its result")


# ---------------------------------------------------------------------------
# Problem C: The n queens
# Place n queens so that no two share a row, column, or diagonal.
# Place one queen per column, left to right. A state is a tuple of row
# numbers, one per column filled so far: (0, 4) means a queen in row 0 of
# column 0 and one in row 4 of column 1. An action is a row for the next column.
# ---------------------------------------------------------------------------

class QueensProblem(Problem):

    def __init__(self, n=8):
        super().__init__(initial=())
        self.n = n

    def actions(self, state):
        """Return the rows in the next column (column len(state)) that no
        queen in state attacks. Return [] once all n columns are filled."""
        raise NotImplementedError("Problem C: implement actions")

    def result(self, state, action):
        return state + (action,)

    def is_goal(self, state):
        return len(state) == self.n


def solve_queens(n=8):
    """Return the goal Node for a valid placement of n queens."""
    problem = QueensProblem(n)
    raise NotImplementedError("Problem C: choose a search and return its result")


if __name__ == "__main__":
    for name, solve, show in [
        ("Ambulance", solve_ambulance, lambda n: f"{path_states(n)}  {n.path_cost} minutes"),
        ("Knight", solve_knight, lambda n: f"{[square_name(s) for s in path_states(n)]}  {n.depth()} moves"),
        ("Queens", solve_queens, lambda n: f"{n.state}"),
    ]:
        try:
            print(f"{name:10} {show(solve())}")
        except NotImplementedError as err:
            print(f"{name:10} not implemented yet ({err})")
