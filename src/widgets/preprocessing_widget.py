import random

from widgets import UnfoldWidget
from PyQt5.QtWidgets import QWidget, QGroupBox, QLabel, QComboBox, QVBoxLayout, QGridLayout
from PyQt5.QtCore import QRect
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib as plt
plt.use('Qt5Agg')


class PreprocessingWidget(UnfoldWidget):
    def __init__(self, parent: QWidget, engine):
        super().__init__(parent)
        self.engine = engine
        self.setObjectName('preprocessing_widget')

        # unfold button
        self.button.setText("PREPROCESSING")
        self.button.clicked.connect(lambda: self.parent().unfold(1))

        # plot picker group
        self.plot_picker_group = QGroupBox(self.frame)
        self.plot_picker_group.setTitle("Choose data to plot")
        self.plot_picker_group.setGeometry(QRect(30, 30, 270, 120))

        self.column_picker_label = QLabel(self.plot_picker_group)
        self.column_picker_label.setText("Select column:")
        self.column_picker_label.setGeometry(QRect(10, 40, 100, 23))
        self.column_select_box = QComboBox(self.plot_picker_group)
        self.column_select_box.setGeometry(QRect(110, 40, 130, 23))
        self.column_select_box.addItems(["mock1", "mock2"])

        self.plot_picker_label = QLabel(self.plot_picker_group)
        self.plot_picker_label.setText("Select plot type:")
        self.plot_picker_label.setGeometry(10, 80, 100, 23)
        self.plot_select_box = QComboBox(self.plot_picker_group)
        self.plot_select_box.setGeometry(QRect(110, 80, 130, 23))
        self.plot_select_box.addItems(['plot1', 'plot2'])

        # estimation group
        self.estimate_group = QGroupBox(self.frame)
        self.estimate_group.setTitle("Estimate missing values")
        self.estimate_group.setGeometry(QRect(330, 30, 270, 120))

        self.estimate_group_todo = QLabel(self.estimate_group)
        self.estimate_group_todo.setText("Todo")
        self.estimate_group_todo.setGeometry(QRect(10, 40, 100, 23))

        # automatic reduction group
        self.auto_reduction_group = QGroupBox(self.frame)
        self.auto_reduction_group.setTitle("Reduce dimensions automatically")
        self.auto_reduction_group.setGeometry(QRect(630, 30, 270, 120))

        self.auto_reduction_todo = QLabel(self.auto_reduction_group)
        self.auto_reduction_todo.setText("Todo")
        self.auto_reduction_todo.setGeometry(QRect(10, 40, 100, 23))

        # plot stats window
        self.plot_widget = QGroupBox(self.frame)
        self.plot_widget.setTitle("Result")
        self.plot_widget.setGeometry(QRect(30, 170, 420, 400))
        self.figure = Figure()
        self.plotting = FigureCanvasQTAgg(self.figure)
        data = [random.random() for i in range(100)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, '*-')
        self.plotting.draw()
        plot_box = QVBoxLayout()
        plot_box.addWidget(self.plotting)
        self.plot_widget.setLayout(plot_box)

        # column rejection group
        self.columns_group = QGroupBox(self.frame)
        self.columns_group.setTitle("Columns")
        self.columns_group.setGeometry(QRect(480, 170, 420, 400))
        self.columns_grid = QGridLayout()
        self.columns_group.setLayout(self.columns_grid)
