import setup
from algorithm import LimitedAlgorithm


def iterative(algorithms, problem, iteration_func, local_limit,
              global_limit=None):
    """
    Runs the RIS method on a list of algorithms.

    In short, in a round-robin fashion give a number of
    iterations to each algorithm determined by the interation
    function, until one of the following happens:
    - it has been a certain number of rounds since an algorithm
      has terminated
    - we pass a certain number of overall iterations
    - all of the algorithms have terminated

    Then, at the end, return the results including the
    intermediate scores of each algorithm before it terminates
    (if that function is provided by the algorithm)

    :param algorithms: a list of algorithms paired with their
        parameters
    :type algorithms: list[tuple(module, map)]
    :param problem: the problem to pass to the algorithm
    :type problem: object
    :param iteration_func: the iteration function for RIS
    :type iteration_func: function(int) -> int
    :param local_limit: the number of iterations that may pass
        after the last successful termination
    :type local_limit: int
    :rtype map<string, object>
    :return the results of the run of RIS
    """
    algorithm_runners = [
        LimitedAlgorithm(
            algorithm, problem, setup.Evaluation(), params
        )
        for algorithm, params in algorithms
    ]

    iteration_values = []
    iterations = 0
    iteration_num = 0
    last_completion = None
    completed_algorithms = set()

    # Only loop if all of the following are true:
    # (1) we haven't passed the local iteration limit
    #     since the last algorithm terminated.
    # (2) we haven't passed the gloabl iteration limit
    #     (if there is one)
    # (3) there are still unfinished algorithms
    while (not (last_completion is not None and
                iteration_num - last_completion > local_limit) and
           not (global_limit is not None and iterations > global_limit) and
           (len(completed_algorithms) < len(algorithm_runners))):
        iterations = iteration_func(iteration_num)
        iteration_values.append(iterations)

        for index, runner in enumerate(algorithm_runners):
            if runner.setup.counter.counter < iterations:
                runner.set_limit(iterations)
                runner.next_output()

                if (runner.setup.counter.counter < iterations and
                        index not in completed_algorithms):
                    completed_algorithms.add(index)
                    last_completion = iteration_num

        iteration_num += 1

    return {
        'iterations': iteration_values,
        'history': [
            [runner.output_history, runner.output_iterations, runner.setup.counter.counter]
            for runner in algorithm_runners
        ]
    }
