import websocket
import json
from datetime import datetime
import geohash

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
    # if gh.startswith('g') or gh.startswith('u') or gh.startswith('e') or gh.startswith('s'):
    save.append({'lat': data['lat'], 'lon': data['lon'], 'geohash': gh})
    print(f"message #{counter} {now} {gh} {data['lat']} {data['lon']} save len: {len(save)}")


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
        # time.sleep(1)
        # ws.close()
        # print("thread terminating...")

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws5.blitzortung.org:3000/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
