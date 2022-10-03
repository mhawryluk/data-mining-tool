from PyQt5.QtWidgets import QWidget, QGroupBox, QFormLayout, QLabel, QTableView, QVBoxLayout

from widgets import QtTable


class APrioriResultsWidget(QWidget):
    def __init__(self, data, frequent_sets, association_rules, options):
        super().__init__()
        self.data = data
        self.frequent_sets = frequent_sets
        self.association_rules = association_rules

        self.layout = QVBoxLayout(self)

        # algorithm parameters
        self.params_group = QGroupBox()
        self.params_group.setTitle("Parameters")
        self.params_layout = QFormLayout(self.params_group)

        for option, value in options.items():
            self.params_layout.addRow(QLabel(f'{option}:'), QLabel(f'{value}'))

        self.layout.addWidget(self.params_group)

        # frequent sets group
        self.frequent_sets_result_group = QGroupBox()
        self.frequent_sets_result_group_layout = QVBoxLayout(self.frequent_sets_result_group)
        self.frequent_sets_result_group.setTitle("Frequent sets result")

        # frequent sets table
        self.frequent_sets_table = QTableView()
        self.frequent_sets_table.setModel(QtTable(frequent_sets))
        self.frequent_sets_result_group_layout.addWidget(self.frequent_sets_table)

        # association rules group
        self.association_rules_group = QGroupBox()
        self.association_rules_group_layout = QVBoxLayout(self.association_rules_group)
        self.association_rules_group.setTitle("Association rules")

        # association rules table
        self.association_rules_table = QTableView()
        self.association_rules_table.setModel(QtTable(association_rules))
        self.association_rules_group_layout.addWidget(self.association_rules_table)

        self.layout.addWidget(self.frequent_sets_result_group, 1)
        self.layout.addWidget(self.association_rules_group, 1)

    def click_listener(self, button_type: str):
        pass
