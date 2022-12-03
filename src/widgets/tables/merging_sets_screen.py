from functools import partial

import numpy as np
import pandas as pd
from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import (
    QBoxLayout,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QStyle,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from data_import import Loader
from widgets import LoadingWidget, QtTable


class DragButton(QPushButton):
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.exec_(Qt.MoveAction)


class ColumnWidget(QWidget):
    def __init__(self, column_name, parent_layout):
        super().__init__()
        self.column_name = column_name
        self.parent_layout = parent_layout

        self.layout = QHBoxLayout(self)
        self.drag_button = DragButton(self.column_name)

        self.layout.addWidget(self.drag_button, stretch=1)

        self.remove_button = QPushButton()
        pixmapi = getattr(QStyle, "SP_DialogCancelButton")
        icon = self.style().standardIcon(pixmapi)
        self.remove_button.setIcon(icon)
        self.remove_button.setFixedWidth(30)
        self.remove_button.clicked.connect(self._on_remove)
        self.layout.addWidget(self.remove_button)

    def _on_remove(self):
        for i in reversed(range(self.parent_layout.count() - 1)):
            if (
                self.parent_layout.itemAt(i).widget().drag_button.text()
                == self.column_name
            ):
                self.parent_layout.itemAt(i).widget().setParent(None)
                break


class MergingSetsScreen(QWidget):
    def __init__(self, widget, on_hide):
        super().__init__()
        self.widget = widget
        self.engine = widget.engine
        self.loader = Loader()
        self.setAcceptDrops(True)
        self.new_data = None
        self.setWindowTitle("Datasets concatenation")
        self._load_styles()
        self.drag_init_pos = None
        self.on_hide_callback = on_hide
        self.cancel_merge = False

        # init all components to have a ref
        self.layout = QHBoxLayout()
        self.current_data_view = QTableView()
        self.new_data_view = QTableView()
        self.load_data_group = QGroupBox(self)
        self.load_data_group_layout = QFormLayout(self.load_data_group)
        self.filepath_label = QLabel(self.load_data_group)
        self.filepath_line = QLineEdit(self.load_data_group)
        self.file_button = QPushButton(self.load_data_group)
        self.database_label = QLabel(self.load_data_group)
        self.database_box = QComboBox(self.load_data_group)
        self.database_button = QPushButton(self.load_data_group)
        self.import_state_label = QLabel(self.load_data_group)
        self.columns_merge_group = QGroupBox(self)
        self.columns_merge_group_layout = QVBoxLayout(self.columns_merge_group)
        self.columns_widget = QWidget()
        self.columns_layout = QHBoxLayout()
        self.left_columns = QWidget()
        self.right_columns = QWidget()
        self.columns_left_layout = QVBoxLayout()
        self.columns_right_layout = QVBoxLayout()
        self.submit_button = QPushButton()

        # layouts stretch settings
        self.columns_left_layout.addStretch(QBoxLayout.BottomToTop)
        self.columns_right_layout.addStretch(QBoxLayout.BottomToTop)

        # rendering content
        self._render_table(self.current_data_view, True)
        self._render_panel()
        self._render_table(self.new_data_view, False)

        self.setLayout(self.layout)

    def _load_styles(self):
        with open("../static/css/styles.css") as stylesheet:
            self.setStyleSheet(stylesheet.read())

    def _render_table(self, table_widget, current):
        table_group = QGroupBox(self)
        table_group_layout = QVBoxLayout(table_group)
        table_group.setTitle("Original table" if current else "Table to merge")
        if current:
            table_widget.setModel(QtTable(self.engine.state.imported_data))
        else:
            data = self.new_data if self.new_data is not None else pd.DataFrame()
            table_widget.setModel(QtTable(data))
        table_group_layout.addWidget(table_widget)
        self.layout.addWidget(table_group, 1)

    def _render_panel(self):
        panel = QWidget()
        panel_layout = QVBoxLayout(panel)
        self._render_import_view()
        self._render_columns_view()
        panel_layout.addWidget(self.load_data_group)
        panel_layout.addWidget(self.columns_merge_group, 1)
        self.layout.addWidget(panel, 1)

    def _render_import_view(self):
        self.load_data_group_layout.setFieldGrowthPolicy(
            QFormLayout.AllNonFixedFieldsGrow
        )
        self.load_data_group.setTitle("Load data")

        self.filepath_label.setText("Load data from file:")
        self.load_data_group_layout.addRow(self.filepath_label)

        self.filepath_line.setReadOnly(True)
        self.filepath_line.setFixedWidth(150)

        self.file_button.setText("Select file")
        self.file_button.clicked.connect(partial(self._click_listener, "load_file"))
        self.load_data_group_layout.addRow(self.filepath_line, self.file_button)

        self.database_label.setText("Choose data from database:")
        self.load_data_group_layout.addRow(self.database_label)

        names = self.engine.get_table_names_from_database()
        for name in names:
            self.database_box.addItem(name)

        self.database_button.setText("Load")
        self.database_button.clicked.connect(
            partial(self._click_listener, "load_database")
        )
        self.load_data_group_layout.addRow(self.database_box, self.database_button)

        self.load_data_group_layout.addRow(self.import_state_label)

    def _render_columns_view(self):
        self.columns_merge_group.setTitle("Merge columns")
        instruction = QLabel()
        instruction.setText(
            "Firstly, you need to import another dataset here.\nIf everything goes well, the new "
            "columns should appear inside the right empty box.\nYou should see two lists of columns "
            "and you can set which columns will be merged together by drag and drop.\nWhen you're "
            "ready, click the 'submit' button, then another screen with results will be shown.\n"
            "You will be asked whether you'd like to accept or reject integration.\nIf you choose to "
            "concatenate, the newly created dataset should be visible on the import screen."
        )
        self.columns_merge_group_layout.addWidget(instruction, 0)

        imported_columns = self._get_imported_columns()
        for column in imported_columns:
            self.columns_left_layout.insertWidget(
                self.columns_left_layout.count() - 1,
                ColumnWidget(column, self.columns_left_layout),
            )

        if self.new_data is not None and self.new_data.columns is not None:
            for column in sorted(self.new_data.columns, key=lambda x: x.upper()):
                self.columns_right_layout.insertWidget(
                    self.columns_right_layout.count() - 1,
                    ColumnWidget(column, self.columns_right_layout),
                )

        self.left_columns.setLayout(self.columns_left_layout)
        self.right_columns.setLayout(self.columns_right_layout)
        self.columns_layout.addWidget(self.left_columns)
        self.columns_layout.addWidget(self.right_columns)
        self.columns_widget.setLayout(self.columns_layout)
        self.columns_merge_group_layout.addWidget(self.columns_widget, 1)

        self.submit_button.setText("Submit")
        self.submit_button.setEnabled(self.new_data is not None)
        self.submit_button.clicked.connect(partial(self._click_listener, "submit"))
        self.columns_merge_group_layout.addWidget(self.submit_button, 0)

    def _click_listener(self, button_type: str):
        match button_type:
            case "load_file":
                loading = LoadingWidget(self._load_from_file_handle)
                loading.execute()
            case "load_database":
                loading = LoadingWidget(self._load_from_database_handle)
                loading.execute()
            case "submit":
                loading = LoadingWidget(self._on_submit)
                loading.execute()

    def _load_from_file_handle(self):
        self.import_state_label.setText("Loading ...")
        file_path = QFileDialog.getOpenFileName(
            self, "Choose file", ".", "*.csv *.json"
        )[0]
        try:
            reader = self.loader.create_file_reader(file_path)
        except ValueError as e:
            self.import_state_label.setText(str(e))
        else:
            self._on_success(reader, file_path)

    def _load_from_database_handle(self):
        self.import_state_label.setText("Loading ...")
        document_name = self.database_box.currentText()
        try:
            reader = self.loader.create_database_reader(document_name)
        except ValueError as e:
            self.import_state_label.setText(str(e))
        else:
            self._on_success(reader)

    def _on_success(self, reader, file_path=None):
        if file_path is not None:
            self.filepath_line.setText(file_path)
        self.import_state_label.clear()
        if self.engine.is_data_big():
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setText("This file is too big.\nYou must save it in database!")
            error.setWindowTitle("Warning")
            error.exec_()
        self.new_data = reader.read(None)
        last_preview = self.layout.takeAt(2).widget()
        if last_preview is not None:
            last_preview.deleteLater()
        self._render_table(self.new_data_view, False)

        for i in reversed(range(self.columns_left_layout.count() - 1)):
            # workaround to delete as low content as possible, removing nested layouts was giving me some segfault
            self.columns_left_layout.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.columns_right_layout.count() - 1)):
            self.columns_right_layout.itemAt(i).widget().setParent(None)

        imported_columns = self._get_imported_columns()
        for column in imported_columns:
            self.columns_left_layout.insertWidget(
                self.columns_left_layout.count() - 1,
                ColumnWidget(column, self.columns_left_layout),
            )

        if self.new_data is not None and self.new_data.columns is not None:
            for column in sorted(self.new_data.columns, key=lambda x: x.upper()):
                self.columns_right_layout.insertWidget(
                    self.columns_right_layout.count() - 1,
                    ColumnWidget(column, self.columns_right_layout),
                )

        self.submit_button.setEnabled(self.new_data is not None)

    def _on_submit(self):
        new_columns_left = []
        new_columns_right = []
        for i in range(self.columns_left_layout.count() - 1):
            new_columns_left.append(
                self.columns_left_layout.itemAt(i).widget().column_name
            )
        for i in range(self.columns_right_layout.count() - 1):
            new_columns_right.append(
                self.columns_right_layout.itemAt(i).widget().column_name
            )

        if len(new_columns_left) != len(new_columns_right):
            self._render_equality_warning()
            if self.cancel_merge:
                self.cancel_merge = False
                return

        num_columns = max(len(new_columns_left), len(new_columns_right))
        labels_left = new_columns_left[:num_columns]
        labels_right = new_columns_right[:num_columns]
        for i in range(len(new_columns_right) - len(new_columns_left)):
            new_column_name = f"Column {i}"
            labels_left.append(new_column_name)
            self.engine.state.imported_data[new_column_name] = np.nan
            self.engine.state.raw_data[new_column_name] = np.nan

        for i in range(len(new_columns_left) - len(new_columns_right)):
            new_column_name = f"Column {i}"
            labels_right.append(new_column_name)
            self.new_data[new_column_name] = np.nan

        labels_mapping = dict(zip(labels_right, labels_left))

        self.engine.reorder_columns(labels_left)
        self.new_data.rename(columns=labels_mapping, inplace=True)

        self.engine.merge_sets(self.new_data[labels_left])
        self.widget.set_columns_grid()

        self.on_hide_callback()
        self.hide()

    def _get_imported_columns(self):
        return sorted(self.engine.state.imported_data.columns, key=lambda x: x.upper())

    def closeEvent(self, event):
        close = QMessageBox.question(
            self,
            "Exit",
            "Are you sure want to exit process? All changes will be discarded.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, e):
        self.drag_init_pos = e.pos()
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source().parent()

        widget_helper = self.columns_left_layout.itemAt(0).widget()
        should_insert = False
        if (
            pos.x()
            < widget_helper.mapToGlobal(widget_helper.rect().topLeft()).x()
            - self.pos().x()
            + widget_helper.size().width()
        ):
            for n in range(self.columns_left_layout.count()):
                w = self.columns_left_layout.itemAt(n).widget()
                if w == widget:
                    should_insert = True
                    break
            if should_insert:
                for n in range(self.columns_left_layout.count()):
                    w = self.columns_left_layout.itemAt(n).widget()
                    if w is None:
                        self.columns_left_layout.insertWidget(n - 1, widget)
                        break
                    elif (
                        pos.y() < w.mapToGlobal(w.rect().topLeft()).y() - self.pos().y()
                    ):
                        self.columns_left_layout.insertWidget(n, widget)
                        break

        elif self.new_data is not None:
            for n in range(self.columns_right_layout.count()):
                w = self.columns_right_layout.itemAt(n).widget()
                if w == widget:
                    should_insert = True
                    break
            if should_insert:
                for n in range(self.columns_right_layout.count()):
                    w = self.columns_right_layout.itemAt(n).widget()
                    if w is None:
                        self.columns_right_layout.insertWidget(n - 1, widget)
                        break
                    elif (
                        pos.y() < w.mapToGlobal(w.rect().topLeft()).y() - self.pos().y()
                    ):
                        self.columns_right_layout.insertWidget(n, widget)
                        break

        e.accept()

    def _render_equality_warning(self):
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Warning)
        warning.setText("The numbers of dimensions are not the same")
        warning.setInformativeText(
            "You can let the system fill the dataset or you can cancel submission and try to remove some columns. Do you want to add extra columns with nulls?"
        )
        warning.setWindowTitle("Dimensions are not the same")
        warning.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        warning.buttonClicked.connect(self._on_warning_submit_callback)
        warning.exec_()

    def _on_warning_submit_callback(self, button):
        self.cancel_merge = "Cancel" in button.text()
