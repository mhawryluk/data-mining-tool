from functools import partial

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QFormLayout, QLabel, QSpinBox, QPushButton, \
    QComboBox, QScrollArea, QSizePolicy
from algorithms import get_samples
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


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


class GMMStepsVisualization(QWidget):
    def __init__(self, df, algorithm_steps, has_animation):
        super().__init__()

        self.df = df.select_dtypes(include=['number'])
        self.algorithm_steps = algorithm_steps

        self.has_animation = has_animation
        self.is_running = False
        self.animation = None

        columns = self.df.columns

        self.layout = QHBoxLayout(self)

        self.num_cluster = np.amax(self.algorithm_steps[0]) + 1

        self.max_step = len(self.algorithm_steps) - 1
        self.current_step = 0
        self.num_samples = min(35, self.df.shape[0] // 2)
        self.samples = get_samples(self.df, self.num_samples)

        self.ox = columns[0]
        self.oy = columns[0] if len(columns) < 2 else columns[1]

        # left column layout
        self.left_column_layout = QVBoxLayout()

        # settings layout
        self.settings_box = QGroupBox()
        self.settings_box.setTitle("Settings")
        self.settings_box.setFixedWidth(250)
        self.settings_box_layout = QFormLayout(self.settings_box)

        # samples
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
        self.ox_box.addItems(columns)
        self.oy_box = QComboBox()
        self.oy_box.addItems(columns)
        if len(columns) > 1:
            self.oy_box.setCurrentIndex(1)
        self.ox_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.oy_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.settings_box_layout.addRow(QLabel("OX:"), self.ox_box)
        self.settings_box_layout.addRow(QLabel("OY:"), self.oy_box)

        self.left_column_layout.addWidget(self.settings_box, 0)

        # visualization layout
        self.visualization_box = QGroupBox()
        self.visualization_box.setTitle("Visualization")
        self.visualization_box_layout = QVBoxLayout(self.visualization_box)

        if self.has_animation:
            # animation
            self.animation_box = QGroupBox()
            self.animation_box.setTitle("Animation")
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

        self.fig, axes = plt.subplots()
        self.canvas = GMMCanvas(self.fig, axes, self.has_animation)
        self.visualization_box_layout.addWidget(self.canvas, 1)
        self.update_plot()

        if not self.has_animation:
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
        description = "Gaussian Mixture Methods algorithm - steps visualization."
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
                self.samples = get_samples(self.df, self.num_samples)
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

        samples_data = self.df.iloc[self.samples]
        x = samples_data[self.ox]
        y = samples_data[self.oy]
        min_x = self.df[self.ox].min()
        max_x = self.df[self.ox].max()
        min_y = self.df[self.oy].min()
        max_y = self.df[self.oy].max()
        sep_x = 0.1 * (max_x - min_x)
        sep_y = 0.1 * (max_y - min_y)

        # canvasy odtad

        return self.canvas.data_plot(x, y, self.ox, self.oy,
                                     min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y,
                                     not self.is_running)
