"""
This file will generate a random planer graph
"""
import sys
import os


def write_graph_to_file(out_file, graph):
    """
    Writes the given graph to the specified file

    :param out_file: Location of the outfile
    :type out_file: str
    :param graph: The adjacency list to write
    :type graph: list
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
    :rtype: list
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
    :rtype: list
    :return: A random planar graph
    """
    pass

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 2:
        print('Usage: {Outfile} {Number of Vertices}')
    else:
        outfile, num_vert = args
        num_vert = int(num_vert)
        write_graph_to_file(outfile, generate_graph(num_vert))
