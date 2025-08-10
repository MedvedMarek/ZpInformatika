import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
import threading
import time
import numpy as np

akcia = 'AMD'
vlakno = 6

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
    
    self.ib.reqRealTimeBars(1, contract1, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(2, contract2, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(3, contract3, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(4, contract4, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(5, contract5, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(6, contract6, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(7, contract7, 1, "TRADES", 1, [])
    
    self.x1 = np.arange(8, dtype=float)
    self.x2 = np.arange(8, dtype=float)
    self.x3 = np.arange(8, dtype=float)
    self.x4 = np.arange(8, dtype=float)
    self.x5 = np.arange(8, dtype=float)
    self.x6 = np.arange(8, dtype=float)
    self.x7 = np.arange(8, dtype=float)

    self.y = np.arange(8, dtype=float)
    
    self.data = {1:self.x1, 2:self.x2, 3:self.x3, 4:self.x4, 5:self.x5, 6:self.x6, 7:self.x7}
    
    self.nazov_burzy = {1:'AMEX', 2:'ARCA', 3:'BATS', 4:'BEX', 5:'BYX', 6:'CHX', 7:'DRCTEDGE'}
  
  def run_loop(self):
    self.ib.run()
  
  def on_bar_update(self, reqId, time, open_, high, low, close, volume, wap, count):
    'vyzera to tak, ze funkcia ide v slucke'
    print(reqId)
    self.y[0], self.y[1], self.y[2], self.y[3], self.y[4] = time, open_, high, low, close
    self.y[5], self.y[6], self.y[7] = wap, volume, count
    self.data[reqId] = np.vstack([self.data[reqId], self.y])
    if time % 50 == 0:
      np.save("/home/marek/"+akcia+'_'+self.nazov_burzy[reqId], self.data[reqId])




bot = Bot()
