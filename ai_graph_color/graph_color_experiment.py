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

algorithm_modules = [
    backtracking,
    backtracking_mac,
    backtracking_forward_checking,
    genetic_algorithm,
    min_conflicts
]

local_limit = 5
global_limit = 500000
param_sets = [({'colors': i}, 'colors={}'.format(i)) for i in [3, 4]]


for problem_path in glob.iglob('problems/*'):
    problem_path = os.path.split(problem_path)[-1]
    problem_name = os.path.splitext(problem_path)[0]
    for param_set, param_name in param_sets:
        with open(
            'results/{}.{}.json'.format(problem_name, param_name), 'w'
        ) as output_file:
            print 'Running problem: {}'.format(problem_name)
            problem = problem_generator.read_graph_from_file(problem_path)
            json.dump(experiment.iterative(
                map(
                    lambda a: (a, param_set),
                    algorithm_modules
                ),
                problem,
                iteration_func,
                local_limit,
                global_limit
            ), output_file, indent=4)
