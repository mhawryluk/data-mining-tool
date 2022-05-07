import numpy as np
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFormLayout, QWidget, QGroupBox, QSpinBox, QPushButton, QComboBox, QLabel
import pandas as pd
from typing import List, Tuple


class KMeansStepsVisualization(QWidget):
    def __init__(self, data: pd.DataFrame, algorithms_steps: List[Tuple[np.ndarray, List[Tuple]]]):
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.algorithms_steps = algorithms_steps
        self.data = data

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
        self.sample_box.setMaximum(200)
        self.sample_box.setProperty("value", 20)
        self.sample_button = QPushButton("Refresh samples")
        self.settings_box_layout.addRow(self.sample_box, self.sample_button)

        # axis
        self.settings_box_layout.addRow(QLabel("Set axis:"))

        self.ox_box = QComboBox()
        self.oy_box = QComboBox()
        self.settings_box_layout.addRow(QLabel("OX:"), self.ox_box)
        self.settings_box_layout.addRow(QLabel("OY:"), self.oy_box)

        self.axis_button = QPushButton("Submit axis")
        self.settings_box_layout.addRow(self.axis_button)

        # visualization layout
        self.visualization_box = QGroupBox()
        self.visualization_box.setTitle("Visualization:")
        self.visualization_box_layout = QVBoxLayout(self.visualization_box)

        # plot
        # todo

        self.visualization_box_layout.addStretch()

        # control buttons
        self.control_buttons_layout = QHBoxLayout()
        self.left_box = QSpinBox()
        self.left_box.setMinimum(1)
        self.right_box = QSpinBox()
        self.right_box.setMinimum(1)
        self.left_button = QPushButton("PREV")
        self.right_button = QPushButton("NEXT")
        self.control_buttons_layout.addWidget(self.left_button)
        self.control_buttons_layout.addWidget(self.left_box)
        self.control_buttons_layout.addStretch()
        self.control_buttons_layout.addWidget(self.right_box)
        self.control_buttons_layout.addWidget(self.right_button)

        self.visualization_box_layout.addLayout(self.control_buttons_layout)

        self.layout.addWidget(self.settings_box)
        self.layout.addWidget(self.visualization_box)
