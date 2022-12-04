from typing import Dict

import numpy as np
import pandas as pd


def clustering_blobs_generator(options: Dict) -> pd.DataFrame:
    blobs_number = options["blobs_number"]
    sample_sizes = options["sample_sizes"]

    dims_number = options["dims_number"]
    blobs_dims_stds = options["dims_stds"]

    seed = options.get("seed")
    np.random.seed(seed)

    noise_percentage = options["noise"]

    centers = np.random.rand(blobs_number, dims_number) * 50

    data = pd.DataFrame()

    for blob_i, (sample_size, center, dims_stds) in enumerate(
        zip(sample_sizes, centers, blobs_dims_stds), start=1
    ):
        noise_count = round(sample_size * noise_percentage)
        blob_data = pd.DataFrame()
        normal_data = np.random.multivariate_normal(
            center, np.diag(np.array(dims_stds)), sample_size
        ).T

        for dim_i, normal_data_i in enumerate(normal_data, start=1):
            blob_data[f"Dim #{dim_i}"] = np.concatenate(
                [
                    normal_data_i,
                    np.random.rand(noise_count),
                ]
            )
        blob_data["Blob number"] = np.full(sample_size + noise_count, fill_value=blob_i)
        data = pd.concat([data, blob_data])

    return data.sample(frac=1).reset_index(drop=True).round(3)
