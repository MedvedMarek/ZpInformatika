from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time
import pandas

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
		self.data = [] #Initialize variable to store candle

	def historicalData(self, reqId, bar):
		self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])
		
def run_loop():
	app.run()


burzy = ['AMEX', 'ARCA', 'BATS', 'BEX', 'BYX', 'CHX', 'DRCTEDGE', 'EDGEA', 'IEX', 'MEMX', 'NYSE', 'PSX', 'SMART', 'PEARL', 'ISLAND']



for i in burzy:
  app = IBapi()
  app.connect('127.0.0.1', 7497, 123)
  
  api_thread = threading.Thread(target=run_loop, daemon=True)
  api_thread.start()
  time.sleep(7)
  
  amd = Contract()
  amd.symbol = 'AMD'
  amd.secType = 'STK'
  amd.exchange = '{}'.format(i)
  amd.currency = 'USD'
  
  app.reqHistoricalData(1, amd, '20221111-21:00:00', '23400 S', '5 secs', 'TRADES', 0, 2, False, [])
  time.sleep(6)
  
  df = pandas.DataFrame(app.data, columns=['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume'])
  df.to_csv('AMD_{}.csv'.format(i))
  
  app.disconnect()
  time.sleep(11)




