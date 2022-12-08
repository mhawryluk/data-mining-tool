from typing import Dict

import numpy as np
import pandas as pd

SCALING_FACTOR = 50


def normal_distribution_blobs_generator(options: Dict) -> pd.DataFrame:
    blobs_number = options["blobs_number"]
    sample_sizes = options["sample_sizes"]

    dims_number = options["dims_number"]
    blobs_dims_stds = options["dims_stds"]

    seed = options.get("seed")
    np.random.seed(seed)

    noise_percentage = options["noise"]

    centers = np.random.rand(blobs_number, dims_number) * SCALING_FACTOR

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
                    np.random.rand(noise_count) * SCALING_FACTOR,
                ]
            )
        blob_data["Blob number"] = np.full(sample_size + noise_count, fill_value=blob_i)
        data = pd.concat([data, blob_data])

    return data.sample(frac=1).reset_index(drop=True).round(3)


def noncentral_f_blobs_generator(options: Dict) -> pd.DataFrame:
    blobs_number = options["blobs_number"]
    sample_sizes = options["sample_sizes"]

    dims_number = options["dims_number"]

    blobs_dfnums = options["df_nums"]
    blobs_dfdens = options["df_dens"]

    seed = options.get("seed")
    np.random.seed(seed)

    noise_percentage = options["noise"]

    centers = np.random.rand(blobs_number, dims_number) * SCALING_FACTOR

    data = pd.DataFrame()

    for blob_i, (sample_size, center, df_num, df_den) in enumerate(
        zip(sample_sizes, centers, blobs_dfnums, blobs_dfdens), start=1
    ):
        noise_count = round(sample_size * noise_percentage)
        blob_data = pd.DataFrame()
        for dim_i, center_loc in enumerate(center, start=1):
            blob_data[f"Dim #{dim_i}"] = np.concatenate(
                [
                    np.random.noncentral_f(df_num, df_den, center_loc, size=sample_size)
                    + center_loc,
                    np.random.rand(noise_count) * SCALING_FACTOR,
                ]
            )
        blob_data["Blob number"] = np.full(sample_size + noise_count, fill_value=blob_i)
        data = pd.concat([data, blob_data])

    return data.sample(frac=1).reset_index(drop=True).round(3)
