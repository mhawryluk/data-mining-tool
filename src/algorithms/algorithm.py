from typing import List
from abc import abstractmethod


class Algorithm:
    """
        Abstract class of algorithm
    """

    def __init__(self):
        pass

    @abstractmethod
    def run(self, with_steps: bool):
        """
            Run algorithm and return result for class AlgorithmResultsWidget
            If with_steps is true, saves steps of algorithm creation
        """
        pass

    @abstractmethod
    def get_steps(self) -> List:
        """
            Return list of steps for visualization by AlgorithmStepsVisualization
        """
        pass
