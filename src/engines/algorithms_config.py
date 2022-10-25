from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel

from algorithms import Algorithm
from algorithms.clustering import KMeans
from algorithms.classification import ExtraTrees
from visualization import AlgorithmStepsVisualization
from visualization.clustering import KMeansStepsVisualization
from visualization.classification import ExtraTreesStepsVisualization
from widgets.results_widgets import KMeansResultsWidget, ExtraTreesResultsWidget, AlgorithmResultsWidget
from widgets.options_widgets import KMeansOptions, ExtraTreesOptions, AlgorithmOptions


class AlgorithmTechniques(Enum):
    CLUSTERING = "clustering"
    ASSOCIATIONS = "associations"
    CLASSIFICATION = "classification"

    @classmethod
    def list(cls) -> List[str]:
        return list(map(lambda e: e.value, cls))


class AlgorithmClasses(BaseModel):
    algorithm: Algorithm
    options: AlgorithmOptions
    steps_visualization: AlgorithmStepsVisualization
    result_widget: AlgorithmResultsWidget


ALGORITHMS_INFO: Dict[AlgorithmTechniques.list(), Dict[str, Optional[AlgorithmClasses]]] = {
    AlgorithmTechniques.CLUSTERING.value: {
        'K-Means': AlgorithmClasses(KMeans, KMeansOptions, KMeansStepsVisualization, KMeansResultsWidget),
        'Gaussian Mixture Models': None,
    },
    AlgorithmTechniques.ASSOCIATIONS.value: {
        'A-priori': None
    },
    AlgorithmTechniques.CLASSIFICATION.value: {
        'Extra Trees': AlgorithmClasses(ExtraTrees, ExtraTreesOptions, ExtraTreesStepsVisualization, ExtraTreesResultsWidget)
    }
}
