from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QSizePolicy, QLabel, QInputDialog, QLineEdit

from widgets import QtTable


class DataPreviewScreen(QWidget):
    def __init__(self, widget):
        super().__init__()
        self.parent = widget
        self.engine = self.parent.engine
        self.setWindowTitle("Reduction results")

        self.layout = QVBoxLayout()
        self.data_table = QTableView()

        self.render_instruction("Double click on a header to change column name")
        self.render_data()
        self.setLayout(self.layout)

    def render_instruction(self, instruction):
        instruction_widget = QLabel(instruction)
        self.layout.addWidget(instruction_widget)

    def render_data(self):
        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.data_table.setModel(QtTable(self.engine.state.imported_data))
        self.data_table.horizontalHeader().sectionDoubleClicked.connect(self.handleHeaderClick)
        self.layout.addWidget(self.data_table)

    def handleHeaderClick(self, index):
        newHeader, ok = QInputDialog.getText(self,
                                                   'Change header label for column %d' % index,
                                                   'Header:',
                                                   QLineEdit.Normal,
                                                   "")
        if ok:
            self.engine.rename_column(index, newHeader)
            self.data_table.setModel(QtTable(self.engine.state.imported_data))

    def closeEvent(self, event):
        self.parent.get_data()
