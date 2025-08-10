import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import pandas as pd
import datetime
plt.style.use('ggplot')

akcia = 'AMD'
vlakno = 2

burza = 4
datum_start = datetime.datetime(2023,4,20,19,25)
datum_stop  = datetime.datetime(2023,4,20,20,00)
cas = [0]
data = {x:np.arange(5, dtype=float).reshape(1,5) for x in np.arange(1,6,1)}
nazov_burzy = {1:'ARCA', 2:'DRCTEDGE', 3:'IEX', 4:'SMART', 5:'ISLAND'}
volume_burzy = {1:20, 2:40, 3:15, 4:300, 5:50}
volume_graf  = {x:{'cas':[], 'cena':[], 'volume':[]} for x in [1,2,3,4,5]}
# {'ARCA':140, 'DRCTEDGE':190, 'IEX':70, 'SMART':1100, 'ISLAND':260}
# red     - ARCA
# blue    - DRCTEDGE 
# green   - IEX
# yellow  - SMART
# magenta - ISLAND

class Vykreslovanie_dat:
  """
  Vykreslovanie dat. Vykreslovanie je vo svojom vlakne.
  """
  def __init__(self):
    self.time_data = 0
    vlakno = threading.Thread(target=self.dodaj_data)
    vlakno.start()
    
    # vytvorenie okna (Canvas) do ktoreho su posielane streamovane data.
    fig, ax = plt.subplots()
    ax.set_xlim([datum_start, datum_stop])
    anim = matplotlib.animation.FuncAnimation(fig=fig, func=self.vykresluj_data, frames=self.dodaj_data, repeat=False, cache_frame_data=False)
    plt.show()
  
  def dodaj_data(self):
    """
    Funkcia ide v nekonecnej slucke. Skuma, ci su aktualizovane data v mnozine "data". Overuje to cez "cas". A ak
    su aktualizovane tak ich dodava na vykreslovanie.
    """
    while True:
      if self.time_data != data[burza][-1,1]:
        yield cas[1:], data[burza][1:,2]
      self.time_data = data[burza][-1,1]
      time.sleep(0.3)
  
  def vykresluj_data(self, data_xy):
    plt.plot(data_xy[0], data_xy[1], color='firebrick', linewidth=0.5)
    plt.scatter(volume_graf[1]['cas'], volume_graf[1]['cena'], s = 40, linewidth=0.5, color='red', edgecolors='black', label='ARCA')
    plt.scatter(volume_graf[2]['cas'], volume_graf[2]['cena'], s = 40, linewidth=0.5, color='blue', edgecolors='black', label='DRCTEDGE')
    plt.scatter(volume_graf[3]['cas'], volume_graf[3]['cena'], s = 40, linewidth=0.5, color='green', edgecolors='black', label='IEX')
    plt.scatter(volume_graf[4]['cas'], volume_graf[4]['cena'], s = 40, linewidth=0.5, color='yellow', edgecolors='black', label='SMART')
    plt.scatter(volume_graf[5]['cas'], volume_graf[5]['cena'], s = 40, linewidth=0.5, color='magenta', edgecolors='black', label='ISLAND')
    # plt.scatter(self.data[i].time[nakup.index] + pd.Timedelta('{}m'.format(np.random.uniform())), self.data[i].SMAc[nakup.index]+np.random.rand()/20, s = (self.data[i][burza][nakup.index]/self.volume[j])*30, linewidth=0.5, edgecolors = 'black', label=j)
    # plt.legend()

class IBApi(EWrapper, EClient):
  def __init__(self):
    EClient.__init__(self,self)
  
  def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
    super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
    bot.on_bar_update(reqId, time, open_, high, low, close, volume, wap, count)


class Bot:
  ib = None
  
  def __init__(self):
    self.ib = IBApi()
    self.ib.connect("127.0.0.1", 7497, vlakno)
    
    ib_thread = threading.Thread(target=self.run_loop, daemon=True)
    ib_thread.start()
    time.sleep(1)
    
    contract1 = Contract()
    contract1.symbol = akcia
    contract1.secType = "STK"
    contract1.exchange = "ARCA"
    contract1.currency = "USD"
    
    contract2 = Contract()
    contract2.symbol = akcia
    contract2.secType = "STK"
    contract2.exchange = "DRCTEDGE"
    contract2.currency = "USD"
    
    contract3 = Contract()
    contract3.symbol = akcia
    contract3.secType = "STK"
    contract3.exchange = "IEX"
    contract3.currency = "USD"
    
    contract4 = Contract()
    contract4.symbol = akcia
    contract4.secType = "STK"
    contract4.exchange = "SMART"
    contract4.currency = "USD"
    
    contract5 = Contract()
    contract5.symbol = akcia
    contract5.secType = "STK"
    contract5.exchange = "ISLAND"
    contract5.currency = "USD"
    
    self.ib.reqRealTimeBars(1, contract1, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(2, contract2, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(3, contract3, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(4, contract4, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(5, contract5, 1, "TRADES", 1, [])
    
    self.y = np.arange(5, dtype=float)
  
  def run_loop(self):
    self.ib.run()
  
  def on_bar_update(self, reqId, time, open_, high, low, close, volume, wap, count):
    'vyzera to tak, ze funkcia ide v slucke'
    print(reqId, volume)
    # print(reqId, time, wap, volume, count)
    self.y[0], self.y[1], self.y[2], self.y[3], self.y[4] = reqId, time, wap, volume, count
    data[reqId] = np.vstack([data[reqId], self.y])
    if time % 50 == 0:
      np.save("/home/marek/"+akcia+'_'+nazov_burzy[reqId], data[reqId])
    
    if reqId == burza:
      # priradenie casu to premennej cas, ktora je pouzita na vykreslovanie cenoveho grafu.
      cas.append(pd.to_datetime(time, unit='s'))
    
    if volume >= volume_burzy[reqId]:
      volume_graf[reqId]['volume'].append(volume)
      volume_graf[reqId]['cas'].append(pd.to_datetime(time, unit='s') + pd.Timedelta('{}m'.format(np.random.uniform())))
      volume_graf[reqId]['cena'].append(wap + np.random.rand()/20 )


bot = Bot()
vykreslovanie = Vykreslovanie_dat()