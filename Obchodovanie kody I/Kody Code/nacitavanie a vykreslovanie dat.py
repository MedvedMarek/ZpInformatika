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
vlakno = 1

burza = 13
datum_start = datetime.datetime(2023,4,18,15,30)
datum_stop  = datetime.datetime(2023,4,18,22,00)
cas = [0]
data = {x:np.arange(5, dtype=float).reshape(1,5) for x in np.arange(1,16,1)}
nazov_burzy = {1:'AMEX', 2:'ARCA', 3:'BATS', 4:'BEX', 5:'BYX', 6:'CHX', 7:'DRCTEDGE', 8:'EDGEA',
               9:'IEX', 10:'MEMX', 11:'NYSE', 12:'PSX', 13:'SMART', 14:'PEARL', 15:'ISLAND'}


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
    contract1.exchange = "AMEX"
    contract1.currency = "USD"
    
    contract2 = Contract()
    contract2.symbol = akcia
    contract2.secType = "STK"
    contract2.exchange = "ARCA"
    contract2.currency = "USD"
    
    contract3 = Contract()
    contract3.symbol = akcia
    contract3.secType = "STK"
    contract3.exchange = "BATS"
    contract3.currency = "USD"
    
    contract4 = Contract()
    contract4.symbol = akcia
    contract4.secType = "STK"
    contract4.exchange = "BEX"
    contract4.currency = "USD"
    
    contract5 = Contract()
    contract5.symbol = akcia
    contract5.secType = "STK"
    contract5.exchange = "BYX"
    contract5.currency = "USD"
    
    contract6 = Contract()
    contract6.symbol = akcia
    contract6.secType = "STK"
    contract6.exchange = "CHX"
    contract6.currency = "USD"
    
    contract7 = Contract()
    contract7.symbol = akcia
    contract7.secType = "STK"
    contract7.exchange = "DRCTEDGE"
    contract7.currency = "USD"
    
    contract8 = Contract()
    contract8.symbol = akcia
    contract8.secType = "STK"
    contract8.exchange = "EDGEA"
    contract8.currency = "USD"
    
    contract9 = Contract()
    contract9.symbol = akcia
    contract9.secType = "STK"
    contract9.exchange = "IEX"
    contract9.currency = "USD"
    
    contract10 = Contract()
    contract10.symbol = akcia
    contract10.secType = "STK"
    contract10.exchange = "MEMX"
    contract10.currency = "USD"
    
    contract11 = Contract()
    contract11.symbol = akcia
    contract11.secType = "STK"
    contract11.exchange = "NYSE"
    contract11.currency = "USD"
    
    contract12 = Contract()
    contract12.symbol = akcia
    contract12.secType = "STK"
    contract12.exchange = "PSX"
    contract12.currency = "USD"
    
    contract13 = Contract()
    contract13.symbol = akcia
    contract13.secType = "STK"
    contract13.exchange = "SMART"
    contract13.currency = "USD"
    
    contract14 = Contract()
    contract14.symbol = akcia
    contract14.secType = "STK"
    contract14.exchange = "PEARL"
    contract14.currency = "USD"
    
    contract15 = Contract()
    contract15.symbol = akcia
    contract15.secType = "STK"
    contract15.exchange = "ISLAND"
    contract15.currency = "USD"
    
    self.ib.reqRealTimeBars(1, contract1, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(2, contract2, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(3, contract3, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(4, contract4, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(5, contract5, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(6, contract6, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(7, contract7, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(8, contract8, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(9, contract9, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(10, contract10, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(11, contract11, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(12, contract12, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(13, contract13, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(14, contract14, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(15, contract15, 1, "TRADES", 1, [])
    
    self.y = np.arange(5, dtype=float)
  
  def run_loop(self):
    self.ib.run()
  
  def on_bar_update(self, reqId, time, open_, high, low, close, volume, wap, count):
    'vyzera to tak, ze funkcia ide v slucke'
    print(reqId, time, wap, volume, count)
    self.y[0], self.y[1], self.y[2], self.y[3], self.y[4] = reqId, time, wap, volume, count
    data[reqId] = np.vstack([data[reqId], self.y])
    
    if reqId == burza:
      # priradenie casu to premennej cas, ktora je pouzita na vykreslovanie cenoveho grafu.
      # Cas je brany len z jednej burzy. Vacsinou je to zo "SMART".
      cas.append(pd.to_datetime(time, unit='s'))


bot = Bot()
vykreslovanie = Vykreslovanie_dat()
