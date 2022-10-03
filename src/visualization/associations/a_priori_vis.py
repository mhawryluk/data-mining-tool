from functools import partial
from typing import List

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFormLayout, QWidget, QGroupBox, \
    QSpinBox, QPushButton, QLabel, QScrollArea, QSizePolicy, QTableView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from widgets import QtTable


class APrioriCanvas(FigureCanvasQTAgg):
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


class APrioriStepsVisualization(QWidget):
    def __init__(self, data: pd.DataFrame, algorithms_steps: List[pd.DataFrame], is_animation: bool):
        super().__init__()

        self.is_animation = is_animation
        self.is_running = False
        self.animation = None

        self.layout = QVBoxLayout(self)

        self.algorithms_steps = algorithms_steps

        self.data = data

        self.max_step = len(algorithms_steps) - 1
        self.current_step = 0

        self.setObjectName("a_priori_steps_visualization")

        # left column layout
        self.bottom_row_layout = QHBoxLayout()

        # visualization layout
        self.visualization_box = QGroupBox()
        self.visualization_box.setTitle("Visualization")
        self.visualization_box_layout = QVBoxLayout(self.visualization_box)

        # sets table
        self.sets_table = QTableView()
        self.visualization_box_layout.addWidget(self.sets_table, 1)

        if self.is_animation:
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

            self.bottom_row_layout.addWidget(self.animation_box, 0)

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
        description = "A-priori algorithm - steps visualization"

        self.description_label = QLabel(description)
        self.description_label.setWordWrap(False)
        self.description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.description_group_box = QGroupBox()
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
        self.bottom_row_layout.addWidget(self.description_group_box, 1)

        self.bottom_row_layout.setSpacing(35)

        self.layout.addWidget(self.visualization_box, 5)
        self.layout.addLayout(self.bottom_row_layout, 1)
        self.update_plot()

    def click_listener(self, button_type: str):
        match button_type:
            case 'prev':
                self.change_step(-self.left_box.value())
            case 'next':
                self.change_step(self.right_box.value())
            case 'restart':
                self.animation = None
                self.change_step(-self.current_step)
                self.change_enabled_buttons(True)
                self.interval_box.setEnabled(True)
                self.run_button.setEnabled(True)
            case 'run':
                self.is_running = not self.is_running
                self.change_enabled_buttons(False)
                self.interval_box.setEnabled(False)
                self.restart_button.setEnabled(not self.is_running)
                # if self.is_running:
                #     if self.animation is None:
                #         self.animation = FuncAnimation(self.fig, self.update_plot, frames=self.max_step + 1,
                #                                        interval=self.interval_box.value(), blit=True,
                #                                        cache_frame_data=False, repeat=False)
                #         self.canvas.draw()
                #     else:
                #         self.animation.resume()
                #     self.run_button.setText("Stop animation")
                # else:
                #     self.animation.pause()
                #     self.run_button.setText("Start animation")

    def change_enabled_buttons(self, value):
        pass

    def change_step(self, change: int):
        new_step = max(0, min(self.max_step, self.current_step + change))
        if new_step == self.current_step:
            return
        self.current_step = new_step
        self.step_label.setText("STEP: {}".format(self.current_step))
        self.update_plot(self.current_step)
        self.step_label.update()

    def update_plot(self, step: int = -1):
        if step == self.max_step:
            if self.is_animation:
                self.run_button.setText("Start animation")
                self.run_button.setEnabled(False)
                self.is_running = False
                self.change_enabled_buttons(True)
        if step == -1:
            step = self.current_step
        else:
            self.current_step = step
        self.sets_table.setModel(QtTable(self.algorithms_steps[step]))
