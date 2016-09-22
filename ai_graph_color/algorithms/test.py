import random

params = {'multiplier': 3}


def run(problem, setup, params):
    setup.logger.debug('Starting Problem: %s', problem)

    multiplier = params['multiplier']
    best = None
    while best != problem:
        value = random.randint(0, multiplier*problem + 1)
        setup.logger.debug('Try Value: %s', value)

        if best is None or abs(problem - value) < abs(problem - best):
            best = value
            setup.logger.debug('New Best Value: %s', best)

        if best != problem and setup.counter.increment():
            setup.logger.debug('Reached iteration limit')
            yield best
    yield best
