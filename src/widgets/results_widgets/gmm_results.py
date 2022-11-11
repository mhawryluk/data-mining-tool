import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout

from visualization import ClusteringCanvas
from widgets.components import ClustersTable, ParametersGroupBox, SamplesColumnsChoice
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

        # algorithm parameters
        self.params_group = ParametersGroupBox(self.options)

        self.layout.addWidget(self.params_group)

        # clustering result group
        self.clustering_result_group = QGroupBox()
        self.clustering_group_layout = QVBoxLayout(self.clustering_result_group)
        self.clustering_result_group.setTitle("Clustering result")

        # samples columns choice
        self.parameters_widget = SamplesColumnsChoice(self.columns, len(self.data))
        self.parameters_widget.samples_columns_changed.connect(self.update_plot)
        self.parameters_widget.samples_columns_changed.connect(self.update_cluster_plot)
        self.clustering_group_layout.addWidget(self.parameters_widget)

        # plot
        self.results_canvas = ClusteringCanvas(False)
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

        self.clusters_canvas = ClusteringCanvas(False)

        self.clusters_group_layout.addWidget(self.clusters_canvas, 1)
        self.layout.addWidget(self.clusters_group, 1)

        self.update_plot()
        self.update_cluster_plot()

    def update_plot(self):
        samples_data = self.data.iloc[self.parameters_widget.samples]
        x = samples_data[self.parameters_widget.ox]
        y = samples_data[self.parameters_widget.oy]
        min_x = self.data[self.parameters_widget.ox].min()
        max_x = self.data[self.parameters_widget.ox].max()
        min_y = self.data[self.parameters_widget.oy].min()
        max_y = self.data[self.parameters_widget.oy].max()
        sep_x = 0.1 * (max_x - min_x)
        sep_y = 0.1 * (max_y - min_y)

        labels = [self.labels[sample] for sample in self.parameters_widget.samples]
        self.results_canvas.clusters_plot(
            x,
            y,
            list(self.columns),
            self.mean.values,
            self.sigma,
            labels,
            self.max_label,
            self.parameters_widget.ox,
            self.parameters_widget.oy,
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
            x = self.data.iloc[indexes][self.parameters_widget.ox]
            y = self.data.iloc[indexes][self.parameters_widget.oy]
            min_x = x.min()
            max_x = x.max()
            min_y = y.min()
            max_y = y.max()
            sep_x = 0.1 * (max_x - min_x)
            sep_y = 0.1 * (max_y - min_y)
            x_means = self.mean[self.parameters_widget.ox]
            y_means = self.mean[self.parameters_widget.oy]
            x_index, y_index = [
                self.columns.get_loc(self.parameters_widget.ox),
                self.columns.get_loc(self.parameters_widget.oy),
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
                self.parameters_widget.ox,
                self.parameters_widget.oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
            )
        else:
            x = self.data[self.parameters_widget.ox]
            y = self.data[self.parameters_widget.oy]
            min_x = x.min()
            max_x = x.max()
            min_y = y.min()
            max_y = y.max()
            sep_x = 0.1 * (max_x - min_x)
            sep_y = 0.1 * (max_y - min_y)
            x_means = self.mean[self.parameters_widget.ox]
            y_means = self.mean[self.parameters_widget.oy]
            x_index, y_index = [
                self.columns.get_loc(self.parameters_widget.ox),
                self.columns.get_loc(self.parameters_widget.oy),
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
                self.parameters_widget.ox,
                self.parameters_widget.oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
            )
