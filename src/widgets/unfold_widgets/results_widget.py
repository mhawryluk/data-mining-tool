from PyQt5.QtWidgets import QTableView, QSizePolicy, QHBoxLayout, QVBoxLayout, QTabWidget, QLabel

from widgets import UnfoldWidget, QtTable


class ResultsWidget(UnfoldWidget):
    def __init__(self, parent, engine):
        super().__init__(parent, engine, 'results_widget', 'RESULTS')
        self.button.disconnect()
        self.button.clicked.connect(self.load_widget)
        self.engine = engine

        # data table
        self.data_table = QTableView(self)
        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # algorithm results tab widget
        self.results_tab_widget = QTabWidget(self)

        # layouts for sections
        self.layout = QVBoxLayout(self.frame)

        self.first_row = QHBoxLayout()
        self.first_row.addWidget(self.results_tab_widget)
        self.first_row.setSpacing(35)

        self.second_row = QHBoxLayout()
        self.second_row.addWidget(self.data_table, 0)

        self.layout.addLayout(self.first_row, 3)
        self.layout.addLayout(self.second_row, 1)

    def load_widget(self):
        self.parent().unfold(self)
        if (data := self.engine.state.imported_data) is not None:
            self.data_table.setModel(QtTable(data))

        for i in reversed(range(self.results_tab_widget.count())):
            self.results_tab_widget.removeTab(i)

        for technique, algorithms in self.engine.state.algorithm_results.items():
            tab_widget = QTabWidget()
            for algorithm, result in algorithms.items():
                tab_widget.addTab(QLabel("\n".join(list(map(str, result)))), algorithm)
            self.results_tab_widget.addTab(tab_widget, technique)

