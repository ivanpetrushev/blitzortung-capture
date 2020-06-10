import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

filter_geohash = ['u0', 'u1', 'u2', 'u3', 'u8', 'u9', 'sp', 'sr', 'sx']


def shorten_geohash(row):
    return row['geohash'][:2]


df = pd.read_json('capture.json')
df['short_geohash'] = df.apply(lambda row: shorten_geohash(row), axis=1)
df = df[df.short_geohash.isin(filter_geohash)]

df.plot.scatter('lon', 'lat', s=1)
plt.show()
