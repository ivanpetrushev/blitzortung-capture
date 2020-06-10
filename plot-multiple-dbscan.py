import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from glob import glob
from shapely.geometry import MultiPoint
from geopy.distance import great_circle
import json

DBSCAN_EPS = 20/6371  # 20 km
DBSCAN_MIN = 5

filter_geohash = ['u2', 'u8', 'sr', 'sx']  # Bulgaria

out = []
out_formatted = {}
labels = []
file_idx = 0
file_list = []


def shorten_geohash(row):
    return row['geohash'][:2]


def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)


for file in glob('capture-2020*'):
    file_list.append(file)

file_list.sort()

for file in file_list:
    file_idx += 1
    df = pd.read_json(file)
    if df.empty:
        continue
    if file not in out_formatted:
        out_formatted[file] = {'cluster_centroids': []}

    df['short_geohash'] = df.apply(lambda row: shorten_geohash(row), axis=1)
    df = df[df.short_geohash.isin(filter_geohash)]
    print(f'file: {file} strikes: {len(df)}')

    # coords = df.drop(['geohash', 'short_geohash'], axis=1).values
    coords = df[['lat', 'lon']].values

    db = DBSCAN(eps=DBSCAN_EPS, min_samples=DBSCAN_MIN, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))

    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels)) - 1  # -1 ?
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
    print('Number of clusters: {}'.format(num_clusters))

    # add Centroids to output
    centermost_points = clusters.map(get_centermost_point)
    for i, point in enumerate(centermost_points):
        out.append({
            'lat': point[0],
            'lon': point[1]
        })
        labels.append(file_idx)
        out_formatted[file]['cluster_centroids'].append({
            'lat': point[0],
            'lon': point[1]
        })

    # add cluster members to output
    # for i, cluster in enumerate(clusters):
    #     for point in cluster:
    #         out.append({
    #             'lat': point[0],
    #             'lon': point[1]
    #         })
    #         labels.append(i)


dfout = pd.DataFrame(out)
dfout.plot.scatter('lon', 'lat', s=2, c=labels, cmap='tab20b')
# plt.plot(dfout)
plt.show()

with open('webserver/data.json', 'w') as fp:
    json.dump(out_formatted, fp)
