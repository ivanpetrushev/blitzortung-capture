import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPoint
from geopy.distance import great_circle


filter_geohash = ['u0', 'u1', 'u2', 'u3', 'u8', 'u9', 'sp', 'sr', 'sx']


def shorten_geohash(row):
    return row['geohash'][:2]


df = pd.read_json('capture-20200610-143104.json')
df['short_geohash'] = df.apply(lambda row: shorten_geohash(row), axis=1)
df = df[df.short_geohash.isin(filter_geohash)]
print(df.head(10))

# show preview of all strikes
# df.plot.scatter('lon', 'lat', s=1)
# plt.show()
# quit()

coords = df.as_matrix(columns=['lat', 'lon'])

db = DBSCAN(eps=10/6371, min_samples=5, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))

print(db)

cluster_labels = db.labels_
num_clusters = len(set(cluster_labels)) - 1  # -1 ?
clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
print('Number of clusters: {}'.format(num_clusters))
print('clusters', clusters)
out = []
labels = []
for i, cluster in enumerate(clusters):
    # print('item', cluster, type(cluster))
    for point in cluster:
        # print('point', point, type(point))
        out.append({
            'lat': point[0],
            'lon': point[1]
        })
        labels.append(i)
dfout = pd.DataFrame(out)
dfout.plot.scatter('lon', 'lat', s=1, c=labels, cmap='tab20b')
# dfout.plot.scatter('lon', 'lat', s=1)
plt.show()
quit()

# plot centroids
# def get_centermost_point(cluster):
#     centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
#     centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
#     return tuple(centermost_point)
#
#
# centermost_points = clusters.map(get_centermost_point)
# print('centermost_points', centermost_points)
#
# lats, lons = zip(*centermost_points)
# rep_points = pd.DataFrame({'lon': lons, 'lat': lats})
#
# fig, ax = plt.subplots(figsize=[10, 6])
# rs_scatter = ax.scatter(rep_points['lon'], rep_points['lat'], c='#99cc99', edgecolor='None', alpha=0.7, s=120)
# df_scatter = ax.scatter(df['lon'], df['lat'], c='k', alpha=0.9, s=3)
# ax.set_title('Full data set vs DBSCAN reduced set')
# ax.set_xlabel('Longitude')
# ax.set_ylabel('Latitude')
# ax.legend([df_scatter, rs_scatter], ['Full set', 'Reduced set'], loc='upper right')
# plt.show()
