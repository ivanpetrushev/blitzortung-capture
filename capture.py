import websocket
import json
from datetime import datetime
import geohash
from random import randint
import pandas as pd
import os
from calculate_dbscan import calculate_clusters

try:
    import thread
except ImportError:
    import _thread as thread
import time

CALCULATE_INTERVAL = 120
KEEP_OLD_DATA_WINDOW = 600

counter = 0
working_set = []


def on_message(ws, message):
    global counter
    global working_set
    data = json.loads(message)
    counter += 1
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    gh = geohash.encode(data['lat'], data['lon'])
    working_set.append({
        'lat': data['lat'],
        'lon': data['lon'],
        'geohash': gh,
        'geohash_short_2': gh[:2],
        'ts': int(time.time())
    })
    print(
        f"message #{counter} {now} {gh} {data['lat']:>10} {data['lon']:>10} working_set len: {len(working_set)}", end='\r')


def on_error(ws, error):
    print("\nerror", error)


def on_close(ws):
    global working_set
    print("\n### closed ###")


def on_open(ws):
    def run(*args):
        ws.send('{"time":0}')
        while True:
            time.sleep(30)  # keep alive websocket
            ws.send('{}')

    def calculate(*args):
        global working_set
        while True:
            time.sleep(CALCULATE_INTERVAL)
            ts_threshold = int(time.time()) - KEEP_OLD_DATA_WINDOW
            working_set = [x for x in working_set if x['ts'] > ts_threshold]
            # filter_geohash = ['u2', 'u8', 'sr', 'sx']  # Bulgaria
            clusters = calculate_clusters(working_set)

            if os.path.exists('webserver/data.json'):
                with open('webserver/data.json', 'r') as fp:
                    old_data = json.load(fp)
            else:
                old_data = {}
            with open('webserver/data.json', 'w') as fp:
                now = datetime.now().strftime('%Y%m%d-%H%M%S')
                old_data[now] = {'cluster_centroids': clusters}
                json.dump(old_data, fp)

    thread.start_new_thread(run, ())
    thread.start_new_thread(calculate, ())


if __name__ == "__main__":
    # websocket.enableTrace(True)
    url = 'ws://ws' + str(randint(1, 5)) + '.blitzortung.org'
    port = str(randint(8050, 8090))
    ws = websocket.WebSocketApp(url + ':' + port + '/',
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
