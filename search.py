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
# Route finding on a map, and the Romania map (Figure 3.1)
# ---------------------------------------------------------------------------

ROADS = [
    ("Arad", "Zerind", 75), ("Arad", "Sibiu", 140), ("Arad", "Timisoara", 118),
    ("Zerind", "Oradea", 71), ("Oradea", "Sibiu", 151), ("Timisoara", "Lugoj", 111),
    ("Lugoj", "Mehadia", 70), ("Mehadia", "Drobeta", 75), ("Drobeta", "Craiova", 120),
    ("Craiova", "Rimnicu Vilcea", 146), ("Craiova", "Pitesti", 138),
    ("Sibiu", "Rimnicu Vilcea", 80), ("Sibiu", "Fagaras", 99),
    ("Rimnicu Vilcea", "Pitesti", 97), ("Fagaras", "Bucharest", 211),
    ("Pitesti", "Bucharest", 101), ("Bucharest", "Giurgiu", 90),
    ("Bucharest", "Urziceni", 85), ("Urziceni", "Hirsova", 98),
    ("Hirsova", "Eforie", 86), ("Urziceni", "Vaslui", 142),
    ("Vaslui", "Iasi", 92), ("Iasi", "Neamt", 87),
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


romania = make_graph(ROADS)


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
    trip = RouteProblem("Arad", "Bucharest", romania)
    for name, search in [("Breadth-first", breadth_first_search),
                         ("Depth-first", depth_first_search),
                         ("Uniform-cost", uniform_cost_search)]:
        try:
            goal = search(trip)
            print(f"{name:14} {path_states(goal)}  {goal.path_cost} miles")
        except NotImplementedError as err:
            print(f"{name:14} not implemented yet ({err})")
