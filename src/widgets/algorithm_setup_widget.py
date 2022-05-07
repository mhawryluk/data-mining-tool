from functools import partial

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QGroupBox, QCheckBox, QLabel, QSpinBox, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFormLayout, QDialog

from widgets import UnfoldWidget, UNFOLD_WIDGET_WIDTH, WINDOW_HEIGHT


class AlgorithmSetupWidget(UnfoldWidget):
    def __init__(self, parent, engine):
        super().__init__(parent)
        self.engine = engine
        self.setObjectName('algorithm_setup_widget')

        # unfold button
        self.button.setText("ALGORITHM SETUP")
        self.button.clicked.connect(lambda: self.parent().unfold(2))

        # layout
        self.layout = QVBoxLayout(self.frame)

        # layouts for sections
        self.vertical_layout = QHBoxLayout()
        self.first_column = QVBoxLayout()
        self.second_column = QVBoxLayout()

        # exploration technique selection
        self.technique_group = QGroupBox()
        self.technique_group.setTitle("Exploration technique")
        self.technique_group.setMinimumSize(220, 110)
        self.technique_group_layout = QFormLayout(self.technique_group)

        self.technique_box = QComboBox()
        self.technique_box.addItem("clustering")
        # self.technique_box.addItem("associations")
        self.technique_group_layout.addRow(self.technique_box)

        # algorithm selection group
        self.algorithm_selection_group = QGroupBox()
        self.algorithm_selection_group.setTitle("Algorithm")
        self.algorithm_selection_group.setMinimumSize(220, 110)
        self.algorithm_selection_group_layout = QFormLayout(self.algorithm_selection_group)

        self.algorithm_box = QComboBox()
        self.algorithm_box.addItem("K-Means")
        self.algorithm_selection_group_layout.addRow(self.algorithm_box)

        self.first_column.addStretch(2)
        self.first_column.addWidget(self.technique_group)
        self.first_column.addStretch(1)
        self.first_column.addWidget(self.algorithm_selection_group)
        self.first_column.addStretch(2)

        # options group
        self.options_group = QGroupBox()
        self.options_group.setTitle("Options")
        self.options_group.setMinimumSize(220, 200)
        self.options_group_layout = QFormLayout(self.options_group)

        self.num_clusters_spinbox = QSpinBox()
        self.num_clusters_spinbox.setMinimum(2)
        self.num_clusters_spinbox.setMaximum(engine.get_maximum_clusters())
        self.num_clusters_spinbox.setValue(5)
        self.options_group_layout.addRow(QLabel("Number of clusters:"), self.num_clusters_spinbox)

        self.metrics_spinbox = QSpinBox()
        self.metrics_spinbox.setMinimum(1)
        self.metrics_spinbox.setValue(1)
        self.metrics_spinbox.setMaximum(6)
        self.options_group_layout.addRow(QLabel("Exponent in metrics:"), self.metrics_spinbox)

        self.second_column.addStretch()
        self.second_column.addWidget(self.options_group)
        self.second_column.addStretch()

        self.vertical_layout.addStretch(2)
        self.vertical_layout.addLayout(self.first_column)
        self.vertical_layout.addStretch(1)
        self.vertical_layout.addLayout(self.second_column)
        self.vertical_layout.addStretch(2)

        # button
        self.run_button = QPushButton(self.frame)
        self.run_button.setText("Submit and run")
        self.run_button.setFixedWidth(300)
        self.run_button.clicked.connect(partial(self.click_listener, 'run'))

        self.layout.addStretch()
        self.layout.addLayout(self.vertical_layout)
        self.layout.addWidget(self.run_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

        # dialog error
        self.dialog = QDialog(self)
        self.dialog.setFixedHeight(50)
        self.dialog.setFixedWidth(400)
        self.dialog.setWindowTitle("Error message")
        QLabel("You didn't set data.\nPlease return to 'IMPORT DATA' window.", self.dialog)

    def click_listener(self, button_type: str):
        if button_type == 'run':
            if self.engine.state.imported_data is None:
                self.dialog.exec_()
                return
            technique = self.technique_box.currentText()
            algorithm = self.algorithm_box.currentText()
            num_clusters = self.num_clusters_spinbox.value()
            metrics = self.metrics_spinbox.value()
            self.engine.run(technique, algorithm, num_clusters=num_clusters, metrics=metrics)
