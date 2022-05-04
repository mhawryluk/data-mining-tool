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
        self.centroids = list(self.data.sample(self.num_clusters, replace=False).itertuples(index=False))
        self.labels = np.zeros(self.data.shape[0])
        self.mark_labels()

    def distance(self, vector_x: Union[Tuple, List], vector_y: Union[Tuple, List]) -> float:
        diff = np.zeros_like(vector_x, dtype=float)
        for i, (x, y) in enumerate(zip(vector_x, vector_y)):
            if self.is_numeric(x):
                diff[i] = np.abs(x - y)
            else:
                if x == y:
                    diff[i] = 0
                else:
                    diff[i] = 1
        diff.astype(float)
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

    def is_numeric(self, element: any) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False

    def mean(self, group: pd.DataFrame) -> Tuple:
        result = []
        for i, (_, row) in enumerate(group.items()):
            if self.is_numeric(list(row)[0]):
                result.append(row.mean())
            else:
                counter = {}
                most_frequent = None
                count = 0
                for element in row:
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

    def run(self) -> Tuple[np.ndarray, List[Tuple]]:
        steps = 0
        while self.step():
            steps += 1
            if self.max_step and steps > self.max_step:
                break
        self.step_counter = steps
        return self.labels, self.centroids

    def run_by_steps(self) -> Generator[Tuple[np.ndarray, List[Tuple]], None, None]:
        steps = 0
        yield self.labels, self.centroids
        while self.step():
            steps += 1
            yield self.labels, self.centroids
            if self.max_step and steps > self.max_step:
                break
        yield self.labels, self.centroids

    def get_steps(self) -> List[Tuple[np.ndarray, List[Tuple]]]:
        return list(self.run_by_steps())
