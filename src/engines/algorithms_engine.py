from typing import List

from state import State
from widgets.options_widgets import AlgorithmOptions

from .algorithms_config import ALGORITHMS_INFO, AlgorithmTechniques


class AlgorithmsEngine:
    def __init__(self, state: State):
        self.state = state

        # init options widgets
        self.options = {}
        for technique, info in ALGORITHMS_INFO.items():
            self.options[technique] = {
                algorithm: classes.options() for algorithm, classes in info.items()
            }

    def run(
        self, technique, algorithm, will_be_visualized, is_animation, **kwargs
    ) -> bool:
        chosen_alg = ALGORITHMS_INFO[technique][algorithm]

        alg = chosen_alg.algorithm(self.state.imported_data, **kwargs)

        result = alg.run(will_be_visualized)

        if result is None:
            return False

        if will_be_visualized:
            steps = alg.get_steps()
            self.state.steps_visualization = chosen_alg.steps_visualization(
                self.state.imported_data, steps, is_animation
            )
        else:
            self.state.steps_visualization = None

        # create a widget for the results
        self.state.last_algorithm = (technique, algorithm)
        if not self.state.algorithm_results_widgets.get(technique):
            self.state.algorithm_results_widgets[technique] = {}
        if not self.state.algorithm_results_widgets[technique].get(algorithm):
            self.state.algorithm_results_widgets[technique][algorithm] = []
        self.state.algorithm_results_widgets[technique][algorithm].append(
            chosen_alg.result_widget(self.state.raw_data, *result, options=kwargs)
        )
        return True

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

    def get_option_widget(
        self, technique: AlgorithmTechniques.list(), algorithm: str
    ) -> AlgorithmOptions:
        return self.options[technique][algorithm]

    def update_options(self):
        clusters = min(self.get_maximum_clusters(), 100)
        self.options[AlgorithmTechniques.CLUSTERING.value]["K-Means"].set_max_clusters(
            clusters
        )
        columns = self.get_columns()
        self.options[AlgorithmTechniques.ASSOCIATIONS.value][
            "Apriori"
        ].set_columns_options(columns)
        self.options[AlgorithmTechniques.CLASSIFICATION.value][
            "Extra Trees"
        ].set_values(columns)
        self.options[AlgorithmTechniques.CLUSTERING.value][
            "Gaussian Mixture Models"
        ].set_max_clusters(clusters)

    def get_algorithm_description(
        self, technique: AlgorithmTechniques.list(), algorithm: str
    ) -> str:
        return ALGORITHMS_INFO[technique][algorithm].description
