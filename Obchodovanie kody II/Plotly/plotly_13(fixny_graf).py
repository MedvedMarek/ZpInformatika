from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import random
from typing import Dict
import argparse
from datetime import datetime, timedelta

# Vytvorenie parsera a definovanie argumentov
parser = argparse.ArgumentParser(description='Načítať obchodné údaje.')
parser.add_argument('--datum', type=str, help='Dátum obchodovania v tvare YYYY_MM_DD')
parser.add_argument('--interval', type=int, help='Minimálny objem obchodov pre filtrovanie')
args = parser.parse_args()


app = Flask(__name__)


path = '/media/marek/zaloha/Data/OHLC_TWS/AAPL/5s/trades/'
burzy = ['ARCA','BATS','DRCTEDGE','EDGEA','IEX','MEMX','NASDAQ','NYSE','PEARL','PSX','SMART']
burzy_male = ['arca','bats','drctedge','edgea','iex','memx','nasdaq','nyse','pearl','psx','smart']
burzy_male2 = ['arca','bats','drctedge','edgea','iex','memx','nasdaq','nyse','pearl','psx']

def konverzia(time_string):
    # Konverzia reťazca na datetime objekt
    time_object = datetime.strptime(time_string, '%H:%M:%S')
    sekunda = random.randint(-3,3)
    # Pridanie sekúnd
    new_time_object = time_object + timedelta(seconds=sekunda)
    # Konverzia späť na reťazec
    new_time_string = new_time_object.strftime('%H:%M:%S')
    return new_time_string


def nacitaj_data(datum, interval) -> Dict[str, np.ndarray]:
    dt = {x.lower(): np.load(f'{path}{datum}/{x}.npy') for x in burzy}
    columns = ['time','open','high','low','close','volume']
    dtypes = {'time':'datetime64[ns]', 'open':'float64', 'high':'float64', 'low':'float64', 'close':'float64', 'volume':'int'}
    data = {x: pd.DataFrame(dt[x], columns=columns) for x in burzy_male}

    for i in burzy_male:
        data[i] = data[i].astype(dtypes)
        data[i]['time'] = data[i]['time'].apply(lambda x: str(x.time()))

    for i in burzy_male2:
        data[i] = data[i][data[i]['volume'] > interval].copy().reset_index(drop=True)
        if data[i].shape[0] > 0:
           data[i]['close'] = data[i]['close'].apply(lambda x: x+random.uniform(-0.01, 0.01))
    
    return data
   
# datum = '2024_01_12'
data = nacitaj_data(args.datum, args.interval)
  
@app.route('/')
def index():
    return render_template('plotly_13(fixny_graf).html')

@app.route('/data')
def data_route():
    response_data = {
        **{'x': data['smart']['time'].tolist(),
           'open': data['smart']['open'].tolist(),  
           'high': data['smart']['high'].tolist(),
           'low': data['smart']['low'].tolist(),
           'close': data['smart']['close'].tolist()},
        **{f'{j}_x': data[j]['time'].tolist() for j in burzy_male2},
        **{f'{j}_y': data[j]['close'].tolist() for j in burzy_male2},
        **{f'{j}_v': (data[j]['volume']/10).tolist() for j in burzy_male2}
    }
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)

    
