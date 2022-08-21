from state import State
import numpy as np
import pandas as pd


class PCAReducer:
    def __init__(self, state: State, acceptable_ratio = 0.05):
        self.state = state
        self.acceptable_ratio = acceptable_ratio

    def reduce(self, dim_number):
        data = self.state.imported_data.select_dtypes(include=np.number)
        data = data - data.mean()
        covariance_matrix = data.cov()
        reduce_matrix = self._pca(covariance_matrix, dim_number)
        override = np.dot(data, reduce_matrix)
        columns = ["column {}".format(i) for i in range(dim_number or override.shape[1])]
        self.state.imported_data = pd.DataFrame(override, columns=columns)

    def _pca(self, matrix, dim_number=None):
        reducer, weights, _ = self._svd(matrix, k=dim_number)
        if dim_number is None:
            total = sum(weights)
            ratios = [weight/total for weight in weights]
            columns_num = len(list(filter(lambda x: x > self.acceptable_ratio, ratios)))
            return reducer[:, :columns_num]
        return reducer

    def _dominant_component(self, M, eps):
        m, n = M.shape
        v = np.ones(n) / np.sqrt(n)
        while True:
            new_v = np.dot(M, v)
            new_v = new_v / np.linalg.norm(new_v)
            if abs(np.linalg.norm(v - new_v)) < eps:
                return v
            v = new_v

    def _svd(self, M, k=None, eps=1e-10):
        matrix = np.array(M)
        m, n = matrix.shape
        svd_components = []
        if k is None:
            k = n
        for i in range(k):
            v = self._dominant_component(matrix, eps=eps)
            u_unnormalized = np.dot(M, v)
            sigma = np.linalg.norm(u_unnormalized)
            u = u_unnormalized / sigma

            matrix -= sigma * np.outer(u, v)

            svd_components.append((u, sigma, v))

        U, Sigma, V = [np.array(x) for x in zip(*svd_components)]
        return U.T, Sigma, V
