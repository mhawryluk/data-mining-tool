from typing import Dict
import pandas as pd
import numpy as np


def clustering_blobs_generator(options: Dict) -> pd.DataFrame:
    sample_sizes = options["sample_sizes"]
    dims_number = options["dims_number"]
    clusters_number = options["clusters_number"]
    cluster_stds = options["cluster_stds"]

    seed = options.get("seed")
    np.random.seed(seed)

    centers = np.random.rand(clusters_number, dims_number)

    data = pd.DataFrame()

    for sample_size, center in zip(sample_sizes, centers):
        cluster_data = pd.DataFrame()
        for i, (center_loc, cluster_std) in enumerate(zip(center, cluster_stds), start=1):
            cluster_data[f"dim {i}"] = np.random.normal(center_loc, cluster_std, size=sample_size)
        data = pd.concat([data, cluster_data])

    return data.sample(frac=1).reset_index(drop=True).round(3)
