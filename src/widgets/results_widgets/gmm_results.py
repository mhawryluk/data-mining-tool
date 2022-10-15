from functools import partial

import numpy as np
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QFormLayout, QLabel, QVBoxLayout, QSpinBox, QPushButton, \
    QComboBox
from algorithms import get_samples
from matplotlib import pyplot as plt

from visualization.clustering import GMMCanvas


class GMMResultsWidget(QWidget):
    def __init__(self, df, labels, mean, sigma, options):
        super().__init__()
        self.df = df.select_dtypes(include=['number'])
        self.columns = self.df.columns
        self.labels = labels
        self.max_label = np.amax(self.labels) + 1
        self.mean = mean
        self.sigma = sigma
        self.selected_cluster = None
        self.layout = QHBoxLayout(self)

        self.num_samples = min(35, self.df.shape[0] // 2)
        self.samples = get_samples(self.df, self.num_samples)
        self.ox = self.columns[0]
        self.oy = self.columns[0] if len(self.columns) < 2 else self.columns[1]

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
        self.sample_box.setMaximum(min(self.df.shape[0], 10000))
        self.sample_box.setProperty("value", self.num_samples)
        self.sample_button = QPushButton("Refresh samples")
        self.sample_button.clicked.connect(partial(self.click_listener, 'new_samples'))
        self.settings_box_layout.addRow(self.sample_box, self.sample_button)
        # axis
        self.settings_box_layout.addRow(QLabel("Set axis:"))
        self.ox_box = QComboBox()
        self.ox_box.addItems(self.columns)
        self.oy_box = QComboBox()
        self.oy_box.addItems(self.columns)
        if len(self.columns) > 1:
            self.oy_box.setCurrentIndex(1)
        self.ox_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.oy_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.settings_box_layout.addRow(QLabel("OX:"), self.ox_box)
        self.settings_box_layout.addRow(QLabel("OY:"), self.oy_box)
        self.settings_box_layout.setSpacing(10)
        self.clustering_group_layout.addWidget(self.settings_group_box)

        # plot
        self.fig, axes = plt.subplots(1, 1)
        self.clusters_canvas = GMMCanvas(self.fig, axes, False)
        self.clustering_group_layout.addWidget(self.clusters_canvas, 1)

        self.layout.addWidget(self.clustering_result_group, 1)
        self.update_plot()

    def click_listener(self, button_type: str):
        match button_type:
            case 'new_samples':
                num = self.sample_box.value()
                self.num_samples = num
                self.samples = get_samples(self.df, self.num_samples)
                self.update_plot()
            case 'set_axis':
                self.ox = self.ox_box.currentText()
                self.oy = self.oy_box.currentText()
                self.update_plot()

    def update_plot(self):
        samples_data = self.df.iloc[self.samples]
        x = samples_data[self.ox]
        y = samples_data[self.oy]
        min_x = self.df[self.ox].min()
        max_x = self.df[self.ox].max()
        min_y = self.df[self.oy].min()
        max_y = self.df[self.oy].max()
        sep_x = 0.1 * (max_x - min_x)
        sep_y = 0.1 * (max_y - min_y)

        labels = [self.labels[sample] for sample in self.samples]

        self.clusters_canvas.clusters_plot(x, y, list(self.columns), self.mean, self.sigma, labels, self.max_label, self.ox,
                                           self.oy, min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y)
