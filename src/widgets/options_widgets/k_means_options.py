from PyQt5.QtWidgets import QWidget, QFormLayout, QSpinBox, QLabel


class KMeansOptions(QWidget):
    def __init__(self, engine):
        super().__init__()

        self.layout = QFormLayout(self)

        self.num_clusters_spinbox = QSpinBox()
        self.num_clusters_spinbox.setMinimum(2)
        self.num_clusters_spinbox.setMaximum(engine.get_maximum_clusters())
        self.num_clusters_spinbox.setMaximum(10)
        self.num_clusters_spinbox.setValue(3)
        self.layout.addRow(QLabel("Number of clusters:"), self.num_clusters_spinbox)

        self.metrics_spinbox = QSpinBox()
        self.metrics_spinbox.setMinimum(1)
        self.metrics_spinbox.setValue(1)
        self.metrics_spinbox.setMaximum(6)
        self.layout.addRow(QLabel("Exponent in metrics:"), self.metrics_spinbox)

    def get_data(self) -> dict:
        return {
            'num_clusters': self.num_clusters_spinbox.value(),
            'metrics': self.metrics_spinbox.value()
        }
