import numpy as np
from matplotlib import pyplot as plt
from matplotlib import transforms
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.patches import Ellipse


class ClusteringCanvas(FigureCanvasQTAgg):
    def __init__(self, animation):
        fig, self.axes = plt.subplots()
        self.animation = animation
        self.sc = None
        super().__init__(fig)

    def data_plot(
        self,
        vector_x,
        vector_y,
        name_x,
        name_y,
        min_x,
        max_x,
        min_y,
        max_y,
        drawing=True,
    ):
        self.axes.cla()
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.sc = self.axes.scatter(x=vector_x, y=vector_y)
        if drawing:
            self.draw()
        if self.animation:
            return self.axes.collections

    def all_plot(
        self,
        vector_x,
        vector_y,
        vector_x_centroids,
        vector_y_centroids,
        labels,
        name_x,
        name_y,
        min_x,
        max_x,
        min_y,
        max_y,
        drawing=True,
    ):
        self.axes.cla()
        label = [labels[i] for i in range(len(vector_x))]
        if vector_x_centroids is not None:
            max_label = len(vector_x_centroids)
        else:
            max_label = max(label) + 1
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.sc = self.axes.scatter(
            vector_x, vector_y, c=label, cmap="gist_rainbow", vmin=0, vmax=max_label
        )
        if vector_x_centroids is not None:
            self.axes.scatter(
                vector_x_centroids,
                vector_y_centroids,
                c=np.arange(max_label),
                marker="s",
                cmap="gist_rainbow",
                vmin=0,
                vmax=max_label,
                edgecolor="black",
                linewidths=1,
            )
        if drawing:
            self.draw()
        if self.animation:
            return self.axes.collections

    def new_centroids_plot(
        self,
        old_vector_x_centroids,
        old_vector_y_centroids,
        vector_x_centroids,
        vector_y_centroids,
        name_x,
        name_y,
        min_x,
        max_x,
        min_y,
        max_y,
        drawing=True,
    ):
        self.axes.cla()
        max_label = len(vector_x_centroids)
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        if old_vector_x_centroids is not None:
            self.axes.scatter(
                old_vector_x_centroids,
                old_vector_y_centroids,
                c=np.arange(max_label),
                marker="s",
                cmap="gist_rainbow",
                vmin=0,
                vmax=max_label,
                alpha=0.3,
            )
        self.axes.scatter(
            vector_x_centroids,
            vector_y_centroids,
            c=np.arange(max_label),
            marker="s",
            cmap="gist_rainbow",
            vmin=0,
            vmax=max_label,
            edgecolor="black",
            linewidths=1,
        )
        if drawing:
            self.draw()
        if self.animation:
            return self.axes.collections

    def chosen_centroid_plot(
        self,
        vector_x,
        vector_y,
        other_x,
        other_y,
        old_x_centroid,
        old_y_centroid,
        x_centroid,
        y_centroid,
        label,
        max_label,
        name_x,
        name_y,
        min_x,
        max_x,
        min_y,
        max_y,
        drawing=True,
    ):
        self.axes.cla()
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.axes.scatter(other_x, other_y, c="white", edgecolor="grey")
        self.axes.scatter(
            vector_x,
            vector_y,
            c=[label] * len(vector_x),
            cmap="gist_rainbow",
            vmin=0,
            vmax=max_label,
            alpha=0.9,
        )
        self.axes.scatter(
            [old_x_centroid], [old_y_centroid], c="black", marker="s", alpha=0.3, s=40
        )
        self.axes.scatter(
            [x_centroid],
            [y_centroid],
            c=[label],
            cmap="gist_rainbow",
            vmin=0,
            vmax=max_label,
            edgecolor="black",
            linewidths=1,
            marker="s",
            alpha=0.7,
            s=50,
        )
        if drawing:
            self.draw()
        if self.animation:
            return self.axes.collections

    def _draw_variance(self, mean, sigma, label, max_label, n_std=2.0):
        pearson = sigma[0][1] / np.sqrt(sigma[0][0] * sigma[1][1])
        ell_radius_x = np.sqrt(1 + pearson)
        ell_radius_y = np.sqrt(1 - pearson)
        cmap = plt.get_cmap("gist_rainbow")
        ellipse = Ellipse(
            (0, 0),
            width=ell_radius_x * 2,
            height=ell_radius_y * 2,
            edgecolor=cmap(label / max_label),
            facecolor="none",
        )
        scale_x = np.sqrt(sigma[0][0]) * n_std
        scale_y = np.sqrt(sigma[1][1]) * n_std
        transf = (
            transforms.Affine2D()
            .rotate_deg(45)
            .scale(scale_x, scale_y)
            .translate(mean[0], mean[1])
        )
        ellipse.set_transform(transf + self.axes.transData)
        self.axes.add_patch(ellipse)

    def clusters_plot(
        self,
        vector_x,
        vector_y,
        columns,
        mean,
        sigma,
        labels,
        max_label,
        name_x,
        name_y,
        min_x,
        max_x,
        min_y,
        max_y,
        drawing=True,
    ):
        self.axes.cla()
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.axes.scatter(
            vector_x, vector_y, c=labels, cmap="gist_rainbow", vmin=0, vmax=max_label
        )
        x_index, y_index = [columns.index(name_x), columns.index(name_y)]
        for i in range(len(mean)):
            mean_i = [mean[i][x_index], mean[i][y_index]]
            sigma_i = [
                [sigma[i][x_index][x_index], sigma[i][x_index][y_index]],
                [sigma[i][y_index][x_index], sigma[i][y_index][y_index]],
            ]
            self.axes.scatter(
                mean_i[0],
                mean_i[1],
                c=i,
                cmap="gist_rainbow",
                marker="s",
                vmin=0,
                vmax=max_label,
            )
            self._draw_variance(mean_i, sigma_i, i, max_label)

        if drawing:
            self.draw()
        if self.animation:
            return self.axes.collections

    def chosen_cluster_plot(
        self,
        vector_x,
        vector_y,
        mean,
        sigma,
        label,
        max_label,
        name_x,
        name_y,
        min_x,
        max_x,
        min_y,
        max_y,
        drawing=True,
    ):
        self.axes.cla()
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.axes.scatter(
            vector_x,
            vector_y,
            c=[label] * len(vector_x),
            cmap="gist_rainbow",
            vmin=0,
            vmax=max_label,
            alpha=0.9,
        )
        self.axes.scatter(
            [mean[0]],
            [mean[1]],
            c=[label],
            cmap="gist_rainbow",
            vmin=0,
            vmax=max_label,
            edgecolor="black",
            linewidths=1,
            marker="s",
            alpha=0.7,
            s=50,
        )
        self._draw_variance(mean, sigma, label, max_label, n_std=1.0)
        if drawing:
            self.draw()

    def clusters_means_plot(
        self, means, sigmas, name_x, name_y, min_x, max_x, min_y, max_y, drawing=True
    ):
        self.axes.cla()
        x_means, y_means = means
        max_label = len(x_means)
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.axes.scatter(
            x_means,
            y_means,
            c=np.arange(max_label),
            marker="s",
            cmap="gist_rainbow",
            vmin=0,
            vmax=max_label,
            edgecolor="black",
            linewidths=1,
        )
        for i in range(len(x_means)):
            self._draw_variance(
                [x_means[i], y_means[i]], sigmas[i], i, max_label, n_std=1.0
            )
        if drawing:
            self.draw()
