"""
Run final graph coloring experiments for all of the algorithms.
"""

import glob
import json
import os

import experiment
import problem_generator
from algorithms import backtracking
from algorithms import backtracking_mac
from algorithms import backtracking_forward_checking
from algorithms import genetic_algorithm
from algorithms import min_conflicts


def iteration_func(i):
    return 100 + 2**i

params = [
    {
        'tournament_size': 20,
    }
]

params += [
    {
        'tournament_size': i,
    } for i in xrange(50, 550, 50)
]

params = params*10

algorithms = [
    (genetic_algorithm, param) for param in params
]


local_limit = 5
global_limit = 100000
param_sets = [({'colors': i}, 'colors={}'.format(i)) for i in [3, 4]]


for problem_path in glob.iglob('problems/*'):
    problem_path = os.path.split(problem_path)[-1]
    problem_name = os.path.splitext(problem_path)[0]
    for param_set, param_name in param_sets:
        with open(
            'tuning/{}.{}.json'.format(problem_name, param_name), 'w'
        ) as output_file:
            print 'Running problem: {}'.format(problem_name)
            problem = problem_generator.read_graph_from_file(problem_path)
            for algorithm in algorithms:
                algorithm[1].update(param_set)
            json.dump(experiment.iterative(
                algorithms,
                problem,
                iteration_func,
                local_limit,
                global_limit
            ), output_file, indent=4)
