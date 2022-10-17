import operator

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from random import random
from itertools import compress


class APrioriCanvas(FigureCanvasQTAgg):
    HIGHLIGHTED_COLOR = "#f17300"
    REGULAR_COLOR = "#F5F5F5"
    HIGHLIGHTED_RULE_A_COLOR = "#81a4cd"
    HIGHLIGHTED_RULE_B_COLOR = "#054a91"
    HIGHLIGHTED_RULE_A_B_COLOR = "#f17300"

    def __init__(self, fig: plt.Figure, axes: plt.Axes, transaction_sets):
        self.axes = axes
        fig.tight_layout()
        self.transaction_sets = transaction_sets
        self._assign_random_positions()

        super().__init__(fig)

    def plot_set(self, highlighted_set: tuple = None):
        self.axes.cla()
        self.axes.axis("off")

        mask = self._get_points_mask_set(set(highlighted_set) if highlighted_set is not None else None)
        self.axes.scatter(
            list(compress(self.x_positions, mask)), list(compress(self.y_positions, mask)),
            color=self.HIGHLIGHTED_COLOR, s=10, zorder=2, label="containing the frequent set"
        )

        inverse_mask = list(map(operator.not_, mask))
        self.axes.scatter(
            list(compress(self.x_positions, inverse_mask)), list(compress(self.y_positions, inverse_mask)),
            color=self.REGULAR_COLOR, s=10, zorder=1, label="not containing"
        )

        self.axes.legend(fontsize=5)
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
            color=self.HIGHLIGHTED_RULE_A_B_COLOR, s=10, zorder=4, label="A and B"
        )

        self.axes.scatter(
            list(compress(self.x_positions, mask_remaining)), list(compress(self.y_positions, mask_remaining)),
            color=self.REGULAR_COLOR, s=10, zorder=1, label="~(A or B)"
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


class APrioriBarPlot(FigureCanvasQTAgg):

    GREEN = "#3C887E"
    RED = "#6B2737"

    def __init__(self, fig: plt.Figure, axes: plt.Axes, min_support, min_confidence):
        self.axes = axes
        self.min_support = min_support
        self.min_confidence = min_confidence

        fig.subplots_adjust(bottom=0.3)

        super().__init__(fig)

    def plot_support(self, support):
        self.axes.cla()
        self.axes.set_ylim(ymin=0, ymax=max(self.min_support, self.min_confidence) + 0.1)
        self.axes.bar(["support"], [support], color=self.RED if support < self.min_support else self.GREEN)
        self.axes.axhline(y=self.min_support, linewidth=.5, color='black', linestyle="--")
        self.draw()

    def plot_confidence(self, confidence):
        self.axes.cla()
        self.axes.set_ylim(ymin=0, ymax=max(self.min_support, self.min_confidence) + 0.1)
        self.axes.bar(["confidence"], [confidence], color=self.RED if confidence < self.min_confidence else self.GREEN)
        self.axes.axhline(y=self.min_confidence, linewidth=.5, color='black', linestyle="--")
        self.draw()
