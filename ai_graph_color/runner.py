import setup
from algorithm import LimitedAlgorithm


def evaluate(algorithm, problem, params=None, iteration_limit=None):
    """
    Execute an algorithm module with an evaluation setup.
    """
    execute(
        algorithm,
        problem,
        setup.Evaluation(),
        params,
        iteration_limit
    )


def test_run(algorithm, problem, test_run_path, params=None,
             iteration_limit=None):
    """
    Execute an algorithm module with an test run setup.
    """
    execute(
        algorithm,
        problem,
        setup.TestRun(test_run_path),
        params,
        iteration_limit
    )


def execute(algorithm, problem, setup, params, iteration_limit):
    """
    Run a given algorithm on a particular problem and setup with
    a particular set of params, up until a particular iteration
    limit.

    Return the result from the algorithm and which iteration it
    terminated on.

    :param algorithm: the algorithm module to run
    :type algorithm: module
    :param problem: the problem to run
    :type problem: object
    :param params: the params to pass to the algorithm
    :type params: map<string, object>
    :iteration_limit: the maximum number of iterations for the run
    :type iteration_limit: int
    :rtype: tuple(object, int)
    :return: the algorithm's result and the iteration it ended on
    """
    runner = LimitedAlgorithm(algorithm, problem, setup, params)
    runner.set_limit(iteration_limit)

    return runner.next_output(), setup.counter.counter
