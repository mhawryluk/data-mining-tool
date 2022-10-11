from time import strptime

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QSizePolicy, QLabel, QInputDialog, QLineEdit, QMessageBox
from widgets import QtTable
from enum import Enum


class PreviewReason(Enum):
    ESTIMATION = 'estimation'
    REDUCTION = 'reduction'
    PREVIEW = 'preview'


def fallback():
    pass


class DataPreviewScreen(QWidget):
    def __init__(self, widget, title="Data preview", reason: PreviewReason = PreviewReason.PREVIEW):
        super().__init__()
        self.parent = widget
        self.engine = self.parent.engine
        self.setWindowTitle(title)

        self.layout = QVBoxLayout()
        self.data_table = QTableView()

        match reason:
            case PreviewReason.ESTIMATION:
                self.render_instruction("Double click on a cell to fill in a missing value or on a header to affect "
                                        "the entire column")
                self.render_data(self.estimation_header_click, self.estimation_cell_click)
            case PreviewReason.REDUCTION:
                self.render_instruction("Double click on a header to change column name")
                self.render_data(self.reduction_header_click, fallback)
            case PreviewReason.PREVIEW:
                self.render_data(fallback, fallback)

        self.setLayout(self.layout)

    def render_instruction(self, instruction):
        instruction_widget = QLabel(instruction)
        self.layout.addWidget(instruction_widget)

    def render_data(self, handle_header_click, handle_cell_click):
        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.data_table.setModel(QtTable(self.engine.state.imported_data))
        self.data_table.horizontalHeader().sectionDoubleClicked.connect(handle_header_click)
        self.data_table.doubleClicked.connect(handle_cell_click)
        self.layout.addWidget(self.data_table)

    def reduction_header_click(self, index):
        newHeader, ok = QInputDialog.getText(self,
                                             f'Change header label for column {index}',
                                             'Header:',
                                             QLineEdit.Normal,
                                             "")
        if ok:
            self.engine.rename_column(index, newHeader)
            self.data_table.setModel(QtTable(self.engine.state.imported_data))

    def estimation_header_click(self, index):
        print(self.engine.state.imported_data.dtypes)
        new_value, ok = QInputDialog.getText(self,
                                             f'Default value for column {index}:',
                                             'Value:',
                                             QLineEdit.Normal,
                                             "")
        if ok:
            column = self.engine.state.imported_data.iloc[:, index]
            new_value = self.cast_input_type(column.dtype, new_value)
            if new_value is not None:
                column.fillna(new_value, inplace=True)
            self.data_table.setModel(QtTable(self.engine.state.imported_data))

    def estimation_cell_click(self):
        cell = self.data_table.selectionModel().selectedIndexes()[0]
        row, col = cell.row(), cell.column()
        new_value, ok = QInputDialog.getText(self,
                                             f'Default value for cell ({row}, {col}):',
                                             'Value:',
                                             QLineEdit.Normal,
                                             "")
        if ok:
            column = self.engine.state.imported_data.iloc[:, col]
            new_value = self.cast_input_type(column.dtype, new_value)
            if new_value is not None:
                self.engine.state.imported_data.iloc[row, col] = new_value
            self.data_table.setModel(QtTable(self.engine.state.imported_data))

    @staticmethod
    def cast_input_type(data_type, value):
        try:
            match data_type:
                case 'int32' | 'int64':
                    return int(value)
                case 'float64':
                    return float(value)
                case 'datetime64[ns]':
                    return strptime(value)
                case _:
                    return value
        except ValueError:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText('Data is not valid')
            error.setWindowTitle("Error")
            error.exec_()

    def closeEvent(self, event):
        self.parent.get_data()
