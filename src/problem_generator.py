"""
This file will generate a random planer graph
"""
import os
import random
import sys


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
    out_file = os.path.join('problems', out_file)
    with open(out_file, 'w') as out_file:
        out_file.writelines(
            ' '.join(
                map(
                    lambda x: str(x), adjacency_list
                )
            ) + '\n' for adjacency_list in graph
        )


def read_graph_from_file(in_file):
    """
    Reads in a graph and returns it

    :param in_file: name of input file
    :type in_file: str
    :rtype: list[list[int]]
    :return: adjacency list representing graph from file
    """
    with open(in_file) as in_file:
        graph = [
            map(lambda x: int(x), line[:-1].split(' ')) for line in in_file
            ]

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
    pass


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
