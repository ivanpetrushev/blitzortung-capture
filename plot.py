import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

filter_geohash = ['u0', 'u1', 'u2', 'u3', 'u8', 'u9', 'sp', 'sr', 'sx']

with open('capture.json') as fp:
    strikes = json.load(fp)

lats = []
lons = []
filtered_strikes = []

for i, item in enumerate(strikes):
    in_filter = False
    for gh_start in filter_geohash:
        if item['geohash'].startswith(gh_start):
            in_filter = True
            break
    if not in_filter:
        continue
    item['lat'] *= 1000000
    item['lon'] *= 1000000
    filtered_strikes.append(item)
    lats.append(item['lat'])
    lons.append(item['lon'])

# print(lats)
# print(lons)
print('Number of filtered strikes', len(filtered_strikes))
plt.scatter(lons, lats, s=1)
plt.show()
