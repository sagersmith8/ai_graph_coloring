import random


def run(graph, params, setup):
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

        for color in colors:
            if color != initial_color:
                coloring[index] = color

                conflicts = num_conflicts_node(graph, index, coloring)
                if conflicts < min_conflicts:
                    min_conflicts = conflicts
                    min_conflicts_value = color

        coloring[index] = min_conflicts_value
        num_conflicts -= initial_conflicts - min_conflicts

    return coloring


def num_conflicts_graph(graph, coloring):
    conflicts = 0
    for from_index, connections in enumerate(graph):
        for to_index in connections:
            if coloring[to_index] == coloring[from_index]:
                conflicts += 1
    conflicts /= 2  # each connection is counted twice
    return conflicts


def num_conflicts_node(graph, index, coloring):
    conflicts = 0
    for to_index in graph[index]:
        if coloring[index] == coloring[to_index]:
            conflicts += 1
    return conflicts
