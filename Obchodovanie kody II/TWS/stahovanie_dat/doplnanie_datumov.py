import os
import numpy as np
import pandas as pd


# nacitava sa csv subor stahovany z yahoofinancial. Dane su len udaje, ktore nie su este
# stiahnute.
data = pd.read_csv('/home/marek/Downloads/AAPL.csv')
datum = [i.replace('-','_') for i in data['Date']]
burzy = ['ARCA','BATS','DRCTEDGE','EDGEA','IEX','MEMX','NASDAQ','NYSE','PEARL','PSX','SMART']
path = '/media/marek/zaloha/Data/OHLC_TWS/xxxDoplnok/'
dt = np.arange(10, )

for i in datum:
    os.mkdir(f'{path}{i}')
    for j in burzy:
        np.save(f'{path}/{i}/{j}.npy', dt)




        
