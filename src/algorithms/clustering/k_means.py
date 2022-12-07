from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from algorithms import Algorithm

from .metrics import davies_bouldin_score, dunn_score, silhouette_score

init_types = ["random", "kmeans++"]


class KMeans(Algorithm):
    def __init__(
        self,
        data: pd.DataFrame,
        num_clusters: int,
        metrics: int = 1,
        iterations: Optional[int] = None,
        repeats: int = 1,
        init_type: init_types = "random",
    ):
        self.num_clusters = num_clusters
        self.metrics = metrics
        self.max_iterations = iterations
        self.repeats = repeats
        if init_type not in init_types:
            raise TypeError(f"{init_type} is invalid value of init_type parameter")
        self.step_counter = 0
        self.data = data.select_dtypes(include=["number"])
        self.centroids = []
        self.labels = np.zeros(self.data.shape[0], dtype=int)
        self.saved_steps = []
        self.get_centroids = {
            "random": self.random_centroids,
            "kmeans++": self.kmeanspp_centroids,
        }[init_type]

    def distance(
        self, vector_x: Union[Tuple, List], vector_y: Union[Tuple, List]
    ) -> float:
        diff = np.abs(np.array(vector_x) - np.array(vector_y))
        return (np.sum(diff**self.metrics)) ** (1 / self.metrics)

    def random_centroids(self) -> List[Tuple]:
        return list(
            self.data.sample(self.num_clusters, replace=False).itertuples(index=False)
        )

    def kmeanspp_centroids(self) -> List[Tuple]:
        centroids = list(self.data.sample(1, replace=False).itertuples(index=False))
        for _ in range(self.num_clusters - 1):
            centroid = None
            max_dis = 0
            for row in self.data.itertuples(index=False):
                min_dis = np.inf
                for cent in centroids:
                    dis = self.distance(row, cent)
                    if dis < min_dis:
                        min_dis = dis
                if min_dis > max_dis:
                    max_dis = min_dis
                    centroid = row
            centroids.append(centroid)
        return centroids

    def mark_labels(self) -> int:
        count = 0
        for i, row in enumerate(self.data.itertuples(index=False)):
            min_dis = np.inf
            m = 0
            for j, centroid in enumerate(self.centroids):
                dis = self.distance(row, centroid)
                if dis < min_dis:
                    min_dis = dis
                    m = j
            if self.labels[i] != m:
                count += 1
            self.labels[i] = m
        return count

    @staticmethod
    def mean(group: pd.DataFrame) -> Tuple:
        return tuple(group.mean(axis="index"))

    def update_centroids(self):
        for i, centroid in enumerate(self.centroids):
            group = self.data[self.labels == i]
            self.centroids[i] = self.mean(group)

    def step(self) -> bool:
        self.update_centroids()
        count = self.mark_labels()
        if count == 0:
            return False
        return True

    def update_metrics(self, labels):
        self.metrics_info = {}
        d_index = dunn_score(self.data, labels)
        db_index = davies_bouldin_score(self.data, labels)
        s_index = silhouette_score(self.data, labels)
        self.metrics_info["Dunn index (higher = better)"] = round(d_index, 3)
        self.metrics_info["Davies Bouldin index (lower = better)"] = round(db_index, 3)
        self.metrics_info["Silhouette Coefficient (higher = better)"] = round(
            s_index, 3
        )

    def check_solution(self, labels):
        """dunn index"""
        return dunn_score(self.data, labels, self.distance)

    def run(self, with_steps) -> Tuple[np.ndarray, pd.DataFrame]:
        runner = (
            self.run_with_saving_steps if with_steps else self.run_without_saving_steps
        )
        if self.repeats == 1:
            solution = runner()
            self.update_metrics(solution[0])
            return solution[0], pd.DataFrame(solution[1], columns=self.data.columns)
        best_value = 0
        solution = None
        steps = None
        for _ in range(self.repeats):
            result = runner()
            value = self.check_solution(result[0])
            if value > best_value:
                solution = (result[0].copy(), result[1].copy())
                steps = [(step[0].copy(), step[1].copy()) for step in self.saved_steps]
                best_value = value
        self.saved_steps = steps
        self.update_metrics(solution[0])
        return solution[0], pd.DataFrame(solution[1], columns=self.data.columns)

    def run_with_saving_steps(self) -> Tuple[np.ndarray, List[Tuple]]:
        steps = 0
        self.saved_steps = []
        self.centroids = self.get_centroids()
        self.mark_labels()
        self.saved_steps.append(
            (
                self.labels.copy(),
                pd.DataFrame(self.centroids, columns=self.data.columns),
            )
        )
        while self.step():
            steps += 1
            self.saved_steps.append(
                (
                    self.labels.copy(),
                    pd.DataFrame(self.centroids, columns=self.data.columns),
                )
            )
            if self.max_iterations and steps > self.max_iterations:
                break
        self.step_counter = steps
        self.saved_steps.append(
            (
                self.labels.copy(),
                pd.DataFrame(self.centroids, columns=self.data.columns),
            )
        )
        return self.labels.copy(), self.centroids

    def run_without_saving_steps(self) -> Tuple[np.ndarray, List[Tuple]]:
        steps = 0
        self.saved_steps = []
        self.centroids = self.get_centroids()
        self.mark_labels()
        while self.step():
            steps += 1
            if self.max_iterations is not None and steps > self.max_iterations:
                break
        self.step_counter = steps
        return self.labels, self.centroids

    def get_steps(self) -> List[Tuple[np.ndarray, pd.DataFrame]]:
        return self.saved_steps
