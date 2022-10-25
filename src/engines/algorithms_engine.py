from state import State
from .algorithms_config import ALGORITHMS_INFO, AlgorithmTechniques
from typing import List
from widgets.options_widgets import AlgorithmOptions


class AlgorithmsEngine:
    def __init__(self, state: State):
        self.state = state

    def run(self, technique, algorithm, will_be_visualized, is_animation, **kwargs):
        chosen_alg = ALGORITHMS_INFO[technique][algorithm]

        alg = chosen_alg.algorithm(self.state.imported_data, **kwargs)

        result = alg.run(will_be_visualized)

        if result is None:
            return

        if will_be_visualized:
            steps = alg.get_steps()
            self.state.steps_visualization = chosen_alg.steps_visualization(self.state.imported_data, steps,
                                                                            is_animation)
        else:
            self.state.steps_visualization = None

        # create a widget for the results
        if not self.state.algorithm_results_widgets.get(technique):
            self.state.algorithm_results_widgets[technique] = {}
        if not self.state.algorithm_results_widgets[technique].get(algorithm):
            self.state.algorithm_results_widgets[technique][algorithm] = []
        self.state.algorithm_results_widgets[technique][algorithm].append(chosen_alg.result_widget(self.state.raw_data,
                                                                                                   *result,
                                                                                                   options=kwargs))

    def get_maximum_clusters(self) -> int:
        if self.state.imported_data is None:
            return 100
        return self.state.imported_data.shape[0]

    def get_columns(self) -> List:
        return list(self.state.imported_data.columns)

    @staticmethod
    def get_all_techniques() -> List:
        return AlgorithmTechniques.list()

    @staticmethod
    def get_algorithms_for_techniques(technique: AlgorithmTechniques.list()) -> List:
        return list(ALGORITHMS_INFO[technique].keys())

    @staticmethod
    def get_option_widget(technique: AlgorithmTechniques.list(), algorithm: str) -> AlgorithmOptions:
        return ALGORITHMS_INFO[technique][algorithm].options

    def update_options(self):
        clusters = min(self.get_maximum_clusters(), 100)
        ALGORITHMS_INFO[AlgorithmTechniques.CLUSTERING.value]["K-Means"].options.set_max_clusters(clusters)
        columns = self.get_columns()
        ALGORITHMS_INFO[AlgorithmTechniques.ASSOCIATIONS.value]["A-priori"].options.set_columns_options(columns)
        ALGORITHMS_INFO[AlgorithmTechniques.CLASSIFICATION.value]["Extra Trees"].options.set_values(columns)
        ALGORITHMS_INFO[AlgorithmTechniques.CLUSTERING.value]["Gaussian Mixture Models"].options\
            .set_max_clusters(clusters)
