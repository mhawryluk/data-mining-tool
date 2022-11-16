from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from widgets import LoadingWidget, UnfoldWidget


class AlgorithmSetupWidget(UnfoldWidget):
    def __init__(self, parent, engine):
        super().__init__(parent, engine, "algorithm_setup_widget", "ALGORITHM SETUP")

        self.button.disconnect()
        self.button.clicked.connect(self.load_widget)

        # layout
        self.layout = QVBoxLayout(self.frame)

        # layouts for sections
        self.vertical_layout = QHBoxLayout()
        self.first_column = QVBoxLayout()
        self.second_column = QVBoxLayout()
        self.third_column = QVBoxLayout()

        # exploration technique selection
        self.technique_group = QGroupBox()
        self.technique_group.setTitle("Exploration technique")
        self.technique_group.setMinimumSize(220, 95)
        self.technique_group_layout = QFormLayout(self.technique_group)
        self.technique_group_layout.setFormAlignment(Qt.AlignVCenter)

        self.technique_box = QComboBox()
        self.technique_box.addItems(self.engine.get_all_techniques())
        self.technique_box.currentTextChanged.connect(
            partial(self.click_listener, "technique")
        )
        self.technique_group_layout.addRow(self.technique_box)

        # algorithm selection group
        self.algorithm_selection_group = QGroupBox()
        self.algorithm_selection_group.setTitle("Algorithm")
        self.algorithm_selection_group.setMinimumSize(220, 95)
        self.algorithm_selection_group_layout = QFormLayout(
            self.algorithm_selection_group
        )
        self.algorithm_selection_group_layout.setFormAlignment(Qt.AlignVCenter)

        self.algorithm_box = QComboBox()
        self.algorithm_box.addItems(
            self.engine.get_algorithms_for_techniques(self.technique_box.currentText())
        )
        self.algorithm_box.currentTextChanged.connect(
            partial(self.click_listener, "algorithm")
        )
        self.algorithm_selection_group_layout.addRow(self.algorithm_box)

        self.first_column.addWidget(self.technique_group)
        self.first_column.addStretch(1)
        self.first_column.addWidget(self.algorithm_selection_group)
        self.first_column.addStretch(1)

        # options group
        self.options_group = QGroupBox()
        self.options_group.setTitle("Options")
        self.options_group.setMinimumSize(220, 200)
        self.options_group_layout = QVBoxLayout(self.options_group)

        self.options_group_layout.addWidget(
            self.engine.get_option_widget(
                self.technique_box.currentText(), self.algorithm_box.currentText()
            )
        )

        self.second_column.addWidget(self.options_group)
        self.second_column.addStretch()

        # animation group
        self.animation_group = QGroupBox()
        self.animation_group.setTitle("Animation")
        self.animation_group.setMinimumSize(220, 65)
        self.animation_group_layout = QFormLayout(self.animation_group)

        self.animation_type = QComboBox()
        self.animation_type.addItems(["Step by step", "Animation", "No visualization"])
        self.animation_group_layout.addRow(
            QLabel("Visualization type"), self.animation_type
        )

        # description group
        self.algorithm_description_group = QGroupBox()
        self.algorithm_description_group.setTitle("Description")
        self.algorithm_description_group.setFixedWidth(280)
        self.algorithm_description_group.setMinimumHeight(125)
        self.algorithm_description_group_layout = QVBoxLayout(
            self.algorithm_description_group
        )
        self.algorithm_description = QLabel("Some description")
        self.algorithm_description.setWordWrap(True)
        self.algorithm_description_group_layout.addWidget(self.algorithm_description)

        self.third_column.addWidget(self.animation_group)
        self.third_column.addStretch(1)
        self.third_column.addWidget(self.algorithm_description_group)
        self.third_column.addStretch(1)

        self.vertical_layout.addStretch(2)
        self.vertical_layout.addLayout(self.first_column)
        self.vertical_layout.addStretch(1)
        self.vertical_layout.addLayout(self.second_column)
        self.vertical_layout.addStretch(1)
        self.vertical_layout.addLayout(self.third_column)
        self.vertical_layout.addStretch(2)

        # button
        self.run_button = QPushButton(self.frame)
        self.run_button.setText("Submit and run")
        self.run_button.setFixedWidth(300)
        self.run_button.clicked.connect(partial(self.click_listener, "run"))

        self.layout.addStretch()
        self.layout.addLayout(self.vertical_layout)
        self.layout.addWidget(self.run_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

    def load_widget(self):
        if self.engine.state.imported_data is None:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("No dataset was selected")
            error.setWindowTitle("Error")
            error.exec_()
            return

        self.engine.update_options()
        self.parent().unfold(self)

    def click_listener(self, button_type: str):
        technique = self.technique_box.currentText()
        algorithm = self.algorithm_box.currentText()
        match button_type:
            case "technique":
                self.algorithm_box.clear()
                self.algorithm_box.addItems(
                    self.engine.get_algorithms_for_techniques(technique)
                )
            case "algorithm":
                for i in reversed(range(self.options_group_layout.count())):
                    self.options_group_layout.itemAt(i).widget().setParent(None)
                if algorithm:
                    self.options_group_layout.addWidget(
                        self.engine.get_option_widget(
                            technique,
                            algorithm,
                        )
                    )
                    self.algorithm_description.setText(
                        f"Some description for {algorithm}"
                    )  # get from algorithm config
            case "run":
                loading = LoadingWidget(self.run_handle)
                loading.execute()

    def run_handle(self):
        technique = self.technique_box.currentText()
        algorithm = self.algorithm_box.currentText()
        data = self.engine.get_option_widget(technique, algorithm).get_data()
        type_visualization = self.animation_type.currentText()
        will_be_visualized = type_visualization != "No visualization"
        is_animation = type_visualization == "Animation"
        is_run = self.engine.run(
            technique, algorithm, will_be_visualized, is_animation, **data
        )
        if is_run:
            if will_be_visualized:
                self.parent().unfold_by_id("algorithm_run_widget")
            else:
                self.parent().unfold_by_id("results_widget")
