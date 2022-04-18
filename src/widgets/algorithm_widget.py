from PyQt5 import QtCore, QtWidgets
from widgets.unfold_widget import UnfoldWidget


class AlgorithmWidget(UnfoldWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # unfold button
        self.button.setText("ALGORITHM")
        self.button.setStyleSheet("background-color: rgb(177, 221, 240);")
        self.button.clicked.connect(lambda: self.parent().unfold(2))

        # algorithm frame
        self.frame.setStyleSheet("background-color: #EBF4F7;")

        # exploration technique selection
        self.technique_group = QtWidgets.QGroupBox(self.frame)
        self.technique_group.setGeometry(QtCore.QRect(30, 90, 221, 111))
        self.technique_group.setTitle("Exploration technique")

        self.technique_box = QtWidgets.QComboBox(self.technique_group)
        self.technique_box.setGeometry(QtCore.QRect(30, 50, 121, 41))
        self.technique_box.setStyleSheet("color: rgb(0,0,0);")
        self.technique_box.addItem("clustering")
        self.technique_box.addItem("associations")

        # algorithm selection group
        self.algorithm_selection_group = QtWidgets.QGroupBox(self.frame)
        self.algorithm_selection_group.setGeometry(QtCore.QRect(30, 270, 221, 111))
        self.algorithm_selection_group.setTitle("Algorithm")

        self.algorithm_box = QtWidgets.QComboBox(self.algorithm_selection_group)
        self.algorithm_box.setGeometry(QtCore.QRect(30, 50, 121, 41))
        self.algorithm_box.setStyleSheet("color: rgb(0,0,0);")

        # options group
        self.options_group = QtWidgets.QGroupBox(self.frame)
        self.options_group.setGeometry(QtCore.QRect(340, 100, 281, 251))
        self.options_group.setTitle("Options")

        self.num_clusters_spinbox = QtWidgets.QSpinBox(self.options_group)
        self.num_clusters_spinbox.setGeometry(QtCore.QRect(160, 70, 81, 31))
        self.num_clusters_spinbox.setStyleSheet("color: rgb(0,0,0)")

        self.num_clusters_label = QtWidgets.QLabel(self.options_group)
        self.num_clusters_label.setGeometry(QtCore.QRect(20, 60, 131, 51))
        self.num_clusters_label.setStyleSheet("color: rgb(0,0,0);")
        self.num_clusters_label.setAlignment(QtCore.Qt.AlignCenter)
        self.num_clusters_label.setText("number of clusters")

        self.num_clusters_label_2 = QtWidgets.QLabel(self.options_group)
        self.num_clusters_label_2.setGeometry(QtCore.QRect(20, 160, 131, 51))
        self.num_clusters_label_2.setStyleSheet("color: rgb(0,0,0);")
        self.num_clusters_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.num_clusters_label_2.setText("initialization method")

        self.checkbox_1 = QtWidgets.QCheckBox(self.options_group)
        self.checkbox_1.setGeometry(QtCore.QRect(170, 170, 81, 41))
        self.checkbox_1.setStyleSheet("color: rgb(0,0,0)")
        self.checkbox_1.setText("Forgy")
