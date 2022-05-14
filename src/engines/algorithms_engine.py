from state import State
from algorithms.clustering import KMeans
from visualization.clustering import KMeansStepsVisualization


class AlgorithmsEngine:
    def __init__(self, state: State):
        self.state = state

        self.algorithms_options = {
            'clustering': {
                'K-Means': KMeans
            },
            'associations': {
                'algorithm': None
            }
        }

    def run(self, technique, algorithm, will_be_visualized, animation_speed, **kwargs):
        chosen_alg = self.algorithms_options[technique][algorithm]
        if chosen_alg is None:
            return
        alg = chosen_alg(self.state.imported_data, **kwargs)
        alg.run(will_be_visualized)
        if will_be_visualized:
            steps = alg.get_steps()
            self.state.steps_visualization = KMeansStepsVisualization(self.state.imported_data, steps, animation_speed)
        else:
            self.state.steps_visualization = None

    def get_maximum_clusters(self) -> int:
        if self.state.imported_data is None:
            return 100
        return self.state.imported_data.shape[0]
