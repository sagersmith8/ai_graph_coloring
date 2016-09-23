class Counter:
    """
    Counts up to a limit, and signals if that limit is reached.
    """
    def __init__(self):
        self.limit = None
        self.counter = 0

    def increment(self, amt=1):
        self.counter += amt

        return self.limit is not None and self.counter >= self.limit
