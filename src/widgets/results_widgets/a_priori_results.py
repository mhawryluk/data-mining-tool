from typing import List

import pandas as pd
from PyQt5.QtWidgets import QWidget, QGroupBox, QFormLayout, QLabel, QTableView, QVBoxLayout, QHBoxLayout
import matplotlib.pyplot as plt

from visualization.associations import APrioriCanvas
from widgets import QtTable


class APrioriResultsWidget(QWidget):
    def __init__(self, data: pd.DataFrame, frequent_sets: pd.DataFrame, association_rules: pd.DataFrame,
                 transaction_sets: List[set], options):
        super().__init__()
        self.transaction_sets = transaction_sets
        self.frequent_sets = frequent_sets
        self.association_rules = association_rules

        self.layout = QHBoxLayout(self)

        self.left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()

        # algorithm parameters
        self.params_group = QGroupBox()
        self.params_group.setTitle("Parameters")
        self.params_layout = QFormLayout(self.params_group)

        for option, value in options.items():
            self.params_layout.addRow(QLabel(f'{option}:'), QLabel(f'{value}'))

        self.left_column.addWidget(self.params_group, 0)

        # transactions group
        self.transactions_group = QGroupBox()
        self.transactions_group_layout = QVBoxLayout(self.transactions_group)
        self.transactions_group.setTitle("Transactions")

        # transactions scatter plot
        self.fig, axes = plt.subplots(1, 1)
        self.transactions_canvas = APrioriCanvas(self.fig, axes, transaction_sets)
        self.transactions_canvas.plot_set()
        self.transactions_group_layout.addWidget(self.transactions_canvas)

        self.left_column.addWidget(self.transactions_group, 1)

        # frequent sets group
        self.frequent_sets_result_group = QGroupBox()
        self.frequent_sets_result_group_layout = QVBoxLayout(self.frequent_sets_result_group)
        self.frequent_sets_result_group.setTitle("Frequent sets result")

        # frequent sets table
        self.frequent_sets_table = QTableView()
        self.frequent_sets_table.setModel(QtTable(frequent_sets))
        self.frequent_sets_result_group_layout.addWidget(self.frequent_sets_table)
        self.frequent_sets_table.clicked.connect(self.highlight_frequent_set)

        # association rules group
        self.association_rules_group = QGroupBox()
        self.association_rules_group_layout = QVBoxLayout(self.association_rules_group)
        self.association_rules_group.setTitle("Association rules")

        # association rules table
        self.association_rules_table = QTableView()
        self.association_rules_table.setModel(QtTable(association_rules))
        self.association_rules_group_layout.addWidget(self.association_rules_table)
        self.association_rules_table.clicked.connect(self.highlight_rule)

        self.right_column.addWidget(self.frequent_sets_result_group, 1)
        self.right_column.addWidget(self.association_rules_group, 1)

        self.layout.addLayout(self.left_column, 1)
        self.layout.addLayout(self.right_column, 1)

    def highlight_frequent_set(self):
        selected_set = self.frequent_sets_table.selectionModel().selectedIndexes()[0].row()
        self.transactions_canvas.plot_set(self.frequent_sets.index.values[selected_set].split(", "))

    def highlight_rule(self):
        selected_rule = self.association_rules_table.selectionModel().selectedIndexes()[0].row()
        set_a, set_b = self.association_rules.index.values[selected_rule].split(" => ")
        self.transactions_canvas.plot_rule(set_a.split(", "), set_b.split(", "))
