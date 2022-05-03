import pandas as pd
import numpy as np
from typing import List, Tuple, Generator


class KMeans:
    def __init__(self, data: pd.DataFrame, k: int, metrics: int = 1, stop: int = 5, max_step: int = None):
        self.k = k
        self.distance = lambda x, y: ((np.abs(x-y))**metrics)**(1/metrics)
        self.stop = stop
        self.max_step = max_step
        self.step_counter = 0
        self.data = data
        self.centroids = list(self.data.sample(k, replace=False).itertuples(index=False))
        self.labels = np.zeros(self.data.size)
        self.mark_labels()

    def mark_labels(self) -> int:
        min_dis = np.inf
        m = 0
        count = 0
        for i, row in enumerate(self.data.items()):
            for j, centroid in enumerate(self.centroids):
                dis = self.distance(row[1].to_numpy(), centroid.to_numpy())
                if dis < min_dis:
                    min_dis = dis
                    m = j
            if self.labels[i] != m:
                count += 1
                self.labels[i] = m
        return count

    def update_centroids(self):
        for i, centroid in enumerate(self.centroids):
            group = self.data[self.labels == i]
            self.centroids[i] = group.mean(axis=0)

    def step(self) -> bool:
        self.update_centroids()
        count = self.mark_labels()
        if count < self.stop:
            return False
        return True

    def run(self) -> Tuple[np.ndarray, List[Tuple]]:
        steps = 0
        while self.step():
            steps += 1
            if self.max_step and steps > self.max_step:
                break
        self.step_counter = steps
        print(self.labels, self.centroids)
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
