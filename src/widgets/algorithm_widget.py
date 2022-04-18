from PyQt5 import QtCore, QtWidgets


class AlgorithmWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(815, 491)

        # vertical label
        self.label = QtWidgets.QLabel(self)
        self.label.setText("ALGORITHM")
        self.label.setGeometry(QtCore.QRect(0, 0, 111, 491))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("background-color:  rgb(177, 221, 240);")
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)

        # algorithm frame
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(109, -1, 711, 491))
        self.frame.setStyleSheet("background-color: rgb(245, 252, 255);")

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
        self.algorithm_selection_group.setGeometry(QtCore.QRect(40, 270, 221, 111))
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
