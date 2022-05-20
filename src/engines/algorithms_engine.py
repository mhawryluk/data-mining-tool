from state import State
from algorithms.clustering import KMeans
from visualization.clustering import KMeansStepsVisualization, KMeansResultsWidget


class AlgorithmsEngine:
    def __init__(self, state: State):
        self.state = state

        self.algorithms_options = {
            'clustering': {
                'K-Means': (KMeans, KMeansStepsVisualization, KMeansResultsWidget),
                'DBSCAN': None,
                'Partition Around Medoids': None,
                'Gaussian Mixture Models': None,
                'Agglomerative clustering': None,
                'Divisive clustering': None
            },
            'associations': {
                'A-priori': None,
                'A-prioriTID': None,
                'FP-Growth': None
            },
            'classification': {
                'KNN': None,
                'Decision Tree': None,
                'SVM': None
            }
        }

    def run(self, technique, algorithm, will_be_visualized, is_animation, **kwargs):
        chosen_alg = self.algorithms_options[technique][algorithm]
        if chosen_alg is None:
            return
        alg = chosen_alg[0](self.state.imported_data, **kwargs)

        result = alg.run(will_be_visualized)

        if will_be_visualized:
            steps = alg.get_steps()
            self.state.steps_visualization = chosen_alg[1](self.state.imported_data, steps, is_animation)
        else:
            self.state.steps_visualization = None

        # create a widget for the results
        if not self.state.algorithm_results.get(technique):
            self.state.algorithm_results[technique] = {}
        if not self.state.algorithm_results[technique].get(algorithm):
            self.state.algorithm_results[technique][algorithm] = []
        self.state.algorithm_results[technique][algorithm].append(chosen_alg[2](self.state.imported_data, *result))

    def get_maximum_clusters(self) -> int:
        if self.state.imported_data is None:
            return 100
        return self.state.imported_data.shape[0]
