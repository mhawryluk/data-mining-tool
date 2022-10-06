import matplotlib
import numpy as np
import pandas as pd
import joblib
from algorithms import check_numeric
from typing import Tuple, List, Callable
from algorithms import get_threads_count

metrics_types = ['gini', 'entropy']


class Leaf:
    def __init__(self, data: pd.Series):
        self.prediction = data.value_counts().index[0]
        self.samples = len(data)

    def graphviz_label(self, get_color: Callable) -> str:
        samples_str = f"samples = {self.samples}"
        class_str = f"class = {self.prediction}"
        color_hex = get_color(self.prediction)
        label_str = f'[label=<{samples_str}</br>{class_str}>, fillcolor="{color_hex}", shape=circle]'
        return label_str


class Node:
    def __init__(self, label: str, pivot: any):
        self.label = label
        self.pivot = pivot
        self.importance = 0
        self.samples = 0
        self.largest_class = None
        self.left = None
        self.right = None

    def graphviz_label(self, get_color: Callable) -> str:
        if isinstance(self.pivot, bool) or isinstance(self.pivot, str):
            pivot_str = f"{self.label} == {self.pivot}"
        elif isinstance(self.pivot, pd.Series):
            pivot_str = f"{self.label} in {self.pivot}"
        elif check_numeric(self.pivot):
            pivot_str = f"{self.label} &gt; {self.pivot}"
        else:
            raise TypeError(f"pivot must be bool, string, list or number not {type(self.pivot)}")
        samples_str = f"samples = {self.samples}"
        class_str = f"class = {self.largest_class}"
        color_hex = get_color(self.largest_class)
        label_str = f'[label=<{pivot_str}</br>{samples_str}</br>{class_str}>, fillcolor="{color_hex}", shape=box]'
        return label_str


class DecisionTree:

    def __init__(self, data: pd.DataFrame, label_name: str, features_number: int, min_child_number: int, max_depth: int,
                 min_metrics: float = 0, metrics_type: metrics_types = 'gini'):
        self.data = data
        self.label_name = label_name
        self.features_number = features_number
        self.min_child_number = min_child_number
        self.max_depth = max_depth
        self.min_metrics = min_metrics
        self.metrics_type = metrics_type
        self.features = pd.Series(data.columns.drop(self.label_name))
        self.root = self.create_node(pd.Series([True] * len(data), index=data.index), 1)

    def create_node(self, mask: pd.Series, depth) -> Node | Leaf:
        if not self._can_be_split(mask, depth):
            return Leaf(self.data[self.label_name][mask])
        features = self.features.sample(self.features_number)
        best_metrics = None
        left_mask = None
        right_mask = None
        best_feature = None
        best_pivot = None
        for feature in features:
            values = pd.Series(list(set(self.data[feature][mask])))
            if check_numeric(self.data[feature]):
                pivot = values.sample(1).iloc[0]
            else:
                if len(values) <= 2:
                    pivot = values.sample(1).iloc[0]
                else:
                    n = np.random.randint(1, len(values))
                    pivot = values.sample(n)
            result = self._split(mask, feature, pivot)
            if isinstance(result, bool):
                continue
            metrics, left, right = result
            if best_metrics is None or metrics > best_metrics:
                best_metrics = metrics
                left_mask = left
                right_mask = right
                best_feature = feature
                best_pivot = pivot

        if best_metrics is None:
            return Leaf(self.data[self.label_name][mask])

        node = Node(best_feature, best_pivot)
        node.importance = best_metrics
        node.left = self.create_node(left_mask, depth + 1)
        node.right = self.create_node(right_mask, depth + 1)
        node.samples = np.sum(mask)
        node.largest_class = self.data[self.label_name][mask].value_counts().index[0]
        return node

    def _can_be_split(self, mask: pd.Series, depth: int) -> bool:
        if len(set(self.data[self.label_name][mask])) == 1: # pure node
            return False
        if self.max_depth is not None and self.max_depth <= depth:
            return False
        if np.sum(mask) < 2 * self.min_child_number: # or add parameter
            return False
        return True

    def _split(self, mask: pd.Series, label: str, pivot: any) -> bool | Tuple[float, pd.Series, pd.Series]:
        def _set_label(row: pd.Series):
            if not mask[row.name]:
                return 0
            value = row[label]
            if isinstance(pivot, bool) or isinstance(pivot, str):
                if value == pivot:
                    return 1
            elif isinstance(pivot, pd.Series):
                if value in pivot:
                    return 1
            elif check_numeric(pivot):
                if float(value) > pivot:
                    return 1
            else:
                raise TypeError(f"pivot must be bool, string, list or number not {type(pivot)}")
            return 2

        division = self.data.apply(_set_label, axis='columns')
        right_mask = division == 1
        left_mask = division == 2
        if np.sum(left_mask) < self.min_child_number or np.sum(right_mask) < self.min_child_number:
            return False

        metrics = self._calculate_metrics(mask, left_mask, right_mask)

        if metrics < self.min_metrics:
            return False

        return metrics, left_mask, right_mask

    def _calculate_metrics(self, mask: pd.Series, left_mask: pd.Series, right_mask: pd.Series) -> float:
        if self.metrics_type == 'gini':
            parent = self._calculate_gini(mask)
            left = self._calculate_gini(left_mask)
            right = self._calculate_gini(right_mask)
        elif self.metrics_type == 'entropy':
            parent = self._calculate_gini(mask)
            left = self._calculate_gini(left_mask)
            right = self._calculate_gini(right_mask)
        else:
            raise ValueError(f"'{self.metrics_type}' is not valid type of metrics")
        split = np.sum(left_mask) * left + np.sum(right_mask) * right
        decrease = (np.sum(mask) * parent - split) / len(mask)
        return decrease

    def _calculate_gini(self, mask: pd.Series):
        labels = self.data[self.label_name][mask]
        gini = 1 - np.sum((labels.value_counts() / len(labels)) ** 2)
        return gini

    def _calculate_entropy(self, mask: pd.Series):
        labels = self.data[self.label_name][mask]
        prob = labels.value_counts() / len(labels)
        entropy = -1 * np.sum(prob * np.log2(prob))
        return entropy

    def predict(self, record: pd.Series) -> pd.Series:
        node = self.root
        while not isinstance(node, Leaf):
            node = self.next_node(record, node)
        return node.prediction

    def next_node(self, record: pd.Series, node: Node) -> Node | Leaf:
        value = record[node.label]
        pivot = node.pivot
        if isinstance(pivot, bool) or isinstance(pivot, str):
            if value == pivot:
                return node.right
        elif isinstance(pivot, pd.Series):
            if value in pivot:
                return node.right
        elif check_numeric(pivot):
            if float(value) > pivot:
                return node.right
        else:
            raise TypeError(f"pivot must be bool, string, list or number not {type(pivot)}")
        return node.left

    def calculate_importance(self) -> pd.Series:
        def add_value(node):
            if isinstance(node, Leaf):
                return
            values[node.label] += node.importance
            add_value(node.left)
            add_value(node.right)

        values = pd.Series(0, index=self.features)
        add_value(self.root)
        values = values / np.sum(values)
        return values

    def graphviz_str(self, get_color: Callable) -> str:
        def make_next_row(num_from, node_next, side=None):
            # global idx
            idx[0] += 1
            num_next = idx[0]
            rows.append(f"{num_next} {node_next.graphviz_label(get_color)} ;")
            if side is None:
                rows.append(f"{num_from} -> {num_next} [width=3] ;")
            elif side:
                rows.append(f"{num_from} -> {num_next} [color=lime, width=3, headlabel={str(side)}] ;")
            else:
                rows.append(f"{num_from} -> {num_next} [color=red, width=3, headlabel={str(side)}] ;")
            if isinstance(node_next, Node):
                make_next_row(num_next, node_next.left, False)
                make_next_row(num_next, node_next.right, True)

        rows = [f"0 {self.root.graphviz_label(get_color)} ;"]
        idx = [0]
        if isinstance(self.root, Node):
            make_next_row(0, self.root.left, False)
            make_next_row(0, self.root.right, True)
        rows_str = "\n".join(rows)
        dot_str = (
            "digraph Tree {\n"
            'node [shape=box, style="filled, rounded", color="black", fontname="helvetica"] ;\n'
            'edge [fontname="helvetica"] ;\n'
            f"{rows_str}\n"
            "}"
        )
        return dot_str


class ExtraTrees:

    def __init__(self, data: pd.DataFrame, forest_size: int, **kwargs):
        self.data = data
        self.forest_size = forest_size
        self.forest = None
        self.kwargs = kwargs
        self.feature_importance = None
        self.labels = np.array(list(set(self.data[kwargs['label_name']])))

    def get_config(self):
        return [(column, self.data[column].dtype) for column in self.data.columns if column != self.kwargs['label_name']]

    def _split_int_to_array(self, num: int, div: int) -> List[int]:
        greater = num % div
        lower = div - greater
        value = num // div
        return [value + 1] * greater + [value] * lower

    def run(self, *args):
        def do_job(num):
            forest = [DecisionTree(self.data, **self.kwargs) for _ in range(num)]
            feature_importance = pd.DataFrame([tree.calculate_importance() for tree in forest])
            return forest, feature_importance

        threads_count = get_threads_count()
        arr = self._split_int_to_array(self.forest_size, threads_count)
        results = joblib.Parallel(n_jobs=threads_count)(joblib.delayed(do_job)(num) for num in arr)
        self.forest = sum([result[0] for result in results], [])
        self.feature_importance = pd.concat([result[1] for result in results]).sum(axis='index') / self.forest_size
        self.feature_importance.sort_values(ascending=False, inplace=True)
        return self.predict, self.get_config(), self.feature_importance

    def predict(self, record: pd.Series) -> any:
        predictions = pd.Series([tree.predict(record) for tree in self.forest]).value_counts() / self.forest_size
        result = pd.Series(0, index=self.labels)
        for idx, item in predictions.iteritems():
            result[idx] = item
        result.sort_values(ascending=False, inplace=True)
        return result

    def get_steps(self) -> list:
        return [tree.graphviz_str(self.get_color) for tree in self.forest]

    def get_feature_importance(self) -> list:
        return self.feature_importance

    def get_color(self, label: str) -> str:
        normalize = matplotlib.colors.Normalize(vmin=0, vmax=len(self.labels))
        colormap = matplotlib.cm.get_cmap('Spectral')
        index = np.argwhere(self.labels == label)[0]
        return matplotlib.colors.to_hex(colormap(normalize(index)))