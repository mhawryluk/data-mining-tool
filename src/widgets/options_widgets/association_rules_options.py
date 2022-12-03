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
            QLabelWithTooltip(
                "Minimum support:",
                "Minimum percentage of transactions containing a specific subset for it to be considered a frequent set.\n"
                "Too low of a value will result in a very big number of sets found which may affect performance.",
            ),
            self.min_support_spinbox,
        )

        self.min_confidence_spinbox = QDoubleSpinBox()
        self.min_confidence_spinbox.setMinimum(0.01)
        self.min_confidence_spinbox.setValue(0.1)
        self.min_confidence_spinbox.setMaximum(1)
        self.layout.addRow(
            QLabelWithTooltip(
                "Minimum confidence:",
                "Confidence of a rule is calculated by dividing the probability of the items occurring together by the probability of the occurrence of the antecedent.\n"
                "It signifies how strong the association rule really is.\n"
                "Too low of a value may lead to obtaining a high amount of rules.\n"
                "Bigger value will limit rules to just the strongest selection.",
            ),
            self.min_confidence_spinbox,
        )

        self.index_columns_combobox = QComboBox()
        self.layout.addRow(
            QLabelWithTooltip(
                "Index column:", "Column containing each transaction's ID"
            ),
            self.index_columns_combobox,
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
