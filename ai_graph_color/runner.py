import setup
from algorithm import LimitedAlgorithm


def evaluate(algorithm, problem, params=None, iteration_limit=None):
    execute(
        algorithm,
        problem,
        setup.Evaluation(),
        params,
        iteration_limit
    )


def test_run(algorithm, problem, test_run_path, params=None,
             iteration_limit=None):
    execute(
        algorithm,
        problem,
        setup.TestRun(test_run_path),
        params,
        iteration_limit
    )


def execute(algorithm, problem, setup, params, iteration_limit):
    runner = LimitedAlgorithm(algorithm, problem, setup, params)
    runner.set_limit(iteration_limit)

    return runner.next_output(), setup.counter.counter
