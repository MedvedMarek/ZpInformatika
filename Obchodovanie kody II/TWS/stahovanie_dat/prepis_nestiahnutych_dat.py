import numpy as np
import os
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading

# final = aapl, amd, tsla, mstf, baba, amzn, googl, spy 
# burza = 'ORCL'
burza = 'TSM'

def najdi_neuplne_stiahnute_data():
  path = f'/media/marek/zaloha/Data/OHLC_TWS/{burza}/5s/trades/'
  zlozky = os.listdir(path)
  zlozky.sort()
  x = []

  for i in zlozky:
    for j in ['ARCA.npy', 'BATS.npy', 'DRCTEDGE.npy', 'EDGEA.npy', 'IEX.npy', 'MEMX.npy', 'NASDAQ.npy', 'NYSE.npy', 'PEARL.npy', 'PSX.npy', 'SMART.npy']:
      if os.path.getsize(f'{path}/{i}/{j}') < 1000:
        x.append([i.replace('_', '-'), j[:j.rfind('.')]])
  x.sort()
  return(x)


class IBapi(EWrapper, EClient):
  def __init__(self):
    EClient.__init__(self, self)
    self.data = []  # Initialize variable to store candle

  def historicalData(self, reqId, bar):
    self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])


class Stahovanie_OHLC:
  def __init__(self, interval_stahovanie):
    self.interval_stahovanie = interval_stahovanie
    self.datum_a_burza = najdi_neuplne_stiahnute_data()
    self.path = f'/media/marek/zaloha/Data/OHLC_TWS/{burza}/5s/trades/'
    self.stiahni_data_pre_OHLC()
  
  def stiahni_data_pre_OHLC(self):
    for i, j in self.datum_a_burza:
      print(i, j)
      app = IBapi()
      time.sleep(1)
      app.connect('127.0.0.1', 7497, 1)
      time.sleep(1)

      def run_loop():
        app.run()
      
      api_thread = threading.Thread(target=run_loop, daemon=True)
      api_thread.start()
      time.sleep(1)

      amd = Contract()
      amd.symbol = burza
      amd.secType = 'STK'
      amd.exchange = '{}'.format(j)
      amd.currency = 'USD'
      
      datum = i.replace('-', '')
      time.sleep(2)
      app.reqHistoricalData(1, amd, datum+'-21:00:00', '23400 S', '5 secs', 'trades', 1, 1, False, [])
      time.sleep(1) 
      path1 = self.path+i.replace('-', '_')+'/'+j+'.npy'
      time.sleep(1)

      dt = app.data
      app.disconnect()
      time.sleep(1)
      np.save(path1, dt)
      if np.asarray(dt).nbytes < 1000:
        print('\033[31m nestiahnute \033[0m')
      else:
        print('\033[32m stiahnute \033[0m')
      time.sleep(self.interval_stahovanie)


# navrhy pre cakanie:
# 5s  - 20

for j in range(6):
  print(f'{j} krat')
  Stahovanie_OHLC(10)

