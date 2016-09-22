class Counter:
    def __init__(self):
        self.limit = None
        self.counter = 0

    def increment(self):
        self.counter += 1

        return self.limit is not None and self.counter >= self.limit
