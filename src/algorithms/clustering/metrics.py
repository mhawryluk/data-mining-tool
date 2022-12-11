import numpy as np
import pandas as pd


def distance(x, y):
    return np.linalg.norm(x - y)


def davies_bouldin_score(df: pd.DataFrame, labels: np.array):
    clusters = np.unique(labels)
    num_cluster = len(clusters)
    centroids = []
    avg_distances = []
    for cluster in clusters:
        cluster_set = df.loc[labels == cluster].to_numpy()
        centroid = cluster_set.mean(axis=0)
        avg_distance = np.linalg.norm(
            cluster_set - np.tile(centroid, (len(cluster_set), 1)), axis=1
        ).mean()
        centroids.append(centroid)
        avg_distances.append(avg_distance)
    R_matrix = np.zeros((num_cluster, num_cluster), dtype=np.float)
    for i in range(num_cluster):
        x = centroids[i]
        for j in range(i + 1, num_cluster):
            y = centroids[j]
            avg_distance = avg_distances[i] + avg_distances[j]
            centroids_dis = distance(x, y)
            if avg_distance == 0:
                R_matrix[i, j] = R_matrix[j, i] = 0
                continue
            if centroids_dis == 0:
                return np.inf
            R_matrix[i, j] = R_matrix[j, i] = avg_distance / centroids_dis
    return np.amax(R_matrix, axis=0).mean()


def dunn_score(df: pd.DataFrame, labels: np.array, distance_function=distance):
    clusters = np.unique(labels)
    centroids = []
    for cluster in clusters:
        cluster_set = df.loc[labels == cluster].to_numpy()
        centroid = cluster_set.mean(axis=0)
        centroids.append(centroid)
    max_distance_intra = 0
    min_distance_inter = np.inf
    for i, first in enumerate(centroids):
        for second in centroids[i + 1 :]:
            dis = distance_function(first, second)
            min_distance_inter = min(min_distance_inter, dis)
    for cluster in clusters:
        cluster_df = df.loc[labels == cluster]
        size = len(cluster_df)
        for i, (_, pointA) in enumerate(cluster_df.iterrows()):
            if i + 1 == size:
                continue
            dis = np.linalg.norm(
                cluster_df.iloc[i + 1 :].to_numpy()
                - np.tile(pointA.to_numpy(), (size - i - 1, 1)),
                axis=1,
            ).max()
            max_distance_intra = max(max_distance_intra, dis)
    if min_distance_inter == 0:
        return 0
    if max_distance_intra == 0:
        return np.inf
    return min_distance_inter / max_distance_intra


def silhouette_score(df: pd.DataFrame, labels: np.array):
    clusters = np.unique(labels)
    dis_same_class = np.zeros_like(labels, dtype=np.float)
    dis_next_class = np.zeros_like(labels, dtype=np.float)
    for i, row in df.iterrows():
        cluster = labels[i]
        same_cluster_df = df.loc[labels == cluster].drop(index=i).to_numpy()
        size = len(same_cluster_df)
        dis_same_class[i] = (
            np.linalg.norm(
                same_cluster_df - np.tile(row.to_numpy(), (size, 1)), axis=1
            ).mean()
            if size
            else 0
        )

        min_dis = np.inf
        for j in clusters:
            if cluster == j:
                continue
            cluster_df = df.loc[labels == j].to_numpy()
            dis = np.linalg.norm(
                cluster_df - np.tile(row.to_numpy(), (len(cluster_df), 1)), axis=1
            ).mean()
            min_dis = min(min_dis, dis)
        dis_next_class[i] = min_dis
    denominator = np.maximum(dis_same_class, dis_next_class)
    if 0 in denominator:
        return np.inf
    silhouette_per_sample = (dis_next_class - dis_same_class) / denominator
    return silhouette_per_sample.mean()
