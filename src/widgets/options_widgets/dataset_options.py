from typing import Dict

from PyQt5.QtWidgets import QLabel, QLineEdit, QSpinBox

from widgets.components import QLabelWithTooltip
from widgets.options_widgets import AlgorithmOptions


class ClusteringBlobsDataOptions(AlgorithmOptions):
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
                "If just one value is provided, it will be used for each blob.",
            ),
            self.sample_size_input,
        )

        self.number_of_dims_box = QSpinBox()
        self.number_of_dims_box.setRange(1, 10)
        self.number_of_dims_box.setValue(2)
        self.layout.addRow(QLabel("Number of dimensions:"), self.number_of_dims_box)

        self.noise_box = QSpinBox()
        self.noise_box.setValue(0)
        self.noise_box.setMaximum(100)

        self.layout.addRow(
            QLabelWithTooltip(
                "Additional noise percentage:",
                "How many more points that do not fall into desired pattern\n"
                "will be added to the generated data set.\n"
                "Counted as percentage of provided total sample size.",
            ),
            self.noise_box,
        )

        self.seed_box = QSpinBox()
        self.seed_box.setRange(0, 10)
        self.seed_box.setSpecialValueText("random")

        self.layout.addRow(
            QLabelWithTooltip(
                "Seed:",
                "Used for setting state of the randomizer.\n"
                "Setting this field to a chosen value will ensure getting the same results every time.",
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

        seed = self.seed_box.value()
        if not seed:
            seed = None

        noise = self.noise_box.value()

        return {
            "sample_sizes": sample_sizes,
            "dims_number": dims_number,
            "blobs_number": blobs_number,
            "seed": seed,
            "noise": noise / 100,
        }


class NormalDistributionClusteringOptions(ClusteringBlobsDataOptions):
    def __init__(self):
        super().__init__()
        self.std_input = QLineEdit("5 1.2, 2.1 2.1")
        self.layout.addRow(
            QLabelWithTooltip(
                "Standard deviation:",
                "Values for different blobs should be separated via a comma.\n"
                "Values for different dimensions in a single blob should be separated via a single space.\n"
                "Format: blob1_dim1 blob1_dim2, blob2_dim1 blob2_dim2\n"
                "If just one value is provided, instead of a series it will be used for every blob/dimension.",
            ),
            self.std_input,
        )

    def get_data(self) -> Dict:
        data = super().get_data()
        blobs_number = data["blobs_number"]
        dims_number = data["dims_number"]

        standard_deviations = list(
            map(
                lambda std_per_blob: list(map(float, std_per_blob.strip().split(" "))),
                self.std_input.text().split(","),
            )
        )

        provided_stds_number_blobs = len(standard_deviations)
        if (
            provided_stds_number_blobs != 1
            and provided_stds_number_blobs != blobs_number
        ):
            raise ValueError(
                "Provided configuration of standard deviations doesn't match set number of blobs"
            )
        if provided_stds_number_blobs == 1:
            standard_deviations *= blobs_number

        for blob_stds in standard_deviations:
            provided_stds_number_dims = len(blob_stds)
            if (
                provided_stds_number_dims != 1
                and provided_stds_number_dims != dims_number
            ):
                raise ValueError(
                    "Provided configuration of standard deviations doesn't match set number of dimensions"
                )
            if provided_stds_number_dims == 1:
                blob_stds *= dims_number

        return data | {
            "dims_stds": standard_deviations,
        }


class NoncentralFClusteringOptions(ClusteringBlobsDataOptions):
    def __init__(self):
        super().__init__()
        self.df_num_input = QLineEdit("3 5")
        self.layout.addRow(
            QLabelWithTooltip(
                "Numerator degrees of freedom:",
                "Number of degrees of freedom of the Chi-squared distribution X.\n"
                "Should be > 0.",
            ),
            self.df_num_input,
        )

        self.df_den_input = QLineEdit("20 15")
        self.layout.addRow(
            QLabelWithTooltip(
                "Denominator degrees of freedom:",
                "Number of degrees of freedom of the Chi-squared distribution Y.\n"
                "Should be > 0.",
            ),
            self.df_den_input,
        )

    def get_data(self) -> Dict:
        data = super().get_data()
        blobs_number = data["blobs_number"]

        df_nums = list(map(float, self.df_num_input.text().split(" ")))
        if len(df_nums) != 1 and len(df_nums) != blobs_number:
            raise ValueError("Incorrect number of provided numerators")
        if len(df_nums) == 1:
            df_nums *= blobs_number

        if any(df_num <= 0 for df_num in df_nums):
            raise ValueError("Degrees of freedom need to be positive numbers")

        df_dens = list(map(float, self.df_den_input.text().split(" ")))
        if len(df_dens) != 1 and len(df_dens) != blobs_number:
            raise ValueError("Incorrect number of provided denominators")
        if len(df_dens) == 1:
            df_dens *= blobs_number

        if any(df_den <= 0 for df_den in df_dens):
            raise ValueError("Degrees of freedom need to be positive numbers")

        return data | {
            "df_nums": df_nums,
            "df_dens": df_dens,
        }
