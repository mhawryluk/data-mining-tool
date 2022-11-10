from functools import partial

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from widgets import QtTable


class ClustersTable(QWidget):
    table_changed = pyqtSignal()

    def __init__(self, data, labels, clusters_representative, columns_num):
        super().__init__()

        self.data = data
        self.labels = labels
        self.selected_cluster = None
        self.clusters_representative = clusters_representative
        self.layout = QVBoxLayout(self)
        self.clusters_table = QTableView()
        self.clusters_table.setModel(QtTable(self.clusters_representative.round(3)))
        self.clusters_table.doubleClicked.connect(self.show_cluster)
        for i in range(columns_num):
            self.clusters_table.setColumnWidth(i, 120)

        self.clusters_table_header = QWidget()
        self.clusters_table_header_layout = QHBoxLayout(self.clusters_table_header)
        self.clusters_table_instruction = QLabel(
            "Double click on any field to preview a cluster"
        )
        self.save_all_button = QPushButton("SAVE RESULTS")
        self.save_all_button.clicked.connect(
            partial(self.on_save_button_click, self.data.assign(cluster=self.labels))
        )
        self.save_all_button.setFixedWidth(120)
        self.clusters_table_header_layout.addWidget(self.clusters_table_instruction)
        self.clusters_table_header_layout.addWidget(self.save_all_button)

        self.layout.addWidget(self.clusters_table_header)
        self.layout.addWidget(self.clusters_table)

    def show_cluster(self):
        self.selected_cluster = (
            self.clusters_table.selectionModel().selectedIndexes()[0].row()
        )
        rows = [
            i
            for i in range(len(self.labels))
            if self.labels[i] == self.selected_cluster
        ]
        elements = self.data.iloc[rows]
        self.clusters_table.setModel(QtTable(elements))
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()
        exit_button = QPushButton("X")
        exit_button.clicked.connect(self.exit_from_cluster)
        exit_button.setFixedWidth(50)
        save_button = QPushButton("SAVE")
        save_button.clicked.connect(partial(self.on_save_button_click, elements))
        save_button.setFixedWidth(100)
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(exit_button)
        buttons_layout.setAlignment(Qt.AlignRight)
        buttons_widget.setLayout(buttons_layout)
        self.layout.insertWidget(0, buttons_widget)
        self.clusters_table_header.hide()
        self.clusters_table.doubleClicked.disconnect()
        self.table_changed.emit()

    def exit_from_cluster(self):
        self.clusters_table.setModel(QtTable(self.clusters_representative.round(3)))
        self.layout.itemAt(0).widget().setParent(None)
        self.clusters_table_header.show()
        self.clusters_table.doubleClicked.connect(self.show_cluster)
        self.selected_cluster = None
        self.table_changed.emit()

    def on_save_button_click(self, elements):
        path, is_ok = QInputDialog.getText(self, "Save to file", "Enter filename")
        if is_ok and path:
            if not path.endswith(".csv"):
                path += ".csv"
            try:
                elements.to_csv(path)
            except:
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setText(
                    "Something wrong happened while writing data to file. Try again."
                )
                error.setWindowTitle("Saving failed")
                error.exec_()
        elif not is_ok:
            pass
        elif not path:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("No path was provided")
            error.setWindowTitle("Empty path")
            error.exec_()
        else:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("This file extension is not supported.")
            error.setWindowTitle("Unsupported extension")
            error.exec_()
