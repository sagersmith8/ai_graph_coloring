import logging
from counter import Counter


class TestRun:
    """
    A setup that allows logging to a file and counting.
    """
    def __init__(self, output_path):
        self.logger = logging.getLogger(output_path)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(output_path)
        file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)

        self.counter = Counter()


class Evaluation:
    """
    A setup that only allows counting.
    """
    def __init__(self):
        self.logger = logging.getLogger('none')
        self.logger.setLevel(logging.CRITICAL)

        self.counter = Counter()
