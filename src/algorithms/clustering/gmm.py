from math import inf

import numpy as np
import pandas as pd
from numpy.linalg import LinAlgError
from PyQt5.QtWidgets import QMessageBox
from scipy.stats import multivariate_normal

from algorithms import Algorithm


class GMM(Algorithm):
    def __init__(self, df, num_clusters, eps=1e-6, max_iterations=None):
        self.df = df.select_dtypes(include=["number"])
        self.num_clusters = num_clusters
        self.rows = self.df.shape[0]
        self.dim = len(self.df.columns)
        self.labels = np.floor_divide(
            np.arange(self.rows), self.rows / self.num_clusters
        )
        self.mu_arr = self.initialize_mu()
        self.sigma_arr = self.initialize_sigma()
        self.pi_arr = self.initialize_pi()
        self.prob_matrix = None
        self.eps = float(eps)
        self.max_iter = max_iterations or inf
        self.scenes = [
            (np.array(self.labels, dtype="int64"), self.mu_arr, self.sigma_arr)
        ]

    def run(self, with_steps):
        try:
            prev_ll = self.log_likelihood()
            i = 0
            while i < self.max_iter:
                self.e_step()
                self.m_step()
                if with_steps:
                    self.scenes.append(
                        (self.get_cluster_labels(), self.mu_arr, self.sigma_arr)
                    )
                new_ll = self.log_likelihood()
                if abs(new_ll - prev_ll) < self.eps:
                    break
                prev_ll = new_ll
                i += 1
        except LinAlgError:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText(
                "Oops, singular matrix error. "
                "This data may not be good for this algorithm. "
                "Try to modify params or choose different algorithm."
            )
            error.setWindowTitle("Error")
            error.exec_()
            return
        return (
            self.get_cluster_labels(),
            pd.DataFrame(self.mu_arr, columns=self.df.columns),
            self.sigma_arr,
        )

    def get_cluster_labels(self):
        return np.argmax(self.prob_matrix, axis=1)

    def get_steps(self):
        return self.scenes

    def initialize_mu(self):
        size = (self.num_clusters, self.dim)
        return np.random.random_sample(size)

    def initialize_sigma(self):
        return np.tile(np.eye(self.dim) * 100, (self.num_clusters, 1, 1))

    def initialize_pi(self):
        _, counts = np.unique(self.labels, return_counts=True)
        return np.divide(counts, self.rows)

    def e_step(self):
        self.prob_matrix = np.fromfunction(
            np.vectorize(self.calculate_prob), (self.rows, self.num_clusters), dtype=int
        )
        self.prob_matrix = self.prob_matrix / self.prob_matrix.sum(
            axis=1, keepdims=True
        )

    def calculate_prob(self, i, c):
        return self.pi_arr[c] * multivariate_normal.pdf(
            self.df.iloc[i], mean=self.mu_arr[c], cov=self.sigma_arr[c]
        )

    def m_step(self):
        self.pi_arr = np.divide(np.sum(self.prob_matrix, axis=0), self.rows)
        self.update_mu()
        self.update_sigma()

    def update_mu(self):
        sums = [
            np.sum((self.df.T * self.prob_matrix[:, c]).T, axis=0)
            for c in range(self.num_clusters)
        ]
        sums = [
            sums[c] / (self.pi_arr[c] * self.rows) for c in range(self.num_clusters)
        ]
        self.mu_arr = np.array(sums)

    def update_sigma(self):
        for c in range(self.num_clusters):
            new_sigma_component = np.zeros((self.dim, self.dim))
            for i in range(self.rows):
                data_row = np.array(self.df.iloc[i]) - self.mu_arr[c]
                new_sigma_component += self.prob_matrix[i, c] * np.outer(
                    data_row.T, data_row
                )
            self.sigma_arr[c] = new_sigma_component / (self.pi_arr[c] * self.rows)

    def log_likelihood(self):
        result = 0
        for i in range(self.rows):
            row_result = 0
            for c in range(self.num_clusters):
                row_result += self.pi_arr[c] * multivariate_normal.pdf(
                    self.df.iloc[i], mean=self.mu_arr[c], cov=self.sigma_arr[c]
                )
            result += np.log(row_result)
        return result
