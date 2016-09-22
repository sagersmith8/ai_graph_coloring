"""
This file will use a genetic algorithm to solve graph coloring
"""
import random
import itertools


def generate_initial_population(graph, population_size, num_colors):
    colors = range(num_colors)

    population = []

    for _ in xrange(population_size):
        choices = [random.choice(colors) for i in xrange(len(graph))]
        population.append((fitness(choices), choices))

    return population


def tournament_selection(population, tournament_size, children_per_generation):
    winners = []
    for _ in range(children_per_generation):
        tournament = random.sample(population, tournament_size)
        winners.append(max(tournament, key=lambda i:i[0]))

    return winners
        

def crossover(parents):
    pass

def mutation(mutation_rate):
    pass
    
def replacement():
    pass
    
def stopping_condition():
    pass

def evaluate_population(population):
    for index, (fitness, coloring) in enumerate(population):
        if fitness == None:
            population[index] = (calculate_fitness(coloring), coloring)


def run(graph, params, setup):
    num_colors = params['colors']
    population_size = params['population_size']
    mutation_rate = params['mutation']
    tournament_size = params['tournament_size']
    children_per_generation = params['children_per_generation']
    
    population = generate_initial_population(graph, population_size, num_colors)
    evaluate_population(population)

    while(not stopping_condition()):
        parents = tournament_selection(population, tournament_size, number_of_winners, children_per_generation)
        children = crossover(parents)
        population = replace(population, children)
        population = mutation(mutation_rate)
        evaluate_population(population)
        
    
