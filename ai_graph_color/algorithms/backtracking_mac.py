params = {}  # default params


# :param 'colors': the number of colors to use for colorings
# :type 'colors': int


def run(graph, setup, params):
    """
    Searches the graph using backtracking

    :param setup: the setup for this algorithm
    :type setup: Setup
    :param problem: The graph to color
    :type problem: list[list[int]]
    :param num_colors: number of colors to try and color with
    :type num_colors: int
    :rtype: dict
    :return: the colored graph
    """
    num_colors = params['colors']
    coloring, avail_colors, stack = init(graph, num_colors)

    while True:
        if len(stack) == 0 or complete(coloring, graph):
            if setup:
                setup.logger.debug(
                    'Finished, final coloring: {}'.format(coloring)
                )
            yield coloring
        cur_node = stack[len(stack) - 1][1]
        coloring[cur_node] = stack[len(stack) - 1][3]
        if setup:
            if setup.counter.increment():
                if setup:
                    setup.logger.debug(
                        "Preempted with coloring:{}".format(coloring)
                    )
                yield coloring
            setup.logger.debug(
                'Finished, final coloring: {}'.format(coloring)
            )
        choose_next_node(
            stack, coloring, graph, avail_colors, num_colors, setup
        )


def init(graph, num_colors):
    """
    Initializes the backtracking algorithm
    :param graph: graph to color
    :type graph: list[list[int]]
    :param num_colors: the number of colors to color with
    :type num_colors: int
    :rtype: tuple
    :return: the inital states of coloring, avail_colors, and stack
    """
    avail_colors = []
    for _ in xrange(len(graph)):
        avail_colors.append(set(xrange(num_colors)))
    coloring = dict()
    stack = list()
    choose_next_node(stack, coloring, graph, avail_colors, num_colors)
    return (
        coloring,
        avail_colors,
        stack
    )


def choose_next_node(
        stack, coloring, graph, avail_colors, num_colors, setup=None):
    """
    Chooses the next node and its coloring and adds it to the stack

    :param setup: the setup with the counter and the logger
    :type setup: Setup
    :param stack: the current stack of the program
    :type stack: list[dict{int:int}, int, set{int}, int}]
    :param coloring: the current coloring of the program
    :type coloring: dict{int:int}
    :param graph: the current graph to color
    :type graph: list[list[int]]
    :param avail_colors: the available colors to color with
    :type avail_colors: set{int}
    :param num_colors: the number of colors to color with
    :type num_colors: int
    :rtype: bool
    :return: True if it picks the next node and False if it doesn't
    """
    keep_choosing = True
    while keep_choosing:
        keep_choosing = False
        next_node = (
            min_remaining_var(coloring, graph)
        )

        while next_node is None:
            if len(stack) == 0:
                if setup:
                    setup.logger.debug('Stack is empty')
                return
            if setup:
                setup.logger.debug('About to backtrack..')
                setup.logger.debug('Current stack is {}'
                                   .format(stack))
            stack.pop()
            if setup:
                setup.logger.debug('Just backtracked..')
                setup.logger.debug('Current stack is {}'
                                   .format(stack))
            next_node = (
                min_remaining_var(coloring, graph)
            )

        chosen_color = min_color_conflicts(
            avail_colors, graph, next_node, num_colors
        )

        avail_colors[next_node] -= {chosen_color}
        nodes_to_check = [(node, next_node) for node in graph[next_node]]
        while len(nodes_to_check) > 0:
            node, prev_node = nodes_to_check.pop(0)
            if len(avail_colors[prev_node]) == 1:
                coloring[prev_node] = list(avail_colors[prev_node])[0]
                avail_colors[node] -= coloring[prev_node]
                if setup:
                    setup.logger.debug('Doing the MAC case')
                    setup.logger.debug(
                        """
                        Removing color : {} from node: {}'s color choices
                        because it is node: {}'s  only color choice
                        """.format(coloring[prev_node], node, prev_node)
                    )
                if setup:
                    setup.logger.debug('About to add to MAC queue..')
                    setup.logger.debug('Cur queue: {}'.format(nodes_to_check))
                nodes_to_check.extend(
                    (temp_node, node)
                    for temp_node in graph[node]
                    if temp_node != prev_node
                )

                if setup:
                    setup.logger.debug("Added to MAC queue..")
                    setup.logger.debug('Cur queue: {}'.format(nodes_to_check))
            elif avail_colors[node] == 0:
                if setup:
                    setup.logger.debug(
                        """
                        MAC found a coloring that won't work,
                        trying new coloring
                        """
                    )
                keep_choosing = True
                break

    if len(avail_colors[next_node]) > 0:
        if setup:
            setup.logger.debug('About to add to stack..')
            setup.logger.debug('Current  stack: {}'.format(stack))
        stack.append(
            [
                coloring,
                next_node,
                avail_colors[next_node],
                chosen_color
            ]
        )
        if setup:
            setup.logger.debug('Added to stack..')
            setup.logger.debug('Current  stack: {}'.format(stack))

    else:
        if setup:
            setup.logger.debug('About to backtrack..')
            setup.logger.debug('Current  stack: {}'.format(stack))
        coloring[next_node] = chosen_color
        stack.pop()
        if setup:
            if setup.counter.increment():
                setup.logger.debug("Didn't finish, final coloring: {}"
                                   .format(coloring))
                # Todo yield coloring, it breaks the function for somereason
            setup.logger.debug('Just backtracked..')
            setup.logger.debug('Current  stack: {}'.format(stack))


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
            avail_colors[node] - (all_colors - avail_colors[cur_node])
        )
        for color in available_colors:
            available_color_count[color][0] = 1
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
        if coloring.get(index) is not None:
            continue
        for node in adj_list:
            if coloring.get(node) is not None:
                colored_neighbors.add(coloring.get(node))
        num_neighbors_colored.append(
            (len(colored_neighbors), len(adj_list), index)
        )
    return max(num_neighbors_colored)[2] if num_neighbors_colored else None


if __name__ == '__main__':
    from ai_graph_color import problem_generator
    from ai_graph_color import setup

    generated_problem = problem_generator.generate_graph(100)
    print generated_problem
    print (
        run(generated_problem, setup.TestRun('test.txt'), {'colors': 4}).next()
    )
