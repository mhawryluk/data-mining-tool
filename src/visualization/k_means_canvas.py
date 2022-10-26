import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class KMeansCanvas(FigureCanvasQTAgg):
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

    def all_plot(self, vector_x, vector_y, vector_x_centroids, vector_y_centroids,
                 labels, name_x, name_y, min_x, max_x, min_y, max_y, drawing=True):
        self.axes.cla()
        label = [labels[i] for i in range(len(vector_x))]
        max_label = len(vector_x_centroids)
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.axes.scatter(vector_x, vector_y, c=label, cmap='gist_rainbow', vmin=0, vmax=max_label)
        self.axes.scatter(vector_x_centroids, vector_y_centroids, c=np.arange(max_label),
                          marker='s', cmap='gist_rainbow', vmin=0, vmax=max_label, edgecolor='black', linewidths=1)
        if drawing:
            self.draw()
        if self.animation:
            return self.axes.collections

    def new_centroids_plot(self, old_vector_x_centroids, old_vector_y_centroids, vector_x_centroids, vector_y_centroids,
                           name_x, name_y, min_x, max_x, min_y, max_y, drawing=True):
        self.axes.cla()
        max_label = len(vector_x_centroids)
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        if old_vector_x_centroids is not None:
            self.axes.scatter(old_vector_x_centroids, old_vector_y_centroids, c=np.arange(max_label),
                              marker='s', cmap='gist_rainbow', vmin=0, vmax=max_label, alpha=0.3)
        self.axes.scatter(vector_x_centroids, vector_y_centroids, c=np.arange(max_label),
                          marker='s', cmap='gist_rainbow', vmin=0, vmax=max_label, edgecolor='black', linewidths=1)
        if drawing:
            self.draw()
        if self.animation:
            return self.axes.collections

    def chosen_centroid_plot(self, vector_x, vector_y, other_x, other_y, old_x_centroid, old_y_centroid, x_centroid,
                             y_centroid, label, max_label, name_x, name_y, min_x, max_x, min_y, max_y, drawing=True):
        self.axes.cla()
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.axes.scatter(other_x, other_y, c='white', edgecolor='grey')
        self.axes.scatter(vector_x, vector_y, c=[label] * len(vector_x), cmap='gist_rainbow',
                          vmin=0, vmax=max_label, alpha=0.9)
        self.axes.scatter([old_x_centroid], [old_y_centroid], c='black', marker='s', alpha=0.3, s=40)
        self.axes.scatter([x_centroid], [y_centroid], c=[label], cmap='gist_rainbow', vmin=0, vmax=max_label,
                          edgecolor='black', linewidths=1, marker='s', alpha=0.7, s=50)
        if drawing:
            self.draw()
        if self.animation:
            return self.axes.collections
