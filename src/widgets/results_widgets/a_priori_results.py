from typing import List

import matplotlib.pyplot as plt
import pandas as pd
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QTableView,
    QVBoxLayout,
)

from visualization import APrioriGauge, APrioriGraphPlot, APrioriScatterPlot
from widgets import QtTable
from widgets.components import ParametersGroupBox
from widgets.results_widgets import AlgorithmResultsWidget


class APrioriResultsWidget(AlgorithmResultsWidget):
    def __init__(
        self,
        data: pd.DataFrame,
        frequent_sets: pd.DataFrame,
        association_rules: pd.DataFrame,
        transaction_sets: List[set],
        options,
    ):
        super().__init__(data, options)

        self.transaction_sets = transaction_sets
        self.frequent_sets = frequent_sets.reset_index()
        self.frequent_sets.rename(columns={"index": "frequent sets"}, inplace=True)
        self.association_rules = association_rules.reset_index()
        self.association_rules.rename(
            columns={"index": "association rules"}, inplace=True
        )
        self.columns = self.data.columns.values
        self.min_support = self.options["min_support"]
        self.min_confidence = self.options["min_confidence"]

        self.layout = QHBoxLayout(self)

        self.left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()

        # algorithm parameters
        self.params_group = ParametersGroupBox(self.options)

        # sets plots and charts
        self.gauge_chart = APrioriGauge()
        self.gauge_chart.layout().setContentsMargins(0, 0, 0, 0)
        self.graph_plot = APrioriGraphPlot()
        self.graph_plot.layout().setContentsMargins(0, 0, 0, 0)
        self.graph_plot.show_placeholder()

        self.fig, axes = plt.subplots(1, 1)
        self.transactions_canvas = APrioriScatterPlot(self.fig, axes, transaction_sets)
        self.transactions_canvas.reset()

        # frequent sets group
        self.frequent_sets_result_group = QGroupBox()
        self.frequent_sets_result_group_layout = QVBoxLayout(
            self.frequent_sets_result_group
        )
        self.frequent_sets_result_group.setTitle("Frequent sets result")

        # frequent sets table
        self.frequent_sets_table = QTableView()
        self.frequent_sets_table.setModel(QtTable(self.frequent_sets))
        self.frequent_sets_result_group_layout.addWidget(self.frequent_sets_table)
        self.frequent_sets_table.clicked.connect(self.highlight_frequent_set)

        # association rules group
        self.association_rules_group = QGroupBox()
        self.association_rules_group_layout = QVBoxLayout(self.association_rules_group)
        self.association_rules_group.setTitle("Association rules")

        # association rules table
        self.association_rules_table = QTableView()
        self.association_rules_table.setModel(QtTable(self.association_rules))
        self.association_rules_group_layout.addWidget(self.association_rules_table)
        self.association_rules_table.clicked.connect(self.highlight_rule)

        self.right_column.addWidget(self.graph_plot, 1)
        self.right_column.addWidget(self.gauge_chart, 1)
        self.right_column.addWidget(self.transactions_canvas, 1)

        self.left_column.addWidget(self.params_group, 0)
        self.left_column.addWidget(self.frequent_sets_result_group, 1)
        self.left_column.addWidget(self.association_rules_group, 1)

        self.layout.addLayout(self.left_column, 1)
        self.layout.addLayout(self.right_column, 1)

    def highlight_frequent_set(self):
        selected_set = (
            self.frequent_sets_table.selectionModel().selectedIndexes()[0].row()
        )
        column_list = self.frequent_sets.iloc[selected_set]["frequent sets"][
            1:-1
        ].split(",  ")
        self.graph_plot.plot_set(column_list)
        self.gauge_chart.plot_value(
            self.frequent_sets.iloc[selected_set]["support"],
            self.min_support,
            "support",
        )
        self.transactions_canvas.plot_set(column_list)

    def highlight_rule(self):
        selected_rule = (
            self.association_rules_table.selectionModel().selectedIndexes()[0].row()
        )
        set_a, set_b = self.association_rules.iloc[selected_rule][
            "association rules"
        ].split(" => ")
        set_a = set_a[1:-1].split(",  ")
        set_b = set_b[1:-1].split(",  ")
        self.graph_plot.plot_rule(set_a, set_b)
        self.gauge_chart.plot_value(
            self.association_rules.iloc[selected_rule]["confidence"],
            self.min_confidence,
            "confidence",
        )
        self.transactions_canvas.plot_rule(set_a, set_b)
