"Zakladny kod je zo stranky: "
"https://www.youtube.com/user/jacobamaral"


import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
import threading
import time
import numpy as np



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
    self.ib.connect("127.0.0.1", 7496, 1)
    ib_thread = threading.Thread(target=self.run_loop, daemon=True)
    ib_thread.start()
    time.sleep(1)
    symbol = input("zadaj co chces obchodovat: ")
    contract = Contract()
    contract.symbol = symbol.upper()
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    self.ib.reqRealTimeBars(0, contract, 1, "TRADES", 1, [])
    
    self.x = np.arange(5, dtype=float)
    self.y = np.arange(5, dtype=float)
  
  def run_loop(self):
    self.ib.run()
  
  def on_bar_update(self, reqId, time, open_, high, low, close, volume, wap, count):
    'vyzera to tak, ze funkcia ide v slucke'
    print(open_, high, low, close, volume)
    self.y[0], self.y[1], self.y[2], self.y[3], self.y[4] = open_, high, low, close,volume
    self.x = np.vstack([self.x,self.y])
    np.save("/home/marek/skuska2", self.x)


bot = Bot()



#-----------------------------------------------------------------------------------











