from functools import partial

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QFormLayout, QLabel, QVBoxLayout, QSpinBox, QPushButton, \
    QComboBox, QTableView, QInputDialog, QMessageBox
from matplotlib import pyplot as plt

from algorithms import check_numeric, get_samples
from visualization.clustering import KMeansCanvas
from widgets import QtTable
from widgets.results_widgets import AlgorithmResultsWidget


class KMeansResultsWidget(AlgorithmResultsWidget):
    def __init__(self, data, labels, centroids, options):
        super().__init__(data, options)

        self.labels = labels
        self.centroids = centroids
        self.selected_cluster = None

        columns = [col for col in self.data.columns if check_numeric(self.data[col])]
        for column in columns:
            self.data[column] = pd.to_numeric(self.data[column])

        self.layout = QHBoxLayout(self)

        self.num_samples = min(35, self.data.shape[0] // 2)
        self.samples = get_samples(self.data, self.num_samples)

        self.ox = columns[0]
        self.oy = columns[0] if len(columns) < 2 else columns[1]

        # algorithm parameters
        self.params_group = QGroupBox()
        self.params_group.setTitle("Parameters")
        self.params_layout = QFormLayout(self.params_group)

        for option, value in self.options.items():
            self.params_layout.addRow(QLabel(f'{option}:'), QLabel(f'{value}'))

        self.layout.addWidget(self.params_group)

        # clustering result group
        self.clustering_result_group = QGroupBox()
        self.clustering_group_layout = QVBoxLayout(self.clustering_result_group)
        self.clustering_result_group.setTitle("Clustering result")

        # samples
        self.settings_group_box = QGroupBox()
        self.settings_box_layout = QFormLayout(self.settings_group_box)
        self.settings_box_layout.addRow(QLabel("Set samples:"))
        self.sample_box = QSpinBox()
        self.sample_box.setMinimum(1)
        self.sample_box.setMaximum(min(self.data.shape[0], 10000))
        self.sample_box.setProperty("value", self.num_samples)
        self.sample_button = QPushButton("Refresh samples")
        self.sample_button.clicked.connect(partial(self.click_listener, 'new_samples'))
        self.settings_box_layout.addRow(self.sample_box, self.sample_button)

        # axis
        self.settings_box_layout.addRow(QLabel("Set axis:"))
        self.ox_box = QComboBox()
        self.ox_box.addItems(columns)
        self.oy_box = QComboBox()
        self.oy_box.addItems(columns)
        if len(columns) > 1:
            self.oy_box.setCurrentIndex(1)
        self.ox_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.oy_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.settings_box_layout.addRow(QLabel("OX:"), self.ox_box)
        self.settings_box_layout.addRow(QLabel("OY:"), self.oy_box)

        self.settings_box_layout.setSpacing(10)
        self.clustering_group_layout.addWidget(self.settings_group_box)

        # plot
        self.fig, axes = plt.subplots(1, 1)
        self.clusters_canvas = KMeansCanvas(self.fig, axes, False)
        self.clustering_group_layout.addWidget(self.clusters_canvas, 1)

        self.layout.addWidget(self.clustering_result_group, 1)

        # centroids
        self.centroids_group = QGroupBox()
        self.centroids_group_layout = QVBoxLayout(self.centroids_group)
        self.centroids_group.setTitle("Centroids")

        self.centroids_table = QTableView()
        self.centroids_table.setModel(QtTable(self.centroids.round(3)))
        self.centroids_table.doubleClicked.connect(self.show_cluster)

        for i in range(len(columns)):
            self.centroids_table.setColumnWidth(i, 120)

        self.centroids_table_header = QWidget()
        self.centroids_table_header_layout = QHBoxLayout()
        self.centroids_table_instruction = QLabel("Double click on any field to preview a cluster")
        self.save_all_button = QPushButton("SAVE RESULTS")
        self.save_all_button.clicked.connect(partial(self.on_save_button_click, self.data.assign(cluster=self.labels)))
        self.save_all_button.setFixedWidth(120)
        self.centroids_table_header_layout.addWidget(self.centroids_table_instruction)
        self.centroids_table_header_layout.addWidget(self.save_all_button)
        self.centroids_table_header.setLayout(self.centroids_table_header_layout)

        self.fig_centroids, ax = plt.subplots(1, 1)
        self.centroids_canvas = KMeansCanvas(self.fig_centroids, ax, False)

        self.centroids_group_layout.addWidget(self.centroids_table_header)
        self.centroids_group_layout.addWidget(self.centroids_table, 1)
        self.centroids_group_layout.addWidget(self.centroids_canvas, 1)

        self.layout.addWidget(self.centroids_group, 1)
        self.update_plot()
        self.update_cluster_plot()

    def click_listener(self, button_type: str):
        match button_type:
            case 'new_samples':
                num = self.sample_box.value()
                self.num_samples = num
                self.samples = get_samples(self.data, self.num_samples)
                self.update_plot()
                self.update_cluster_plot()
            case 'set_axis':
                self.ox = self.ox_box.currentText()
                self.oy = self.oy_box.currentText()
                self.update_plot()
                self.update_cluster_plot()

    def update_plot(self):
        samples_data = self.data.iloc[self.samples]
        x = samples_data[self.ox]
        y = samples_data[self.oy]
        min_x = self.data[self.ox].min()
        max_x = self.data[self.ox].max()
        min_y = self.data[self.oy].min()
        max_y = self.data[self.oy].max()
        sep_x = 0.1 * (max_x - min_x)
        sep_y = 0.1 * (max_y - min_y)

        labels = [self.labels[sample] for sample in self.samples]
        if self.ox in self.centroids.columns:
            x_centroids = self.centroids[self.ox]
        else:
            x_centroids = pd.Series(
                [self.data.iloc[self.labels == label][self.ox].mean() for label in range(max(self.labels) + 1)])
        if self.oy in self.centroids.columns:
            y_centroids = self.centroids[self.oy]
        else:
            y_centroids = pd.Series(
                [self.data.iloc[self.labels == label][self.oy].mean() for label in range(max(self.labels) + 1)])

        self.clusters_canvas.all_plot(x, y, x_centroids, y_centroids, labels, self.ox, self.oy,
                                      min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y)

    def update_cluster_plot(self):
        if self.selected_cluster is not None:
            indexes = [i for i in range(len(self.labels)) if self.labels[i] == self.selected_cluster]
            x = self.data.iloc[indexes][self.ox]
            y = self.data.iloc[indexes][self.oy]
            min_x = x.min()
            max_x = x.max()
            min_y = y.min()
            max_y = y.max()
            sep_x = 0.1 * (max_x - min_x)
            sep_y = 0.1 * (max_y - min_y)

            if self.ox in self.centroids.columns:
                x_centroids = self.centroids[self.ox]
            else:
                x_centroids = pd.Series([self.data.iloc[self.labels == label][self.ox].mean() for label in range(max(self.labels) + 1)])
            if self.oy in self.centroids.columns:
                y_centroids = self.centroids[self.oy]
            else:
                y_centroids = pd.Series([self.data.iloc[self.labels == label][self.oy].mean() for label in range(max(self.labels) + 1)])

            self.centroids_canvas.chosen_centroid_plot(x, y, None, None, None, None, x_centroids.iloc[self.selected_cluster],
                                                       y_centroids.iloc[self.selected_cluster], self.selected_cluster,
                                                       len(x_centroids), self.ox, self.oy, min_x - sep_x, max_x + sep_x,
                                                       min_y - sep_y, max_y + sep_y,)
        else:
            x = self.data[self.ox]
            y = self.data[self.oy]
            min_x = x.min()
            max_x = x.max()
            min_y = y.min()
            max_y = y.max()
            sep_x = 0.1 * (max_x - min_x)
            sep_y = 0.1 * (max_y - min_y)

            if self.ox in self.centroids.columns:
                x_centroids = self.centroids[self.ox]
            else:
                x_centroids = pd.Series([self.data.iloc[self.labels == label][self.ox].mean() for label in range(max(self.labels) + 1)])
            if self.oy in self.centroids.columns:
                y_centroids = self.centroids[self.oy]
            else:
                y_centroids = pd.Series([self.data.iloc[self.labels == label][self.oy].mean() for label in range(max(self.labels) + 1)])

            self.centroids_canvas.new_centroids_plot(None, None, x_centroids, y_centroids, self.ox, self.oy,
                                                     min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y,
                                                     )

    def show_cluster(self):
        self.selected_cluster = self.centroids_table.selectionModel().selectedIndexes()[0].row()
        rows = [i for i in range(len(self.labels)) if self.labels[i] == self.selected_cluster]
        elements = self.data.iloc[rows]
        self.centroids_table.setModel(QtTable(elements))
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
        self.centroids_group_layout.insertWidget(0, buttons_widget)
        self.centroids_table_header.hide()
        self.centroids_table.doubleClicked.disconnect()
        self.update_cluster_plot()

    def exit_from_cluster(self):
        self.centroids_table.setModel(QtTable(self.centroids.round(3)))
        self.centroids_group_layout.itemAt(0).widget().setParent(None)
        self.centroids_table_header.show()
        self.centroids_table.doubleClicked.connect(self.show_cluster)
        self.selected_cluster = None
        self.update_cluster_plot()

    def on_save_button_click(self, elements):
        path, is_ok = QInputDialog.getText(self, 'Save to file', 'Enter filename')
        if is_ok and path:
            if not path.endswith(".csv"):
                path += ".csv"
            try:
                elements.to_csv(path)
            except:
                error = QMessageBox()
                error.setIcon(QMessageBox.Critical)
                error.setText("Something wrong happened while writing data to file. Try again")
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
