from functools import partial
from random import randint

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QGroupBox
import numpy as np
import pandas as pd
import pygraphviz as pgv
from typing import List, Dict, Optional

import QGraphViz
from QGraphViz.Engines import Dot
from QGraphViz.QGraphViz import QGraphViz
from QGraphViz.DotParser import Graph, GraphType


class ExtraTreesStepsVisualization(QWidget):
    def __init__(self, data: pd.DataFrame, algorithms_steps: List[str], is_animation: bool):
        super().__init__()

        self.data = data
        self.steps = algorithms_steps
        self.is_animation = is_animation

        self.layout = QVBoxLayout(self)
        self.graphs = [self.make_graph(dot_string) for dot_string in self.steps]
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
        self.control_panel_layout.addWidget(self.description)
        self.control_panel_layout.addStretch()
        self.control_panel_layout.addWidget(self.num_label)
        self.control_panel_layout.addStretch()
        self.control_panel_layout.addWidget(self.left_button)
        self.control_panel_layout.addWidget(self.random_button)
        self.control_panel_layout.addWidget(self.right_button)
        self.layout.addLayout(self.control_panel_layout, 0)

    def postprocess_label(self, label: Optional[str]):
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
        qgv.new(Dot(Graph("graph", graph_type=GraphType.DirectedGraph), font=QFont("Helvetica", 12), margins=[10, 500]))
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
