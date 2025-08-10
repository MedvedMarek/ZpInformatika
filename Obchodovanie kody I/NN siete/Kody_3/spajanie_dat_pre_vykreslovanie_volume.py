import numpy as np
import pandas as pd
import os


class SpajanieDat:
  """
  Spajanie dat na vykreslovanie volume. Budu pouzite data iba pre trades, ktore obsahuju volume.
  """
  def __init__(self):
    self.burzy = ['ARCA','BATS','CHX','DRCTEDGE','IEX','ISLAND','MEMX','NYSE','PEARL','PSX','SMART']
    self.path = '/media/marek/zaloha/Data/OHLC_TWS/AAPL/'
  
  def nacitaj_data(self,interval,datum,burza):
    """
    Nacitava data pre dany datum a danu burzu.
    
    Arguments
    ---------
    interval: str, '5s', '15m', atd...
    datum: str, '2022_01_03'
    burza: str, napr: 'ARCA','SMART', atd... 
    
    Returns
    -------
    data: DataFrame
    """
    data = np.load(f'{self.path}/{interval}/trades/{datum}/{burza}.npy')
    if burza != 'SMART':
      if data.size < 1:
        data = np.load(f'{self.path}/{interval}/trades/{datum}/SMART.npy')
      columns = ['time',f'v_{burza}']
      dtypes = {'time':'datetime64[ns]',f'v_{burza}':'int32'}
      data = pd.DataFrame(data[:,[0,5]],columns=columns)
    else:
      columns = ['time','o','h','l','c','v_SMART']
      dtypes = {'time':'datetime64[ns]','o':'float32','h':'float32','l':'float32','c':'float32','v_SMART':'int32'}
      data = pd.DataFrame(data,columns=columns)
    data = data.astype(dtypes)
    data.insert(0,'stamp',None)
    data['stamp'] = data['time'].apply(lambda x: int(pd.to_datetime(x).timestamp()))
    data['stamp'] = data['stamp'].astype(dtype='int32')
    if burza != 'SMART':
      data = data.drop('time',axis=1)
    data = data.drop_duplicates(subset=['stamp'])
    return data
  
  def spoj_den(self,interval,datum):
    """
    Spaja data pre jednotlive burzy do jedneho datasetu.
    """
    data = self.nacitaj_data(interval,datum,'SMART')
    for i in self.burzy[:-1]:
      dt = self.nacitaj_data(interval,datum,i)
      data = pd.merge(data,dt,how='left',on='stamp')
    return data
  
  def spoj_data(self,interval):
    datumy = os.listdir(f'{self.path}/{interval}/trades/')
    data = self.spoj_den(interval,datumy[0])
    for i in datumy[1:]:
      dt = self.spoj_den(interval,i)
      data = pd.concat([data,dt],ignore_index=True)
    data = data.fillna(value=0)
    return data


    

interval = ['5s','10s','15s','30s','1m','2m','3m','5m','10m']

spajanie = SpajanieDat()

for i in interval:
  data = spajanie.spoj_data(i)
  data.to_csv(f'/media/marek/zaloha/Data/CSV/AAPL/{i}_trades.csv',index=False)
































