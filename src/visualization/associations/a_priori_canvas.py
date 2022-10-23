import operator
from itertools import compress
from random import random

import matplotlib.pyplot as plt
import networkx as nx
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import plotly.graph_objects as go


class APrioriScatterPlot(FigureCanvasQTAgg):
    HIGHLIGHTED_COLOR = "#f17300"
    REGULAR_COLOR = "#F5F5F5"
    HIGHLIGHTED_RULE_A_COLOR = "#81a4cd"
    HIGHLIGHTED_RULE_B_COLOR = "#054a91"
    HIGHLIGHTED_RULE_A_B_COLOR = "#f17300"

    def __init__(self, fig: plt.Figure, axes: plt.Axes, transaction_sets):
        self.annot = None
        self.sc = None
        self.axes = axes
        fig.tight_layout()
        self.transaction_sets = transaction_sets
        self._assign_random_positions()
        self.fig = fig

        super().__init__(fig)

    def plot_set(self, highlighted_set: tuple = None):
        self.axes.cla()
        self.axes.axis("off")

        self.annot = self.axes.annotate(
            "",
            xy=(0, 0),
            xytext=(-20, 0),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
        )
        self.annot.set_visible(True)

        mask = self._get_points_mask_set(set(highlighted_set) if highlighted_set is not None else None)
        self.sc = self.axes.scatter(
            list(compress(self.x_positions, mask)), list(compress(self.y_positions, mask)),
            color=self.HIGHLIGHTED_COLOR, s=10, zorder=2, label="containing the frequent set"
        )

        inverse_mask = list(map(operator.not_, mask))
        self.axes.scatter(
            list(compress(self.x_positions, inverse_mask)), list(compress(self.y_positions, inverse_mask)),
            color=self.REGULAR_COLOR, s=10, zorder=1, label="not containing"
        )

        self.axes.legend(fontsize=5)
        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        self.draw()

    def plot_rule(self, set_a: tuple, set_b: tuple):
        self.axes.cla()
        self.axes.axis("off")

        mask_a, mask_b, mask_a_b, mask_remaining = self._get_points_mask_rule(set(set_a), set(set_b))
        self.axes.scatter(
            list(compress(self.x_positions, mask_a)), list(compress(self.y_positions, mask_a)),
            color=self.HIGHLIGHTED_RULE_A_COLOR, s=10, zorder=3, label="A",
        )

        self.axes.scatter(
            list(compress(self.x_positions, mask_b)), list(compress(self.y_positions, mask_b)),
            color=self.HIGHLIGHTED_RULE_B_COLOR, s=10, zorder=2, label="B",
        )

        self.axes.scatter(
            list(compress(self.x_positions, mask_a_b)), list(compress(self.y_positions, mask_a_b)),
            color=self.HIGHLIGHTED_RULE_A_B_COLOR, s=10, zorder=4, label="A and B",
        )

        self.axes.scatter(
            list(compress(self.x_positions, mask_remaining)), list(compress(self.y_positions, mask_remaining)),
            color=self.REGULAR_COLOR, s=10, zorder=1, label="~(A or B)",
        )

        self.axes.legend(fontsize=5)
        self.draw()

    def _assign_random_positions(self):
        self.x_positions = [random() for _ in self.transaction_sets]
        self.y_positions = [random() for _ in self.transaction_sets]

    def _get_points_mask_set(self, highlighted_set: set = None):
        if highlighted_set is None:
            return [False] * len(self.transaction_sets)

        return [set(highlighted_set).issubset(transaction_set) for transaction_set in self.transaction_sets]

    def _get_points_mask_rule(self, set_a: set, set_b: set):
        return [
                   set_a.issubset(transaction_set) and not set_b.issubset(transaction_set)
                   for transaction_set in self.transaction_sets
               ], [
                   set_b.issubset(transaction_set) and not set_a.issubset(transaction_set)
                   for transaction_set in self.transaction_sets
               ], [
                   set_a.issubset(transaction_set) and set_b.issubset(transaction_set)
                   for transaction_set in self.transaction_sets
               ], [
                   not set_a.issubset(transaction_set) and not set_b.issubset(transaction_set)
                   for transaction_set in self.transaction_sets
               ],

    def update_annot(self, ind):
        pos = self.sc.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        text = "\n---\n".join("\n".join(self.transaction_sets[n]) for n in ind["ind"])
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)

    def hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.axes:
            cont, ind = self.sc.contains(event)
            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()


class APrioriGauge(QWidget):
    BLUE = "#054a91"
    ORANGE = "#f17300"

    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.browser)
        self.resize(1000, 1000)

    def plot_value(self, metric, threshold, metric_name=""):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=metric,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': metric_name, 'font': {'size': 15}},
            gauge=dict(
                axis={'range': [None, 1], 'tickwidth': 1},
                bar={'color': (self.BLUE if metric >= threshold else self.ORANGE)},
                bgcolor="#dbe4ee",
                borderwidth=0,
                threshold={
                    'line': {'color': "red", 'width': 4},
                    'thickness': 1,
                    'value': threshold
                }
            )
        ))
        fig.update_layout(margin=dict(t=40, b=20, l=0, r=0))
        self.browser.setHtml(fig.to_html(include_plotlyjs="cdn"))

    def reset(self):
        self.browser.setHtml("")


class APrioriGraphPlot(QWidget):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.browser)
        self.resize(1000, 800)

    def plot_set(self, set_):
        graph = nx.complete_graph(len(set_))
        nx.relabel_nodes(graph, dict(enumerate(set_)), copy=False)
        self.plot_graph(graph, nx.spring_layout(graph), set_)

    def plot_rule(self, set_a, set_b):
        graph_a = nx.complete_graph(len(set_a))
        nx.relabel_nodes(graph_a, dict(enumerate(set_a)), copy=False)

        graph_b = nx.complete_graph(len(set_b))
        nx.relabel_nodes(graph_b, dict(enumerate(set_b)), copy=False)

        graph = nx.compose(graph_a, graph_b)
        self.plot_graph(graph, nx.spring_layout(graph, k=0.15, iterations=20), set_a + set_b)

    def plot_graph(self, graph: nx.Graph, pos, labels):
        edge_x = []
        edge_y = []
        for edge in graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=4, color='#054a91'),
            mode='lines',
            hoverinfo='skip',
        )

        node_trace = go.Scatter(
            x=[pos[node][0] for node in graph.nodes()],
            y=[pos[node][1] for node in graph.nodes()],
            mode='markers+text',
            textposition="top center",
            hoverinfo='text',
            text=labels,
            marker=dict(
                color='#054a91',
                size=20,
            )
        )

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                showlegend=False,
                paper_bgcolor="#dbe4ee",
                margin=dict(t=0, b=0, l=0, r=0),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 2]),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 2]),
            ),
        )

        self.browser.setHtml(fig.to_html(include_plotlyjs="cdn"))

    def reset(self):
        self.browser.setHtml("")
