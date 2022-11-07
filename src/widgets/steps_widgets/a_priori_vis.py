from functools import partial
from typing import List

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFormLayout, QGroupBox, \
    QSpinBox, QPushButton, QLabel, QScrollArea, QSizePolicy, QTableView

from utils import AutomateSteps, format_set
from visualization import APrioriGauge, APrioriGraphPlot
from widgets import QtTable
from algorithms.associations import APrioriPartLabel
from widgets.steps_widgets import AlgorithmStepsVisualization


class APrioriStepsVisualization(AlgorithmStepsVisualization):
    def __init__(self, data: pd.DataFrame, algorithms_steps: List[dict], is_animation: bool):
        super().__init__(data, algorithms_steps, is_animation)

        self.is_running = False
        self.animation = None
        self.max_step = len(algorithms_steps) - 1
        self.current_step = 0

        self.setObjectName("a_priori_steps_visualization")

        # layout
        self.layout = QVBoxLayout(self)
        self.bottom_row_layout = QHBoxLayout()
        self.bottom_row_layout.setSpacing(35)

        # visualization layout
        self.visualization_box = QGroupBox()
        self.visualization_box.setTitle("APriori step by step")
        self.visualization_box_layout = QVBoxLayout(self.visualization_box)

        # visualization charts and plots
        self.sets_table = QTableView()
        self.gauge_chart = APrioriGauge()
        self.gauge_chart.layout().setContentsMargins(0, 0, 0, 0)
        self.graph_plot = APrioriGraphPlot()
        self.graph_plot.layout().setContentsMargins(0, 0, 0, 0)
        self.algorithm_part_label = QLabel()

        self.step_vis_layout = QHBoxLayout()
        self.step_charts_layout = QVBoxLayout()

        self.step_charts_layout.addWidget(self.graph_plot, 1)
        self.step_charts_layout.addWidget(self.gauge_chart, 1)

        self.step_vis_layout.addWidget(self.sets_table, 1)
        self.step_vis_layout.addLayout(self.step_charts_layout, 1)

        self.visualization_box_layout.addWidget(self.algorithm_part_label, 0, alignment=Qt.AlignCenter)
        self.visualization_box_layout.addLayout(self.step_vis_layout, 3)
        self.visualization_box_layout.addWidget(self._render_description(), 2)

        # controls
        self._render_control_ui()

        self.layout.addWidget(self.visualization_box)
        self.update_plot(0)

    def _render_control_ui(self):
        if self.is_animation:
            self.automat = AutomateSteps(lambda: self.change_step(1), lambda: self.change_step(-1 * self.current_step))
            self.is_running = False

            # animation
            self.animation_box = QGroupBox()
            self.animation_box.setFixedWidth(250)
            self.animation_box.setTitle("Animation")
            self.animation_box_layout = QFormLayout(self.animation_box)

            self.restart_button = QPushButton("Restart")
            self.restart_button.clicked.connect(partial(self.click_listener, 'restart'))
            self.run_button = QPushButton("Start animation")
            self.run_button.clicked.connect(partial(self.click_listener, 'run'))
            self.interval_box = QSpinBox()
            self.interval_box.setMinimum(500)
            self.interval_box.setMaximum(3000)
            self.interval_box.setValue(1000)
            self.interval_box.setSingleStep(20)

            self.animation_box_layout.addRow(QLabel("Interval time [ms]:"), self.interval_box)
            self.animation_box_layout.addRow(self.restart_button)
            self.animation_box_layout.addRow(self.run_button)

            self.step_label = QLabel("STEP: {}".format(self.current_step))
            self.animation_box_layout.addWidget(self.step_label)

            self.description_group_box_layout.addWidget(self.animation_box, 0)

        else:
            self.visualization_box_layout.addStretch()

            # control buttons
            self.control_buttons_layout = QHBoxLayout()
            self.left_box = QSpinBox()
            self.left_box.setMinimum(1)
            self.right_box = QSpinBox()
            self.right_box.setMinimum(1)
            self.left_button = QPushButton("PREV")
            self.left_button.clicked.connect(partial(self.click_listener, 'prev'))
            self.right_button = QPushButton("NEXT")
            self.right_button.clicked.connect(partial(self.click_listener, 'next'))
            self.step_label = QLabel("STEP: {}".format(self.current_step))

            self.next_part_button = QPushButton("NEXT PART")
            self.next_part_button.clicked.connect(partial(self.click_listener, 'next part'))
            self.prev_part_button = QPushButton("PREV PART")
            self.prev_part_button.clicked.connect(partial(self.click_listener, 'prev part'))

            self.control_buttons_layout.addWidget(self.prev_part_button)
            self.control_buttons_layout.addWidget(self.left_button)
            self.control_buttons_layout.addWidget(self.left_box)
            self.control_buttons_layout.addStretch()
            self.control_buttons_layout.addWidget(self.step_label)
            self.control_buttons_layout.addStretch()
            self.control_buttons_layout.addWidget(self.right_box)
            self.control_buttons_layout.addWidget(self.right_button)
            self.control_buttons_layout.addWidget(self.next_part_button)

            self.visualization_box_layout.addLayout(self.control_buttons_layout, 0)

    def _render_description(self):
        description = "Apriori algorithm - steps visualization"

        self.description_label = QLabel(description)
        self.description_label.setWordWrap(True)
        self.description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.description_group_box = QGroupBox()
        self.description_group_box.setTitle("Description")
        self.description_group_box_layout = QHBoxLayout(self.description_group_box)

        self.scroll_box = QGroupBox()
        self.scroll_box_layout = QFormLayout(self.scroll_box)
        self.scroll = QScrollArea()
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll.setWidget(self.scroll_box)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumHeight(26)
        self.description_group_box_layout.addWidget(self.scroll)

        self.scroll_box_layout.addWidget(self.description_label)
        return self.description_group_box

    def click_listener(self, button_type: str):
        match button_type:
            case 'prev':
                self.change_step(-self.left_box.value())
            case 'next':
                self.change_step(self.right_box.value())
            case 'restart':
                self.is_running = False
                self.interval_box.setEnabled(True)
                self.run_button.setEnabled(True)
                self.automat.restart()
                self.run_button.setText("Start animation")
            case 'run':
                self.is_running = not self.is_running
                if self.is_running:
                    self.restart_button.setEnabled(False)
                    self.interval_box.setEnabled(False)
                    self.automat.set_time(self.interval_box.value())
                    self.automat.resume()
                    self.run_button.setText("Stop animation")
                else:
                    self.automat.pause()
                    self.run_button.setText("Start animation")
                    self.restart_button.setEnabled(True)
            case 'next part':
                step_delta = 1
                current_part = self.algorithms_steps[self.current_step]['part']
                while self.current_step + step_delta <= self.max_step and \
                        self.algorithms_steps[self.current_step + step_delta]['part'] == current_part:
                    step_delta += 1

                self.change_step(step_delta)
            case 'prev part':
                step_delta = -1
                current_part = self.algorithms_steps[self.current_step]['part']
                while self.current_step + step_delta >= 0 and \
                        self.algorithms_steps[self.current_step + step_delta]['part'] == current_part:
                    step_delta -= 1

                current_part = self.algorithms_steps[self.current_step + step_delta]['part']
                while self.current_step + step_delta >= 0 and \
                        self.algorithms_steps[self.current_step + step_delta]['part'] == current_part:
                    step_delta -= 1

                step_delta += 1
                self.change_step(step_delta)

    def change_step(self, change: int):
        new_step = max(0, min(self.max_step, self.current_step + change))
        if new_step == self.current_step:
            return
        self.current_step = new_step
        self.step_label.setText("STEP: {}".format(self.current_step))
        self.update_plot(self.current_step)
        self.step_label.update()

    def update_plot(self, step: int):
        if step == self.max_step:
            if self.is_animation:
                self.run_button.setText("Start animation")
                self.run_button.setEnabled(False)
                self.is_running = False
                self.change_enabled_buttons(True)

        self.current_step = step
        step_dict = self.algorithms_steps[self.current_step]
        df = step_dict['data_frame']
        if df is not None:
            df = df.reset_index()
            if "confidence" in df:
                df.rename(columns={'index': 'association rules'}, inplace=True)
            else:
                df.rename(columns={'index': 'frequent sets'}, inplace=True)

        self.sets_table.setModel(QtTable(df) if df is not None else None)
        self.algorithm_part_label.setText(step_dict['part'].value)
        self.gauge_chart.reset()
        self.graph_plot.reset()

        description = ""
        match step_dict['part']:
            case APrioriPartLabel.CALCULATE_SUPPORT:
                description = "Checking whether set: {} is frequent.\nIts support equals {} \nIt is {}a frequent set." \
                    .format(format_set(step_dict['set']), round(step_dict['support'], 3),
                            'not ' if step_dict['support'] < step_dict['min_support'] else '')
                self.gauge_chart.plot_value(round(step_dict['support'], 3), step_dict['min_support'], 'support')
                self.graph_plot.plot_set(step_dict['set'])
            case APrioriPartLabel.FILTER_BY_SUPPORT:
                description = "We have found that the following sets are frequent:\n{}, whereas those are not:\n{}".format(
                    '\n'.join(map(format_set, step_dict['frequent_sets'])),
                    '\n'.join(map(format_set, step_dict['infrequent_sets'])))
            case APrioriPartLabel.SAVE_K_SETS:
                description = "We have found all frequent sets for k={}".format(step_dict['k'])
            case APrioriPartLabel.SAVE_RULES:
                description = "We have found all association rules for specified minimum confidence and support."
            case APrioriPartLabel.JOIN_AND_PRUNE:
                description = "We are joining sets: {} and {}, then analyzing resulting set: {}. ".format(
                    format_set(step_dict['set_1']), format_set(step_dict['set_2']), format_set(step_dict['new_set']))

                if step_dict['infrequent_subset'] is None:
                    description += "This set does not contain any infrequent subsets.  It might be frequent itself."
                else:
                    description += "This set contains an infrequent subset: {}. Therefore it is not frequent itself.".format(
                        step_dict['infrequent_subset'])
                self.graph_plot.plot_set(step_dict['new_set'])

            case APrioriPartLabel.GENERATE_RULES:
                description = "We divide frequent set into A = {} and B = {}. The confidence of the rule A => B " \
                              "equals {}\n\n".format(format_set(step_dict['set_a']), format_set(step_dict['set_b']),
                                                     round(step_dict['confidence'], 3))

                if step_dict['confidence'] >= step_dict['min_confidence']:
                    description += "We have found a new association rule."
                else:
                    description += "It is not enough to consider it a valid association rule for our data."

                self.graph_plot.plot_rule(step_dict['set_a'], step_dict['set_b'])
                self.gauge_chart.plot_value(round(step_dict['confidence'], 3), step_dict['min_confidence'],
                                            'confidence')

        self.description_label.setText(description)
