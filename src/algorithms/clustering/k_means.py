import pandas as pd
import numpy as np
from typing import List, Tuple, Union, Optional

initial_types = ['random', 'kmeans++']


class KMeans:
    def __init__(self, data: pd.DataFrame, num_clusters: int, metrics: int = 1, iterations: Optional[int] = None, repeats: int = 1, init_type: initial_types = 'random'):
        self.num_clusters = num_clusters
        self.metrics = metrics
        self.max_iterations = iterations
        self.repeats = repeats
        if init_type not in initial_types:
            raise TypeError(f"{init_type} is invalid value of init_type parameter")
        self.step_counter = 0
        self.data = data
        self.is_numeric = [self.check_numeric(column) for _, column in self.data.items()]
        self.centroids = []
        self.labels = np.zeros(self.data.shape[0], dtype=int)
        self.saved_steps = []
        self.get_centroids = {'random': self.random_centroids, 'kmeans++': self.kmeanspp_centroids}[init_type]

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

    def random_centroids(self) -> List[Tuple]:
        return list(self.data.sample(self.num_clusters, replace=False).itertuples(index=False))

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
        if count == 0:
            return False
        return True

    def check_solution(self, labels, centroids):
        """ dunn index """
        max_distance_intra = 0
        min_distance_inter = np.inf
        for i, first in enumerate(centroids):
            for second in centroids[i+1:]:
                dis = self.distance(first, second)
                if dis > max_distance_intra:
                    max_distance_intra = dis
        for i, row in enumerate(self.data.itertuples(index=False)):
            dis = self.distance(row, centroids[labels[i]])
            if dis < min_distance_inter:
                min_distance_inter = dis
        return min_distance_inter / max_distance_intra

    def run(self, with_steps) -> Tuple[np.ndarray, pd.DataFrame]:
        runner = self.run_with_saving_steps if with_steps else self.run_without_saving_steps
        if self.repeats == 1:
            solution = runner()
            return solution[0], pd.DataFrame(solution[1], columns=self.data.columns)
        best_value = np.inf
        solution = None
        steps = None
        for _ in range(self.repeats):
            result = runner()
            value = self.check_solution(*result)
            if value < best_value:
                solution = result
                steps = [(step[0].copy(), step[1].copy()) for step in self.saved_steps]
                best_value = value
        self.saved_steps = steps
        return solution[0], pd.DataFrame(solution[1], columns=self.data.columns)

    def run_with_saving_steps(self) -> Tuple[np.ndarray, List[Tuple]]:
        steps = 0
        self.saved_steps = []
        self.centroids = self.get_centroids()
        self.mark_labels()
        self.saved_steps.append((self.labels, pd.DataFrame(self.centroids, columns=self.data.columns)))
        while self.step():
            steps += 1
            self.saved_steps.append((self.labels, pd.DataFrame(self.centroids, columns=self.data.columns)))
            if self.max_iterations and steps > self.max_iterations:
                break
        self.step_counter = steps
        self.saved_steps.append((self.labels, pd.DataFrame(self.centroids, columns=self.data.columns)))
        return self.labels, self.centroids

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
