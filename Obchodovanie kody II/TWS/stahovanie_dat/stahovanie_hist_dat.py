from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import pandas as pd
import os
import numpy as np


class IBapi(EWrapper, EClient):
  def __init__(self):
    EClient.__init__(self, self)
    self.data = []

  def historicalData(self, reqId, bar):
    self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])


class Stahovanie_OHLC:
  def __init__(self, interval_stahovanie):
    self.burza = 'TSLA'  # men len burzu. Ostatne je nastavene.
    self.datumy = list(pd.read_csv(f'/home/marek/Desktop/{self.burza}.csv')['Date'])
    self.burzy = ['ARCA', 'BATS', 'DRCTEDGE', 'EDGEA', 'IEX', 'MEMX', 'NASDAQ', 'NYSE', 'PEARL', 'PSX', 'SMART']
    self.path = f'/media/marek/zaloha/Data/OHLC_TWS/{self.burza}/5s/trades/'
    self.interval_stahovanie = interval_stahovanie
    self.stiahni_data_pre_OHLC()

  def stiahni_data_pre_OHLC(self):
    for i in self.datumy:
      os.mkdir(self.path+i.replace('-', '_'))
      for j in self.burzy:
        app = IBapi()
        app.connect('127.0.0.1', 7497, 123)
        time.sleep(1)

        def run_loop():
          app.run()

        api_thread = threading.Thread(target=run_loop, daemon=True)
        api_thread.start()

        amd = Contract()
        amd.symbol = self.burza
        amd.secType = 'STK'
        amd.exchange = '{}'.format(j)
        amd.currency = 'USD'

        datum = i.replace('-', '')
        app.reqHistoricalData(1, amd, datum+'-21:00:00', '23400 S', '5 secs', 'TRADES', 1, 1, False, [])
        time.sleep(1)
        path1 = self.path+i.replace('-', '_')+'/'+j+'.npy'

        dt = app.data
        app.disconnect()
        time.sleep(self.interval_stahovanie)
        np.save(path1, dt)
        print(f'\033[35m{i} - {j} - {len(dt)}\033[0m')


# navrhy pre cakanie:
# 5s  - 20

Stahovanie_OHLC(25)
