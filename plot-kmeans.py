import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans

filter_geohash = ['u0', 'u1', 'u2', 'u3', 'u8', 'u9', 'sp', 'sr', 'sx']


def shorten_geohash(row):
    return row['geohash'][:2]


df = pd.read_json('capture.json')
df['short_geohash'] = df.apply(lambda row: shorten_geohash(row), axis=1)
df = df[df.short_geohash.isin(filter_geohash)]
print(df.head(10))

# show preview of all strikes
# df.plot.scatter('lon', 'lat', s=1)
# plt.show()
# quit()

# show preview of elbow curve
# K_clusters = range(1, 15)
# kmeans = [KMeans(n_clusters=i) for i in K_clusters]
# Y_axis = df[['lat']]
# X_axis = df[['lon']]
# score = [kmeans[i].fit(Y_axis).score(Y_axis) for i in range(len(kmeans))]
# # Visualize
# plt.plot(K_clusters, score)
# plt.xlabel('Number of Clusters')
# plt.ylabel('Score')
# plt.title('Elbow Curve')
# plt.show()
# quit()

kmeans = KMeans(n_clusters=5, init='k-means++')
kmeans.fit(df[df.columns[0:2]])  # Compute k-means clustering.
df['cluster_label'] = kmeans.fit_predict(df[df.columns[0:2]])
centers = kmeans.cluster_centers_  # Coordinates of cluster centers.
labels = kmeans.predict(df[df.columns[0:2]])  # Labels of each point
print('After labelizing')
print(df.head(10))

df.plot.scatter(x='lon', y='lat', c=labels, s=2, cmap='viridis')
plt.scatter(centers[:, 1], centers[:, 0], c='black', s=100, alpha=0.5)
plt.show()
