from typing import Optional
from state import State
import numpy as np
import pandas as pd


class PCAReducer:
    def __init__(self, state: State, acceptable_ratio=0.05):
        self.state = state
        self.acceptable_ratio = acceptable_ratio
        self.initial_columns = []

    def reduce(self, dim_number: Optional[int]) -> list[str]:
        data = self.state.imported_data.select_dtypes(include=np.number)
        data = data - data.mean()
        self.initial_columns = list(data.columns)
        covariance_matrix = data.cov()
        reduce_matrix = self._pca(covariance_matrix, dim_number)
        override = np.dot(data, reduce_matrix)
        columns = ["{}".format(self.format_column_name(reduce_matrix[:, i])) for i in range(dim_number or override.shape[1])]
        self.state.imported_data = pd.concat([self.state.imported_data, pd.DataFrame(override, columns=columns)], axis=1)
        self.state.raw_data = pd.concat([self.state.raw_data, pd.DataFrame(override, columns=columns)], axis=1)
        return columns

    def _pca(self, matrix, dim_number=None):
        reducer, weights = self._svd(matrix, k=dim_number)
        if dim_number is None:
            total = sum(weights)
            ratios = [weight/total for weight in weights]
            columns_num = max(len(list(filter(lambda x: x > self.acceptable_ratio, ratios))), 2)
            return reducer[:, :columns_num]
        return reducer

    @staticmethod
    def _dominant_component(matrix, eps):
        m, n = matrix.shape
        v = np.ones(n) / np.sqrt(n)
        while True:
            new_v = np.dot(matrix, v)
            new_v = new_v / np.linalg.norm(new_v)
            if abs(np.linalg.norm(v - new_v)) < eps:
                return v
            v = new_v

    def _svd(self, matrix, k=None, eps=1e-10):
        matrix_helper = np.array(matrix)
        m, n = matrix_helper.shape
        svd_components = []
        if k is None:
            k = n
        for i in range(k):
            v = self._dominant_component(matrix_helper, eps=eps)
            u_unnormalized = np.dot(matrix, v)
            sigma = np.linalg.norm(u_unnormalized)
            u = u_unnormalized / sigma

            matrix_helper -= sigma * np.outer(u, v)

            svd_components.append((u, sigma))

        U, Sigma = [np.array(x) for x in zip(*svd_components)]
        return U.T, Sigma

    def format_column_name(self, vector):
        label = ""
        indexes = np.argpartition(vector, -2)[-2:]
        for index in indexes:  # arbitrary value
            label += "{}*{}+".format(round(vector[index], 2), self.initial_columns[index])
        return label.rstrip("+")
