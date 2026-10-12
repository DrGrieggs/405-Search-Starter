"""Tests for Parts 1-3: breadth-first, depth-first, and best-first search.

Run from the repository folder:  python -m pytest tests/test_search.py -v
"""

import pytest

from search import (Problem, Node, RouteProblem, make_graph, path_states, western_pa,
                    breadth_first_search, depth_first_search,
                    best_first_search, uniform_cost_search)


# ---------------------------------------------------------------------------
# Helpers and small test problems
# ---------------------------------------------------------------------------

def assert_valid_solution(problem, node):
    """The node must be a real path: start to goal, legal steps, correct cost."""
    assert node is not None, "search returned None, but a solution exists"
    assert isinstance(node, Node), "search should return a Node"
    states = path_states(node)
    assert states[0] == problem.initial, "path must start at the initial state"
    assert problem.is_goal(states[-1]), "path must end at a goal state"
    cost = 0
    for s, s2 in zip(states, states[1:]):
        moves = [a for a in problem.actions(s) if problem.result(s, a) == s2]
        assert moves, f"illegal step in path: {s} -> {s2}"
        cost += problem.action_cost(s, moves[0], s2)
    assert node.path_cost == cost, "node.path_cost doesn't match the path"


class GridProblem(Problem):
    """Move up, down, left, or right on an open width x height grid. Each move costs 1."""

    def __init__(self, initial, goal, width, height):
        super().__init__(initial, goal)
        self.width, self.height = width, height

    def actions(self, state):
        x, y = state
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return [(dx, dy) for dx, dy in moves
                if 0 <= x + dx < self.width and 0 <= y + dy < self.height]

    def result(self, state, action):
        return (state[0] + action[0], state[1] + action[1])


# Two islands: nothing connects {A, B} with {X, Y}.
ISLANDS = make_graph([("A", "B", 1), ("X", "Y", 1)])

# The direct road S-G is one action but costly; S-M-N-G is three cheap actions.
SHORTCUT = make_graph([("S", "G", 50), ("S", "M", 5), ("M", "N", 5), ("N", "G", 5)])

ALL_SEARCHES = [
    pytest.param(breadth_first_search, id="breadth-first"),
    pytest.param(depth_first_search, id="depth-first"),
    pytest.param(uniform_cost_search, id="uniform-cost"),
]


# ---------------------------------------------------------------------------
# Behavior every search should share
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("search", ALL_SEARCHES)
def test_finds_a_valid_route_indiana_to_erie(search):
    problem = RouteProblem("Indiana", "Erie", western_pa)
    assert_valid_solution(problem, search(problem))


@pytest.mark.parametrize("search", ALL_SEARCHES)
def test_start_is_already_the_goal(search):
    problem = RouteProblem("Indiana", "Indiana", western_pa)
    node = search(problem)
    assert node is not None
    assert path_states(node) == ["Indiana"]
    assert node.path_cost == 0


@pytest.mark.parametrize("search", ALL_SEARCHES)
def test_returns_none_when_goal_is_unreachable(search):
    problem = RouteProblem("A", "Y", ISLANDS)
    assert search(problem) is None


@pytest.mark.parametrize("search", ALL_SEARCHES)
def test_finds_a_route_on_a_grid(search):
    problem = GridProblem((0, 0), (3, 2), width=4, height=3)
    assert_valid_solution(problem, search(problem))


# ---------------------------------------------------------------------------
# Part 1: breadth-first search
# ---------------------------------------------------------------------------

def test_bfs_finds_fewest_actions_indiana_to_erie():
    # Several 5-road routes reach Erie; any of them is correct.
    problem = RouteProblem("Indiana", "Erie", western_pa)
    node = breadth_first_search(problem)
    assert_valid_solution(problem, node)
    assert node.depth() == 5


def test_bfs_minimizes_actions_not_cost():
    problem = RouteProblem("S", "G", SHORTCUT)
    node = breadth_first_search(problem)
    assert path_states(node) == ["S", "G"]
    assert node.path_cost == 50


def test_bfs_finds_shortest_path_on_a_grid():
    # From one corner of a 6 x 6 grid to the other takes exactly 10 moves.
    node = breadth_first_search(GridProblem((0, 0), (5, 5), width=6, height=6))
    assert node.depth() == 10


# ---------------------------------------------------------------------------
# Part 2: depth-first search
# ---------------------------------------------------------------------------

def test_dfs_terminates_on_a_map_with_cycles():
    # The map has loops (Somerset-Latrobe-Greensburg-Somerset); without a
    # cycle check this test times out.
    problem = RouteProblem("Indiana", "Erie", western_pa)
    assert_valid_solution(problem, depth_first_search(problem))


def test_dfs_path_never_repeats_a_state():
    node = depth_first_search(RouteProblem("Indiana", "Erie", western_pa))
    states = path_states(node)
    assert len(states) == len(set(states)), "the returned path contains a cycle"


def test_dfs_explores_unreachable_goal_and_gives_up():
    # A small map with a loop and no route to the goal: DFS must try every
    # cycle-free path, then return None.
    loop = make_graph([("A", "B", 1), ("B", "C", 1), ("C", "A", 1), ("C", "D", 1)])
    assert depth_first_search(RouteProblem("A", "Z", loop)) is None


# ---------------------------------------------------------------------------
# Part 3: best-first search
# ---------------------------------------------------------------------------

def test_ucs_finds_cheapest_route_indiana_to_erie():
    node = uniform_cost_search(RouteProblem("Indiana", "Erie", western_pa))
    assert node.path_cost == 156
    assert path_states(node) == ["Indiana", "Kittanning", "Butler", "Grove City", "Meadville", "Erie"]


def test_ucs_finds_cheapest_of_equal_length_routes():
    # Two 3-road routes reach Uniontown: via Pittsburgh (103 mi) and via
    # Greensburg (72 mi). Only the cheaper one is correct.
    node = uniform_cost_search(RouteProblem("Indiana", "Uniontown", western_pa))
    assert node.path_cost == 72
    assert path_states(node) == ["Indiana", "Blairsville", "Greensburg", "Uniontown"]


def test_ucs_prefers_cheap_path_over_short_path():
    node = uniform_cost_search(RouteProblem("S", "G", SHORTCUT))
    assert path_states(node) == ["S", "M", "N", "G"]
    assert node.path_cost == 15


def test_ucs_uses_late_goal_test():
    # Like Figure 3.10: Brookville is first generated via Kittanning (66 mi),
    # but the cheaper path via Punxsutawney (48 mi) must win. An early goal
    # test returns 66.
    node = uniform_cost_search(RouteProblem("Indiana", "Brookville", western_pa))
    assert node.path_cost == 48
    assert path_states(node) == ["Indiana", "Punxsutawney", "Brookville"]


def test_best_first_updates_reached_with_cheaper_path():
    # B is first reached directly (cost 10), then more cheaply via C (cost 2).
    graph = make_graph([("A", "B", 10), ("A", "C", 1), ("C", "B", 1), ("B", "G", 1)])
    node = uniform_cost_search(RouteProblem("A", "G", graph))
    assert path_states(node) == ["A", "C", "B", "G"]
    assert node.path_cost == 3


def test_best_first_respects_the_evaluation_function():
    # With f(n) = depth, best-first search finds the fewest actions, like BFS.
    node = best_first_search(RouteProblem("Indiana", "Erie", western_pa), lambda n: n.depth())
    assert node.depth() == 5


def test_best_first_handles_ties_without_comparing_nodes():
    # Every action costs 1 here, so many nodes share the same f value.
    problem = GridProblem((0, 0), (4, 4), width=5, height=5)
    node = uniform_cost_search(problem)
    assert_valid_solution(problem, node)
    assert node.path_cost == 8
