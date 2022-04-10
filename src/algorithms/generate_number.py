import numpy as np


class NumberGenerator:

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def get_number(self) -> float:
        value = np.random.random() * (self.end - self.start) + self.start
        return round(value, 2)
