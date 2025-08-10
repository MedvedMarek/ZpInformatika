import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')


class VykresliVolume:
  """
  Vykresluje cenovy graf a do neho volume.
  """
  def __init__(self):
    self.path   = '/media/marek/zaloha/Data/CSV/AAPL/'
    self.burzy  = ['SMART','ARCA','BATS','CHX','DRCTEDGE','IEX','ISLAND','MEMX','NYSE','PEARL','PSX']
    self.dtypes = {'stamp':'int32','time':'datetime64[ns]','o':'float32','h':'float32','l':'float32','c':'float32','v_SMART':'int32','v_ARCA':'int32','v_BATS':'int32','v_CHX':'int32','v_DRCTEDGE':'int32','v_IEX':'int32','v_ISLAND':'int32','v_MEMX':'int32','v_NYSE':'int32','v_PEARL':'int32','v_PSX':'int32'}
    self.interval = ['5s','10s','15s','30s','1m','2m','3m','5m','10m']
    # self.interval = ['5s']
    self.volume = {'5s' :{'v_SMART': 429, 'v_ARCA': 235, 'v_BATS': 170, 'v_CHX': 128, 'v_DRCTEDGE': 111, 'v_IEX': 95, 'v_ISLAND': 95, 'v_MEMX': 85, 'v_NYSE': 77, 'v_PEARL': 70, 'v_PSX': 64},
                   '10s':{'v_SMART': 136, 'v_ARCA': 127, 'v_BATS': 120, 'v_CHX': 111, 'v_DRCTEDGE': 107, 'v_IEX': 101, 'v_ISLAND': 103, 'v_MEMX': 97, 'v_NYSE': 92, 'v_PEARL': 87, 'v_PSX': 83},
                   '15s':{'v_SMART': 107, 'v_ARCA': 105, 'v_BATS': 104, 'v_CHX': 101, 'v_DRCTEDGE': 99, 'v_IEX': 97, 'v_ISLAND': 98, 'v_MEMX': 96, 'v_NYSE': 94, 'v_PEARL': 92, 'v_PSX': 90},
                   '30s':{'v_SMART': 135, 'v_ARCA': 133, 'v_BATS': 131, 'v_CHX': 128, 'v_DRCTEDGE': 127, 'v_IEX': 123, 'v_ISLAND': 126, 'v_MEMX': 123, 'v_NYSE': 120, 'v_PEARL': 117, 'v_PSX': 114},
                   '1m' :{'v_SMART': 141, 'v_ARCA': 140, 'v_BATS': 140, 'v_CHX': 137, 'v_DRCTEDGE': 137, 'v_IEX': 135, 'v_ISLAND': 137, 'v_MEMX': 136, 'v_NYSE': 134, 'v_PEARL': 132, 'v_PSX': 130},
                   '2m' :{'v_SMART': 183, 'v_ARCA': 183, 'v_BATS': 182, 'v_CHX': 179, 'v_DRCTEDGE': 179, 'v_IEX': 176, 'v_ISLAND': 180, 'v_MEMX': 178, 'v_NYSE': 175, 'v_PEARL': 172, 'v_PSX': 169},
                   '3m' :{'v_SMART': 216, 'v_ARCA': 215, 'v_BATS': 214, 'v_CHX': 211, 'v_DRCTEDGE': 211, 'v_IEX': 208, 'v_ISLAND': 211, 'v_MEMX': 208, 'v_NYSE': 205, 'v_PEARL': 202, 'v_PSX': 199},
                   '5m' :{'v_SMART': 241, 'v_ARCA': 240, 'v_BATS': 239, 'v_CHX': 236, 'v_DRCTEDGE': 235, 'v_IEX': 232, 'v_ISLAND': 234, 'v_MEMX': 231, 'v_NYSE': 228, 'v_PEARL': 225, 'v_PSX': 222},
                   '10m':{'v_SMART': 308, 'v_ARCA': 309, 'v_BATS': 310, 'v_CHX': 307, 'v_DRCTEDGE': 309, 'v_IEX': 306, 'v_ISLAND': 313, 'v_MEMX': 310, 'v_NYSE': 307, 'v_PEARL': 304, 'v_PSX': 300}}
    self.shake = {'5s':3,'10s':5,'15s':5,'30s':10,'1m':20,'2m':25,'3m':40,'5m':50,'10m':60}
    self.data = {x:self.nacitaj_data(x) for x in self.interval}
    self.datumy = self.stiahni_datumy2()
    # self.datumy = self.stiahni_datumy()
    # self.volume2 = self.nastav_volume()
  
  def nacitaj_data(self,interval):
    """
    Arguments
    ---------
    interval: str, '5s','10s', atd...
    """
    data = pd.read_csv(f'{self.path}/{interval}_trades.csv')
    data = data.astype(dtype=self.dtypes)
    return data
  
  def stiahni_datumy(self):
    datumy = {x:None for x in self.interval}
    for i in self.interval:
      data = self.data[i]['time']
      data = data.apply(lambda x: x.normalize())
      data = data.drop_duplicates()
      data = data.reset_index()
      data = data['time']
      datumy[i] = data
      data.to_csv(f'/media/marek/zaloha/Data/CSV/AAPL/{i}_datumy.csv',index=False)
    return datumy
  
  def stiahni_datumy2(self):
    """
    Stahuje data zo suboru. Neupravuje ich. Dlho to trva, ked sa to stale upravuje.
    """
    datumy = {x:None for x in self.interval}
    for i in self.interval:
      data = pd.read_csv(f'/media/marek/zaloha/Data/CSV/AAPL/{i}_datumy.csv')
      data = data['time'].astype('datetime64[ns]')
      datumy[i] = data
    return datumy
  
  def nastav_volume(self):
    suma = []
    volume = {x:{f'v_{y}':None for y in self.burzy} for x in self.interval}
    for i in self.interval:
      for j in self.burzy:
        for k in self.datumy[i]:
          maska = (self.data[i]['time'] >= k) & (self.data[i]['time'] < k + pd.Timedelta(days=1))
          x = self.data[i][f'v_{j}'][maska].sort_values(ascending=False)[:100].iloc[-1]
          suma.append(x)
        volume[i][f'v_{j}'] = int(np.mean(suma))
    return volume
  
  def vykresli_volume(self,interval,datum):
    """
    interval: str, '2m','3m', atd... .
    datum: str, '2021-01-01', atd... .
    """
    if not isinstance(datum,(pd.Timestamp)):
      datum = pd.Timestamp(datum)
    maska = (self.data[interval]['time'] >= datum) & (self.data[interval]['time'] < datum + pd.Timedelta(days=1))
    data = self.data[interval][maska]
    
    plt.clf()
    plt.plot(data['time'],data['o'],linewidth=0.2,color='black')
    
    for i in self.burzy:
      index = data[data[f'v_{i}'] > self.volume[interval][f'v_{i}']].index
      x = data['time'].loc[index]
      x = x+pd.Timedelta(f'{self.shake[interval] * (np.random.normal()*4)}s')
      y = data['o'].loc[index] + (np.random.rand()/20)
      s = (data[f'v_{i}'].loc[index]/self.volume[interval][f'v_{i}'])*30
      plt.scatter(x,y,s=s,linewidth=1, edgecolors = 'black',label=i, alpha=0.5)
    plt.legend()
    plt.show()


vykreslovanie = VykresliVolume()


for i in vykreslovanie.datumy['30s'][400:405]:
  vykreslovanie.vykresli_volume('30s',i)


