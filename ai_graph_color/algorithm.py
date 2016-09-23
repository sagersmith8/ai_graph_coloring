class LimitedAlgorithm:
    """
    Handles the direct running of algorithms as generators and saving
    their intermediate results and setup.
    """
    def __init__(self, module, problem, setup, params):
        """
        :param module: the module of the algorithm to run
        :type module: module
        :param problem: the problem to run with the algorithm
        :type problem: object
        :param setup: the pre-setup objects useful for running
            any algorithm
        :type setup: one of {Evaluation, TestRun}
        :param params: the parameters to the algorithm
        :type params: map<str, object>
        """
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
        """
        Get the next intermediate output from the algorithm, or its
        final output if it is done.
        """
        try:
            output = self.runner.next()
        except StopIteration:
            output = None

        self.output_history.append(output)
        return output
