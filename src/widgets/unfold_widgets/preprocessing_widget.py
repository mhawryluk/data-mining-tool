import matplotlib.pyplot as plt
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDesktopWidget,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QSplashScreen,
    QVBoxLayout,
    QWidget,
)

from visualization import plots
from widgets import UnfoldWidget
from widgets.components import QLabelWithTooltip, SamplesColumnsChoice
from widgets.tables import DataPreviewScreen, PreviewReason


class PreprocessingWidget(UnfoldWidget):
    def __init__(self, parent: QWidget, engine):
        super().__init__(parent, engine, "preprocessing_widget", "PREPROCESSING")

        self.data_submitted = False
        self.mark_reduced_columns = False
        self.button.disconnect()
        self.button.clicked.connect(lambda: self.get_data())

        self.plot_types = ["Histogram", "Pie", "Null frequency", "Scatter plot"]

        # plot picker group
        self.plot_picker_group = QGroupBox(self.frame)
        self.plot_picker_group_layout = QFormLayout(self.plot_picker_group)

        self.plot_picker_group.setTitle("Choose data to plot")

        self.column_picker_label = QLabel(self.plot_picker_group)
        self.column_picker_label.setText("Select column:")
        self.column_picker_label.setMinimumHeight(23)
        self.column_select_box = QComboBox(self.plot_picker_group)
        self.column_select_box.setMinimumHeight(23)
        self.parameters_widget = SamplesColumnsChoice()
        self.parameters_widget_connection = None
        self.group_picker_label = QLabel("Group by:")
        self.group_picker_label.setMinimumHeight(23)
        self.group_select_box = QComboBox()
        self.group_select_box.setMinimumHeight(23)

        self.plot_picker_group.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.plot_picker_label = QLabel(self.plot_picker_group)
        self.plot_picker_label.setText("Select plot type:")
        self.plot_picker_label.setMinimumHeight(23)
        self.plot_select_box = QComboBox(self.plot_picker_group)
        self.plot_select_box.currentTextChanged.connect(self.change_settings)
        self.plot_select_box.setMinimumHeight(23)
        self.plot_select_box.addItems(self.plot_types)

        self.plot_picker_group_layout.addRow(
            self.plot_picker_label, self.plot_select_box
        )

        self.plot_picker_submit = QPushButton(self.plot_picker_group)
        self.plot_picker_submit.setText("Plot")
        self.plot_picker_submit.setMinimumHeight(23)
        self.plot_picker_submit.clicked.connect(
            lambda: self.plot_data(
                self.column_select_box.currentText(), self.plot_select_box.currentText()
            )
        )

        self.plot_picker_group_layout.addRow(self.plot_picker_submit)

        # estimation group
        self.estimate_group = QGroupBox(self.frame)
        self.estimate_group_layout = QFormLayout(self.estimate_group)
        self.estimate_manually_button = QPushButton(self.estimate_group)
        self.estimate_automatically_button = QPushButton(self.estimate_group)
        self.render_estimation_group()

        # initialize reduction results screen
        self.preview_screen = None

        # automatic reduction group
        self.auto_reduction_group = QGroupBox(self.frame)
        self.auto_reduction_group.setTitle("Reduce dimensions")
        self.auto_reduction_group_layout = QFormLayout(self.auto_reduction_group)

        self.num_dimensions_spinbox = QSpinBox()
        self.manual_reduction = QPushButton(self.auto_reduction_group)
        self.auto_reduction = QPushButton(self.auto_reduction_group)

        self.num_dimensions_spinbox.setMinimum(1)
        self.num_dimensions_spinbox.setValue(1)
        self.auto_reduction_group_layout.addRow(
            QLabel("Number of dimensions:"), self.num_dimensions_spinbox
        )

        self.manual_reduction_label = QLabelWithTooltip(
            "Reduce with fixed number",
            "Reduce dimensions using the Principal Component Analysis algorithm.",
        )
        self.manual_reduction_label.layout.setAlignment(
            Qt.AlignCenter | Qt.AlignVCenter
        )
        self.manual_reduction.setLayout(self.manual_reduction_label.layout)
        self.manual_reduction.setMinimumHeight(23)
        self.auto_reduction_group_layout.addRow(self.manual_reduction)
        self.manual_reduction.clicked.connect(
            lambda: self.reduce_dimensions(self.num_dimensions_spinbox.value())
        )

        self.auto_reduction_label = QLabelWithTooltip(
            "Reduce dynamically",
            "Reduce dimensions using the Principal Component Analysis algorithm.\nTake dimensions with imapct more than 5%.",
        )
        self.auto_reduction_label.layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.auto_reduction.setLayout(self.auto_reduction_label.layout)
        self.auto_reduction.setMinimumHeight(23)
        self.auto_reduction_group_layout.addRow(self.auto_reduction)
        self.auto_reduction.clicked.connect(lambda: self.reduce_dimensions())

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

        layout.addLayout(self.first_row, 3)
        layout.addLayout(self.second_row, 1)

    def change_settings(self):
        if self.plot_select_box.currentText() == "Scatter plot":
            self.column_select_box.setParent(None)
            self.column_picker_label.setParent(None)
            self.plot_picker_group_layout.insertRow(0, self.parameters_widget)
            self.plot_picker_group_layout.insertRow(
                1, self.group_picker_label, self.group_select_box
            )
        else:
            self.parameters_widget.setParent(None)
            self.group_picker_label.setParent(None)
            self.group_select_box.setParent(None)
            self.plot_picker_group_layout.insertRow(
                0, self.column_picker_label, self.column_select_box
            )

    def activate_scatter_plot(self):
        self.parameters_widget_connection = (
            self.parameters_widget.samples_changed.connect(
                lambda: self.plot_data(
                    self.column_select_box.currentText(),
                    self.plot_select_box.currentText(),
                )
            )
        )
        self.parameters_widget.sample_button.setEnabled(True)
        self.parameters_widget.sample_box.setEnabled(True)

    def deactivate_scatter_plot(self):
        if self.parameters_widget_connection is not None:
            self.parameters_widget.samples_changed.disconnect(
                self.parameters_widget_connection
            )
            self.parameters_widget_connection = None
        self.parameters_widget.sample_button.setEnabled(False)
        self.parameters_widget.sample_box.setEnabled(False)

    def get_data(self):
        """check column names every time coming to that frame (potential changes)"""
        if self.engine.state.imported_data is None:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("No dataset was selected")
            error.setWindowTitle("Error")
            error.exec_()
            return

        loading_screen = QSplashScreen()
        size = QDesktopWidget().screenGeometry(-1)
        loading_screen.showMessage("<h1>Loading...</h1>", Qt.AlignCenter)
        loading_screen.setGeometry(
            QRect(size.width() // 2 - 125, size.height() // 2 - 50, 250, 100)
        )  # hardcoded alignment
        loading_screen.show()
        QApplication.processEvents()

        self.parent().unfold(self)
        self.column_select_box.clear()
        self.column_select_box.addItems(self.engine.get_columns())
        self.group_select_box.clear()
        self.group_select_box.addItems([""] + list(self.engine.get_columns()))
        self._clear_plot()
        self.parameters_widget.new_columns_name(self.engine.get_numeric_columns())
        self.parameters_widget.new_size(self.engine.get_size())
        self.add_columns_to_layout()
        self.engine.clean_data("cast")

        max_dimensions = self.engine.number_of_numeric_columns() - len(
            [
                column
                for column in self.engine.state.reduced_columns
                if column in self.engine.state.imported_data
            ]
        )
        self.set_reduction_bounds(max_dimensions)
        loading_screen.close()

    def plot_data(self, column_name, plot_type):
        self._clear_plot()
        scatter_settings = self.parameters_widget.get_parameters()
        group_by = self.group_select_box.currentText()
        scatter_settings["group_by"] = group_by if group_by else None
        plot_box = self.create_plot(column_name, plot_type, scatter_settings)
        if plot_type == "Scatter plot":
            self.activate_scatter_plot()
        self.plot_layout.addWidget(plot_box)

    def _clear_plot(self):
        self.deactivate_scatter_plot()
        for i in reversed(range(self.plot_layout.count())):
            figure = self.plot_layout.itemAt(i).widget().figure
            plt.close(figure)
            self.plot_layout.itemAt(i).widget().setParent(None)

    def add_columns_to_layout(self):
        self.clear_column_layout()
        columns = self.engine.get_raw_columns()
        selected_columns = self.engine.get_columns()
        self.mark_reduced_columns = False
        for column in columns:
            checkbox = QCheckBox(column)
            checkbox.setChecked(column in selected_columns)
            self.columns_group_form_layout.addRow(checkbox)

    def clear_column_layout(self):
        for i in reversed(range(self.columns_group_form_layout.count())):
            self.columns_group_form_layout.itemAt(i).widget().setParent(None)

    def submit_columns(self):
        self.data_submitted = False
        columns = []
        for i in range(self.columns_group_form_layout.count()):
            if self.columns_group_form_layout.itemAt(i).widget().isChecked():
                columns.append(self.columns_group_form_layout.itemAt(i).widget().text())
        if not columns:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("No columns were chosen")
            error.setWindowTitle("Error")
            error.exec_()
            return
        if self.engine.has_rows_with_nulls(columns):
            self.remove_nulls_warning()
        else:
            self.data_submitted = True
        if self.data_submitted:
            self.engine.set_state(columns)
            self.engine.clean_data("remove")
            self.get_data()

    def create_plot(self, column_name, plot_type, scatter_settings):
        plotter = None
        if column_name == "":
            plotter = plots.FallbackPlot([])
            return plotter.plot()
        column = self.engine.state.imported_data.loc[:, column_name]
        match plot_type:
            case "Histogram":
                plotter = plots.HistogramPlot(column)
            case "Pie":
                plotter = plots.PiePlot(column)
            case "Null frequency":
                plotter = plots.NullFrequencyPlot(column)
            case "Scatter plot":
                plotter = plots.ScatterPlot(
                    self.engine.state.imported_data,
                    scatter_settings,
                )
        return plotter.plot()

    def remove_nulls_warning(self):
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Warning)
        warning.setText("Null values in set")
        warning.setInformativeText(
            "This data contains some empty values. After proceeding some of the rows will be "
            "discarded. Continue?"
        )
        warning.setWindowTitle("Cleaning data")
        warning.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        warning.buttonClicked.connect(self.handle_warning_click)
        warning.exec_()

    def handle_warning_click(self, button):
        self.data_submitted = "OK" in button.text()

    def reduce_dimensions(self, dim_number=None):
        self.engine.state.imported_data.drop(
            self.engine.state.reduced_columns, axis=1, inplace=True, errors="ignore"
        )
        self.engine.state.raw_data.drop(
            self.engine.state.reduced_columns, axis=1, inplace=True
        )
        self.engine.state.reduced_columns = self.engine.reduce_dimensions(dim_number)
        self.mark_reduced_columns = True
        self.show_reduction_results()

    def set_reduction_bounds(self, max_dimensions):
        self.num_dimensions_spinbox.setMinimum(1)
        self.num_dimensions_spinbox.setMaximum(max(max_dimensions - 1, 1))
        self.manual_reduction.setDisabled(max_dimensions < 2)
        self.auto_reduction.setDisabled(max_dimensions < 2)

    def show_reduction_results(self):
        self.preview_screen = DataPreviewScreen(
            self, title="Reduction results", reason=PreviewReason.REDUCTION
        )
        self.preview_screen.show()

    def render_estimation_group(self):
        self.estimate_group.setTitle("Fill missing values")

        self.estimate_manually_button.setText("Enter manually")
        self.estimate_manually_button.setMinimumHeight(23)
        self.estimate_group_layout.addRow(self.estimate_manually_button)
        self.estimate_manually_button.clicked.connect(self.estimate_manually)

        self.estimate_automatically_button.setText("Mean/mode estimation")
        self.estimate_automatically_button.setMinimumHeight(23)
        self.estimate_group_layout.addRow(self.estimate_automatically_button)
        self.estimate_automatically_button.clicked.connect(
            self.estimate_with_mean_or_mode
        )

    def estimate_manually(self):
        self.preview_screen = DataPreviewScreen(
            self, title="Input missing values", reason=PreviewReason.ESTIMATION
        )
        self.preview_screen.show()

    def estimate_with_mean_or_mode(self):
        self.engine.mean_or_mode_estimate()
        self.preview_screen = DataPreviewScreen(
            self, title="Estimation results", reason=PreviewReason.PREVIEW
        )
        self.preview_screen.show()
