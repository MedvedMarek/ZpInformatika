import numpy as np
import pandas as pd
import os

class NacitanieDat:
  """
  Nacitava vsetky trhove data a prevadza ich na tabulky pre jednotlive trhy ('trades','midpoint', atd... ).
  
  Arguments
  ---------
  interval: z akej zlozky casoveho intervalu sa maju stahovat data
  
  Parameters
  ----------
  burzy: Z ktorych burz sa budu stahovat data
  """
  def __init__(self,interval):
    self.interval   = interval
    self.burzy  = ['ARCA','BATS','CHX','DRCTEDGE','IEX','ISLAND','MEMX','NYSE','PEARL','PSX','SMART']
    self.path   = f'/media/marek/zaloha/Data/OHLC_TWS/AAPL/{interval}/'
    self.datumy = os.listdir(f'{self.path}/trades/')
  
  def nacitaj_data_pre_trades(self,datum,burza):
    """
    Nacitava trades data pre danu burzu a dany datum.
    
    Arguments
    ---------
    datum:  str, je to datum pre ktory sa budu stahovat data. Napriklad: '2022_01_03', atd... .
    burza:  str, nazov burzy pre ktoru sa maju stahovat data
    
    Returns
    -------
    data:   DataFrame. Vystupom je pandas dataframe.
    """
    data = np.load(f'{self.path}/trades/{datum}/{burza}.npy')
    if burza != 'SMART':
      columns = ['time',f'v_{burza}']
      dtypes  = {'time':'datetime64[ns]',f'v_{burza}':'int32'}
      data = pd.DataFrame(data[:,[0,5]],columns=columns)
    else:
      columns = ['time','o','h','l','c','v']
      dtypes  = {'time':'datetime64[ns]','o':'float32','h':'float32','l':'float32','c':'float32','v':'int32'}
      data = pd.DataFrame(data,columns=columns)
    data = data.astype(dtypes)
    data.insert(0,'stamp',None)
    data['stamp'] = data['time'].apply(lambda x: int(pd.to_datetime(x).timestamp()))
    data['stamp'] = data['stamp'].astype(dtype='int32')
    if burza != 'SMART':
      data = data.drop('time',axis=1)
    data = data.drop_duplicates(subset=['stamp'])
    return data
  
  def nacitaj_data_pre_MidBidAsk(self,trh,datum,burza):
    """
    Nacitava data z: midpoint, bid, ask, bid_ask.
    
    Arguments
    ---------
    datum:  str, je to datum pre ktory sa budu stahovat data. Napriklad: '2022_01_03', atd... .
    burza:  str, nazov burzy pre ktoru sa maju stahovat data
    
    Returns
    -------
    data:   DataFrame. Vystupom je pandas dataframe
    """
    data = np.load(f'{self.path}/{trh}/{datum}/{burza}.npy')
    columns = ['time',f'o_{burza}',f'h_{burza}',f'l_{burza}',f'c_{burza}']
    dtypes = {'time':'datetime64[ns]',f'o_{burza}':'float32',f'h_{burza}':'float32',f'l_{burza}':'float32',f'c_{burza}':'float32'}
    
    if data.size > 0:
      data = pd.DataFrame(data,columns=columns)
      data = data.astype(dtypes)
      data.insert(0,'stamp',None)
      data['stamp'] = data['time'].apply(lambda x: int(pd.to_datetime(x).timestamp()))
      data['stamp'] = data['stamp'].astype(dtype='int32')
      data = data.drop_duplicates(subset=['stamp'])
    else:
      data = np.load(f'{self.path}/trades/{datum}/SMART.npy')
      data = pd.DataFrame(data[:,:-1],columns=columns)
      data = data.astype(dtypes)
      data.insert(0,'stamp',None)
      data['stamp'] = data['time'].apply(lambda x: int(pd.to_datetime(x).timestamp()))
      data['stamp'] = data['stamp'].astype(dtype='int32')
      data = data.drop_duplicates(subset=['stamp'])
      data[[f'o_{burza}',f'h_{burza}',f'l_{burza}',f'c_{burza}']]=0
    return data
  
  def spoj_den (self,trh,datum):
    """
    Spaja data v jednom dni.
    
    Argumensts
    ----------
    trh: str, pre ktory trh sa maju srahovat data
    datum: str, pre ktory datum sa maju stahovat data
    """
    if trh != 'trades':
      data = self.nacitaj_data_pre_MidBidAsk(trh,datum,'ARCA')
      for i in self.burzy[1:]:
        dt = self.nacitaj_data_pre_MidBidAsk(trh,datum,i)
        data = pd.merge(data,dt.drop(labels='time',axis=1),how='left',on='stamp')
    
    else:
      data = self.nacitaj_data_pre_trades(datum,'SMART')
      for i in self.burzy[:-1]:
        dt = self.nacitaj_data_pre_trades(datum,i)
        data = pd.merge(data,dt,how='left',on='stamp')
    return data
  
  def spoj_data(self,trh):
    """
    Spaja vsetky dni do jedneho datasetu.
    """
    if trh != 'option_implied_volatility':
      data = self.spoj_den(trh,self.datumy[0])
      for i in self.datumy[1:]:
        dt = self.spoj_den(trh,i)
        data = pd.concat([data,dt],ignore_index=True)
      return data
    
    else:
      columns = ['time','o','h','l','c']
      dtypes = {'time':'datetime64[ns]','o':'float32','h':'float32','l':'float32','c':'float32'}
      data = np.load(f'{self.path}/option_implied_volatility/{self.datumy[0]}/SMART.npy')
      data = pd.DataFrame(data,columns=columns)
      data = data.astype(dtypes)
      data.insert(0,'stamp',None)
      data['stamp'] = data['time'].apply(lambda x: int(pd.to_datetime(x).timestamp()))
      data['stamp'] = data['stamp'].astype(dtype='int32')
      data = data.drop_duplicates(subset=['stamp'])
      
      for i in self.datumy[1:]:
        dt = np.load(f'{self.path}/option_implied_volatility/{i}/SMART.npy')
        if dt.size > 0:
          dt = pd.DataFrame(dt,columns=columns)
          dt = dt.astype(dtypes)
          dt.insert(0,'stamp',None)
          dt['stamp'] = dt['time'].apply(lambda x: int(pd.to_datetime(x).timestamp()))
          dt['stamp'] = dt['stamp'].astype(dtype='int32')
          dt = dt.drop_duplicates(subset=['stamp'])
        else:
          shape = np.load(f'{self.path}/trades/{self.datumy[0]}/SMART.npy')
          zero = np.zeros(shape.shape)
          dt = pd.DataFrame(zero,columns=columns)
          dt['time'] = shape[:,0]
          dt = dt.astype(dtypes)
          dt.insert(0,'stamp',None)
          dt['stamp'] = dt['time'].apply(lambda x: int(pd.to_datetime(x).timestamp()))
          dt['stamp'] = dt['stamp'].astype(dtype='int32')
          dt = dt.drop_duplicates(subset=['stamp'])
        data = pd.concat([data,dt],ignore_index=True)
      return data





path = '/media/marek/zaloha/Data/CSV/AAPL/1m/'
zoznam = ['trades','midpoint','bid','ask','bid_ask','option_implied_volatility']
nacitanie = NacitanieDat('1m')

for i in zoznam:
  x = nacitanie.spoj_data(i)
  x.to_csv(f'{path}/{i}.csv',index=False)



















































