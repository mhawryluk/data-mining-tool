from PyQt5.QtWidgets import QSpinBox, QLabel, QComboBox

from widgets.options_widgets import AlgorithmOptions


class GMMOptions(AlgorithmOptions):
    def __init__(self):
        super().__init__()

        self.num_clusters_spinbox = QSpinBox()
        self.num_clusters_spinbox.setMinimum(2)
        self.num_clusters_spinbox.setValue(3)
        self.layout.addRow(QLabel("Number of clusters:"), self.num_clusters_spinbox)

        self.precision_box = QComboBox()
        self.precision_box.addItems(['1e-10', '1e-8', '1e-6', '1e-4', '1e-2', '1'])
        self.layout.addRow(QLabel("Precision:"), self.precision_box)

        self.num_steps_spinbox = QSpinBox()
        self.num_steps_spinbox.setMinimum(0)
        self.num_steps_spinbox.setMaximum(10000)
        self.num_steps_spinbox.setSpecialValueText('no limit')
        self.num_steps_spinbox.setValue(0)
        self.layout.addRow(QLabel("Maximum number of iterations:"), self.num_steps_spinbox)

    def get_data(self) -> dict:
        return {
            'num_clusters': self.num_clusters_spinbox.value(),
            'eps': self.precision_box.currentText(),
            'max_iterations': self.num_steps_spinbox.value() or None,
        }

    def set_max_clusters(self, clusters_num):
        self.num_clusters_spinbox.setMaximum(clusters_num)
