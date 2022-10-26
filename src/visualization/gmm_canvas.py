import numpy as np
from matplotlib import pyplot as plt, transforms
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.patches import Ellipse


class GMMCanvas(FigureCanvasQTAgg):
    def __init__(self, fig, axes, animation):
        self.axes = axes
        self.animation = animation
        super().__init__(fig)

    def data_plot(self, vector_x, vector_y, name_x, name_y, min_x, max_x, min_y, max_y, drawing=True):
        self.axes.cla()
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.axes.scatter(x=vector_x, y=vector_y)
        if drawing:
            self.draw()
        if self.animation:
            return self.axes.collections

    def _draw_variance(self, mean, sigma, label, max_label, n_std=2.0):
        pearson = sigma[0][1] / np.sqrt(sigma[0][0] * sigma[1][1])
        ell_radius_x = np.sqrt(1 + pearson)
        ell_radius_y = np.sqrt(1 - pearson)
        cmap = plt.get_cmap('gist_rainbow')
        ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                          edgecolor=cmap(label / max_label), facecolor='none')
        scale_x = np.sqrt(sigma[0][0]) * n_std
        scale_y = np.sqrt(sigma[1][1]) * n_std
        transf = transforms.Affine2D() \
            .rotate_deg(45) \
            .scale(scale_x, scale_y) \
            .translate(mean[0], mean[1])
        ellipse.set_transform(transf + self.axes.transData)
        self.axes.add_patch(ellipse)

    def clusters_plot(self, vector_x, vector_y, columns, mean, sigma, labels, max_label, name_x, name_y, min_x, max_x,
                      min_y, max_y, drawing=True):
        self.axes.cla()
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.axes.scatter(vector_x, vector_y, c=labels, cmap='gist_rainbow', vmin=0, vmax=max_label)
        x_index, y_index = [columns.index(name_x), columns.index(name_y)]
        for i in range(len(mean)):
            mean_i = [mean[i][x_index], mean[i][y_index]]
            sigma_i = [
                [sigma[i][x_index][x_index], sigma[i][x_index][y_index]],
                [sigma[i][y_index][x_index], sigma[i][y_index][y_index]],
            ]
            self.axes.scatter(mean_i[0], mean_i[1], c=i, cmap='gist_rainbow', marker='s', vmin=0, vmax=max_label)
            self._draw_variance(mean_i, sigma_i, i, max_label)

        if drawing:
            self.draw()
        if self.animation:
            return self.axes.collections

    def chosen_cluster_plot(self, vector_x, vector_y, mean, sigma, label, max_label, name_x, name_y, min_x, max_x,
                            min_y, max_y, drawing=True):
        self.axes.cla()
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.axes.scatter(vector_x, vector_y, c=[label] * len(vector_x), cmap='gist_rainbow',
                          vmin=0, vmax=max_label, alpha=0.9)
        self.axes.scatter([mean[0]], [mean[1]], c=[label], cmap='gist_rainbow', vmin=0, vmax=max_label,
                          edgecolor='black', linewidths=1, marker='s', alpha=0.7, s=50)
        self._draw_variance(mean, sigma, label, max_label, n_std=1.0)
        if drawing:
            self.draw()

    def clusters_means_plot(self, means, sigmas, name_x, name_y, min_x, max_x, min_y, max_y, drawing=True):
        self.axes.cla()
        x_means, y_means = means
        max_label = len(x_means)
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.axes.scatter(x_means, y_means, c=np.arange(max_label),
                          marker='s', cmap='gist_rainbow', vmin=0, vmax=max_label, edgecolor='black', linewidths=1)
        for i in range(len(x_means)):
            self._draw_variance([x_means[i], y_means[i]], sigmas[i], i, max_label, n_std=1.0)
        if drawing:
            self.draw()
