from algorithms.associations import APriori
from algorithms.classification import ExtraTrees
from algorithms.clustering import KMeans, GMM
from state import State
from visualization.associations import APrioriStepsVisualization
from visualization.clustering import KMeansStepsVisualization, GMMStepsVisualization
from visualization.classification import ExtraTreesStepsVisualization
from widgets.results_widgets import KMeansResultsWidget, ExtraTreesResultsWidget, APrioriResultsWidget, KMeansResultsWidget, GMMResultsWidget


class AlgorithmsEngine:
    def __init__(self, state: State):
        self.state = state

        self.algorithms_options = {
            'clustering': {
                'K-Means': (KMeans, KMeansStepsVisualization, KMeansResultsWidget),
                'DBSCAN': None,
                'Partition Around Medoids': None,
                'Gaussian Mixture Models': (GMM, GMMStepsVisualization, GMMResultsWidget),
                'Agglomerative clustering': None,
                'Divisive clustering': None
            },
            'associations': {
                'A-priori': (APriori, APrioriStepsVisualization, APrioriResultsWidget),
                'A-prioriTID': None,
                'FP-Growth': None
            },
            'classification': {
                'KNN': None,
                'Extra Trees': (ExtraTrees, ExtraTreesStepsVisualization, ExtraTreesResultsWidget),
                'SVM': None
            }
        }

    def run(self, technique, algorithm, will_be_visualized, is_animation, **kwargs):
        chosen_alg = self.algorithms_options[technique][algorithm]
        if chosen_alg is None:
            return
        alg = chosen_alg[0](self.state.imported_data, **kwargs)

        result = alg.run(will_be_visualized)

        if result is None:
            return

        if will_be_visualized:
            steps = alg.get_steps()
            self.state.steps_visualization = chosen_alg[1](self.state.imported_data, steps, is_animation)
        else:
            self.state.steps_visualization = None

        # create a widget for the results
        if not self.state.algorithm_results_widgets.get(technique):
            self.state.algorithm_results_widgets[technique] = {}
        if not self.state.algorithm_results_widgets[technique].get(algorithm):
            self.state.algorithm_results_widgets[technique][algorithm] = []
        self.state.algorithm_results_widgets[technique][algorithm].append(chosen_alg[2](self.state.raw_data, *result,
                                                                                        options=kwargs))

    def get_maximum_clusters(self) -> int:
        if self.state.imported_data is None:
            return 100
        return self.state.imported_data.shape[0]

    def get_columns(self) -> list:
        return list(self.state.imported_data.columns)
