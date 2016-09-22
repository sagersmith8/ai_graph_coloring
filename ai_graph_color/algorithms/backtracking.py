def run(setup, problem, *params):
    """
    This will execute the algorithm

    :param setup: the setup for this algorithm
    :type setup: :class: ~ai_graph_color.Setup
    :param problem: the graph to color
    :type problem: the graph to color
    :param params: the params for this algorithm
    :type params: tuple
    :rtype: list[int] the list of coloring
    :return: the list of colorings for this graph
    """
    len_problem = 0
    for adj_list in problem:
        len_problem += len(adj_list)
    return backtrack({}, problem, len_problem, 0, params[0])


def backtrack(final_color, problem, len_problem, cur_node, num_colors):
    """
    Performs the backtracking algorithm

    :param final_color: dictionary in which to store colorings
    :type final_color: dict
    :param problem: graph to color
    :type problem: list[list]
    :param len_problem: number of nodes to color
    :type len_problem: int
    :param cur_node: index of current node to color
    :type cur_node: int
    :param num_colors: number of colors to use
    :rtype: dict
    :return: the dictionary of correctly colored nodes if it exists
    """
    used_colors = set()
    available_colors = set(i for i in xrange(num_colors))
    for node in problem[cur_node]:
        cur_color = final_color.get(node)
        if cur_color:
            used_colors.add(cur_color)
    available_colors = available_colors.difference(used_colors)
    for color in available_colors:
        final_color[cur_node] = color
        if len(final_color) == len_problem:
            yield final_color
        yield (
            backtrack(
                final_color, problem, len_problem, cur_node+1, num_colors
            )
        )
