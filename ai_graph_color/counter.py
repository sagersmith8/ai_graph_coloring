class Counter:
    """
    Counts up to a limit, and signals if that limit is reached.
    """
    def __init__(self):
        self.limit = None
        self.counter = 0

    def increment(self):
        self.counter += 1

        return self.limit is not None and self.counter >= self.limit
