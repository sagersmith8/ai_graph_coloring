"""
This file will generate a random planer graph
"""
from itertools import combinations
from line import Line
from llist import dllist

import os
import random
import sys
import json


def write_graph_to_file(out_file, graph):
    """
    Writes the given graph to the specified file

    :param out_file: Location of the outfile
    :type out_file: str
    :param graph: The adjacency list to write
    :type graph: list[list[int]]
    :rtype: None
    :return: Nothing, but a file is written
    """
    out_file = generate_file_path(out_file)
    with open(out_file, 'w') as out_file:
        json.dump(graph, out_file, encoding='utf8')


def generate_file_path(file_name):
    """
    Returns the file path to problems

    :param file_name: The file to create
    :type file_name: str
    :rtype: str
    :return: The file path to the problem
    """
    return os.path.join('problems', file_name)


def read_graph_from_file(in_file):
    """
    Reads in a graph and returns it

    :param in_file: name of input file
    :type in_file: str
    :rtype: list[list[int]]
    :return: adjacency list representing graph from file
    """
    in_file = generate_file_path(in_file)
    with open(in_file) as in_file:
        graph = json.load(in_file, encoding='utf8')
    return graph


def generate_graph(num_vert):
    """
    Generates a random planar graph with specified number of vertices

    :param num_vert: The number of vertices to have in the graph
    :type num_vert: int
    :rtype: list[list[int]]
    :return: A random planar graph as an adjacency list
    """
    random_points = scatter_points(num_vert)
    return build_graph(random_points)


def build_graph(points):
    """
    Generates a planar graph from a set of points by following a particular
    set of rules:
    - Each point is a vertex in the graph
    - Each line connecting two points is an edge between two vertices
    - Connections are made with the following procedure:
      - Until there are no more connections that can be made between vertices:
        - Pick a random point X
        - With a straight line, connect X to the closest point Y that has the
          following properties:
          1. X is not connected to Y
          2. the line connecting X and Y does not cross any other existing
             lines

    :param points: the points from which to generate the graph
    :type points: list[tuple(int,int)]
    :rtype: graph (adjacency list)
    :return: a planar graph constructed from the given vertices
    """
    lines = create_lines(points)
    point_distances = create_distance_list(lines, len(points))
    point_distances = point_distances  # TODO use point_distances


def create_lines(points):
    """
    Generate a map of all the possible lines between points, indexed by an
    immutable set of the indexes of the two points connected by the line

    :param points: the points to create lines from
    :type points: list[tuple(float, float)]
    :return: the map of lines
    :rtype: map<frozenset(int), Line>
    """
    lines = {}
    for point_a, point_b in combinations(enumerate(points), 2):
        connecting_line = Line(point_a[1], point_b[1])
        key = frozenset([point_a[0], point_b[0]])
        lines[key] = connecting_line

        connecting_line.add_reference(dict.pop, lines, key)
    return lines


def create_distance_list(lines, num_points):
    """
    Generate a list of doubly-linked lists ordering the given lines by
    increasing distance from the point at the current index.

    :param lines: the map of lines
    :type lines: map<frozenset(int), Line>
    :param num_points: the number of points being connected
    :type num_points: int
    :return: the distance list
    :rtype: list[dllist(tuple(int, Line))]
    """
    point_distances = [[] for _ in xrange(num_points)]
    for point_pair, connecting_line in lines.items():
        if len(point_pair) != 2:
            raise Exception(
                ("Expected set indexes into set-line-map to have exactly 2 "
                 "point indexes")
            )

        point_a, point_b = tuple(point_pair)

        point_distances[point_a].append((point_b, connecting_line))
        point_distances[point_b].append((point_a, connecting_line))

    for index, distance_list in enumerate(point_distances):
        point_distances[index] = dllist(
            sorted(distance_list, key=lambda x: x[1].distance)
        )

        cur_node = point_distances[index].first
        while cur_node is not None:
            connected_index = cur_node.value[0]
            lines[frozenset([index, connected_index])].add_reference(
                dllist.remove, point_distances[index], cur_node
            )
            cur_node = cur_node.next
    return point_distances


def scatter_points(num_points, seed=None):
    """
    Generates a specified number of random 2d points in the rectangle from
    (0, 0) to (1, 1).

    If no seed is specified, the current time is used as the seed.

    :param num_points: the number of points to generate
    :type num_points: int
    :param seed: the seed for the pseudo-random number generator
    :type seed: int
    :rtype: list[tuple(int,int)]
    :return: list of generated points
    """
    random.seed(seed)

    return [
        (random.random(), random.random()) for _ in range(num_points)
    ]


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 2:
        print('Usage: {Outfile} {Number of Vertices}')
    else:
        outfile, num_vert = args
        num_vert = int(num_vert)
        write_graph_to_file(outfile, generate_graph(num_vert))
