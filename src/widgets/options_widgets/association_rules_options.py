from typing import List

from PyQt5.QtWidgets import QComboBox, QDoubleSpinBox

from widgets.components import QLabelWithTooltip
from widgets.options_widgets import AlgorithmOptions


class AssociationRulesOptions(AlgorithmOptions):
    def __init__(self):
        super().__init__()

        self.min_support_spinbox = QDoubleSpinBox()
        self.min_support_spinbox.setMinimum(0.01)
        self.min_support_spinbox.setValue(0.05)
        self.min_support_spinbox.setMaximum(1)
        self.min_support_spinbox.setSingleStep(0.1)
        self.layout.addRow(
            QLabelWithTooltip("Minimum support:", "example"), self.min_support_spinbox
        )

        self.min_confidence_spinbox = QDoubleSpinBox()
        self.min_confidence_spinbox.setMinimum(0.01)
        self.min_confidence_spinbox.setValue(0.1)
        self.min_confidence_spinbox.setMaximum(1)
        self.layout.addRow(
            QLabelWithTooltip("Minimum confidence:"), self.min_confidence_spinbox
        )

        self.index_columns_combobox = QComboBox()
        self.layout.addRow(
            QLabelWithTooltip("Index column:"), self.index_columns_combobox
        )

    def get_data(self) -> dict:
        return {
            "min_support": self.min_support_spinbox.value(),
            "min_confidence": self.min_confidence_spinbox.value(),
            "index_column": self.index_columns_combobox.currentText(),
        }

    def set_columns_options(self, columns: List[str]):
        self.index_columns_combobox.clear()
        self.index_columns_combobox.addItems(columns)
