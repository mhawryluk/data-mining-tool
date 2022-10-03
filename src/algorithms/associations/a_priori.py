from itertools import combinations, chain
from typing import List, Any

import pandas as pd


class APriori:
    def __init__(self, data: pd.DataFrame, index_column, min_support: float, min_confidence: float):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.step_counter = 0
        self.data = data
        self.data = self.data.set_index(index_column)
        self.columns = self.data.columns
        self.transaction_sets = list(
            map(set, self.data.apply(lambda x: x > 0).apply(lambda x: list(self.columns[x.values]), axis=1)))
        self.saved_steps = []
        self.frequent_sets = pd.DataFrame(
            columns=["support"],
        )

    def step(self) -> bool:
        self.saved_steps = [self.frequent_sets]
        return False

    def run(self, with_steps):
        runner = self.run_with_saving_steps if with_steps else self.run_without_saving_steps
        return runner()

    def run_with_saving_steps(self):
        frequent_sets = self.get_frequent_singletons()
        k = 1
        while frequent_sets:
            k_frequent_sets_df = pd.DataFrame(
                data=[round(self.support(frequent_set), 3) for frequent_set in frequent_sets],
                columns=["support"],
                index=frequent_sets
            )
            self.frequent_sets = pd.concat([self.frequent_sets, k_frequent_sets_df])
            self.saved_steps.append(k_frequent_sets_df)
            k += 1
            new_frequent_steps = list(filter(
                lambda frequent_set: self.support(frequent_set) > self.min_support,
                self.apriori_gen(frequent_sets)
            ))
            frequent_sets = new_frequent_steps

        rules = self.get_association_rules()
        self.saved_steps.append(rules)
        return self.frequent_sets, rules

    def run_without_saving_steps(self):
        frequent_sets = self.get_frequent_singletons()
        k = 1
        while frequent_sets:
            self.frequent_sets = pd.concat([self.frequent_sets, pd.DataFrame(
                data=[self.support(frequent_set) for frequent_set in frequent_sets],
                columns=["support"],
                index=frequent_sets
            )])
            k += 1
            new_frequent_steps = list(filter(
                lambda frequent_set: self.support(frequent_set) > self.min_support,
                self.apriori_gen(frequent_sets)
            ))
            frequent_sets = new_frequent_steps

        rules = self.get_association_rules()
        return self.frequent_sets, rules

    def get_steps(self) -> List[pd.DataFrame]:
        return self.saved_steps

    def get_frequent_singletons(self) -> list[tuple[Any]]:
        return [(item,) for item in self.columns.values if self.support((item,)) > self.min_support]

    def apriori_gen(self, frequent_sets):
        new_frequent_sets = list()
        for frequent_set_1 in frequent_sets:
            for frequent_set_2 in frequent_sets:
                for i in range(len(frequent_set_1) - 1):
                    if frequent_set_1[i] != frequent_set_2[i]:
                        break
                else:
                    if frequent_set_1[-1] < frequent_set_2[-1]:
                        new_frequent_set = self.join(frequent_set_1, frequent_set_2)
                        if not self.has_infrequent_subsets(new_frequent_set, frequent_sets):
                            new_frequent_sets.append(new_frequent_set)

        return new_frequent_sets

    @staticmethod
    def join(frequent_set_1: tuple, frequent_set_2: tuple):
        return frequent_set_1 + (frequent_set_2[-1],)

    @staticmethod
    def has_infrequent_subsets(new_frequent_set, prev_frequent_sets):
        for subset in combinations(new_frequent_set, len(new_frequent_set) - 1):
            if subset not in prev_frequent_sets:
                return True
        return False

    def support(self, item_set: tuple) -> float:
        count = 0
        for transaction_set in self.transaction_sets:
            if set(item_set).issubset(transaction_set):
                count += 1
        return count / self.data.shape[0]

    def confidence(self, item_set_a: tuple, item_set_b: tuple) -> float:  # a => b
        return self.support(tuple(set(item_set_a) | set(item_set_b))) / self.support(item_set_a)

    @staticmethod
    def get_all_subsets(item_set: tuple):
        return chain.from_iterable(combinations(item_set, i) for i in range(len(item_set) + 1))

    def get_association_rules(self):
        rules = {}
        for frequent_set in self.frequent_sets.iterrows():
            for subset_a in self.get_all_subsets(frequent_set[0]):
                subset_b = tuple(set(frequent_set[0]) - set(subset_a))
                if not subset_a or not subset_b:
                    continue
                if (confidence := self.confidence(subset_a, subset_b)) > self.min_confidence:
                    rules[f"{subset_a} => {subset_b}"] = round(confidence, 3)

        return pd.DataFrame.from_dict(rules, orient="index", columns=["confidence"])


def test():
    data = pd.read_csv("groceries_crosstab.csv")
    min_support = 0.05
    min_confidence = 0.3
    print(APriori(data, "Member_number", min_support, min_confidence).run(False))


if __name__ == "__main__":
    test()
