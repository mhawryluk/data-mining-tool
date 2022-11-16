from PyQt5.QtWidgets import QComboBox, QSpinBox

from widgets.components import QLabelWithTooltip
from widgets.options_widgets import AlgorithmOptions


class KMeansOptions(AlgorithmOptions):
    def __init__(self):
        super().__init__()

        self.num_clusters_spinbox = QSpinBox()
        self.num_clusters_spinbox.setMinimum(2)
        self.num_clusters_spinbox.setValue(3)
        self.layout.addRow(
            QLabelWithTooltip(
                "Number of clusters:",
                "Clusters number depends on the nature of the data.\nScatter plot (in the PREPROCESSING section)\ncan be helpful to enter correct number.",
            ),
            self.num_clusters_spinbox,
        )

        self.start_type_box = QComboBox()
        self.start_type_box.addItems(["random", "kmeans++"])
        self.start_type_box.setCurrentIndex(1)
        self.layout.addRow(
            QLabelWithTooltip(
                "Type of initial solution:",
                "Method for centroids initialization. Choose rows from dataset.\n'random': selects random rows from dataset\n'kmeans++': uses sampling based on an empirical probability distribution of the points’ contribution to the overall inertia\n You should use 'kmeans++', which speeds up convergence.",
            ),
            self.start_type_box,
        )

        self.metrics_spinbox = QSpinBox()
        self.metrics_spinbox.setMinimum(1)
        self.metrics_spinbox.setValue(2)
        self.metrics_spinbox.setMaximum(6)
        self.layout.addRow(
            QLabelWithTooltip(
                "Exponent in metrics:",
                "Define value of p in the p-norm space. The default value is 2.",
            ),
            self.metrics_spinbox,
        )

        self.num_steps_spinbox = QSpinBox()
        self.num_steps_spinbox.setMinimum(0)
        self.num_steps_spinbox.setMaximum(1000)
        self.num_steps_spinbox.setSpecialValueText("no limit")
        self.num_steps_spinbox.setValue(0)
        self.layout.addRow(
            QLabelWithTooltip(
                "Maximum number of iterations:",
                "Maximum number of iterations of the k-means algorithm for a single run.\n'no limit' option exists, because k-means converges quickly.",
            ),
            self.num_steps_spinbox,
        )

        self.num_repeat_spinbox = QSpinBox()
        self.num_repeat_spinbox.setMinimum(1)
        self.num_repeat_spinbox.setMaximum(100)
        self.num_repeat_spinbox.setValue(5)
        self.layout.addRow(
            QLabelWithTooltip(
                "Number of repetitions:",
                "Number of time the algorithm will be run with different initial centroids.\nThe final results will be the best output based on Dunn index.",
            ),
            self.num_repeat_spinbox,
        )

    def get_data(self) -> dict:
        return {
            "num_clusters": self.num_clusters_spinbox.value(),
            "metrics": self.metrics_spinbox.value(),
            "repeats": self.num_repeat_spinbox.value(),
            "iterations": self.num_steps_spinbox.value() or None,
            "init_type": self.start_type_box.currentText(),
        }

    def set_max_clusters(self, clusters_num):
        self.num_clusters_spinbox.setMaximum(clusters_num)
