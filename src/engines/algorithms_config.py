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
        The K-Means algorithm clusters data by trying to separate samples in n groups of equal variance, minimizing distance to the centers of clusters.
        This algorithm requires the number of clusters to be specified and works only on numeric data. It scales well to large numbers of samples and has been used across a large range of application areas in many different fields.
        The K-Means algorithm divides a set of samples into disjoint clusters, each described by the mean of the samples in the cluster. The means are commonly called the cluster “centroids”.
    """,
    "Gaussian Mixture Models": """
        A Gaussian mixture model is a probabilistic model that assumes all the data points are generated from a mixture of a finite number of Gaussian distributions with unknown parameters.
        This algorithm requires the number of clusters to be specified and works only on numeric data.
        One can think of mixture models as generalizing k-means clustering to incorporate information about the covariance structure of the data as well as the centers of the latent Gaussians.
    """,
    "Apriori": """
        Apriori Algorithm is a Machine Learning algorithm which is used to gain insight into the structured relationships between different items involved. The most prominent practical application of the algorithm is to recommend products based on the products already present in the user’s cart.
        This algorithm needs table in special formats. The columns are products and the rows are receipts. Values in table describe number of the product in the receipt.
    """,
    "Extra Trees": """
        The Extremely Randomized Trees is forest of the decision trees. Decision trees are a non-parametric supervised learning method used for classification. The goal is to create a model that predicts the value of a target variable by learning simple decision rules inferred from the data features.
        In Extra Trees create process is fully random. The random subset of candidate features is used in the split step and thresholds are drawn at random for each candidate feature and the best of these randomly-generated thresholds is picked as the splitting rule.
        This usually allows to reduce the variance of the model a bit more, at the expense of a slightly greater increase in bias.
    """,
}


def preprocess_description(description: str):
    return "\n".join([line.strip() for line in description.split("\n")]).strip()


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
