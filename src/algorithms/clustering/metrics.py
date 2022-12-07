import numpy as np
import pandas as pd


def distance(x, y):
    return np.sqrt(np.sum(x**2 + y**2))


def davies_bouldin_score(df: pd.DataFrame, labels: np.array):
    num_cluster = np.amax(labels) + 1
    centroids = []
    avg_distances = []
    for cluster in range(num_cluster):
        cluster_set = df.loc[labels == cluster].to_numpy()
        centroid = cluster_set.mean(axis=0)
        avg_distance = np.sqrt(
            (cluster_set**2 + np.stack([centroid**2] * len(cluster_set))).sum(
                axis=1
            )
        ).mean()
        centroids.append(centroid)
        avg_distances.append(avg_distance)
    R_matrix = np.zeros((num_cluster, num_cluster), dtype=np.float)
    for i in range(num_cluster):
        x = centroids[i]
        for j in range(i + 1, num_cluster):
            y = centroids[j]
            R_matrix[i, j] = R_matrix[j, i] = (
                avg_distances[i] + avg_distances[j]
            ) / distance(x, y)
    return np.sum(np.amax(R_matrix, axis=0)) / num_cluster


def dunn_score(df: pd.DataFrame, labels: np.array, distance_function=distance):
    num_cluster = np.amax(labels) + 1
    centroids = []
    for cluster in range(num_cluster):
        cluster_set = df.loc[labels == cluster].to_numpy()
        centroid = cluster_set.mean(axis=0)
        centroids.append(centroid)
    max_distance_intra = 0
    min_distance_inter = np.inf
    for i, first in enumerate(centroids):
        for second in centroids[i + 1 :]:
            dis = distance_function(first, second)
            min_distance_inter = min(min_distance_inter, dis)
    for cluster in range(num_cluster):
        cluster_df = df.loc[labels == cluster]
        for i, pointA in cluster_df.iterrows():
            for _, pointB in cluster_df.loc[i + 1 :].iterrows():
                dis = distance_function(pointA.to_numpy(), pointB.to_numpy())
                max_distance_intra = max(max_distance_intra, dis)
    return min_distance_inter / max_distance_intra


def silhouette_score(df: pd.DataFrame, labels: np.array):
    dis_same_class = np.zeros_like(labels, dtype=np.float)
    dis_next_class = np.zeros_like(labels, dtype=np.float)
    num_cluster = np.amax(labels) + 1
    for i, row in df.iterrows():
        cluster = labels[i]
        same_cluster_df = df.loc[labels == cluster].drop(index=i).to_numpy()
        dis_same_class[i] = np.sqrt(
            (
                same_cluster_df**2
                + np.stack([row.to_numpy() ** 2] * len(same_cluster_df))
            ).sum(axis=1)
        ).mean()

        min_dis = np.inf
        for j in range(num_cluster):
            if i == j:
                continue
            cluster_df = df.loc[labels == j].to_numpy()
            dis = np.sqrt(
                (
                    cluster_df**2 + np.stack([row.to_numpy() ** 2] * len(cluster_df))
                ).sum(axis=1)
            ).mean()
            min_dis = min(min_dis, dis)
        dis_next_class[i] = min_dis
    silhouette_per_sample = (dis_next_class - dis_same_class) / np.maximum(
        dis_same_class, dis_next_class
    )
    return silhouette_per_sample.mean()
