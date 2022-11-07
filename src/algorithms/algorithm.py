from typing import List
from abc import abstractmethod


class Algorithm:
    """
        Abstract class of algorithm
    """

    @abstractmethod
    def run(self, with_steps: bool):
        """
            Run algorithm and return result for class AlgorithmResultsWidget
            If with_steps is true, saves steps of algorithm creation
        """
        raise NotImplementedError

    @abstractmethod
    def get_steps(self) -> List:
        """
            Return list of steps for visualization by AlgorithmStepsVisualization
        """
        raise NotImplementedError
