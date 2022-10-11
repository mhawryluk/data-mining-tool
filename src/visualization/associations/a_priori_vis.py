from functools import partial
from typing import List

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFormLayout, QWidget, QGroupBox, \
    QSpinBox, QPushButton, QLabel, QScrollArea, QSizePolicy, QTableView

from widgets import QtTable


class APrioriStepsVisualization(QWidget):
    def __init__(self, data: pd.DataFrame, algorithms_steps: List[pd.DataFrame], is_animation: bool):
        super().__init__()

        self.is_animation = is_animation
        self.is_running = False
        self.animation = None
        self.algorithms_steps = algorithms_steps
        self.data = data
        self.max_step = len(algorithms_steps) - 1
        self.current_step = 0

        self.setObjectName("a_priori_steps_visualization")

        # layout
        self.layout = QVBoxLayout(self)
        self.bottom_row_layout = QHBoxLayout()
        self.bottom_row_layout.setSpacing(35)

        # visualization layout
        self.visualization_box = QGroupBox()
        self.visualization_box.setTitle("Visualization")
        self.visualization_box_layout = QVBoxLayout(self.visualization_box)

        # sets table
        self.sets_table = QTableView()
        self.visualization_box_layout.addWidget(self.sets_table, 1)

        # description
        self.bottom_row_layout.addWidget(self._render_description(), 1)

        # controls
        self._render_control_ui()

        self.layout.addWidget(self.visualization_box, 5)
        self.layout.addLayout(self.bottom_row_layout, 1)
        self.update_plot(0)

    def _render_control_ui(self):
        if self.is_animation:
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
            self.step_label = QLabel("STEP: {}".format(self.current_step))
            self.visualization_box_layout.addWidget(self.step_label, 0, alignment=Qt.AlignCenter)

        else:
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

    def _render_description(self):
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
        return self.description_group_box

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
                self.restart_button.setEnabled(not self.is_running)
                if self.is_running:
                    self.run_button.setText("Stop animation")
                else:
                    self.run_button.setText("Start animation")

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

    def update_plot(self, step: int):
        if step == self.max_step:
            if self.is_animation:
                self.run_button.setText("Start animation")
                self.run_button.setEnabled(False)
                self.is_running = False
                self.change_enabled_buttons(True)

        self.current_step = step
        self.sets_table.setModel(QtTable(self.algorithms_steps[self.current_step]))
