from PyQt5.QtWidgets import QWidget, QGroupBox, QSpinBox, QPushButton, QComboBox, QLabel
from PyQt5.QtCore import QRect
import numpy as np
import pandas as pd
from typing import List, Tuple


class KMeansStepsVisualization(QWidget):
    def __init__(self, parent: QWidget, data: pd.DataFrame, algorithms_steps: Tuple[List[int], List[Tuple]]):
        super().__init__(parent)

        self.algorithms_steps = algorithms_steps
        self.data = data

        self.setObjectName("k_means_steps_visualization")

        # visualization
        self.visualization_box = QGroupBox(self)
        self.visualization_box.setTitle("Visualization:")
        self.visualization_box.setGeometry(QRect(260, 10, 731, 471))

        self.left_box = QSpinBox(self.visualization_box)
        self.left_box.setGeometry(QRect(20, 110, 46, 26))
        self.left_box.setMinimum(1)
        self.right_box = QSpinBox(self.visualization_box)
        self.right_box.setGeometry(QRect(680, 110, 46, 26))
        self.right_box.setMinimum(1)
        self.left_button = QPushButton(self.visualization_box)
        self.left_button.setText("PREV")
        self.left_button.setGeometry(QRect(20, 150, 61, 28))
        self.right_button = QPushButton(self.visualization_box)
        self.right_button.setText("NEXT")
        self.right_button.setGeometry(QRect(670, 140, 61, 28))

        # settings
        self.settings_box = QGroupBox(self)
        self.settings_box.setTitle("Settings:")
        self.settings_box.setGeometry(QRect(10, 10, 201, 461))

        self.sample_box = QSpinBox(self.settings_box)
        self.sample_box.setGeometry(QRect(0, 40, 46, 26))
        self.sample_box.setMinimum(1)
        self.sample_box.setMaximum(200)
        self.sample_box.setProperty("value", 20)
        self.sample_label = QLabel(self.settings_box)
        self.sample_label.setText("Set samples:")
        self.sample_label.setGeometry(QRect(0, 20, 121, 16))
        self.sample_button = QPushButton(self.settings_box)
        self.sample_button.setText("Refresh samples")
        self.sample_button.setGeometry(QRect(70, 40, 131, 28))

        self.axis_label = QLabel(self.settings_box)
        self.axis_label.setText("Set axis:")
        self.axis_label.setGeometry(QRect(0, 80, 161, 16))
        self.ox_box = QComboBox(self.settings_box)
        self.ox_box.setGeometry(QRect(70, 90, 121, 24))
        self.ox_label = QLabel(self.settings_box)
        self.ox_label.setText("OX:")
        self.ox_label.setGeometry(QRect(0, 100, 58, 16))
        self.oy_label = QLabel(self.settings_box)
        self.oy_label.setText("OY:")
        self.oy_label.setGeometry(QRect(0, 120, 58, 16))
        self.oy_box = QComboBox(self.settings_box)
        self.oy_box.setGeometry(QRect(70, 120, 121, 24))
        self.axis_button = QPushButton(self.settings_box)
        self.axis_button.setText("Submit axis")
        self.axis_button.setGeometry(QRect(90, 160, 90, 28))






