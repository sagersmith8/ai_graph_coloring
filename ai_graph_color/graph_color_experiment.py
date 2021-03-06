"""
Run final graph coloring experiments for all of the algorithms.
"""

import glob
import json
import os

import experiment
import problem_generator
from algorithms import test


def iteration_func(i):
    return 100 + 2**i

algorithm_modules = [test]
local_limit = 5
global_limit = 100000
param_sets = [({'colors': i}, '{}.colors'.format(i)) for i in [3, 4]]


for problem_path in glob.iglob('problems/*'):
    problem_path = os.path.split(problem_path)[1]
    problem_name = os.path.splitext(problem_path)[0]
    for param_set, param_name in param_sets:
        with open(
            'results/{}_{}.json'.format(problem_name, param_name), 'w'
        ) as output_file:
            print problem_path
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
