from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Type

from algorithms import Algorithm
from algorithms.associations import APriori
from algorithms.classification import ExtraTrees
from algorithms.clustering import GMM, KMeans
from widgets.options_widgets import (
    AlgorithmOptions,
    AssociationRulesOptions,
    ExtraTreesOptions,
    GMMOptions,
    KMeansOptions,
)
from widgets.results_widgets import (
    AlgorithmResultsWidget,
    APrioriResultsWidget,
    ExtraTreesResultsWidget,
    GMMResultsWidget,
    KMeansResultsWidget,
)
from widgets.steps_widgets import (
    AlgorithmStepsVisualization,
    APrioriStepsVisualization,
    ExtraTreesStepsVisualization,
    GMMStepsVisualization,
    KMeansStepsVisualization,
)


class AlgorithmTechniques(Enum):
    CLUSTERING = "clustering"
    ASSOCIATIONS = "associations"
    CLASSIFICATION = "classification"

    @classmethod
    def list(cls) -> List[str]:
        return list(map(lambda e: e.value, cls))


@dataclass
class AlgorithmConfig:
    algorithm: Type[Algorithm]
    options: Type[AlgorithmOptions]
    steps_visualization: Type[AlgorithmStepsVisualization]
    result_widget: Type[AlgorithmResultsWidget]


ALGORITHMS_INFO: Dict[str, Dict[str, AlgorithmConfig]] = {
    AlgorithmTechniques.CLUSTERING.value: {
        "K-Means": AlgorithmConfig(
            algorithm=KMeans,
            options=KMeansOptions,
            steps_visualization=KMeansStepsVisualization,
            result_widget=KMeansResultsWidget,
        ),
        "Gaussian Mixture Models": AlgorithmConfig(
            algorithm=GMM,
            options=GMMOptions,
            steps_visualization=GMMStepsVisualization,
            result_widget=GMMResultsWidget,
        ),
    },
    AlgorithmTechniques.ASSOCIATIONS.value: {
        "Apriori": AlgorithmConfig(
            algorithm=APriori,
            options=AssociationRulesOptions,
            steps_visualization=APrioriStepsVisualization,
            result_widget=APrioriResultsWidget,
        )
    },
    AlgorithmTechniques.CLASSIFICATION.value: {
        "Extra Trees": AlgorithmConfig(
            algorithm=ExtraTrees,
            options=ExtraTreesOptions,
            steps_visualization=ExtraTreesStepsVisualization,
            result_widget=ExtraTreesResultsWidget,
        )
    },
}
