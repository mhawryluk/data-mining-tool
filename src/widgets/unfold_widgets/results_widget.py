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
        # self.data_table.setMinimumHeight(300)
        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # algorithm results tab widget
        self.results_tab_widget = QTabWidget(self)
        self.results_tab_widget.addTab(QLabel("Result"), "Clastering")

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
