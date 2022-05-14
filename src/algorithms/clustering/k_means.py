import pandas as pd
import numpy as np
from typing import List, Tuple, Generator, Union

num_types = [int, float, np.float, np.int]


class KMeans:
    def __init__(self, data: pd.DataFrame, num_clusters: int, metrics: int = 1, stop: int = 0, max_step: int = None):
        self.num_clusters = num_clusters
        self.metrics = metrics
        self.stop = stop
        self.max_step = max_step
        self.step_counter = 0
        self.data = data
        self.is_numeric = [self.check_numeric(column) for _, column in self.data.items()]
        self.centroids = list(self.data.sample(self.num_clusters, replace=False).itertuples(index=False))
        self.labels = np.zeros(self.data.shape[0])
        self.mark_labels()
        self.steps = []

    def distance(self, vector_x: Union[Tuple, List], vector_y: Union[Tuple, List]) -> float:
        diff = np.zeros_like(vector_x, dtype=float)
        for i, (x, y) in enumerate(zip(vector_x, vector_y)):
            if self.is_numeric[i]:
                diff[i] = np.abs(float(x) - float(y))
            else:
                if x == y:
                    diff[i] = 0
                else:
                    diff[i] = 1
        return (np.sum(diff**self.metrics))**(1/self.metrics)

    def mark_labels(self) -> int:
        count = 0
        for i, row in enumerate(self.data.itertuples(index=False)):
            min_dis = np.inf
            m = 0
            for j, centroid in enumerate(self.centroids):
                dis = self.distance(list(row), centroid)
                if dis < min_dis:
                    min_dis = dis
                    m = j
            if self.labels[i] != m:
                count += 1
            self.labels[i] = m
        return count

    def check_numeric(self, element: any) -> bool:
        try:
            pd.to_numeric(element)
            return True
        except ValueError:
            return False

    def mean(self, group: pd.DataFrame) -> Tuple:
        result = []
        for i, (_, column) in enumerate(group.items()):
            if self.is_numeric[i]:
                result.append(column.mean())
            else:
                counter = {}
                most_frequent = None
                count = 0
                for element in column:
                    counter[element] = counter.get(element, 0) + 1
                    if counter[element] > count:
                        count = counter[element]
                        most_frequent = element
                result.append(most_frequent)
        return tuple(result)

    def update_centroids(self):
        for i, centroid in enumerate(self.centroids):
            group = self.data[self.labels == i]
            self.centroids[i] = self.mean(group)

    def step(self) -> bool:
        self.update_centroids()
        count = self.mark_labels()
        if count <= self.stop:
            return False
        return True

    def run(self, with_steps) -> Tuple[np.ndarray, pd.DataFrame]:
        steps = 0
        if with_steps:
            self.steps.append((self.labels, pd.DataFrame(self.centroids, columns=self.data.columns)))
        while self.step():
            steps += 1
            if with_steps:
                self.steps.append((self.labels, pd.DataFrame(self.centroids, columns=self.data.columns)))
            if self.max_step and steps > self.max_step:
                break
        self.step_counter = steps
        if with_steps:
            self.steps.append((self.labels, pd.DataFrame(self.centroids, columns=self.data.columns)))
        return self.labels, pd.DataFrame(self.centroids, columns=self.data.columns)

    # def run_by_steps(self) -> Generator[Tuple[np.ndarray, pd.DataFrame], None, None]:
    #     steps = 0
    #     yield self.labels, pd.DataFrame(self.centroids, columns=self.data.columns)
    #     while self.step():
    #         steps += 1
    #         yield self.labels, pd.DataFrame(self.centroids, columns=self.data.columns)
    #         if self.max_step and steps > self.max_step:
    #             break
    #     yield self.labels, pd.DataFrame(self.centroids, columns=self.data.columns)

    def get_steps(self) -> List[Tuple[np.ndarray, pd.DataFrame]]:
        return self.steps
