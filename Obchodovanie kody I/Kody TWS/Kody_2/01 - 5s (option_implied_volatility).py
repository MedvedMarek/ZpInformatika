# Nacitavanie historickych dat pre OHLC.
# Data pre OHLC sa dudu stahovat len pre akciu AMD.

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import pandas as pd
import sys
import os
import numpy as np


class IBapi(EWrapper, EClient):
	def __init__(self):
	  EClient.__init__(self, self)
	  self.data = [] #Initialize variable to store candle
	
	def historicalData(self, reqId, bar):
	  self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close])#----------------------------------



class Stahovanie_OHLC:
  """
  Stahovanie OHLC dat z TWS. 
  """
  def __init__(self):
    """
    Parameters
    ----------
    datumy: tu su ulozene vsetky datumy pre ktore sa dubu stahovat udaje. Je to spravene tak, ze boli stiahnute
            historicke data z yahoo financial. Tam su zaznamenane vsetky obchodne dni. A potom bol nacitany 
            stlpec Date, z ktore holi vytiahnute datumy, podla ktorych sa stahuju historicke data.
    burzy:  tu su ulozene vsetky burzy, z ktorych sa budu stahovat udaje
    path:   uplna cesta do zlozky, kde sa budu vytvarat zlozky z datumov a ukladanie do nich
    """
    self.datumy = list(pd.read_csv('/home/marek/Desktop/AAPL.csv')['Date']) #-----------------------------------------------------------------
    self.burzy  = ['SMART']
    self.path   = '/media/marek/zaloha/Data/OHLC_TWS/AAPL/5s/option_implied_volatility/' #----------------------------------------------------
    self.stiahni_data_pre_OHLC()
  
  def stiahni_data_pre_OHLC(self):
    """
    Kompletne spracovanie stahovanych dat a ich ulozenie do vytvorenej zlozky.
    """
    for i in self.datumy:
      os.mkdir(self.path+i.replace('-','_'))
      for j in self.burzy:
        app = IBapi()
        time.sleep(1)
        app.connect('127.0.0.1', 7497, 123)
        time.sleep(1)
        def run_loop():
          app.run()
        
        api_thread = threading.Thread(target=run_loop, daemon=True)
        api_thread.start()
        time.sleep(1)
        
        amd = Contract()
        amd.symbol = 'AAPL' #----------------------------------------------------------------------------------------------------------------------------
        amd.secType = 'STK'
        amd.exchange = '{}'.format(j)
        amd.currency = 'USD'
        
        datum = i.replace('-','')
        time.sleep(1)
        app.reqHistoricalData(1,amd, datum+'-21:00:00', '23400 S', '5 secs', 'OPTION_IMPLIED_VOLATILITY', 1, 1, False, []) #-------------------------
        time.sleep(1)
        path1 = self.path+i.replace('-','_')+'/'+j+'.npy'
        time.sleep(1)
        
        dt = app.data
        #np.save(path1, app.data)
        app.disconnect()
        time.sleep(1)
        np.save(path1,dt)
        time.sleep(10)


stahovanie = Stahovanie_OHLC()











































