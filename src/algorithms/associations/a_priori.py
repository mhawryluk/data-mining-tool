from itertools import combinations, chain
from typing import List, Tuple, Optional
from enum import Enum
from utils import format_set

import pandas as pd


class APriori:
    def __init__(self, data: pd.DataFrame, index_column: str, min_support: float, min_confidence: float):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.data = data.set_index(index_column)
        self.columns = self.data.columns
        self.transaction_sets = list(
            map(set, self.data.apply(lambda x: x > 0).apply(lambda x: list(self.columns[x.values]), axis=1))
        )
        self.all_frequent_sets = {}
        self.k_frequent_sets_df = None
        self.saved_steps: List[dict] = []

    def run(self, with_steps) -> Tuple[pd.DataFrame, pd.DataFrame, List[set]]:
        frequent_sets = None

        for k in range(1, len(self.columns)):  # k as in k-item_sets - sets that contain k elements
            generated_item_sets = self._generate_item_sets(with_steps, frequent_sets)
            new_frequent_sets = {}
            for item_set, item_set_support in zip(generated_item_sets,
                                                  map(lambda item_set: self.support(item_set), generated_item_sets)):
                if item_set_support >= self.min_support:
                    new_frequent_sets[item_set] = item_set_support

                if with_steps:
                    self.saved_steps.append(
                        {
                            "part": APrioriPartLabel.CALCULATE_SUPPORT,
                            "set": item_set,
                            "support": item_set_support,
                            "min_support": self.min_support,
                            "data_frame": self.k_frequent_sets_df,
                        }
                    )

            if with_steps:
                self.saved_steps.append(
                    {
                        "part": APrioriPartLabel.FILTER_BY_SUPPORT,
                        "frequent_sets": list(new_frequent_sets.keys()),
                        "infrequent_sets": [set_ for set_ in generated_item_sets if set_ not in new_frequent_sets],
                        "data_frame": self.k_frequent_sets_df,
                    }
                )

            if not new_frequent_sets:
                break

            self.all_frequent_sets |= new_frequent_sets
            self.k_frequent_sets_df = self._get_frequent_set_pd(new_frequent_sets)

            if with_steps:
                self.saved_steps.append(
                    {
                        "part": APrioriPartLabel.SAVE_K_SETS,
                        "k": k,
                        "data_frame": self.k_frequent_sets_df,
                    }
                )

            frequent_sets = new_frequent_sets

        rules = self._get_association_rules(with_steps)
        if with_steps:
            self.saved_steps.append(
                {
                    "part": APrioriPartLabel.SAVE_RULES,
                    "data_frame": rules,
                }
            )

        return self._get_frequent_set_pd(self.all_frequent_sets), rules, self.transaction_sets

    def get_steps(self) -> List[dict]:
        return self.saved_steps

    def _get_frequent_set_pd(self, frequent_sets: dict):
        return pd.DataFrame.from_dict({
            format_set(frequent_set): round(self.support(frequent_set), 3)
            for frequent_set, support
            in frequent_sets.items()
        },
            orient="index",
            columns=["support"]
        ).sort_values(by="support", ascending=False)

    def _generate_item_sets(self, with_steps: bool, frequent_sets: Optional[List[tuple]]) -> List[tuple]:
        """
            Generates (k+1)-item_sets from k-item_sets
            Returns all found sets, not only strong ones
        """
        if frequent_sets is None:
            return [(item,) for item in self.columns.values]

        new_item_sets = []
        for frequent_set_1, frequent_set_2 in combinations(frequent_sets, 2):
            if not (frequent_set_1[:-1] == frequent_set_2[:-1] and frequent_set_1[-1] < frequent_set_2[-1]):
                continue

            new_item_set = self.join(frequent_set_1, frequent_set_2)

            if with_steps:
                self.saved_steps.append(
                    {
                        "part": APrioriPartLabel.JOIN_AND_PRUNE,
                        "set_1": frequent_set_1,
                        "set_2": frequent_set_2,
                        "new_set": new_item_set,
                        "data_frame": self.k_frequent_sets_df,
                    }
                )

            if not self._has_infrequent_subsets(with_steps, new_item_set, frequent_sets):
                new_item_sets.append(new_item_set)

        return new_item_sets

    @staticmethod
    def join(frequent_set_1: tuple, frequent_set_2: tuple) -> tuple:
        return frequent_set_1 + (frequent_set_2[-1],)

    def _has_infrequent_subsets(self, with_steps, new_frequent_set, prev_frequent_sets) -> bool:
        for subset in combinations(new_frequent_set, len(prev_frequent_sets)):
            if subset not in prev_frequent_sets:
                if with_steps:
                    self.saved_steps[-1]["infrequent_subset"] = subset
                return True

        if with_steps:
            self.saved_steps[-1]["infrequent_subset"] = None
        return False

    def support(self, item_set: tuple) -> float:
        count = 0
        for transaction_set in self.transaction_sets:
            if set(item_set).issubset(transaction_set):
                count += 1
        return count / len(self.transaction_sets)

    def confidence(self, item_set_a: tuple, item_set_b: tuple) -> float:  # a => b
        return self.all_frequent_sets[tuple(sorted(set(item_set_a) | set(item_set_b)))] \
               / self.all_frequent_sets[item_set_a]

    @staticmethod
    def get_all_subsets(item_set: tuple):
        return chain.from_iterable(combinations(item_set, i) for i in range(len(item_set) + 1))

    def _get_association_rules(self, with_steps) -> pd.DataFrame:
        rules = {}
        for frequent_set in self.all_frequent_sets.keys():
            for subset_a in self.get_all_subsets(frequent_set):
                subset_b = tuple(set(frequent_set) - set(subset_a))
                if not subset_a or not subset_b:
                    continue
                if (confidence := self.confidence(subset_a, subset_b)) >= self.min_confidence:
                    rules[f"{format_set(subset_a)} => {format_set(subset_b)}"] = round(confidence, 3)

                if with_steps:
                    self.saved_steps.append(
                        {
                            "part": APrioriPartLabel.GENERATE_RULES,
                            "set": frequent_set,
                            "set_a": subset_a,
                            "set_b": subset_b,
                            "confidence": confidence,
                            "min_confidence": self.min_confidence,
                            "data_frame": self.k_frequent_sets_df,
                        }
                    )

        return pd.DataFrame.from_dict(
            rules, orient="index", columns=["confidence"]
        ).sort_values(by="confidence", ascending=False)


class APrioriPartLabel(Enum):
    CALCULATE_SUPPORT = "Calculating support"
    FILTER_BY_SUPPORT = "Selecting frequent sets from generated and not already pruned"
    SAVE_K_SETS = "Saving found k-frequent sets"
    SAVE_RULES = "Saving found association rules"
    JOIN_AND_PRUNE = "Joining sets and pruning ones with infrequent subsets"
    GENERATE_RULES = "Generating and verifying potential rules from frequent sets"