from functools import partial

import numpy as np
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFormLayout, QWidget, QGroupBox, QSpinBox, QPushButton, QComboBox, QLabel
import pandas as pd
from typing import List, Tuple
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class KMeansCanvas(FigureCanvasQTAgg):
    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

    def data_plot(self, vector_x, vector_y, name_x, name_y, min_x, max_x, min_y, max_y):
        self.axes.cla()
        self.axes.scatter(x=vector_x, y=vector_y)
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.draw()

    def make_plot(self, vector_x, vector_y, vector_x_centroids, vector_y_centroids, labels, name_x, name_y, min_x, max_x, min_y, max_y):
        self.axes.cla()
        label = [labels[i] for i in range(len(vector_x))]
        max_label = len(vector_x_centroids)
        self.axes.scatter(vector_x, vector_y, c=label, cmap='gist_ncar', vmin=0, vmax=max_label)
        self.axes.scatter(vector_x_centroids, vector_y_centroids, c=np.arange(max_label), marker='s', cmap='gist_ncar', vmin=0, vmax=max_label)
        self.axes.set_xlabel(name_x)
        self.axes.set_ylabel(name_y)
        self.axes.set_xlim(min_x, max_x)
        self.axes.set_ylim(min_y, max_y)
        self.draw()


class KMeansStepsVisualization(QWidget):
    def __init__(self, data: pd.DataFrame, algorithms_steps: List[Tuple[np.ndarray, pd.DataFrame]]):
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.algorithms_steps = algorithms_steps
        self.data = data
        self.max_step = len(algorithms_steps)
        self.current_step = 0
        self.num_samples = min(20, self.data.shape[0])
        self.samples = self.get_samples()
        self.ox = self.oy = self.data.columns[0]

        self.setObjectName("k_means_steps_visualization")

        # settings layout
        self.settings_box = QGroupBox()
        self.settings_box.setTitle("Settings:")
        self.settings_box.setFixedWidth(200)
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

        columns = [col for col in self.data.columns if self.is_numeric(self.data[col][0])]

        self.ox_box = QComboBox()
        self.ox_box.addItems(columns)
        self.oy_box = QComboBox()
        self.oy_box.addItems(columns)
        self.settings_box_layout.addRow(QLabel("OX:"), self.ox_box)
        self.settings_box_layout.addRow(QLabel("OY:"), self.oy_box)

        self.axis_button = QPushButton("Submit axis")
        self.axis_button.clicked.connect(partial(self.click_listener, 'set_axis'))
        self.settings_box_layout.addRow(self.axis_button)

        # visualization layout
        self.visualization_box = QGroupBox()
        self.visualization_box.setTitle("Visualization:")
        self.visualization_box_layout = QVBoxLayout(self.visualization_box)

        # plot
        self.canvas = KMeansCanvas()
        self.update_plot()

        self.visualization_box_layout.addWidget(self.canvas)

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

        self.visualization_box_layout.addLayout(self.control_buttons_layout)

        self.layout.addWidget(self.settings_box)
        self.layout.addWidget(self.visualization_box)

    def is_numeric(self, element: any) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False

    def get_samples(self) -> List[int]:
        array = np.arange(self.data.shape[0])
        np.random.shuffle(array)
        return list(array[:self.num_samples])

    def click_listener(self, button_type: str):
        if button_type == 'new_samples':
            num = self.sample_box.value()
            self.num_samples = num
            self.samples = self.get_samples()
            self.update_plot()
        elif button_type == 'set_axis':
            self.ox = self.ox_box.currentText()
            self.oy = self.oy_box.currentText()
            self.update_plot()
        elif button_type == 'prev':
            num = self.left_box.value()
            self.change_step(-1 * num)
        elif button_type == 'next':
            num = self.right_box.value()
            self.change_step(num)

    def change_step(self, change: int):
        new_step = max(0, min(self.max_step, self.current_step + change))
        if new_step == self.current_step:
            return
        self.current_step = new_step
        self.step_label.setText("STEP: {}".format(self.current_step))
        self.update_plot()
        self.step_label.update()

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

        if self.current_step == 0:
            self.canvas.data_plot(x, y, self.ox, self.oy, min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y)
            return

        step_labels, step_centroids = self.algorithms_steps[self.current_step - 1]
        labels = [step_labels[sample] for sample in self.samples]
        x_centroids = step_centroids[self.ox]
        y_centroids = step_centroids[self.oy]

        self.canvas.make_plot(x, y, x_centroids, y_centroids, labels, self.ox, self.oy, min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y)
