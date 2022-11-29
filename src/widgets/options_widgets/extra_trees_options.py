from PyQt5.QtWidgets import QComboBox, QDoubleSpinBox, QLabel, QSpinBox

from widgets.options_widgets import AlgorithmOptions


class ExtraTreesOptions(AlgorithmOptions):
    def __init__(self):
        super().__init__()

        self.label_name_box = QComboBox()
        self.layout.addRow(QLabel("Column with labels:"), self.label_name_box)

        self.forest_size_spinbox = QSpinBox()
        self.forest_size_spinbox.setMinimum(1)
        self.forest_size_spinbox.setMaximum(200)
        self.forest_size_spinbox.setValue(10)
        self.layout.addRow(QLabel("Number of trees:"), self.forest_size_spinbox)

        self.features_number_spinbox = QSpinBox()
        self.features_number_spinbox.setMinimum(1)
        self.features_number_spinbox.setValue(1)
        self.layout.addRow(
            QLabel("Number of features to sample:"), self.features_number_spinbox
        )

        self.min_child_number_spinbox = QSpinBox()
        self.min_child_number_spinbox.setMinimum(1)
        self.min_child_number_spinbox.setMaximum(1000)
        self.min_child_number_spinbox.setValue(1)
        self.layout.addRow(
            QLabel("Minimum number of samples in child:"), self.min_child_number_spinbox
        )

        self.max_depth_spinbox = QSpinBox()
        self.max_depth_spinbox.setMinimum(1)
        self.max_depth_spinbox.setMaximum(100)
        self.max_depth_spinbox.setSpecialValueText("no limit")
        self.max_depth_spinbox.setValue(1)
        self.layout.addRow(QLabel("Maximum depth:"), self.max_depth_spinbox)

        self.min_metrics_spinbox = QDoubleSpinBox()
        self.min_metrics_spinbox.setMinimum(0)
        self.min_metrics_spinbox.setMaximum(1)
        self.min_metrics_spinbox.setValue(0)
        self.min_metrics_spinbox.setSingleStep(0.01)
        self.layout.addRow(QLabel("Minimum metrics change:"), self.min_metrics_spinbox)

        self.metrics_type_box = QComboBox()
        self.metrics_type_box.addItems(["gini", "entropy"])
        self.layout.addRow(QLabel("Metrics type:"), self.metrics_type_box)

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
        self.features_number_spinbox.setMaximum(len(columns) - 1)
