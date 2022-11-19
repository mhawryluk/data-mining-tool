from typing import Dict

from .options import Options
from PyQt5.QtWidgets import QLabel, QLineEdit, QSpinBox


class ClusteringBlobsDataOptions(Options):
    def __init__(self):
        super().__init__()
        self.number_of_blobs_box = QSpinBox()
        self.number_of_blobs_box.setRange(0, 20)
        self.number_of_blobs_box.setValue(2)
        self.layout.addRow(QLabel("Number of blobs:"), self.number_of_blobs_box)

        self.sample_size_input = QLineEdit("50 30")
        self.layout.addRow(QLabel("Sample sizes per blob:"), self.sample_size_input)

        self.number_of_dims_box = QSpinBox()
        self.number_of_dims_box.setRange(1, 10)
        self.number_of_dims_box.setValue(2)
        self.layout.addRow(QLabel("Number of dimensions:"), self.number_of_dims_box)

        self.std_input = QLineEdit("0.1 0.1")
        self.layout.addRow(QLabel("Standard deviation per dimension:"), self.std_input)

        self.seed_box = QSpinBox()
        self.seed_box.setRange(0, 10)
        self.layout.addRow(QLabel("Seed:"), self.seed_box)

    def get_data(self) -> Dict:
        sample_sizes = list(map(int, self.sample_size_input.text().split(" ")))
        cluster_stds = list(map(float, self.std_input.text().split(" ")))
        clusters_number = self.number_of_blobs_box.value()
        dims_number = self.number_of_dims_box.value()
        seed = self.seed_box.value()

        return {
            "sample_sizes": sample_sizes,
            "dims_number": dims_number,
            "clusters_number": clusters_number,
            "cluster_stds": cluster_stds,
            "seed": seed,
        }
