import numpy as np
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QHBoxLayout

from visualization import ClusteringCanvas
from widgets.components import ClusteringStepsTemplate
from widgets.steps_widgets import AlgorithmStepsVisualization


class GMMStepsVisualization(AlgorithmStepsVisualization):
    def __init__(self, data, algorithms_steps, is_animation):
        super().__init__(data, algorithms_steps, is_animation)

        description = (
            "Gaussian Mixture Models algorithm - steps visualization.\n\n"
            "Colors of points show division into clusters.\n\n"
            "Square points represents means of each distribution and "
            "ellipses are showing variances."
        )

        self.layout = QHBoxLayout(self)
        self.num_cluster = np.amax(self.algorithms_steps[0][0]) + 1
        self.max_step = len(self.algorithms_steps) - 1
        self.columns = list(self.data.select_dtypes(include=["number"]).columns)

        fig, axes = plt.subplots()
        self.canvas = ClusteringCanvas(fig, axes, self.is_animation)

        self.clustering_template = ClusteringStepsTemplate(
            self.columns,
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

        index = step - 1
        step_labels, mean, sigma = self.algorithms_steps[index]
        labels = [step_labels[sample] for sample in samples]
        return self.canvas.clusters_plot(
            x,
            y,
            list(self.columns),
            mean,
            sigma,
            labels,
            self.num_cluster,
            ox,
            oy,
            min_x - sep_x,
            max_x + sep_x,
            min_y - sep_y,
            max_y + sep_y,
            not is_running,
        )
