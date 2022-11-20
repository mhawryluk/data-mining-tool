from typing import Dict

from PyQt5.QtWidgets import QLabel, QLineEdit, QSpinBox

from widgets.components import QLabelWithTooltip
from .options import Options


class ClusteringBlobsDataOptions(Options):
    def __init__(self):
        super().__init__()
        self.number_of_blobs_box = QSpinBox()
        self.number_of_blobs_box.setRange(0, 20)
        self.number_of_blobs_box.setValue(2)
        self.layout.addRow(QLabel("Number of blobs:"), self.number_of_blobs_box)

        self.sample_size_input = QLineEdit("50 30")
        self.layout.addRow(
            QLabelWithTooltip(
                "Sample sizes per blob:",
                "Series of integer values separated by a single space.\n"
                "There should be as many numbers listed as the number of blobs.\n"
                "If just one value is provided, it will be used for each blob."
            ),
            self.sample_size_input,
        )

        self.number_of_dims_box = QSpinBox()
        self.number_of_dims_box.setRange(1, 10)
        self.number_of_dims_box.setValue(2)
        self.layout.addRow(QLabel("Number of dimensions:"), self.number_of_dims_box)

        self.std_input = QLineEdit("0.1 0.1")
        self.layout.addRow(
            QLabelWithTooltip(
                "Standard deviation per dimension:",
                "Series of decimal values separated by a single space.\n"
                "There should be as many numbers listed as the number of dimensions.\n"
                "If just one value is provided, it will be used for each dimension."
            ),
            self.std_input,
        )

        self.seed_box = QSpinBox()
        self.seed_box.setRange(0, 10)
        self.seed_box.setSpecialValueText("random")

        self.layout.addRow(
            QLabelWithTooltip(
                "Seed:",
                "Used for setting state of the randomizer.\n"
                "Setting this field to a chosen value will ensure getting the same results every time."
            ),
            self.seed_box,
        )

    def get_data(self) -> Dict:
        blobs_number = self.number_of_blobs_box.value()
        sample_sizes = list(map(int, self.sample_size_input.text().split(" ")))
        provided_sample_sizes = len(sample_sizes)

        if provided_sample_sizes != 1 and provided_sample_sizes != blobs_number:
            raise ValueError("Incorrect number of provided sample sizes")

        if provided_sample_sizes == 1:
            sample_sizes *= blobs_number

        dims_number = self.number_of_dims_box.value()
        dims_stds = list(map(float, self.std_input.text().split(" ")))
        provided_stds_number = len(dims_stds)

        if provided_stds_number != 1 and provided_stds_number != dims_number:
            raise ValueError("Incorrect number of provided values of standard deviation")

        if provided_stds_number == 1:
            dims_stds *= dims_number

        seed = self.seed_box.value()
        if not seed:
            seed = None

        return {
            "sample_sizes": sample_sizes,
            "dims_number": dims_number,
            "blobs_number": blobs_number,
            "dims_stds": dims_stds,
            "seed": seed,
        }
