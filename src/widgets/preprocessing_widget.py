from widgets import UnfoldWidget
from PyQt5.QtWidgets import QWidget, QGroupBox, QLabel, QComboBox, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import QRect


class PreprocessingWidget(UnfoldWidget):
    def __init__(self, parent: QWidget, engine):
        super().__init__(parent)
        self.engine = engine
        self.plot_types = ['Histogram', 'Pie']
        self.setObjectName('preprocessing_widget')

        # unfold button
        self.button.setText("PREPROCESSING")
        self.button.clicked.connect(lambda: self.get_data())

        # plot picker group
        self.plot_picker_group = QGroupBox(self.frame)
        self.plot_picker_group.setTitle("Choose data to plot")
        self.plot_picker_group.setGeometry(QRect(30, 30, 270, 160))

        self.column_picker_label = QLabel(self.plot_picker_group)
        self.column_picker_label.setText("Select column:")
        self.column_picker_label.setGeometry(QRect(10, 40, 100, 23))
        self.column_select_box = QComboBox(self.plot_picker_group)
        self.column_select_box.setGeometry(QRect(110, 40, 130, 23))

        self.plot_picker_label = QLabel(self.plot_picker_group)
        self.plot_picker_label.setText("Select plot type:")
        self.plot_picker_label.setGeometry(10, 80, 100, 23)
        self.plot_select_box = QComboBox(self.plot_picker_group)
        self.plot_select_box.setGeometry(QRect(110, 80, 130, 23))
        self.plot_select_box.addItems(self.plot_types)

        self.plot_picker_submit = QPushButton(self.plot_picker_group)
        self.plot_picker_submit.setText("Plot")
        self.plot_picker_submit.setGeometry(QRect(10, 120, 50, 23))
        self.plot_picker_submit.clicked.connect(lambda: self.plot_data(self.column_select_box.currentText(),
                                                                       self.plot_select_box.currentText()))

        # estimation group
        self.estimate_group = QGroupBox(self.frame)
        self.estimate_group.setTitle("Estimate missing values")
        self.estimate_group.setGeometry(QRect(330, 30, 270, 120))

        self.estimate_group_todo = QLabel(self.estimate_group)
        self.estimate_group_todo.setText("Future")
        self.estimate_group_todo.setGeometry(QRect(10, 40, 100, 23))

        # automatic reduction group
        self.auto_reduction_group = QGroupBox(self.frame)
        self.auto_reduction_group.setTitle("Reduce dimensions automatically")
        self.auto_reduction_group.setGeometry(QRect(630, 30, 270, 120))

        self.auto_reduction_todo = QLabel(self.auto_reduction_group)
        self.auto_reduction_todo.setText("Future")
        self.auto_reduction_todo.setGeometry(QRect(10, 40, 100, 23))

        # plot stats window
        self.plot_widget = QGroupBox(self.frame)
        self.plot_widget.setTitle("Result")
        self.plot_widget.setGeometry(QRect(30, 200, 420, 350))

        self.plot_layout = QVBoxLayout()
        self.plot_widget.setLayout(self.plot_layout)

        # column rejection group
        self.columns_group = QGroupBox(self.frame)
        self.columns_group.setTitle("Columns")
        self.columns_group.setGeometry(QRect(480, 200, 420, 350))
        self.columns_grid = QGridLayout()
        self.columns_group.setLayout(self.columns_grid)

    def get_data(self):
        """ check column names every time coming to that frame (potential changes) """
        self.parent().unfold(1)
        self.column_select_box.clear()
        self.column_select_box.addItems(self.engine.get_columns())

    def plot_data(self, column_name, plot_type):
        self._clear_plot()
        plot_box = self.engine.create_plot(column_name, plot_type)
        self.plot_layout.addWidget(plot_box)

    def _clear_plot(self):
        for i in reversed(range(self.plot_layout.count())):
            self.plot_layout.itemAt(i).widget().setParent(None)
