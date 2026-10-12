"""Search framework and the three algorithms you will implement.

Parts 1-3 of the worksheet: fill in breadth_first_search, depth_first_search,
and best_first_search at the bottom of this file. Everything above them is
given to you; read it before you start.
"""

from collections import deque
import heapq
import itertools


# ---------------------------------------------------------------------------
# The five parts of a search problem (Section 3.1.1)
# ---------------------------------------------------------------------------

class Problem:
    """A search problem. Subclass it and fill in the methods."""

    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):            # ACTIONS(s)
        raise NotImplementedError

    def result(self, state, action):     # RESULT(s, a)
        raise NotImplementedError

    def is_goal(self, state):            # IS-GOAL(s)
        return state == self.goal

    def action_cost(self, s, a, s2):     # ACTION-COST(s, a, s')
        return 1


# ---------------------------------------------------------------------------
# Search-tree nodes (Section 3.3.2)
# ---------------------------------------------------------------------------

class Node:
    """A node in the search tree."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def depth(self):
        d, node = 0, self
        while node.parent is not None:
            d, node = d + 1, node.parent
        return d

    def __repr__(self):
        return f"<Node {self.state} g={self.path_cost}>"


def expand(problem, node):
    """Yield a child node for each action applicable in node's state."""
    s = node.state
    for action in problem.actions(s):
        s2 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s2)
        yield Node(s2, node, action, cost)


def path_states(node):
    """Follow PARENT pointers back to the root; return the states in order."""
    states = []
    while node is not None:
        states.append(node.state)
        node = node.parent
    return states[::-1]


def is_cycle(node):
    """True if node's state already appears earlier on its own path."""
    state, ancestor = node.state, node.parent
    while ancestor is not None:
        if ancestor.state == state:
            return True
        ancestor = ancestor.parent
    return False


# ---------------------------------------------------------------------------
# Route finding on a map: main roads of western Pennsylvania
# ---------------------------------------------------------------------------

# Each road's length is the real driving distance in miles between the two
# towns' centers, from the OpenStreetMap routing engine (OSRM), rounded to
# the nearest mile. Like the textbook's Romania map (Figure 3.1), it is
# simplified: 24 towns and the main highways between them.
ROADS = [
    ("Indiana", "Blairsville", 16), ("Indiana", "Kittanning", 27), ("Indiana", "Punxsutawney", 28),
    ("Indiana", "Ebensburg", 29), ("Indiana", "Johnstown", 27), ("Blairsville", "Latrobe", 12),
    ("Blairsville", "Johnstown", 25), ("Blairsville", "Ebensburg", 31), ("Blairsville", "Pittsburgh", 42),
    ("Latrobe", "Greensburg", 11), ("Blairsville", "Greensburg", 20), ("Greensburg", "Pittsburgh", 34),
    ("Ebensburg", "Johnstown", 18), ("Ebensburg", "Altoona", 24), ("Kittanning", "Butler", 23),
    ("Kittanning", "Pittsburgh", 42), ("Pittsburgh", "Butler", 33), ("Butler", "New Castle", 27),
    ("Butler", "Grove City", 25), ("Butler", "Franklin", 43), ("New Castle", "Grove City", 21),
    ("Grove City", "Meadville", 40), ("Grove City", "Franklin", 24), ("Meadville", "Erie", 41),
    ("Franklin", "Meadville", 27), ("Franklin", "Clarion", 29), ("Kittanning", "Clarion", 37),
    ("Clarion", "Brookville", 20), ("Brookville", "Punxsutawney", 20), ("Brookville", "DuBois", 20),
    ("Punxsutawney", "DuBois", 20), ("DuBois", "Clearfield", 21), ("Clearfield", "State College", 41),
    ("Altoona", "State College", 41), ("Pittsburgh", "Washington", 27), ("Washington", "Uniontown", 44),
    ("Uniontown", "Greensburg", 36), ("Greensburg", "Somerset", 43), ("Somerset", "Johnstown", 28),
    ("Altoona", "Clearfield", 50), ("Somerset", "Uniontown", 50), ("Pittsburgh", "Uniontown", 45),
    ("Latrobe", "Somerset", 33), ("Kittanning", "Greensburg", 42), ("Kittanning", "Brookville", 39),
    ("Greensburg", "Washington", 47), ("Clarion", "Grove City", 43), ("Butler", "Clarion", 50),
    ("Ebensburg", "DuBois", 57),
]


def make_graph(edges):
    """Turn a list of (a, b, cost) roads into a two-way adjacency dict."""
    graph = {}
    for a, b, cost in edges:
        graph.setdefault(a, {})[b] = cost
        graph.setdefault(b, {})[a] = cost
    return graph


class RouteProblem(Problem):
    """Travel between places on a map; an action is 'go to this neighbor'."""

    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, s):
        return list(self.graph.get(s, {}))

    def result(self, s, a):
        return a

    def action_cost(self, s, a, s2):
        return self.graph[s][a]


western_pa = make_graph(ROADS)


# ---------------------------------------------------------------------------
# YOUR CODE: the three search algorithms
# Each returns a goal Node, or None if there is no solution.
# ---------------------------------------------------------------------------

def breadth_first_search(problem):
    """Part 1. Return a goal Node with the fewest actions, or None.

    Frontier: a FIFO queue (collections.deque: append / popleft).
    Reached: a set of states.
    Goal test: early, as soon as a child is generated.
    """
    raise NotImplementedError("Part 1: implement breadth-first search")


def depth_first_search(problem):
    """Part 2. Return the first goal Node found, or None.

    Frontier: a LIFO stack (a Python list: append / pop).
    No reached table: skip any node for which is_cycle(node) is True.
    """
    raise NotImplementedError("Part 2: implement depth-first search")


def best_first_search(problem, f):
    """Part 3. Expand the frontier node with the lowest f(node); return a goal Node or None.

    Frontier: a priority queue (heapq). Push (f(node), tie_breaker, node);
    itertools.count() makes tie-breakers so Nodes are never compared.
    Reached: a dict mapping each state to the best Node found for it so far.
    Goal test: late, when a node is popped.
    """
    raise NotImplementedError("Part 3: implement best-first search")


def uniform_cost_search(problem):
    """Best-first search with f(n) = path cost (Dijkstra's algorithm)."""
    return best_first_search(problem, lambda node: node.path_cost)


if __name__ == "__main__":
    trip = RouteProblem("Indiana", "Erie", western_pa)
    for name, search in [("Breadth-first", breadth_first_search),
                         ("Depth-first", depth_first_search),
                         ("Uniform-cost", uniform_cost_search)]:
        try:
            goal = search(trip)
            print(f"{name:14} {path_states(goal)}  {goal.path_cost} miles")
        except NotImplementedError as err:
            print(f"{name:14} not implemented yet ({err})")
