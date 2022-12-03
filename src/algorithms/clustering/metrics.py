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


def dunn_index(df: pd.DataFrame, labels: np.array):
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
            dis = distance(first, second)
            if dis > max_distance_intra:
                max_distance_intra = dis
    for i, row in enumerate(df.itertuples(index=False)):
        dis = distance(np.array(row), centroids[labels[i]])
        if dis < min_distance_inter:
            min_distance_inter = dis
    return min_distance_inter / max_distance_intra
