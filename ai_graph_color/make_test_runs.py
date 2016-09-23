import problem_generator
import runner
from algorithms import backtracking
from algorithms import backtracking_mac
from algorithms import backtracking_forward_checking
from algorithms import genetic_algorithm
from algorithms import min_conflicts

algorithms = [
    backtracking,
    backtracking_mac,
    backtracking_forward_checking,
    genetic_algorithm,
    min_conflicts
]

problem = problem_generator.generate_graph(25)

for algorithm in algorithms:
    runner.test_run(
        algorithm,
        problem,
        'testruns/{}.txt'.format(algorithm.__name__.split('.')[-1]),
        {'colors': 4},
        10000
    )
