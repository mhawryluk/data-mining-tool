from state import State
from algorithms.clustering import KMeans
from visualization.clustering import KMeansStepsVisualization


class AlgorithmsEngine:
    def __init__(self, state: State):
        self.state = state
        self.steps_vis = None

    def run(self, technique, algorithm, **kwargs):
        print(technique, algorithm)
        alg = KMeans(self.state.imported_data, **kwargs)
        steps = alg.get_steps()
        self.steps_vis = KMeansStepsVisualization(self.state.imported_data, steps)
