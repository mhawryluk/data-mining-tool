from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QWidget, QGroupBox, QLabel, QComboBox, QVBoxLayout, QPushButton, QCheckBox, \
    QMessageBox, QSplashScreen, QApplication, QDesktopWidget, QFormLayout, QHBoxLayout, QSizePolicy, QScrollArea

from widgets import UnfoldWidget


class PreprocessingWidget(UnfoldWidget):
    def __init__(self, parent: QWidget, engine):
        super().__init__(parent, engine, 'preprocessing_widget', 'PREPROCESSING')

        self.button.disconnect()
        self.button.clicked.connect(lambda: self.get_data())

        self.plot_types = ['Histogram', 'Pie']

        # plot picker group
        self.plot_picker_group = QGroupBox(self.frame)
        self.plot_picker_group_layout = QFormLayout(self.plot_picker_group)

        self.plot_picker_group.setTitle("Choose data to plot")

        self.column_picker_label = QLabel(self.plot_picker_group)
        self.column_picker_label.setText("Select column:")
        self.column_picker_label.setMinimumHeight(23)
        self.column_select_box = QComboBox(self.plot_picker_group)
        self.column_select_box.setMinimumHeight(23)

        self.plot_picker_group_layout.addRow(self.column_picker_label, self.column_select_box)
        self.plot_picker_group.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.plot_picker_label = QLabel(self.plot_picker_group)
        self.plot_picker_label.setText("Select plot type:")
        self.plot_picker_label.setMinimumHeight(23)
        self.plot_select_box = QComboBox(self.plot_picker_group)
        self.plot_select_box.setMinimumHeight(23)
        self.plot_select_box.addItems(self.plot_types)

        self.plot_picker_group_layout.addRow(self.plot_picker_label, self.plot_select_box)

        self.plot_picker_submit = QPushButton(self.plot_picker_group)
        self.plot_picker_submit.setText("Plot")
        self.plot_picker_submit.setMinimumHeight(23)
        self.plot_picker_submit.clicked.connect(lambda: self.plot_data(self.column_select_box.currentText(),
                                                                       self.plot_select_box.currentText()))

        self.plot_picker_group_layout.addRow(self.plot_picker_submit)

        # estimation group
        self.estimate_group = QGroupBox(self.frame)
        self.estimate_group.setTitle("Estimate missing values")
        self.estimate_group_layout = QFormLayout(self.estimate_group)

        self.estimate_group_todo = QLabel(self.estimate_group)
        self.estimate_group_todo.setText("Future")
        self.estimate_group_todo.setMinimumHeight(23)
        self.estimate_group_layout.addRow(self.estimate_group_todo)

        # automatic reduction group
        self.auto_reduction_group = QGroupBox(self.frame)
        self.auto_reduction_group.setTitle("Reduce dimensions automatically")
        self.auto_reduction_group_layout = QFormLayout(self.auto_reduction_group)

        self.auto_reduction_todo = QLabel(self.auto_reduction_group)
        self.auto_reduction_todo.setText("Future")
        self.auto_reduction_todo.setMinimumHeight(23)
        self.auto_reduction_group_layout.addRow(self.auto_reduction_todo)

        # plot stats window
        self.plot_widget = QGroupBox(self.frame)
        self.plot_widget.setTitle("Result")

        self.plot_layout = QVBoxLayout()
        self.plot_widget.setLayout(self.plot_layout)

        # column rejection group
        self.columns_group = QGroupBox(self.frame)
        self.columns_group.setTitle("Columns")
        self.columns_group_layout = QHBoxLayout(self.columns_group)

        self.scroll_box = QGroupBox(self.frame)
        self.columns_group_form_layout = QFormLayout(self.scroll_box)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.scroll_box)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumHeight(26)

        self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.columns_group_layout.addWidget(self.scroll)
        self.columns_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.submit_checkboxes_button = QPushButton()
        self.submit_checkboxes_button.setFixedHeight(23)
        self.submit_checkboxes_button.setText("Select")
        self.submit_checkboxes_button.clicked.connect(lambda: self.submit_columns())
        self.columns_group_layout.addWidget(self.submit_checkboxes_button)

        self.add_columns_to_layout()

        # layouts for sections
        layout = QVBoxLayout(self.frame)

        self.plot_picker_column = QVBoxLayout()
        self.plot_picker_column.addStretch(1)
        self.plot_picker_column.addWidget(self.plot_picker_group)
        self.plot_picker_column.addStretch(1)

        self.first_row = QHBoxLayout()
        self.first_row.addLayout(self.plot_picker_column, 0)
        self.first_row.addWidget(self.plot_widget, 1)

        self.second_row = QHBoxLayout()
        self.second_row.addWidget(self.estimate_group, 1)
        self.second_row.addWidget(self.auto_reduction_group, 1)
        self.second_row.addWidget(self.columns_group, 1)

        layout.addLayout(self.first_row, 1)
        layout.addLayout(self.second_row, 0)

    def get_data(self):
        """ check column names every time coming to that frame (potential changes) """
        if self.engine.state.imported_data is None:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText('No dataset was selected')
            error.setWindowTitle("Error")
            error.exec_()
            return

        loading_screen = QSplashScreen()
        size = QDesktopWidget().screenGeometry(-1)
        loading_screen.showMessage("<h1>Loading...</h1>", Qt.AlignCenter)
        loading_screen.setGeometry(QRect(size.width()//2-125, size.height()//2-50, 250, 100)) # hardcoded alignment
        loading_screen.show()
        QApplication.processEvents()

        self.parent().unfold(self)
        self.column_select_box.clear()
        self.column_select_box.addItems(self.engine.get_columns())
        self.add_columns_to_layout()
        self.engine.clean_data()
        loading_screen.close()

    def plot_data(self, column_name, plot_type):
        self._clear_plot()
        plot_box = self.engine.create_plot(column_name, plot_type)
        self.plot_layout.addWidget(plot_box)

    def _clear_plot(self):
        for i in reversed(range(self.plot_layout.count())):
            self.plot_layout.itemAt(i).widget().setParent(None)

    def add_columns_to_layout(self):
        self.clear_column_layout()
        columns = self.engine.get_columns()
        for column in columns:
            checkbox = QCheckBox(column)
            checkbox.setChecked(True)
            self.columns_group_form_layout.addRow(checkbox)

    def clear_column_layout(self):
        for i in reversed(range(self.columns_group_form_layout.count())):
            self.columns_group_form_layout.itemAt(i).widget().setParent(None)

    def submit_columns(self):
        columns = []
        for i in range(self.columns_group_form_layout.count()):
            if self.columns_group_form_layout.itemAt(i).widget().isChecked():
                columns.append(self.columns_group_form_layout.itemAt(i).widget().text())
        self.engine.set_state(columns)
        self.get_data()
