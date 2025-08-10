import numpy as np
import pandas as pd
import os

class NacitanieDat():
  """
  Nacitava data a vytvara z nich jeden datovy subor.
  
  Arguments
  ---------
  interval: str, interval ktory urcuje, z ktorej zlozky sa budu nacitavat data. Akceptuje sa vstup
            '5s','10s','15s','30s',atd... .,
  
  Parameters
  ----------
  trhove_data:list, Zoznam zloziek pre data, z ktorych sa preberaju datumy
  burzy:      list, Zoznam burz, pre ktore sa budu stahovat data
  path:       str, cesta ku zlozke s trhovimi datami. 
  datumy:     list, Nacitanie datumov, pre ktore sa budu stahovat data. Datumy su stiahnute zo zlozky trades.
              Tam je najvacsia pravdepodobnost, ze budu stiahnute vsetky datumy.
  """
  def __init__(self,interval):
    self.interval   = interval
    self.trhove_data = ['trades','midpoint','bid','ask','bid_ask','option_implied_volatility']
    self.burzy  = ['ARCA','BATS','CHX','DRCTEDGE','IEX','ISLAND','MEMX','NYSE','PEARL','PSX','SMART']
    self.path   = '/media/marek/zaloha/Data/OHLC_TWS/AAPL/'
    self.datumy = os.listdir(f'{self.path}/{interval}/trades/')
  
  def nacitaj_trades_data_pre_datum(self,datum,burza):
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
    data = np.load(f'{self.path}/{self.interval}/trades/{datum}/{burza}.npy')
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
  
  def spoj_trades_data_pre_datum(self,datum):
    data = self.nacitaj_trades_data_pre_datum(datum,'SMART')
    burzy = [x for x in self.burzy if x != 'SMART']
    for x in burzy:
      dt = self.nacitaj_trades_data_pre_datum(datum,x)
      data = pd.merge(data,dt,how='left',on='stamp')
    return data
  
  def spoj_trades_data(self):
    data = self.spoj_trades_data_pre_datum(self.datumy[0])
    for i in self.datumy[1:]:
      dt = self.spoj_trades_data_pre_datum(i)
      data = pd.concat([data,dt],ignore_index=True)
    return data

    


nacitanie = NacitanieDat('1m')
data = nacitanie.spoj_trades_data()












