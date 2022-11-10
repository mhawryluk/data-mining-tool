import pandas as pd
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout

from visualization import ClusteringCanvas
from widgets.components import ClustersTable, ParametersGroupBox, SamplesColumnsChoice
from widgets.results_widgets import AlgorithmResultsWidget


class KMeansResultsWidget(AlgorithmResultsWidget):
    def __init__(self, data, labels, centroids, options):
        super().__init__(data, options)

        self.labels = labels
        self.centroids = centroids

        columns = self.data.select_dtypes(include=["number"]).columns

        self.layout = QHBoxLayout(self)

        # algorithm parameters
        self.params_group = ParametersGroupBox(self.options)

        self.layout.addWidget(self.params_group)

        # clustering result group
        self.clustering_result_group = QGroupBox()
        self.clustering_group_layout = QVBoxLayout(self.clustering_result_group)
        self.clustering_result_group.setTitle("Clustering result")

        # samples columns choice
        self.parameters_widget = SamplesColumnsChoice(columns, len(self.data))
        self.parameters_widget.samples_columns_changed.connect(self.update_plot)
        self.parameters_widget.samples_columns_changed.connect(self.update_cluster_plot)
        self.clustering_group_layout.addWidget(self.parameters_widget)

        # plot
        self.fig, axes = plt.subplots(1, 1)
        self.results_canvas = ClusteringCanvas(self.fig, axes, False)
        self.clustering_group_layout.addWidget(self.results_canvas, 1)

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
        if self.parameters_widget.ox in self.centroids.columns:
            x_centroids = self.centroids[self.parameters_widget.ox]
        else:
            x_centroids = pd.Series(
                [
                    self.data.iloc[self.labels == label][
                        self.parameters_widget.ox
                    ].mean()
                    for label in range(max(self.labels) + 1)
                ]
            )
        if self.parameters_widget.oy in self.centroids.columns:
            y_centroids = self.centroids[self.parameters_widget.oy]
        else:
            y_centroids = pd.Series(
                [
                    self.data.iloc[self.labels == label][
                        self.parameters_widget.oy
                    ].mean()
                    for label in range(max(self.labels) + 1)
                ]
            )

        self.results_canvas.all_plot(
            x,
            y,
            x_centroids,
            y_centroids,
            labels,
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

            if self.parameters_widget.ox in self.centroids.columns:
                x_centroids = self.centroids[self.parameters_widget.ox]
            else:
                x_centroids = pd.Series(
                    [
                        self.data.iloc[self.labels == label][
                            self.parameters_widget.ox
                        ].mean()
                        for label in range(max(self.labels) + 1)
                    ]
                )
            if self.parameters_widget.oy in self.centroids.columns:
                y_centroids = self.centroids[self.parameters_widget.oy]
            else:
                y_centroids = pd.Series(
                    [
                        self.data.iloc[self.labels == label][
                            self.parameters_widget.oy
                        ].mean()
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

            if self.parameters_widget.ox in self.centroids.columns:
                x_centroids = self.centroids[self.parameters_widget.ox]
            else:
                x_centroids = pd.Series(
                    [
                        self.data.iloc[self.labels == label][
                            self.parameters_widget.ox
                        ].mean()
                        for label in range(max(self.labels) + 1)
                    ]
                )
            if self.parameters_widget.oy in self.centroids.columns:
                y_centroids = self.centroids[self.parameters_widget.oy]
            else:
                y_centroids = pd.Series(
                    [
                        self.data.iloc[self.labels == label][
                            self.parameters_widget.oy
                        ].mean()
                        for label in range(max(self.labels) + 1)
                    ]
                )

            self.clusters_canvas.new_centroids_plot(
                None,
                None,
                x_centroids,
                y_centroids,
                self.parameters_widget.ox,
                self.parameters_widget.oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
            )
