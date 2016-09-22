import setup
from algorithm import LimitedAlgorithm


def iterative(algorithms, problem, iteration_func, local_limit,
              global_limit=None):
    algorithm_runners = map(
        lambda m: LimitedAlgorithm(
            m[0], problem, setup.Evaluation(), m[1]
        ),
        algorithms
    )

    iteration_values = []
    iterations = 0
    iteration_num = 0
    last_completion = None
    completed_algorithms = set()

    while (not (last_completion is not None and
                iteration_num - last_completion > local_limit) and
           not (global_limit is not None and iterations > global_limit)):
        iterations = iteration_func(iteration_num)
        iteration_values.append(iterations)

        for index, runner in enumerate(algorithm_runners):
            runner.set_limit(iterations)

            if (runner.next_output() is None and
                    index not in completed_algorithms):
                completed_algorithms.add(index)
                last_completion = iteration_num

        iteration_num += 1

    return {
        'iterations': iteration_values,
        'history': [runner.output_history for runner in algorithm_runners]
    }
