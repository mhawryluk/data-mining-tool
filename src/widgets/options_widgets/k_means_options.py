from PyQt5.QtWidgets import QSpinBox, QLabel, QComboBox

from widgets.options_widgets import AlgorithmOptions


class KMeansOptions(AlgorithmOptions):
    def __init__(self):
        super().__init__()

        self.num_clusters_spinbox = QSpinBox()
        self.num_clusters_spinbox.setMinimum(2)
        self.num_clusters_spinbox.setValue(3)
        self.layout.addRow(QLabel("Number of clusters:"), self.num_clusters_spinbox)

        self.start_type_box = QComboBox()
        self.start_type_box.addItems(['random', 'kmeans++'])
        self.layout.addRow(QLabel('Type of initial solution:'), self.start_type_box)

        self.metrics_spinbox = QSpinBox()
        self.metrics_spinbox.setMinimum(1)
        self.metrics_spinbox.setValue(2)
        self.metrics_spinbox.setMaximum(6)
        self.layout.addRow(QLabel("Exponent in metrics:"), self.metrics_spinbox)

        self.num_steps_spinbox = QSpinBox()
        self.num_steps_spinbox.setMinimum(0)
        self.num_steps_spinbox.setMaximum(1000)
        self.num_steps_spinbox.setSpecialValueText('no limit')
        self.num_steps_spinbox.setValue(0)
        self.layout.addRow(QLabel("Maximum number of iterations:"), self.num_steps_spinbox)

        self.num_repeat_spinbox = QSpinBox()
        self.num_repeat_spinbox.setMinimum(1)
        self.num_repeat_spinbox.setMaximum(100)
        self.num_repeat_spinbox.setValue(1)
        self.layout.addRow(QLabel("Number of repetitions:"), self.num_repeat_spinbox)

    def get_data(self) -> dict:
        return {
            'num_clusters': self.num_clusters_spinbox.value(),
            'metrics': self.metrics_spinbox.value(),
            'repeats': self.num_repeat_spinbox.value(),
            'iterations': self.num_steps_spinbox.value() or None,
            'init_type': self.start_type_box.currentText()
        }

    def set_max_clusters(self, clusters_num):
        self.num_clusters_spinbox.setMaximum(clusters_num)
