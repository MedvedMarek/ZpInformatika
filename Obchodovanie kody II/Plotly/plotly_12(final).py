from flask import Flask, render_template, jsonify
import pandas as pd
import threading
import time
import numpy as np
import random
from typing import Dict
lock = threading.Lock()
app = Flask(__name__)


path = '/media/marek/zaloha/Data/OHLC_TWS/AAPL/5s/trades/2021_01_04/'
burzy = ['ARCA','BATS','DRCTEDGE','EDGEA','IEX','MEMX','NASDAQ','NYSE','PEARL','PSX','SMART']
burzy_male = ['arca','bats','drctedge','edgea','iex','memx','nasdaq','nyse','pearl','psx','smart']
burzy_male2 = ['arca','bats','drctedge','edgea','iex','memx','nasdaq','nyse','pearl','psx']

def nacitaj_data(datum) -> Dict[str, np.ndarray]:
    dt = {x.lower(): np.load(f'{path}{x}.npy') for x in burzy}
    columns = ['time','open','high','low','close','volume']
    dtypes = {'time':'datetime64[ns]', 'open':'float64', 'high':'float64', 'low':'float64', 'close':'float64', 'volume':'int'}
    data = {x: pd.DataFrame(dt[x], columns=columns) for x in burzy_male}
    for i in burzy_male:
        data[i] = data[i].astype(dtypes)
        data[i]['time'] = data[i]['time'].apply(lambda x: str(x.time()))
    return data

datum = '2024_01_12'
dt = nacitaj_data(datum)
data_live = {x: dt[x][0:1].copy() for x in burzy_male}

i = 1
# Funkcia, ktorá pravidelne aktualizuje údaje
def update_data():
    global i
    global data_live

    while True:
        lock.acquire()
        try:
            data_live['smart'] = dt['smart'][i:i+1].copy()
            for j in burzy_male2:
                data_live[j] = dt[j][i:i+1].copy()
                if dt[j].loc[i,'volume']<100:
                    data_live[j]['volume'] = 0
                else:
                    data_live[j]['close'] = data_live[j]['close'] + random.uniform(-0.05,0.05)
            i += 1
        finally:
            lock.release()
        time.sleep(1)

# Spustenie vlákna pre aktualizáciu údajov
data_thread = threading.Thread(target=update_data, daemon=True)
data_thread.start()

@app.route('/')
def index():
    return render_template('plotly_12(final).html')

@app.route('/data')
def data():
    lock.acquire()
    try:
        if not data_live['smart'].empty:
            data = {
                **{'x': data_live['smart']['time'].tolist(),
                   'open': data_live['smart']['open'].tolist(),  
                   'high': data_live['smart']['high'].tolist(),
                   'low': data_live['smart']['low'].tolist(),
                   'close': data_live['smart']['close'].tolist()},
                **{f'{j}_x': data_live[j]['time'].tolist() for j in burzy_male2},
                **{f'{j}_y': data_live[j]['close'].tolist() for j in burzy_male2},
                **{f'{j}_v': (data_live[j]['volume']/10).tolist() for j in burzy_male2}
            }
            return jsonify(data)
        return jsonify({})
    finally:
        lock.release()

if __name__ == '__main__':
    app.run(debug=True)
