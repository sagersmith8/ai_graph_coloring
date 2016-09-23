"""
Color a graph using min-conflicts:

First generate a random coloring for the graph.
Until there are no conflicts in the graph,
    choose a random node in the graph, and change it to have the color
    which reduces the number of conflicts in the graph the most.

:param colors: the number of colors to color the graph with
:type colors: int
"""

import random

params = {}


def run(graph, setup, params):
    num_colors = params['colors']

    colors = range(num_colors)
    coloring = [random.choice(colors) for _ in graph]
    num_conflicts = num_conflicts_graph(graph, coloring)

    while num_conflicts > 0:
        index = random.randint(0, len(graph) - 1)

        initial_conflicts = num_conflicts_node(graph, index, coloring)
        initial_color = coloring[index]
        min_conflicts = initial_conflicts
        min_conflicts_value = initial_color

        colors = range(num_colors)
        colors.remove(initial_color)  # don't recheck the same color

        for color in colors:
            coloring[index] = color

            conflicts = num_conflicts_node(graph, index, coloring)
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                min_conflicts_value = color

        coloring[index] = min_conflicts_value
        num_conflicts -= initial_conflicts - min_conflicts

    return coloring


def num_conflicts_graph(graph, coloring):
    """
    Compute the number of conflicting edges on a graph for a given
    coloring.

    :param graph: the graph, in adjacency list form
    :type graph: list[list[int]]
    :param coloring: the coloring of the graph
    :type coloring: list[int]
    :rtype: int
    :return: the number of conflicting edges for the coloring of the
        given graph.
    """
    conflicts = 0
    for from_index, connections in enumerate(graph):
        for to_index in connections:
            if (from_index < to_index and
                    coloring[to_index] == coloring[from_index]):
                conflicts += 1
    return conflicts


def num_conflicts_node(graph, index, coloring):
    """
    Compute the number of conflicting edges coming from a particular
    node on a graph with a particular coloring.

    :param graph: a graph in adjacency list form
    :type graph: list[list[int]]
    :param index: the index of the node in the graph
    :type index: int
    :param coloring: the coloring of the graph
    :type coloring: list[int]
    :return: the number of conflicting edges coming from the given
        node for the given coloring
    """
    conflicts = 0
    for to_index in graph[index]:
        if coloring[index] == coloring[to_index]:
            conflicts += 1
    return conflicts
