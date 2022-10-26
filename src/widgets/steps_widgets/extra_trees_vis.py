from functools import partial
from random import randint

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QGroupBox, QTableView, \
    QFormLayout, QSpinBox
import pandas as pd
import pygraphviz as pgv
from typing import List, Dict, Optional, Tuple

from QGraphViz.QGraphViz import QGraphViz
from QGraphViz.Engines import Dot
from QGraphViz.DotParser import Graph, GraphType

import graphviz

from widgets import QtTable
from widgets.steps_widgets import AlgorithmStepsVisualization
from utils import QtImageViewer, AutomateSteps, QImage


class StepWidget(QWidget):
    def __init__(self, graph: QWidget, info: Optional[List] = None):
        super().__init__()
        self.graph = graph
        self.info = info
        self.layout = QHBoxLayout(self)

        self.info_group = QGroupBox("Description")
        self.info_group.setFixedWidth(300)
        self.info_group_layout = QVBoxLayout(self.info_group)
        if self.info:
            self.table_info = QTableView()
            self.table_info.setModel(QtTable(pd.DataFrame(self.info,
                                                          columns=["Column name", "Pivot", "Metric changes"])))
            self.info_group_layout.addWidget(self.table_info)
        self.info_group_layout.addStretch(1)
        self.info_group_layout.addWidget(QLabel("Extremely Randomized Trees algorithm - steps visualization."))
        self.info_group_layout.addStretch(2)
        self.layout.addWidget(self.info_group)
        self.layout.addWidget(self.graph)


class TreeStepsVisualization(QWidget):
    def __init__(self, widget: QWidget, node_info: Dict, dot_steps: List[str], is_animation: bool):
        super().__init__()
        self.setWindowTitle("Tree creation steps")
        self.parent = widget
        self.node_info = node_info
        self.dot_steps = dot_steps
        self.max_steps = len(self.dot_steps)
        self.is_animation = is_animation
        self.current_step = 0

        self.layout = QVBoxLayout(self)

        self.step_group = QGroupBox()
        self.step_group_layout = QVBoxLayout(self.step_group)
        self.step_group_layout.addWidget(self.create_step_graph(self.current_step))
        self.layout.addWidget(self.step_group, 1)

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

            self.layout.addWidget(self.animation_box, 0)

        if not self.is_animation:
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
            self.control_buttons_layout.addWidget(self.left_button)
            self.control_buttons_layout.addWidget(self.left_box)
            self.control_buttons_layout.addStretch()
            self.control_buttons_layout.addWidget(self.step_label)
            self.control_buttons_layout.addStretch()
            self.control_buttons_layout.addWidget(self.right_box)
            self.control_buttons_layout.addWidget(self.right_button)

            self.layout.addLayout(self.control_buttons_layout, 0)
        else:
            self.step_label = QLabel("STEP: {}".format(self.current_step))
            self.layout.addWidget(self.step_label, 0, alignment=Qt.AlignCenter)

        self.showMaximized()

    def create_step_graph(self, step_num: int):
        if step_num % 2 == 0:
            info = self.node_info[step_num]
        else:
            info = None
        graph = graphviz.Source(self.dot_steps[step_num])
        graph.render("tmp/graph", format="png")
        if self.is_animation:
            image = QImage()
            image.setPixmap(QPixmap("tmp/graph.png"))
        else:
            image = QtImageViewer()
            image.open("tmp/graph.png")
        return StepWidget(image, info)

    def update_step(self):
        for i in reversed(range(self.step_group_layout.count())):
            self.step_group_layout.itemAt(i).widget().setParent(None)
        self.step_group_layout.addWidget(self.create_step_graph(self.current_step))

        self.step_label.setText("STEP: {}".format(self.current_step))
        self.step_label.update()

    def click_listener(self, button_type: str):
        match button_type:
            case 'prev':
                num = self.left_box.value()
                self.change_step(-1 * num)
            case 'next':
                num = self.right_box.value()
                self.change_step(num)
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

    def change_step(self, delta: int):
        new_step = delta + self.current_step
        new_step = max(0, min(new_step, self.max_steps - 1))
        if new_step == self.current_step:
            return
        self.current_step = new_step
        self.update_step()
        if self.current_step == self.max_steps - 1 and self.is_animation:
            self.automat.pause()
            self.run_button.setText("Start animation")
            self.run_button.setEnabled(False)
            self.restart_button.setEnabled(True)


class ExtraTreesStepsVisualization(AlgorithmStepsVisualization):
    def __init__(self, data: pd.DataFrame, algorithms_steps: List[Tuple[str, Dict, List[str]]], is_animation: bool):
        super().__init__(data, algorithms_steps, is_animation)

        self.steps_window = None
        self.layout = QVBoxLayout(self)
        self.graphs = [self.make_graph(dot_string) for dot_string, _, _ in self.algorithms_steps]
        self.current_graph = 1

        # graph section
        self.graph_group = QGroupBox()
        self.graph_group.setTitle("Graph")
        self.graph_group_layout = QVBoxLayout(self.graph_group)
        self.graph_group_layout.addWidget(self.graphs[self.current_graph - 1])
        self.layout.addWidget(self.graph_group, 1)

        # control panel
        self.control_panel_layout = QHBoxLayout()
        self.left_button = QPushButton("PREV")
        self.left_button.clicked.connect(partial(self.click_listener, 'prev'))
        self.right_button = QPushButton("NEXT")
        self.right_button.clicked.connect(partial(self.click_listener, 'next'))
        self.num_label = QLabel(f"Tree {self.current_graph}")
        self.description = QLabel("Orange -> FALSE\nBlue -> TRUE")
        self.random_button = QPushButton("Random graph")
        self.random_button.clicked.connect(partial(self.click_listener, 'random'))
        self.steps_button = QPushButton("Creation steps")
        self.steps_button.clicked.connect(partial(self.click_listener, 'steps'))
        self.control_panel_layout.addWidget(self.description)
        self.control_panel_layout.addStretch()
        self.control_panel_layout.addWidget(self.num_label)
        self.control_panel_layout.addStretch()
        self.control_panel_layout.addWidget(self.steps_button)
        self.control_panel_layout.addWidget(self.random_button)
        self.control_panel_layout.addWidget(self.left_button)
        self.control_panel_layout.addWidget(self.right_button)
        self.layout.addLayout(self.control_panel_layout, 0)

    @staticmethod
    def postprocess_label(label: Optional[str]):
        if label is None:
            return ''
        label = label[1:-1]
        label = label.replace('&gt;', '>')
        if '<br/>' not in label:
            return label
        return '\n'.join(label.split('<br/>'))
        
    def dict_of_param(self, data: Optional[str]) -> Dict:
        if data is None:
            return {}
        res = {}
        params = data.split(', ')
        for param in params:
            key, value = param.split('=', 1)
            if key == 'fillcolor':
                value = value[1:-1]
            if key == 'label':
                value = self.postprocess_label(value)
            res[key] = value
        return res

    def make_graph(self, data: str):
        graph_info = pgv.AGraph(data)
        graph_info.layout(prog='dot')
        poses = [float(node.attr['pos'].split(',')[1]) for node in graph_info.nodes_iter()]
        pos_delta = min(poses) + max(poses) + 20
        lines = data.split('{', 1)[1].rsplit('}', 1)[0].split('\n')
        qgv = QGraphViz(auto_freeze=True, hilight_Nodes=True)
        qgv.setStyleSheet("background-color:white;")
        qgv.new(Dot(Graph("graph", graph_type=GraphType.DirectedGraph), font=QFont("Helvetica", 12), margins=[20, 20]))
        nodes = {}
        for line in lines:
            if not line:
                continue
            if line.startswith('node') or line.startswith('edge'):
                continue
            param = None
            if '[' in line:
                value, param = line.split('[', 1)
                param = param.rsplit(']', 1)[0]
            else:
                value = line.rsplit(';', 1)[0]
            value_list = value.split()
            if len(value_list) == 1:
                node = value_list[0]
                param_dict = self.dict_of_param(param)
                if 'label' in param_dict.keys():
                    label_lines = param_dict["label"].split('\n')
                    max_len = max(label_lines, key=len)
                    rect = qgv.engine.fm.boundingRect(max_len)
                    width = rect.width() + 20
                    height = rect.height() * len(label_lines) + 20
                    param_dict['size'] = (width, height)
                param_dict['pos'] = [float(value) for value in graph_info.get_node(node).attr['pos'].split(',')]
                param_dict['pos'][0] = int(param_dict['pos'][0])
                param_dict['pos'][1] = int(pos_delta - param_dict['pos'][1])
                nodes[node] = qgv.addNode(qgv.engine.graph, str(node), **param_dict)
            elif len(value_list) == 3:
                node1 = value_list[0]
                node2 = value_list[2]
                param_dict = self.dict_of_param(param)
                qgv.addEdge(nodes[node1], nodes[node2], param_dict)
            else:
                raise ValueError("Invalid format of dot string")
        qgv.build()
        return qgv

    def click_listener(self, button_type: str):
        match button_type:
            case 'steps':
                data = self.algorithms_steps[self.current_graph - 1]
                self.steps_window = TreeStepsVisualization(self, data[1], data[2], self.is_animation)
                self.steps_window.show()
                return
            case 'next':
                new_graph = min(len(self.graphs), self.current_graph + 1)
                if new_graph == self.current_graph:
                    return
                self.current_graph = new_graph
            case 'prev':
                new_graph = max(1, self.current_graph - 1)
                if new_graph == self.current_graph:
                    return
                self.current_graph = new_graph
            case 'random':
                self.current_graph = randint(1, len(self.graphs))
        self.update_graph()

    def update_graph(self):
        for i in reversed(range(self.graph_group_layout.count())):
            self.graph_group_layout.itemAt(i).widget().setParent(None)
        self.graph_group_layout.addWidget(self.graphs[self.current_graph - 1])
        self.num_label.setText(f"Tree {self.current_graph}")
        self.num_label.update()
