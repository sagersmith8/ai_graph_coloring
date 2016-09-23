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
    return backtracking_search(problem, params[0])


def backtracking_search(graph, num_colors):
    """

    :param problem:
    :param num_colors:
    :return:
    """
    coloring, avail_colors, stack = init(graph, num_colors)

    iteration = 0
    while True:
        print (
            'iteration_num: {} stack :{}'.format(
                iteration, stack
            )
        )

        cur_node = stack[len(stack)-1][1]
        coloring[cur_node] = stack[len(stack)-1][3]
        choose_next_node(stack, coloring, graph, avail_colors, num_colors)
        iteration += 1
    return coloring


def init(graph, num_colors):
    avail_colors = []
    for _ in xrange(len(graph)):
        avail_colors.append(set(xrange(num_colors)))
    coloring = dict()
    stack = list()
    cur_node = min_remaining_var(coloring, graph)
    chosen_color = min_color_conflicts(
        avail_colors, graph, cur_node, num_colors
    )

    for node in graph[cur_node]:
        avail_colors[node] -= {coloring[cur_node]}

    stack.append([coloring, cur_node, avail_colors, chosen_color])
    return (
        coloring,
        avail_colors,
        stack
    )


def choose_next_node(stack, coloring, graph, avail_colors, num_colors):
    """

    :param stack:
    :param coloring:
    :param graph:
    :param avail_colors:
    :param num_colors:
    :return:
    """
    next_node = (
        min_remaining_var(coloring, graph)
    )

    for node in graph[next_node]:
        avail_colors[node] -= {coloring[next_node]}

    min_color_conflicts(
        avail_colors[next_node], graph, next_node, num_colors
    )

    if len(avail_colors[next_node]) > 0:
        stack.append(
            coloring,
            next_node,
            avail_colors[next_node],
        )
    else:
        stack.pop()


def min_color_conflicts(avail_colors, graph, cur_node, num_color):
    """
    Returns the color with the least number of conflicts
    :param graph: the graph to color
    :type graph: [(int, {int})]
    :param cur_node: index of the not you are attempting to color
    :type cur_node: int
    :param num_color: number of colors we are using
    :type num_color: int
    :rtype: int
    :return: the color that causes the lease number of conflict
    """
    available_color_count = [[0, i] for i in xrange(num_color)]
    all_colors = set(range(num_color))
    for node in graph[cur_node]:
        available_colors = (
            avail_colors[node]-(all_colors -
                                avail_colors[cur_node])
        )
        for color in available_colors:
            available_color_count[color][0] += 1
    return max(available_color_count)[1]


def complete(coloring, graph):
    """
    Checks if the problem is solved

    :param coloring: the coloring dictionary
    :type coloring: dict{int: int}
    :param graph: the graph to color
    :type graph: [[(int, {int}]]
    :rtype: bool
    :return: True if problem is solved false otherwise
    """
    return len(coloring) == len(graph)


def min_remaining_var(coloring, graph):
    """
    Finds the minimum remaining variable in the graph
       - The node connected to the most nodes with colors
    :param coloring: list of chosen colors
    :type coloring: dict{int : int}
    :param graph: graph to color
    :type graph: [[(int, {int}]]
    :rtype: int
    :return: the index of the MRV
    """
    num_neighbors_colored = list()

    for index, adj_list in enumerate(graph):
        colored_neighbors = set()
        for node in adj_list:
            if coloring.get(node) is not None:
                colored_neighbors.add(coloring.get(node))
        num_neighbors_colored.append(
            (len(colored_neighbors), len(adj_list), index)
        )
    return max(num_neighbors_colored)[2]


if __name__ == '__main__':
    from ai_graph_color import problem_generator
    generated_problem = problem_generator.generate_graph(5)
    print generated_problem, '\n', backtracking_search(generated_problem, 4)
