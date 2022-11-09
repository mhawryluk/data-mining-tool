from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QHBoxLayout

from visualization import ClusteringCanvas
from widgets.components import ClusteringStepsTemplate
from widgets.steps_widgets import AlgorithmStepsVisualization


class KMeansStepsVisualization(AlgorithmStepsVisualization):
    def __init__(
        self,
        data: pd.DataFrame,
        algorithms_steps: List[Tuple[np.ndarray, pd.DataFrame]],
        is_animation: bool,
    ):
        super().__init__(data, algorithms_steps, is_animation)

        description = (
            "K-Means algorithm - steps visualization.\n\n"
            "Each color represents one cluster.\n\n"
            "Circles are the points of the data set.\n"
            "Squares are centroids of the clusters."
        )

        self.layout = QHBoxLayout(self)
        self.num_cluster = algorithms_steps[0][1].shape[0]
        self.max_step = (len(algorithms_steps) - 1) * (2 + self.num_cluster) + 2
        columns = list(self.data.select_dtypes(include=["number"]).columns)

        fig, axes = plt.subplots()
        self.canvas = ClusteringCanvas(fig, axes, self.is_animation)

        self.clustering_template = ClusteringStepsTemplate(
            columns,
            self.max_step,
            self.data.shape[0],
            description,
            self.is_animation,
            self.canvas,
            self.update_plot,
        )
        self.clustering_template.update_plot()
        self.layout.addWidget(self.clustering_template)

    def update_plot(self, step: int = -1):
        if step == self.max_step:
            self.clustering_template.end_animation()
        if step == -1:
            step = self.clustering_template.current_step
        else:
            self.clustering_template.current_step = step
            self.clustering_template.update_step_label()

        samples = self.clustering_template.samples
        ox = self.clustering_template.ox
        oy = self.clustering_template.oy
        is_running = self.clustering_template.is_running

        samples_data = self.data.iloc[samples]
        x = samples_data[ox]
        y = samples_data[oy]
        min_x = self.data[ox].min()
        max_x = self.data[ox].max()
        min_y = self.data[oy].min()
        max_y = self.data[oy].max()
        sep_x = 0.1 * (max_x - min_x)
        sep_y = 0.1 * (max_y - min_y)

        if step == 0:
            return self.canvas.data_plot(
                x,
                y,
                ox,
                oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
                not is_running,
            )

        step_labels, step_centroids = self.algorithms_steps[0]
        labels = [step_labels[sample] for sample in samples]
        x_centroids = step_centroids[ox]
        y_centroids = step_centroids[oy]

        if step == 1:
            return self.canvas.new_centroids_plot(
                None,
                None,
                x_centroids,
                y_centroids,
                ox,
                oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
                not is_running,
            )

        if step == 2:
            return self.canvas.all_plot(
                x,
                y,
                x_centroids,
                y_centroids,
                labels,
                ox,
                oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
                not is_running,
            )

        index = (step - 3) // (self.num_cluster + 2) + 1
        mode = (step - 3) % (self.num_cluster + 2)

        step_labels, step_centroids = self.algorithms_steps[index]
        labels = [step_labels[sample] for sample in samples]
        x_centroids = step_centroids[ox]
        y_centroids = step_centroids[oy]

        old_step_labels, old_step_centroids = self.algorithms_steps[index - 1]
        old_x_centroids = old_step_centroids[ox]
        old_y_centroids = old_step_centroids[oy]

        if mode < self.num_cluster:
            old_labels = np.array([old_step_labels[sample] for sample in samples])
            vector_x = x.loc[old_labels == mode]
            vector_y = y.loc[old_labels == mode]
            other_x = x.loc[old_labels != mode]
            other_y = y.loc[old_labels != mode]
            return self.canvas.chosen_centroid_plot(
                vector_x,
                vector_y,
                other_x,
                other_y,
                old_x_centroids.iloc[mode],
                old_y_centroids.iloc[mode],
                x_centroids.iloc[mode],
                y_centroids.iloc[mode],
                mode,
                len(x_centroids),
                ox,
                oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
                not is_running,
            )
        elif mode == self.num_cluster:
            return self.canvas.new_centroids_plot(
                old_x_centroids,
                old_y_centroids,
                x_centroids,
                y_centroids,
                ox,
                oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
                not is_running,
            )
        else:
            return self.canvas.all_plot(
                x,
                y,
                x_centroids,
                y_centroids,
                labels,
                ox,
                oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
                not is_running,
            )
