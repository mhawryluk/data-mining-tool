from typing import Dict

import numpy as np
import pandas as pd


def clustering_blobs_generator(options: Dict) -> pd.DataFrame:
    blobs_number = options["blobs_number"]
    sample_sizes = options["sample_sizes"]

    dims_number = options["dims_number"]
    dims_stds = options["dims_stds"]

    seed = options.get("seed")
    np.random.seed(seed)

    noise_percentage = options["noise"]

    centers = np.random.rand(blobs_number, dims_number)

    data = pd.DataFrame()

    for blob_i, (sample_size, center) in enumerate(zip(sample_sizes, centers), start=1):
        noise_count = round(sample_size * noise_percentage)
        blob_data = pd.DataFrame()
        for dim_i, (center_loc, dim_std) in enumerate(zip(center, dims_stds), start=1):
            blob_data[f"Dim #{dim_i}"] = np.concatenate(
                [
                    np.random.normal(center_loc, dim_std, size=sample_size),
                    np.random.rand(noise_count),
                ]
            )
        blob_data["Blob number"] = np.full(sample_size + noise_count, fill_value=blob_i)
        data = pd.concat([data, blob_data])

    return data.sample(frac=1).reset_index(drop=True).round(3)
