from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

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
    algorithm: Algorithm.__class__
    options: AlgorithmOptions.__class__
    steps_visualization: AlgorithmStepsVisualization.__class__
    result_widget: AlgorithmResultsWidget.__class__
    description: str = ""


descriptions = {
    "K-Means": """
        Some description.
    """,
    "Gaussian Mixture Models": "",
    "Apriori": "",
    "Extra Trees": "",
}


def preprocess_description(description: str):
    return "\n".join([line.strip() for line in description.split("\n")])


ALGORITHMS_INFO: Dict[str, Dict[str, AlgorithmConfig]] = {
    AlgorithmTechniques.CLUSTERING.value: {
        "K-Means": AlgorithmConfig(
            algorithm=KMeans,
            options=KMeansOptions,
            steps_visualization=KMeansStepsVisualization,
            result_widget=KMeansResultsWidget,
            description=preprocess_description(descriptions["K-Means"]),
        ),
        "Gaussian Mixture Models": AlgorithmConfig(
            algorithm=GMM,
            options=GMMOptions,
            steps_visualization=GMMStepsVisualization,
            result_widget=GMMResultsWidget,
            description=preprocess_description(descriptions["Gaussian Mixture Models"]),
        ),
    },
    AlgorithmTechniques.ASSOCIATIONS.value: {
        "Apriori": AlgorithmConfig(
            algorithm=APriori,
            options=AssociationRulesOptions,
            steps_visualization=APrioriStepsVisualization,
            result_widget=APrioriResultsWidget,
            description=preprocess_description(descriptions["Apriori"]),
        )
    },
    AlgorithmTechniques.CLASSIFICATION.value: {
        "Extra Trees": AlgorithmConfig(
            algorithm=ExtraTrees,
            options=ExtraTreesOptions,
            steps_visualization=ExtraTreesStepsVisualization,
            result_widget=ExtraTreesResultsWidget,
            description=preprocess_description(descriptions["Extra Trees"]),
        )
    },
}
