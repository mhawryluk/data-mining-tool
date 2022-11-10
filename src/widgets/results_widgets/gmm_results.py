from functools import partial

import numpy as np
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


class GMMResultsWidget(AlgorithmResultsWidget):
    def __init__(self, df, labels, mean, sigma, options):
        super().__init__(df.select_dtypes(include=["number"]), options)

        self.columns = self.data.columns
        self.labels = labels
        self.max_label = np.amax(self.labels) + 1
        self.mean = pd.DataFrame(mean, columns=self.columns)
        self.sigma = sigma
        self.layout = QHBoxLayout(self)

        self.num_samples = min(35, self.data.shape[0] // 2)
        self.samples = get_samples(self.data, self.num_samples)
        self.ox = self.columns[0]
        self.oy = self.columns[0] if len(self.columns) < 2 else self.columns[1]

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
        self.ox_box.addItems(self.columns)
        self.oy_box = QComboBox()
        self.oy_box.addItems(self.columns)
        if len(self.columns) > 1:
            self.oy_box.setCurrentIndex(1)
        self.ox_box.currentTextChanged.connect(partial(self.click_listener, "set_axis"))
        self.oy_box.currentTextChanged.connect(partial(self.click_listener, "set_axis"))
        self.settings_box_layout.addRow(QLabel("OX:"), self.ox_box)
        self.settings_box_layout.addRow(QLabel("OY:"), self.oy_box)
        self.settings_box_layout.setSpacing(10)
        self.clustering_group_layout.addWidget(self.settings_group_box)

        # plot
        self.fig, axes = plt.subplots(1, 1)
        self.results_canvas = ClusteringCanvas(self.fig, axes, False)
        self.clustering_group_layout.addWidget(self.results_canvas, 1)

        self.layout.addWidget(self.clustering_result_group, 1)

        # cluster details
        self.clusters_group = QGroupBox()
        self.clusters_group_layout = QVBoxLayout(self.clusters_group)
        self.clusters_group.setTitle("Clusters")

        self.clusters_table = ClustersTable(
            self.data, self.labels, self.mean, len(self.columns)
        )
        self.clusters_table.table_changed.connect(self.update_cluster_plot)
        self.clusters_group_layout.addWidget(self.clusters_table, 1)

        self.fig_distributions, ax = plt.subplots(1, 1)
        self.clusters_canvas = ClusteringCanvas(self.fig_distributions, ax, False)

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
        self.results_canvas.clusters_plot(
            x,
            y,
            list(self.columns),
            self.mean.values,
            self.sigma,
            labels,
            self.max_label,
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
            x_means = self.mean[self.ox]
            y_means = self.mean[self.oy]
            x_index, y_index = [
                self.columns.get_loc(self.ox),
                self.columns.get_loc(self.oy),
            ]
            mean = [
                x_means.iloc[self.clusters_table.selected_cluster],
                y_means.iloc[self.clusters_table.selected_cluster],
            ]
            sigma_helper = self.sigma[self.clusters_table.selected_cluster]
            sigma = [
                [sigma_helper[x_index][x_index], sigma_helper[x_index][y_index]],
                [sigma_helper[y_index][x_index], sigma_helper[y_index][y_index]],
            ]

            self.clusters_canvas.chosen_cluster_plot(
                x,
                y,
                mean,
                sigma,
                self.clusters_table.selected_cluster,
                len(x_means),
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
            x_means = self.mean[self.ox]
            y_means = self.mean[self.oy]
            x_index, y_index = [
                self.columns.get_loc(self.ox),
                self.columns.get_loc(self.oy),
            ]
            means = [x_means, y_means]
            sigmas = []
            for i in range(len(self.sigma)):
                sigma_helper = self.sigma[i]
                sigmas.append(
                    [
                        [
                            sigma_helper[x_index][x_index],
                            sigma_helper[x_index][y_index],
                        ],
                        [
                            sigma_helper[y_index][x_index],
                            sigma_helper[y_index][y_index],
                        ],
                    ]
                )

            self.clusters_canvas.clusters_means_plot(
                means,
                sigmas,
                self.ox,
                self.oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
            )
