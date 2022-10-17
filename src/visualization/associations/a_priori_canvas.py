import operator

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from random import random
from itertools import compress


class APrioriCanvas(FigureCanvasQTAgg):
    HIGHLIGHTED_COLOR = "#f17300"
    REGULAR_COLOR = "#F5F5F5"
    HIGHLIGHTED_RULE_A_COLOR = "#81a4cd"
    HIGHLIGHTED_RULE_B_COLOR = "#054a91"
    HIGHLIGHTED_RULE_A_B_COLOR = "#f17300"

    def __init__(self, fig, axes, transaction_sets):
        self.axes = axes
        self.transaction_sets = transaction_sets
        self._assign_random_positions()

        super().__init__(fig)

    def plot_set(self, highlighted_set: tuple = None):
        self.axes.cla()

        mask = self._get_points_mask_set(set(highlighted_set) if highlighted_set is not None else None)
        self.axes.scatter(
            list(compress(self.x_positions, mask)), list(compress(self.y_positions, mask)),
            color=self.HIGHLIGHTED_COLOR, s=10, zorder=2
        )

        inverse_mask = list(map(operator.not_, mask))
        self.axes.scatter(
            list(compress(self.x_positions, inverse_mask)), list(compress(self.y_positions, inverse_mask)),
            color=self.REGULAR_COLOR, s=10, zorder=1,
        )
        self.draw()

    def plot_rule(self, set_a: tuple, set_b: tuple):
        self.axes.cla()

        mask_a, mask_b, mask_a_b, mask_remaining = self._get_points_mask_rule(set(set_a), set(set_b))
        self.axes.scatter(
            list(compress(self.x_positions, mask_a)), list(compress(self.y_positions, mask_a)),
            color=self.HIGHLIGHTED_RULE_A_COLOR, s=10, zorder=3
        )

        self.axes.scatter(
            list(compress(self.x_positions, mask_b)), list(compress(self.y_positions, mask_b)),
            color=self.HIGHLIGHTED_RULE_B_COLOR, s=10, zorder=2
        )

        self.axes.scatter(
            list(compress(self.x_positions, mask_a_b)), list(compress(self.y_positions, mask_a_b)),
            color=self.HIGHLIGHTED_RULE_A_B_COLOR, s=10, zorder=4
        )

        self.axes.scatter(
            list(compress(self.x_positions, mask_remaining)), list(compress(self.y_positions, mask_remaining)),
            color=self.REGULAR_COLOR, s=10, zorder=1
        )

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
