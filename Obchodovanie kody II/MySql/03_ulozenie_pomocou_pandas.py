from sqlalchemy import create_engine
import os
import numpy as np
import pandas as pd

user = 'marek'
password = '138'
host = 'localhost'
database = 'AAPL_2'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

burzy = ['arca','bats','drctedge','edgea','iex','memx','nasdaq','nyse','pearl','psx','smart']
columns = {'time':'datetime64[ns]', 'open':'float', 'high':'float', 'low':'float', 'close':'float', 'volume':'int'}
path = '/media/marek/zaloha/Data/OHLC_TWS/AAPL/5s/trades/'
datumy = os.listdir(path)
datumy.sort()

for i in datumy[729:]:
    for j in burzy:
        data = np.load(f'{path}{i}/{j.upper()}.npy')
        data = pd.DataFrame(data, columns=columns.keys())
        data = data.astype(dtype=columns)
        data.to_sql(j, con=engine, if_exists='append', index=False)
    print(i)







