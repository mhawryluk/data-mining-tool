from math import sqrt

from PyQt5.QtWidgets import QComboBox, QDoubleSpinBox, QSpinBox

from widgets.components import QLabelWithTooltip
from widgets.options_widgets import AlgorithmOptions


class ExtraTreesOptions(AlgorithmOptions):
    def __init__(self):
        super().__init__()

        self.label_name_box = QComboBox()
        self.layout.addRow(
            QLabelWithTooltip("Column with labels:", "Column with target values."),
            self.label_name_box,
        )

        self.forest_size_spinbox = QSpinBox()
        self.forest_size_spinbox.setMinimum(1)
        self.forest_size_spinbox.setMaximum(200)
        self.forest_size_spinbox.setValue(50)
        self.layout.addRow(
            QLabelWithTooltip(
                "Number of trees:",
                "The number of the trees in the forest. The more, the better.",
            ),
            self.forest_size_spinbox,
        )

        self.features_number_spinbox = QSpinBox()
        self.features_number_spinbox.setMinimum(1)
        self.layout.addRow(
            QLabelWithTooltip(
                "Number of features to sample:",
                "The number of features to consider when looking for the best split.\nRecommended tu use sqrt or log2 of number of columns.\nThe default value is sqrt.",
            ),
            self.features_number_spinbox,
        )

        self.min_child_number_spinbox = QSpinBox()
        self.min_child_number_spinbox.setMinimum(1)
        self.min_child_number_spinbox.setMaximum(1000)
        self.min_child_number_spinbox.setValue(1)
        self.layout.addRow(
            QLabelWithTooltip(
                "Minimum number of samples in child:",
                "The minimum number of samples required to be at a leaf node.\nA split point will only be considered if it leaves at least this number of training samples in both branches.",
            ),
            self.min_child_number_spinbox,
        )

        self.max_depth_spinbox = QSpinBox()
        self.max_depth_spinbox.setMinimum(1)
        self.max_depth_spinbox.setMaximum(100)
        self.max_depth_spinbox.setSpecialValueText("no limit")
        self.max_depth_spinbox.setValue(1)
        self.layout.addRow(
            QLabelWithTooltip(
                "Maximum depth:",
                "The maximum depth of the tree.\nIf 'no limit', then nodes are expanded until all leaves are pure\nor until algorithm do not draw threshold fulfilling requirements\nabout number of samples in child and minimum metrics change.",
            ),
            self.max_depth_spinbox,
        )

        self.min_metrics_spinbox = QDoubleSpinBox()
        self.min_metrics_spinbox.setMinimum(0)
        self.min_metrics_spinbox.setMaximum(1)
        self.min_metrics_spinbox.setValue(0)
        self.min_metrics_spinbox.setSingleStep(0.01)
        self.layout.addRow(
            QLabelWithTooltip(
                "Minimum metrics change:",
                "A node will be split if this split induces a decrease of the impurity greater than or equal to this value.",
            ),
            self.min_metrics_spinbox,
        )

        self.metrics_type_box = QComboBox()
        self.metrics_type_box.addItems(["gini", "entropy"])
        self.layout.addRow(
            QLabelWithTooltip(
                "Metrics type:",
                "The function to measure the quality of a split.\n'gini': Gini impurity\n'entropy': based on Shannon information gain",
            ),
            self.metrics_type_box,
        )

    def get_data(self) -> dict:
        max_depth = (
            self.max_depth_spinbox.value()
            if self.max_depth_spinbox.value() > 1
            else None
        )
        return {
            "label_name": self.label_name_box.currentText(),
            "forest_size": self.forest_size_spinbox.value(),
            "features_number": self.features_number_spinbox.value(),
            "min_child_number": self.min_child_number_spinbox.value(),
            "max_depth": max_depth,
            "min_metrics": self.min_metrics_spinbox.value(),
            "metrics_type": self.metrics_type_box.currentText(),
        }

    def set_values(self, columns: list):
        self.label_name_box.clear()
        self.label_name_box.addItems(columns)
        max_number = len(columns) - 1
        self.features_number_spinbox.setMaximum(max_number)
        self.features_number_spinbox.setValue(max(1, round(sqrt(max_number))))
