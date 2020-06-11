import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPoint
from geopy.distance import great_circle

DBSCAN_EPS = 20/6371  # 20 km
DBSCAN_MIN = 5


def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(
        cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)


def calculate_clusters(data, gh_filter=[]):
    out = []
    df = pd.DataFrame(data)
    if gh_filter:
        df = df[df.geohash_short_2.isin(gh_filter)]

    coords = df[['lat', 'lon']].values
    db = DBSCAN(eps=DBSCAN_EPS, min_samples=DBSCAN_MIN,
                algorithm='ball_tree', metric='haversine').fit(np.radians(coords))

    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels)) - 1  # -1 ?
    clusters = pd.Series([coords[cluster_labels == n]
                          for n in range(num_clusters)])
    print('Number of clusters: {}'.format(num_clusters))

    # add Centroids to output
    centermost_points = clusters.map(get_centermost_point)
    for point in centermost_points:
        out.append({
            'lat': point[0],
            'lon': point[1]
        })

    return out
