import websocket
import json
from datetime import datetime
import geohash
from random import randint
import pandas as pd

try:
    import thread
except ImportError:
    import _thread as thread
import time

counter = 0
save = []


def on_message(ws, message):
    global counter
    global save
    data = json.loads(message)
    counter += 1
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    gh = geohash.encode(data['lat'], data['lon'])
    save.append({
        'lat': data['lat'],
        'lon': data['lon'],
        'geohash': gh,
        'geohash_short_2': gh[:2],
        'ts': int(time.time())
    })
    print(
        f"message #{counter} {now} {gh} {data['lat']} {data['lon']} save len: {len(save)}")


def on_error(ws, error):
    print('error', error)


def on_close(ws):
    global save
    print("### closed ###")
    now = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = 'capture-' + now + '.json'
    with open(filename, 'w') as fp:
        json.dump(save, fp)
    print('saved')


def on_open(ws):
    def run(*args):
        ws.send('{"time":0}')
        while True:
            time.sleep(30)
            ws.send('{}')

    def calculate(*args):
        global save
        while True:
            time.sleep(10)
            ts_threshold = int(time.time()) - 15
            save = [x for x in save if x['ts'] > ts_threshold]
            print("CALCULATING")

    thread.start_new_thread(run, ())
    thread.start_new_thread(calculate, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    url = 'ws://ws' + str(randint(1, 5)) + '.blitzortung.org'
    port = str(randint(8050, 8090))
    ws = websocket.WebSocketApp(url + ':' + port + '/',
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
