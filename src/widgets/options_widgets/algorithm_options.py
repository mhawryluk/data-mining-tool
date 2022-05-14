from PyQt5.QtWidgets import QWidget, QFormLayout, QSpinBox, QLabel


class Algorithm(QWidget):
    def __init__(self, engine):
        super().__init__()

        self.layout = QFormLayout(self)

        self.num_clusters_spinbox = QSpinBox()
        self.num_clusters_spinbox.setMinimum(2)
        # self.num_clusters_spinbox.setMaximum(engine.get_maximum_clusters())
        self.num_clusters_spinbox.setMaximum(10)
        self.num_clusters_spinbox.setValue(3)
        self.layout.addRow(QLabel("Something:"), self.num_clusters_spinbox)

    def get_data(self) -> dict:
        return {
            'num_clusters': self.num_clusters_spinbox.value(),
            'metrics': 2
        }
