from functools import partial

import numpy as np
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QFormLayout, QLabel, QVBoxLayout, QSpinBox, QPushButton, \
    QComboBox, QTableView, QInputDialog, QMessageBox
from algorithms import get_samples
from matplotlib import pyplot as plt

from visualization.clustering import GMMCanvas

from src.widgets import QtTable


class GMMResultsWidget(QWidget):
    def __init__(self, df, labels, mean, sigma, options):
        super().__init__()
        self.df = df.select_dtypes(include=['number'])
        self.columns = self.df.columns
        self.labels = labels
        self.max_label = np.amax(self.labels) + 1
        self.mean = pd.DataFrame(mean, columns=self.columns)
        self.sigma = sigma
        self.selected_cluster = None
        self.layout = QHBoxLayout(self)

        self.num_samples = min(35, self.df.shape[0] // 2)
        self.samples = get_samples(self.df, self.num_samples)
        self.ox = self.columns[0]
        self.oy = self.columns[0] if len(self.columns) < 2 else self.columns[1]

        # algorithm parameters
        self.params_group = QGroupBox()
        self.params_group.setTitle("Parameters")
        self.params_layout = QFormLayout(self.params_group)
        for option, value in options.items():
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
        self.sample_box.setMaximum(min(self.df.shape[0], 10000))
        self.sample_box.setProperty("value", self.num_samples)
        self.sample_button = QPushButton("Refresh samples")
        self.sample_button.clicked.connect(partial(self.click_listener, 'new_samples'))
        self.settings_box_layout.addRow(self.sample_box, self.sample_button)
        # axis
        self.settings_box_layout.addRow(QLabel("Set axis:"))
        self.ox_box = QComboBox()
        self.ox_box.addItems(self.columns)
        self.oy_box = QComboBox()
        self.oy_box.addItems(self.columns)
        if len(self.columns) > 1:
            self.oy_box.setCurrentIndex(1)
        self.ox_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.oy_box.currentTextChanged.connect(partial(self.click_listener, 'set_axis'))
        self.settings_box_layout.addRow(QLabel("OX:"), self.ox_box)
        self.settings_box_layout.addRow(QLabel("OY:"), self.oy_box)
        self.settings_box_layout.setSpacing(10)
        self.clustering_group_layout.addWidget(self.settings_group_box)

        # plot
        self.fig, axes = plt.subplots(1, 1)
        self.clusters_canvas = GMMCanvas(self.fig, axes, False)
        self.clustering_group_layout.addWidget(self.clusters_canvas, 1)

        # cluster details
        self.clusters_details_group = QGroupBox()
        self.clusters_group_layout = QVBoxLayout(self.clusters_details_group)
        self.clusters_details_group.setTitle("Cluster")
        self.clusters_table = QTableView()
        self.clusters_table.setModel(QtTable(self.mean.round(3)))
        self.clusters_table.doubleClicked.connect(self.show_cluster)
        for i in range(len(self.columns)):
            self.clusters_table.setColumnWidth(i, 120)
        self.clusters_table_header = QWidget()
        self.clusters_table_header_layout = QHBoxLayout()
        self.clusters_table_instruction = QLabel("Double click on any field to preview a cluster")
        self.save_all_button = QPushButton("SAVE RESULTS")
        self.save_all_button.clicked.connect(partial(self.on_save_button_click, self.df.assign(cluster=self.labels)))
        self.save_all_button.setFixedWidth(120)
        self.clusters_table_header_layout.addWidget(self.clusters_table_instruction)
        self.clusters_table_header_layout.addWidget(self.save_all_button)
        self.clusters_table_header.setLayout(self.clusters_table_header_layout)
        self.fig_distributions, ax = plt.subplots(1, 1)
        self.clusters_canvas = GMMCanvas(self.fig_distributions, ax, False)
        self.clusters_group_layout.addWidget(self.clusters_table_header)
        self.clusters_group_layout.addWidget(self.clusters_table, 1)
        self.clusters_group_layout.addWidget(self.clusters_canvas, 1)
        self.layout.addWidget(self.clustering_result_group, 1)
        self.layout.addWidget(self.clusters_details_group, 1)
        self.update_plot()
        self.update_cluster_plot()

    def click_listener(self, button_type: str):
        match button_type:
            case 'new_samples':
                num = self.sample_box.value()
                self.num_samples = num
                self.samples = get_samples(self.df, self.num_samples)
                self.update_plot()
                self.update_cluster_plot()
            case 'set_axis':
                self.ox = self.ox_box.currentText()
                self.oy = self.oy_box.currentText()
                self.update_plot()
                self.update_cluster_plot()

    def update_plot(self):
        samples_data = self.df.iloc[self.samples]
        x = samples_data[self.ox]
        y = samples_data[self.oy]
        min_x = self.df[self.ox].min()
        max_x = self.df[self.ox].max()
        min_y = self.df[self.oy].min()
        max_y = self.df[self.oy].max()
        sep_x = 0.1 * (max_x - min_x)
        sep_y = 0.1 * (max_y - min_y)

        labels = [self.labels[sample] for sample in self.samples]
        self.clusters_canvas.clusters_plot(x, y, list(self.columns), self.mean.values, self.sigma, labels, self.max_label,
                                           self.ox, self.oy, min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y)

    def update_cluster_plot(self):
        if self.selected_cluster is not None:
            indexes = [i for i in range(len(self.labels)) if self.labels[i] == self.selected_cluster]
            x = self.df.iloc[indexes][self.ox]
            y = self.df.iloc[indexes][self.oy]
            min_x = x.min()
            max_x = x.max()
            min_y = y.min()
            max_y = y.max()
            sep_x = 0.1 * (max_x - min_x)
            sep_y = 0.1 * (max_y - min_y)
            x_means = self.mean[self.ox]
            y_means = self.mean[self.oy]
            x_index, y_index = [self.columns.get_loc(self.ox), self.columns.get_loc(self.oy)]
            mean = [x_means.iloc[self.selected_cluster], y_means.iloc[self.selected_cluster]]
            sigma_helper = self.sigma[self.selected_cluster]
            sigma = [
                [sigma_helper[x_index][x_index], sigma_helper[x_index][y_index]],
                [sigma_helper[y_index][x_index], sigma_helper[y_index][y_index]],
            ]

            self.clusters_canvas.chosen_cluster_plot(x, y, mean, sigma, self.selected_cluster,
                                                     len(x_means), self.ox, self.oy, min_x - sep_x, max_x + sep_x,
                                                     min_y - sep_y, max_y + sep_y)
        else:
            x = self.df[self.ox]
            y = self.df[self.oy]
            min_x = x.min()
            max_x = x.max()
            min_y = y.min()
            max_y = y.max()
            sep_x = 0.1 * (max_x - min_x)
            sep_y = 0.1 * (max_y - min_y)
            x_means = self.mean[self.ox]
            y_means = self.mean[self.oy]
            x_index, y_index = [self.columns.get_loc(self.ox), self.columns.get_loc(self.oy)]
            means = [x_means, y_means]
            sigmas = []
            for i in range(len(self.sigma)):
                sigma_helper = self.sigma[i]
                sigmas.append([
                    [sigma_helper[x_index][x_index], sigma_helper[x_index][y_index]],
                    [sigma_helper[y_index][x_index], sigma_helper[y_index][y_index]],
                ])

            self.clusters_canvas.clusters_means_plot(means, sigmas, self.ox, self.oy,
                                                     min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y)

    def show_cluster(self):
        self.selected_cluster = self.clusters_table.selectionModel().selectedIndexes()[0].row()
        rows = [i for i in range(len(self.labels)) if self.labels[i] == self.selected_cluster]
        elements = self.df.iloc[rows]
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
        self.clusters_group_layout.insertWidget(0, buttons_widget)
        self.clusters_table_header.hide()
        self.clusters_table.doubleClicked.disconnect()
        self.update_cluster_plot()

    def exit_from_cluster(self):
        self.clusters_table.setModel(QtTable(self.mean.round(3)))
        self.clusters_group_layout.itemAt(0).widget().setParent(None)
        self.clusters_table_header.show()
        self.clusters_table.doubleClicked.connect(self.show_cluster)
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
