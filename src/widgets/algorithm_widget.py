from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QGroupBox, QCheckBox, QLabel, QSpinBox, QComboBox

from widgets import UnfoldWidget


class AlgorithmWidget(UnfoldWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('algorithm_widget')

        # unfold button
        self.button.setText("ALGORITHM")
        self.button.clicked.connect(lambda: self.parent().unfold(2))

        # exploration technique selection
        self.technique_group = QGroupBox(self.frame)
        self.technique_group.setGeometry(QRect(30, 90, 221, 111))
        self.technique_group.setTitle("Exploration technique")

        self.technique_box = QComboBox(self.technique_group)
        self.technique_box.setGeometry(QRect(30, 50, 121, 41))
        self.technique_box.addItem("clustering")
        self.technique_box.addItem("associations")

        # algorithm selection group
        self.algorithm_selection_group = QGroupBox(self.frame)
        self.algorithm_selection_group.setGeometry(QRect(30, 270, 221, 111))
        self.algorithm_selection_group.setTitle("Algorithm")

        self.algorithm_box = QComboBox(self.algorithm_selection_group)
        self.algorithm_box.setGeometry(QRect(30, 50, 121, 41))

        # options group
        self.options_group = QGroupBox(self.frame)
        self.options_group.setGeometry(QRect(340, 100, 281, 251))
        self.options_group.setTitle("Options")

        self.num_clusters_spinbox = QSpinBox(self.options_group)
        self.num_clusters_spinbox.setGeometry(QRect(160, 70, 81, 31))

        self.num_clusters_label = QLabel(self.options_group)
        self.num_clusters_label.setGeometry(QRect(20, 60, 131, 51))
        self.num_clusters_label.setAlignment(Qt.AlignCenter)
        self.num_clusters_label.setText("number of clusters")

        self.num_clusters_label_2 = QLabel(self.options_group)
        self.num_clusters_label_2.setGeometry(QRect(20, 160, 131, 51))
        self.num_clusters_label_2.setAlignment(Qt.AlignCenter)
        self.num_clusters_label_2.setText("initialization method")

        self.checkbox_1 = QCheckBox(self.options_group)
        self.checkbox_1.setGeometry(QRect(170, 170, 81, 41))
        self.checkbox_1.setText("Forgy")
