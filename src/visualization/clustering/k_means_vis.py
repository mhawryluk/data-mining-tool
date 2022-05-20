from functools import partial

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFormLayout, QWidget, QGroupBox, \
    QSpinBox, QPushButton, QComboBox, QLabel, QScrollArea, QSizePolicy
import pandas as pd
from typing import List, Tuple

from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from algorithms import get_samples, check_numeric


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

    def chosen_centroid_plot(self, vector_x, vector_y, old_x_centroid, old_y_centroid, x_centroid, y_centroid,
                             label, max_label, name_x, name_y, min_x, max_x, min_y, max_y, drawing=True):
        self.axes.cla()
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.axes.scatter(vector_x, vector_y, c=[label] * len(vector_x), cmap='gist_rainbow',
                          vmin=0, vmax=max_label, alpha=0.6)
        self.axes.scatter([old_x_centroid], [old_y_centroid], c='black', marker='s', alpha=0.3)
        self.axes.scatter([x_centroid], [y_centroid], c='black', marker='s')
        if drawing:
            self.draw()
        if self.animation:
            return self.axes.collections


class KMeansStepsVisualization(QWidget):
    def __init__(self, data: pd.DataFrame, algorithms_steps: List[Tuple[np.ndarray, pd.DataFrame]], is_animation: bool):
        super().__init__()

        self.is_animation = is_animation
        self.is_running = False
        self.animation = None

        self.layout = QHBoxLayout(self)

        self.algorithms_steps = algorithms_steps
        self.num_cluster = algorithms_steps[0][1].shape[0]
        self.data = data
        columns = [col for col in self.data.columns if check_numeric(self.data[col])]
        for column in columns:
            self.data[column] = pd.to_numeric(self.data[column])
        self.max_step = (len(algorithms_steps) - 1) * (2 + self.num_cluster) + 2
        self.current_step = 0
        self.num_samples = min(35, self.data.shape[0] // 2)
        self.samples = get_samples(self.data, self.num_samples)
        self.ox = self.oy = columns[0]

        self.setObjectName("k_means_steps_visualization")

        # left column layout
        self.left_column_layout = QVBoxLayout()

        # settings layout
        self.settings_box = QGroupBox()
        self.settings_box.setTitle("Settings:")
        self.settings_box.setFixedWidth(250)
        self.settings_box_layout = QFormLayout(self.settings_box)

        # samples
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
        self.ox_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.oy_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.settings_box_layout.addRow(QLabel("OX:"), self.ox_box)
        self.settings_box_layout.addRow(QLabel("OY:"), self.oy_box)

        # visualization layout
        self.visualization_box = QGroupBox()
        self.visualization_box.setTitle("Visualization:")
        self.visualization_box_layout = QVBoxLayout(self.visualization_box)

        self.left_column_layout.addWidget(self.settings_box, 0)

        if self.is_animation:
            # animation
            self.animation_box = QGroupBox()
            self.animation_box.setTitle("Animation:")
            self.animation_box.setFixedWidth(250)
            self.animation_box_layout = QFormLayout(self.animation_box)

            self.restart_button = QPushButton("Restart")
            self.restart_button.clicked.connect(partial(self.click_listener, 'restart'))
            self.run_button = QPushButton("Start animation")
            self.run_button.clicked.connect(partial(self.click_listener, 'run'))
            self.interval_box = QSpinBox()
            self.interval_box.setMinimum(20)
            self.interval_box.setMaximum(2000)
            self.interval_box.setValue(200)
            self.interval_box.setSingleStep(20)

            self.animation_box_layout.addRow(QLabel("Interval time [ms]:"), self.interval_box)
            self.animation_box_layout.addRow(self.restart_button)
            self.animation_box_layout.addRow(self.run_button)

            self.left_column_layout.addWidget(self.animation_box, 0)

        # plot
        self.fig, axes = plt.subplots()
        self.canvas = KMeansCanvas(self.fig, axes, self.is_animation)
        self.visualization_box_layout.addWidget(self.canvas, 1)
        self.update_plot()

        if not self.is_animation:
            self.visualization_box_layout.addStretch()

            # control buttons
            self.control_buttons_layout = QHBoxLayout()
            self.left_box = QSpinBox()
            self.left_box.setMinimum(1)
            self.right_box = QSpinBox()
            self.right_box.setMinimum(1)
            self.left_button = QPushButton("PREV")
            self.left_button.clicked.connect(partial(self.click_listener, 'prev'))
            self.right_button = QPushButton("NEXT")
            self.right_button.clicked.connect(partial(self.click_listener, 'next'))
            self.step_label = QLabel("STEP: {}".format(self.current_step))
            self.control_buttons_layout.addWidget(self.left_button)
            self.control_buttons_layout.addWidget(self.left_box)
            self.control_buttons_layout.addStretch()
            self.control_buttons_layout.addWidget(self.step_label)
            self.control_buttons_layout.addStretch()
            self.control_buttons_layout.addWidget(self.right_box)
            self.control_buttons_layout.addWidget(self.right_button)

            self.visualization_box_layout.addLayout(self.control_buttons_layout, 0)
        else:
            self.step_label = QLabel("STEP: {}".format(self.current_step))
            self.visualization_box_layout.addWidget(self.step_label, 0, alignment=Qt.AlignCenter)

        # description
        description = "K-Means algorithm - steps visualization.\nEach color represents one cluster.\n" \
                      "Circles are the points of the data set. Squares are centroids of the clusters."
        self.description_label = QLabel(description)
        self.description_label.setWordWrap(True)

        self.description_group_box = QGroupBox()
        self.description_group_box.setFixedWidth(250)
        self.description_group_box.setTitle("Description")
        self.description_group_box_layout = QVBoxLayout(self.description_group_box)

        self.scroll_box = QGroupBox()
        self.scroll_box_layout = QFormLayout(self.scroll_box)
        self.scroll = QScrollArea()
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll.setWidget(self.scroll_box)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumHeight(26)
        self.description_group_box_layout.addWidget(self.scroll)

        self.scroll_box_layout.addWidget(self.description_label)

        self.left_column_layout.addWidget(self.description_group_box, 1)

        self.left_column_layout.setSpacing(35)

        self.layout.addLayout(self.left_column_layout)
        self.layout.addWidget(self.visualization_box)

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
            case 'prev':
                num = self.left_box.value()
                self.change_step(-1 * num)
            case 'next':
                num = self.right_box.value()
                self.change_step(num)
            case 'restart':
                self.animation = None
                self.change_step(-1 * self.current_step)
                self.change_enabled_buttons(True)
                self.interval_box.setEnabled(True)
                self.run_button.setEnabled(True)
            case 'run':
                self.is_running = not self.is_running
                self.change_enabled_buttons(False)
                self.interval_box.setEnabled(False)
                self.restart_button.setEnabled(not self.is_running)
                if self.is_running:
                    if self.animation is None:
                        self.animation = FuncAnimation(self.fig, self.update_plot, frames=self.max_step + 1,
                                                       interval=self.interval_box.value(), blit=True,
                                                       cache_frame_data=False, repeat=False)
                        self.canvas.draw()
                    else:
                        self.animation.resume()
                    self.run_button.setText("Stop animation")
                else:
                    self.animation.pause()
                    self.run_button.setText("Start animation")

    def change_enabled_buttons(self, value):
        self.ox_box.setEnabled(value)
        self.oy_box.setEnabled(value)
        self.sample_button.setEnabled(value)
        self.sample_box.setEnabled(value)

    def change_step(self, change: int):
        new_step = max(0, min(self.max_step, self.current_step + change))
        if new_step == self.current_step:
            return
        self.current_step = new_step
        self.step_label.setText("STEP: {}".format(self.current_step))
        self.update_plot()
        self.step_label.update()

    def update_plot(self, step: int = -1):
        if step == self.max_step:
            self.run_button.setText("Start animation")
            self.change_enabled_buttons(True)
            self.run_button.setEnabled(False)
            self.restart_button.setEnabled(True)
            self.is_running = False
        if step == -1:
            step = self.current_step
        else:
            self.current_step = step
            self.step_label.setText("STEP: {}".format(self.current_step))
        samples_data = self.data.iloc[self.samples]
        x = samples_data[self.ox]
        y = samples_data[self.oy]
        min_x = self.data[self.ox].min()
        max_x = self.data[self.ox].max()
        min_y = self.data[self.oy].min()
        max_y = self.data[self.oy].max()
        sep_x = 0.1 * (max_x - min_x)
        sep_y = 0.1 * (max_y - min_y)

        if step == 0:
            return self.canvas.data_plot(x, y, self.ox, self.oy,
                                         min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y,
                                         not self.is_running)

        step_labels, step_centroids = self.algorithms_steps[0]
        labels = [step_labels[sample] for sample in self.samples]
        x_centroids = step_centroids[self.ox]
        y_centroids = step_centroids[self.oy]

        if step == 1:
            return self.canvas.new_centroids_plot(None, None, x_centroids, y_centroids, self.ox, self.oy,
                                                  min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y,
                                                  not self.is_running)

        if step == 2:
            return self.canvas.all_plot(x, y, x_centroids, y_centroids, labels, self.ox, self.oy,
                                        min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y, not self.is_running)

        index = (step - 3) // (self.num_cluster + 2) + 1
        mode = (step - 3) % (self.num_cluster + 2)

        step_labels, step_centroids = self.algorithms_steps[index]
        labels = [step_labels[sample] for sample in self.samples]
        x_centroids = step_centroids[self.ox]
        y_centroids = step_centroids[self.oy]

        old_step_labels, old_step_centroids = self.algorithms_steps[index - 1]
        old_x_centroids = old_step_centroids[self.ox]
        old_y_centroids = old_step_centroids[self.oy]

        if mode < self.num_cluster:
            vector_x = self.data.loc[old_step_labels == mode][self.ox]
            vector_y = self.data.loc[old_step_labels == mode][self.oy]
            return self.canvas.chosen_centroid_plot(vector_x, vector_y, old_x_centroids.iloc[mode],
                                                    old_y_centroids.iloc[mode], x_centroids.iloc[mode],
                                                    y_centroids.iloc[mode],
                                                    mode, len(x_centroids), self.ox, self.oy,
                                                    min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y,
                                                    not self.is_running)
        elif mode == self.num_cluster:
            return self.canvas.new_centroids_plot(old_x_centroids, old_y_centroids, x_centroids, y_centroids, self.ox,
                                                  self.oy,
                                                  min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y,
                                                  not self.is_running)
        else:
            return self.canvas.all_plot(x, y, x_centroids, y_centroids, labels, self.ox, self.oy,
                                        min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y, not self.is_running)


class KMeansResultsWidget(QWidget):
    def __init__(self, data, labels, centroids):
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
        self.ox = self.oy = columns[0]

        # clustering result group
        self.clustering_result_group = QGroupBox()
        self.clustering_group_layout = QVBoxLayout(self.clustering_result_group)
        self.clustering_result_group.setTitle("Clustering result")

        self.settings_box_layout = QFormLayout()
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
        self.ox_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.oy_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.settings_box_layout.addRow(QLabel("OX:"), self.ox_box)
        self.settings_box_layout.addRow(QLabel("OY:"), self.oy_box)

        self.clustering_group_layout.addLayout(self.settings_box_layout)

        # plot
        self.fig, axes = plt.subplots()
        self.canvas = KMeansCanvas(self.fig, axes, False)
        self.clustering_group_layout.addWidget(self.canvas, 1)

        self.layout.addWidget(self.clustering_result_group)

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

        return self.canvas.all_plot(x, y, x_centroids, y_centroids, labels, self.ox, self.oy,
                                    min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y)
