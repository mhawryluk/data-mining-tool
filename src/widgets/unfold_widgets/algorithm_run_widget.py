from functools import partial

from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QFormLayout, QSpinBox, QPushButton, QDialog, \
    QHBoxLayout

from widgets import UnfoldWidget


class AlgorithmRunWidget(UnfoldWidget):
    def __init__(self, parent, engine):
        super().__init__(parent, engine, 'algorithm_run_widget', 'ALGORITHM RUN')

        # layout
        self.layout = QVBoxLayout(self.frame)

        # animation
        self.animation_group = QGroupBox()
        self.animation_group.setTitle("Animation")
        self.animation_group.setMinimumWidth(200)
        self.animation_group_layout = QFormLayout(self.animation_group)

        self.animation_speed_box = QSpinBox()
        self.animation_group_layout.addRow(QLabel("Speed"), self.animation_speed_box)

        # "run" button
        self.run_animation_button = QPushButton("RUN")
        self.run_animation_button.clicked.connect(partial(self.click_listener, 'run_animation'))
        self.animation_group_layout.addRow(self.run_animation_button)

        # step by step
        self.steps_group = QGroupBox()
        self.steps_group.setTitle("Step by step")
        self.steps_group.setMinimumWidth(200)
        self.steps_group_layout = QFormLayout(self.steps_group)

        # "run" button
        self.run_steps_button = QPushButton("RUN")
        self.run_steps_button.clicked.connect(partial(self.click_listener, 'run_steps'))
        self.steps_group_layout.addRow(self.run_steps_button)

        # dialog error
        self.dialog = QDialog(self)
        self.dialog.setFixedHeight(50)
        self.dialog.setFixedWidth(400)
        self.dialog.setWindowTitle("Error message")
        QLabel("You didn't choose algorithm.\nPlease return to 'ALGORITHM SETUP' window.", self.dialog)

        # "exit" button
        self.exit_button = QPushButton("EXIT")
        self.exit_button.clicked.connect(partial(self.click_listener, 'exit'))
        self.exit_button.setFixedHeight(30)

        self.start_widget()

    def clear_layout(self, layout=None):
        if layout is None:
            layout = self.layout
        for i in reversed(range(layout.count())):
            child = layout.itemAt(i)
            if child.widget():
                child.widget().setParent(None)
            elif child.layout():
                self.clear_layout(child.layout())
            else:
                layout.removeItem(child)

    def start_widget(self):
        self.clear_layout()
        self.layout.addStretch(1)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch(1)
        horizontal_layout.addWidget(self.animation_group)
        horizontal_layout.addStretch(1)
        horizontal_layout.addWidget(self.steps_group)
        horizontal_layout.addStretch(3)
        self.layout.addLayout(horizontal_layout)
        self.layout.addStretch(3)
        self.layout.update()

    def click_listener(self, button_type: str):
        if button_type == 'run_steps':
            if self.engine.steps_vis is None:
                self.dialog.exec_()
                return
            self.clear_layout()
            self.layout.addWidget(self.exit_button)
            self.layout.addWidget(self.engine.steps_vis)
            self.layout.update()
        elif button_type == 'run_animation':
            pass
        elif button_type == 'exit':
            self.clear_layout()
            self.start_widget()
            self.layout.update()
