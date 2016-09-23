"""
This file will use a genetic algorithm to solve graph coloring
"""
import random

params = {
    'colors': 4,
    'population_size': 1000,
    'mutation': 0.05,
    'tournament_size': 20,
    'children_per_generation': 20,
    'crossover_rate': 0.25
}


def generate_initial_population(graph, population_size, num_colors):
    """
    Randomly initializes population, each as a potential solution

    :param graph: the adjacency list of nodes to be colored
    :type: list[list[int]]
    :param population_size: the number of potential solutions to generate
    :type: int
    :param num_colors: number of colors the program attemps
        to color the graph with
    :type: int

    :return: the initial population
    :rtype: list[tuple(int,list[int])]
    """
    colors = range(num_colors)

    population = []

    for _ in xrange(population_size):
        choices = [random.choice(colors) for i in xrange(len(graph))]
        population.append((calculate_fitness(choices, graph), choices))

    return population


def tournament_selection(population, tournament_size,
                         children_per_generation, setup):
    """
    Determines the parents for crossover via tournament selection

    :param population: the current potential graph coloring solutions
    :type: list[tuple(int,list[int])]
    :param tournament_size: number of members of the population to select for
        each tournament
    :type: int
    :param children_per_generation: number of new children
        each generation
    :type: int

    :return: list of parents for crossover
    :rtype: list[tuple(int,list[int])]
    """
    winners = []
    for i in range(children_per_generation):
        tournament = random.sample(population, tournament_size)
        winners.append(min(tournament, key=lambda i: i[0]))
        setup.logger.debug('Holding tournament %s, picked winner ' +
                           'with fitness %s out of a max fitness of %s.',
                           i, min(tournament, key=lambda i: i[0]),
                           best_fitness(population))

    return winners


def crossover(graph, parents, children_per_generation, crossover_rate, setup):
    """
    Mixes the genome of 2 parents to create 2 children

    :param graph: the adjacency list of nodes to be colored
    :type: list[list[int]]
    :param parents: the previously selected solutions,
        used to create children
    :type: list[tuple(int,list[int])]
    :param children_per_generation: number of new children
        each generation
    :type: int
    :param crossover_rate: likelyhood for a neighboring node to
        be added to the crossover area
    :type: float

    :return: list of children resulting from crossover
    :rtype: list[tuple(None,list[int])]
    """
    children = []
    for parent_pair in ([parents[2*i], parents[2*i+1]]
                        for i in xrange(len(parents)/2)):
        crossover_point = random.randint(0, len(parent_pair[0][1])-1)
        visited = set()
        to_visit = [crossover_point]
        crossover_area = set([crossover_point])
        while len(to_visit) > 0:
            node = to_visit.pop()
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    if random.random() < crossover_rate:
                        crossover_area.add(neighbor)
                        to_visit.append(neighbor)

        setup.logger.debug('Performing crossover, crossover area: %s',
                           crossover_area)
        children.extend([
            (None, [
                (parent_pair[p][1][i] if i in crossover_area
                 else parent_pair[1-p][1][i])
                for i in xrange(len(parent_pair[0][1]))
            ])
            for p in xrange(2)
        ])
    return children


def mutation(population, mutation_rate, num_colors, setup):
    """
    Randomly mutate the state of a given node based on
        the given mutation rate

    :param population: the current potential graph coloring solutions
    :type: list[tuple(int,list[int])]
    :param mutation_rate: likelyhood for a node to mutate to
        a different random color
    :type: float
    :param num_colors: number of colors the program attemps to
        color the graph with
    :type: int

    :return: the population
    :rtype: list[tuple(int,list[int])]
    """
    solutions = [individual[1] for individual in population]
    for index, solution in enumerate(solutions):
        for node in solution:
            if random.random() <= mutation_rate:
                mutated = new_color(
                    population[index][1][node], num_colors
                )
                setup.logger.debug('Mutated a %s to a %s',
                                   population[index][1][node],
                                   mutated)
                population[index][1][node] = mutated
                population[index] = (None, population[index][1])
    return population


def new_color(old_color, num_colors):
    """
    Returns a random new color such that new color != old_color

    :param old_color: current color of a node
    :type: int
    :param num_colors: number of colors the program attemps to
        color the graph with
    :type: int

    :return: a new color
    :rtype: int
    """
    possible_colors = range(num_colors)
    possible_colors.remove(old_color)
    return random.choice(possible_colors)


def replacement(population, children):
    """
    Replaces the worst individuals in the population with new children
        such that the population size remains the same

    :param population: the current potential graph coloring solutions
    :type: list[tuple(int,list[int])]
    :param population: new children generated by crossover
    :type: list[tuple(int,list[int])]

    :return: the new population
    :rtype: list[tuple(int,list[int])]
    """
    population = sorted(population, key=lambda i: i[0])
    population = population[:len(population) - len(children)] + children
    return population


def stopping_condition(population):
    """
    Determines if a valid coloring has been achieved

    :param population: the population
    :type: list[tuple(int,list[int])]

    :return: if the program has reached a valid coloring
    :rtype: boolean
    """
    return best_fitness(population) == 0


def best_fitness(population):
    """
    Returns the best fitness currently within the population

    :param population: the population
    :type: list[tuple(int,list[int])]

    :return: best fitness within the population
    :rtype: int
    """
    return min(population, key=lambda i: i[0])[0]


def calculate_fitness(solution, graph):
    """
    Determines the fitness of a potential solution in the population

    :param solution: a potential solution
    :type: tuple(int, list[int])
    :param graph: the adjacency list of nodes to be colored
    :type: list[list[int]]

    :return: number of conflicts
    :rtype: int
    """

    conflicts = 0

    for node, adj_list in enumerate(graph):
        for neighbor in adj_list:
            if neighbor > node and solution[node] == solution[neighbor]:
                conflicts += 1

    return conflicts


def evaluate_population(population, graph, setup):
    """
    Determines the fitness of every potential solution in the population

    :param population: the population
    :type: list[tuple(int,list[int])]
    :param graph: the adjacency list of nodes to be colored
    :type: list[list[int]]
    """
    num_evaluations = 0
    for index, (fitness, coloring) in enumerate(population):
        if fitness is None:
            population[index] = (calculate_fitness(coloring, graph), coloring)
            num_evaluations += 1

    return num_evaluations


def run(graph, setup, params):
    """
    Executes the GA on specified graph, with specified parameters

    :param params: set of parameters used in running GA
        - :num_colors: number of colors the program attemps
              to color the graph with
          :type: int
        - :population_size: the number of potential solutions to generate
          :type: int
        - :mutation_rate: likelyhood of a given node to mutate
          :type: float
        - :tournament_size: size of the tournament to hold
          :type: int
        - :children_per_generation: number of children generated
              each generation
          :type: int
        - :crossover_rate: likelyhood of a node to be
              part of the crossover area
    """
    num_colors = params['colors']
    population_size = params['population_size']
    mutation_rate = params['mutation']
    tournament_size = params['tournament_size']
    children_per_generation = params['children_per_generation']
    crossover_rate = params['crossover_rate']

    if children_per_generation % 2 != 0:
        raise Exception("children_per_generation must be a multiple of 2")

    population = generate_initial_population(
        graph, population_size, num_colors
    )
    setup.logger.debug('Initializing population of size: %s', population_size)
    num_evaluations = evaluate_population(population, graph, setup)
    if setup.counter.increment(num_evaluations):
        yield best_fitness(population)

    while(not stopping_condition(population)):
        parents = tournament_selection(
            population, tournament_size, children_per_generation, setup
        )

        children = crossover(
            graph, parents, children_per_generation, crossover_rate, setup
        )
        population = replacement(population, children)
        population = mutation(population, mutation_rate, num_colors, setup)
        num_evaluations = evaluate_population(population, graph, setup)
        setup.logger.debug('Current best fitness: %s',
                           best_fitness(population))

        if setup.counter.increment(num_evaluations):
            yield best_fitness(population)
