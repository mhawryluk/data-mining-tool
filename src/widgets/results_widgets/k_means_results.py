from functools import partial

import pandas as pd
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from algorithms import get_samples
from visualization import ClusteringCanvas
from widgets.components import ClustersTable, ParametersGroupBox
from widgets.results_widgets import AlgorithmResultsWidget


class KMeansResultsWidget(AlgorithmResultsWidget):
    def __init__(self, data, labels, centroids, options):
        super().__init__(data, options)

        self.labels = labels
        self.centroids = centroids

        columns = self.data.select_dtypes(include=["number"]).columns

        self.layout = QHBoxLayout(self)

        self.num_samples = min(35, self.data.shape[0] // 2)
        self.samples = get_samples(self.data, self.num_samples)

        self.ox = columns[0]
        self.oy = columns[0] if len(columns) < 2 else columns[1]

        # algorithm parameters
        self.params_group = ParametersGroupBox(self.options)

        self.layout.addWidget(self.params_group)

        # clustering result group
        self.clustering_result_group = QGroupBox()
        self.clustering_group_layout = QVBoxLayout(self.clustering_result_group)
        self.clustering_result_group.setTitle("Clustering result")

        # samples
        self.settings_group_box = QGroupBox()
        self.settings_box_layout = QFormLayout(self.settings_group_box)
        self.settings_box_layout.addRow(QLabel("Set samples:"))
        self.sample_box = QSpinBox()
        self.sample_box.setMinimum(1)
        self.sample_box.setMaximum(min(self.data.shape[0], 10000))
        self.sample_box.setProperty("value", self.num_samples)
        self.sample_button = QPushButton("Refresh samples")
        self.sample_button.clicked.connect(partial(self.click_listener, "new_samples"))
        self.settings_box_layout.addRow(self.sample_box, self.sample_button)

        # axis
        self.settings_box_layout.addRow(QLabel("Set axis:"))
        self.ox_box = QComboBox()
        self.ox_box.addItems(columns)
        self.oy_box = QComboBox()
        self.oy_box.addItems(columns)
        if len(columns) > 1:
            self.oy_box.setCurrentIndex(1)
        self.ox_box.currentTextChanged.connect(partial(self.click_listener, "set_axis"))
        self.oy_box.currentTextChanged.connect(partial(self.click_listener, "set_axis"))
        self.settings_box_layout.addRow(QLabel("OX:"), self.ox_box)
        self.settings_box_layout.addRow(QLabel("OY:"), self.oy_box)

        self.settings_box_layout.setSpacing(10)
        self.clustering_group_layout.addWidget(self.settings_group_box)

        # plot
        self.fig, axes = plt.subplots(1, 1)
        self.clusters_canvas = ClusteringCanvas(self.fig, axes, False)
        self.clustering_group_layout.addWidget(self.clusters_canvas, 1)

        self.layout.addWidget(self.clustering_result_group, 1)

        # centroids
        self.clusters_group = QGroupBox()
        self.clusters_group_layout = QVBoxLayout(self.clusters_group)
        self.clusters_group.setTitle("Clusters")

        self.clusters_table = ClustersTable(
            self.data, self.labels, self.centroids, len(columns)
        )
        self.clusters_table.table_changed.connect(self.update_cluster_plot)
        self.clusters_group_layout.addWidget(self.clusters_table, 1)

        self.fig_centroids, ax = plt.subplots(1, 1)
        self.clusters_canvas = ClusteringCanvas(self.fig_centroids, ax, False)

        self.clusters_group_layout.addWidget(self.clusters_canvas, 1)
        self.layout.addWidget(self.clusters_group, 1)

        self.update_plot()
        self.update_cluster_plot()

    def click_listener(self, button_type: str):
        match button_type:
            case "new_samples":
                num = self.sample_box.value()
                self.num_samples = num
                self.samples = get_samples(self.data, self.num_samples)
                self.update_plot()
                self.update_cluster_plot()
            case "set_axis":
                self.ox = self.ox_box.currentText()
                self.oy = self.oy_box.currentText()
                self.update_plot()
                self.update_cluster_plot()

    def update_plot(self):
        samples_data = self.data.iloc[self.samples]
        x = samples_data[self.ox]
        y = samples_data[self.oy]
        min_x = self.data[self.ox].min()
        max_x = self.data[self.ox].max()
        min_y = self.data[self.oy].min()
        max_y = self.data[self.oy].max()
        sep_x = 0.1 * (max_x - min_x)
        sep_y = 0.1 * (max_y - min_y)

        labels = [self.labels[sample] for sample in self.samples]
        if self.ox in self.centroids.columns:
            x_centroids = self.centroids[self.ox]
        else:
            x_centroids = pd.Series(
                [
                    self.data.iloc[self.labels == label][self.ox].mean()
                    for label in range(max(self.labels) + 1)
                ]
            )
        if self.oy in self.centroids.columns:
            y_centroids = self.centroids[self.oy]
        else:
            y_centroids = pd.Series(
                [
                    self.data.iloc[self.labels == label][self.oy].mean()
                    for label in range(max(self.labels) + 1)
                ]
            )

        self.clusters_canvas.all_plot(
            x,
            y,
            x_centroids,
            y_centroids,
            labels,
            self.ox,
            self.oy,
            min_x - sep_x,
            max_x + sep_x,
            min_y - sep_y,
            max_y + sep_y,
        )

    def update_cluster_plot(self):
        if self.clusters_table.selected_cluster is not None:
            indexes = [
                i
                for i in range(len(self.labels))
                if self.labels[i] == self.clusters_table.selected_cluster
            ]
            x = self.data.iloc[indexes][self.ox]
            y = self.data.iloc[indexes][self.oy]
            min_x = x.min()
            max_x = x.max()
            min_y = y.min()
            max_y = y.max()
            sep_x = 0.1 * (max_x - min_x)
            sep_y = 0.1 * (max_y - min_y)

            if self.ox in self.centroids.columns:
                x_centroids = self.centroids[self.ox]
            else:
                x_centroids = pd.Series(
                    [
                        self.data.iloc[self.labels == label][self.ox].mean()
                        for label in range(max(self.labels) + 1)
                    ]
                )
            if self.oy in self.centroids.columns:
                y_centroids = self.centroids[self.oy]
            else:
                y_centroids = pd.Series(
                    [
                        self.data.iloc[self.labels == label][self.oy].mean()
                        for label in range(max(self.labels) + 1)
                    ]
                )

            self.clusters_canvas.chosen_centroid_plot(
                x,
                y,
                None,
                None,
                None,
                None,
                x_centroids.iloc[self.clusters_table.selected_cluster],
                y_centroids.iloc[self.clusters_table.selected_cluster],
                self.clusters_table.selected_cluster,
                len(x_centroids),
                self.ox,
                self.oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
            )
        else:
            x = self.data[self.ox]
            y = self.data[self.oy]
            min_x = x.min()
            max_x = x.max()
            min_y = y.min()
            max_y = y.max()
            sep_x = 0.1 * (max_x - min_x)
            sep_y = 0.1 * (max_y - min_y)

            if self.ox in self.centroids.columns:
                x_centroids = self.centroids[self.ox]
            else:
                x_centroids = pd.Series(
                    [
                        self.data.iloc[self.labels == label][self.ox].mean()
                        for label in range(max(self.labels) + 1)
                    ]
                )
            if self.oy in self.centroids.columns:
                y_centroids = self.centroids[self.oy]
            else:
                y_centroids = pd.Series(
                    [
                        self.data.iloc[self.labels == label][self.oy].mean()
                        for label in range(max(self.labels) + 1)
                    ]
                )

            self.clusters_canvas.new_centroids_plot(
                None,
                None,
                x_centroids,
                y_centroids,
                self.ox,
                self.oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
            )
