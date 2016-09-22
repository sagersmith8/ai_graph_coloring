class LimitedAlgorithm:
    def __init__(self, module, problem, setup, params):
        self.setup = setup
        self.problem = problem
        self.module = module

        self.params = self.module.params.copy()
        self.params.update(params)

        self.runner = module.run(self.problem, self.setup, self.params)

        self.output_history = []

    def set_limit(self, limit):
        self.setup.counter.limit = limit

    def next_output(self):
        try:
            output = self.runner.next()
        except:
            output = None

        self.output_history.append(output)
        return output
