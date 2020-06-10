import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from glob import glob

DBSCAN_EPS = 20/6371
DBSCAN_MIN = 5

filter_geohash = ['u2', 'u8', 'sr', 'sx']  # Bulgaria

out = []
labels = []


def shorten_geohash(row):
    return row['geohash'][:2]


for file in glob('capture-2020*'):
    df = pd.read_json(file)
    if df.empty:
        continue
    df['short_geohash'] = df.apply(lambda row: shorten_geohash(row), axis=1)
    df = df[df.short_geohash.isin(filter_geohash)]
    print(f'file: {file} strikes: {len(df)}')

    coords = df.drop(['geohash', 'short_geohash'], axis=1).values

    db = DBSCAN(eps=DBSCAN_EPS, min_samples=DBSCAN_MIN, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))

    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels)) - 1  # -1 ?
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
    print('Number of clusters: {}'.format(num_clusters))

    for i, cluster in enumerate(clusters):
        for point in cluster:
            out.append({
                'lat': point[0],
                'lon': point[1]
            })
            labels.append(i)
dfout = pd.DataFrame(out)
dfout.plot.scatter('lon', 'lat', s=2, c=labels, cmap='tab20b')
# plt.plot(dfout)
plt.show()
