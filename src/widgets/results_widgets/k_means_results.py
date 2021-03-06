from functools import partial

import pandas as pd
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QFormLayout, QLabel, QVBoxLayout, QSpinBox, QPushButton, \
    QComboBox, QTableView
from matplotlib import pyplot as plt

from algorithms import check_numeric, get_samples
from visualization.clustering import KMeansCanvas
from widgets import QtTable


class KMeansResultsWidget(QWidget):
    def __init__(self, data, labels, centroids, options):
        super().__init__()
        self.data = data
        self.labels = labels
        self.centroids = centroids

        columns = [col for col in self.data.columns if check_numeric(self.data[col])]
        for column in columns:
            self.data[column] = pd.to_numeric(self.data[column])

        self.layout = QHBoxLayout(self)

        self.num_samples = min(35, self.data.shape[0] // 2)
        self.samples = get_samples(self.data, self.num_samples)

        self.ox = columns[0]
        self.oy = columns[0] if len(columns) < 2 else columns[1]

        # algorithm parameters
        self.params_group = QGroupBox()
        self.params_group.setTitle("Parameters")
        self.params_layout = QFormLayout(self.params_group)

        for option, value in options.items():
            self.params_layout.addRow(QLabel(f'{option}:'), QLabel(f'{value}'))

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
        self.sample_box.setMaximum(min(self.data.shape[0], 200))
        self.sample_box.setProperty("value", self.num_samples)
        self.sample_button = QPushButton("Refresh samples")
        self.sample_button.clicked.connect(partial(self.click_listener, 'new_samples'))
        self.settings_box_layout.addRow(self.sample_box, self.sample_button)

        # axis
        self.settings_box_layout.addRow(QLabel("Set axis:"))
        self.ox_box = QComboBox()
        self.ox_box.addItems(columns)
        self.oy_box = QComboBox()
        self.oy_box.addItems(columns)
        if len(columns) > 1:
            self.oy_box.setCurrentIndex(1)
        self.ox_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.oy_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.settings_box_layout.addRow(QLabel("OX:"), self.ox_box)
        self.settings_box_layout.addRow(QLabel("OY:"), self.oy_box)

        self.settings_box_layout.setSpacing(10)
        self.clustering_group_layout.addWidget(self.settings_group_box)

        # plot
        self.fig, axes = plt.subplots(1, 1)
        self.clusters_canvas = KMeansCanvas(self.fig, axes, False)
        self.clustering_group_layout.addWidget(self.clusters_canvas, 1)

        self.layout.addWidget(self.clustering_result_group, 1)

        # centroids
        self.centroids_group = QGroupBox()
        self.centroids_group_layout = QVBoxLayout(self.centroids_group)
        self.centroids_group.setTitle("Centroids")

        self.centroids_table = QTableView()
        self.centroids_table.setModel(QtTable(self.centroids.round(3)))

        for i in range(len(columns)):
            self.centroids_table.setColumnWidth(i, 120)

        self.fig_centroids, ax = plt.subplots(1, 1)
        self.centroids_canvas = KMeansCanvas(self.fig_centroids, ax, False)

        self.centroids_group_layout.addWidget(self.centroids_table, 1)
        self.centroids_group_layout.addWidget(self.centroids_canvas, 1)

        self.layout.addWidget(self.centroids_group, 1)
        self.update_plot()

    def click_listener(self, button_type: str):
        match button_type:
            case 'new_samples':
                num = self.sample_box.value()
                self.num_samples = num
                self.samples = get_samples(self.data, self.num_samples)
                self.update_plot()
            case 'set_axis':
                self.ox = self.ox_box.currentText()
                self.oy = self.oy_box.currentText()
                self.update_plot()

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
        x_centroids = self.centroids[self.ox]
        y_centroids = self.centroids[self.oy]

        self.clusters_canvas.all_plot(x, y, x_centroids, y_centroids, labels, self.ox, self.oy,
                                      min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y)

        self.centroids_canvas.new_centroids_plot(None, None, x_centroids, y_centroids, self.ox, self.oy,
                                                 min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y,
                                                 )
