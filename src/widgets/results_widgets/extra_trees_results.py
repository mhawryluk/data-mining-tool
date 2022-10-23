from functools import partial

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QGroupBox, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QScrollArea
from widgets.results_widgets import AlgorithmResultsWidget


class ExtraTreesResultsWidget(AlgorithmResultsWidget):
    def __init__(self, data, predict, configs, feature_importance, options):
        super().__init__(data, options)

        self.predict = predict
        self.configs = configs
        self.feature_importance = feature_importance
        self.first_prediction = True

        self.layout = QHBoxLayout(self)

        # algorithm parameters
        self.params_group = QGroupBox()
        self.params_group.setTitle("Parameters")
        self.params_layout = QFormLayout(self.params_group)

        for option, value in self.options.items():
            self.params_layout.addRow(QLabel(f'{option}:'), QLabel(f'{value}'))

        self.layout.addWidget(self.params_group)

        # feature importance
        self.feature_importance_group = QGroupBox()
        self.feature_importance_group.setTitle("Feature importance")
        self.feature_importance_layout = QFormLayout(self.feature_importance_group)

        for feature, value in self.feature_importance.items():
            self.feature_importance_layout.addRow(QLabel(feature), QLabel(str(round(value, 2))))

        self.layout.addWidget(self.feature_importance_group)

        # prediction
        self.prediction_group = QGroupBox()
        self.prediction_group.setTitle("Prediction")
        self.prediction_layout = QFormLayout(self.prediction_group)

        self.prediction_input = {}
        self.input_type = {}
        for label, t in configs:
            self.prediction_input[label] = QLineEdit()
            self.input_type[label] = t
            self.prediction_layout.addRow(QLabel(f"{label} [{str(t)}]"), self.prediction_input[label])
        self.prediction_button = QPushButton("Predict")
        self.prediction_button.clicked.connect(partial(self.click_listener, 'predict'))
        self.prediction_layout.addRow(self.prediction_button)

        self.scroll_box = QGroupBox()
        self.results_layout = QFormLayout(self.scroll_box)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.scroll_box)
        self.scroll.setWidgetResizable(True)
        self.prediction_layout.addRow(self.scroll)

        self.layout.addWidget(self.prediction_group)

    def click_listener(self, button_type: str):
        match button_type:
            case 'predict':
                try:
                    input_dict = {label: [field.text()] for label, field in self.prediction_input.items()}
                    input_data = pd.DataFrame(input_dict)
                    input_data.astype(self.input_type, copy=False)
                except ValueError:
                    error = QMessageBox()
                    error.setIcon(QMessageBox.Critical)
                    error.setText('Entered data are not in valid types.')
                    error.setWindowTitle("Error")
                    error.exec_()
                    return
                if self.first_prediction:
                    self.results_layout.addRow(QLabel("Results:"))
                    self.first_prediction = False
                result = self.predict(input_data.iloc[0])
                result_label = QLabel("\n".join([f"{label}: {100 * value}%" for label, value in result.items()]))
                result_label.setAlignment(Qt.AlignRight)
                input_label = QLabel("\n".join([f"{label}: {value}" for label, [value] in input_dict.items()]))
                self.results_layout.addRow(input_label, result_label)
