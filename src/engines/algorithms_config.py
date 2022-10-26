from typing import Dict, List
from enum import Enum
from dataclasses import dataclass

from algorithms import Algorithm
from algorithms.clustering import KMeans, GMM
from algorithms.associations import APriori
from algorithms.classification import ExtraTrees
from widgets.steps_widgets import AlgorithmStepsVisualization, APrioriStepsVisualization, KMeansStepsVisualization, \
    ExtraTreesStepsVisualization, GMMStepsVisualization
from widgets.results_widgets import KMeansResultsWidget, ExtraTreesResultsWidget, AlgorithmResultsWidget, \
    APrioriResultsWidget, GMMResultsWidget
from widgets.options_widgets import KMeansOptions, ExtraTreesOptions, AlgorithmOptions, AssociationRulesOptions, \
    GMMOptions


class AlgorithmTechniques(Enum):
    CLUSTERING = "clustering"
    ASSOCIATIONS = "associations"
    CLASSIFICATION = "classification"

    @classmethod
    def list(cls) -> List[str]:
        return list(map(lambda e: e.value, cls))


@dataclass
class AlgorithmClasses:
    algorithm: Algorithm.__class__
    options: AlgorithmOptions.__class__
    steps_visualization: AlgorithmStepsVisualization.__class__
    result_widget: AlgorithmResultsWidget.__class__


ALGORITHMS_INFO: Dict[str, Dict[str, AlgorithmClasses]] = {
    AlgorithmTechniques.CLUSTERING.value: {
        'K-Means': AlgorithmClasses(algorithm=KMeans, options=KMeansOptions,
                                    steps_visualization=KMeansStepsVisualization,
                                    result_widget=KMeansResultsWidget),
        'Gaussian Mixture Models': AlgorithmClasses(algorithm=GMM, options=GMMOptions,
                                                    steps_visualization=GMMStepsVisualization,
                                                    result_widget=GMMResultsWidget)
    },
    AlgorithmTechniques.ASSOCIATIONS.value: {
        'A-priori': AlgorithmClasses(algorithm=APriori, options=AssociationRulesOptions,
                                     steps_visualization=APrioriStepsVisualization,
                                     result_widget=APrioriResultsWidget)
    },
    AlgorithmTechniques.CLASSIFICATION.value: {
        'Extra Trees': AlgorithmClasses(algorithm=ExtraTrees, options=ExtraTreesOptions,
                                        steps_visualization=ExtraTreesStepsVisualization,
                                        result_widget=ExtraTreesResultsWidget)
    }
}
