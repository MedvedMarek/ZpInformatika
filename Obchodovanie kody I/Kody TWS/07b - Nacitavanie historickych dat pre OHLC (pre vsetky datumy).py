# Nacitavanie historickych dat pre OHLC. Je to z dovodu, lebo OHLC nebolo stahovane sucastne
# zo streamu. Doplnene je to az neskor.
# Data pre OHLC sa dudu stahovat len pre akciu AMD.

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import pandas
import sys
import os
import numpy as np


class IBapi(EWrapper, EClient):
	def __init__(self):
	  EClient.__init__(self, self)
	  self.data = [] #Initialize variable to store candle
	
	def historicalData(self, reqId, bar):
	  self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])



class Stahovanie_OHLC:
  """
  Stahovanie OHLC dat z TWS. Data su stahovane z dovodu, lebo neboli zahrnute hned pri
  prvom stahovani. Od tohoto datumu, budu data stahovane aj s OHLC, preto tento kod
  uz nebude potrebny pre dalsie pouzitie.
  """
  def __init__(self):
    """
    Parameters
    ----------
    datumy: tu su ulozene vsetky datumyk pre ktore sa dubu stahovat udaje
    burzy:  tu su ulozene vsetky burzy, z ktorych sa budu stahovat udaje
    path:   uplna cesta do zlozky, kde sa budu vytvarat zlozky z datumov a ukladanie do nich
    """
    self.datumy = os.listdir('/home/marek/Dropbox/Data/TWS Docasne prelozene  data/')
    self.datumy.sort()
    self.burzy  = ['AMEX', 'ARCA', 'BATS', 'BEX', 'BYX', 'CHX', 'DRCTEDGE', 'EDGEA', 'IEX', 'MEMX', 'NYSE', 'PSX', 'SMART', 'PEARL', 'ISLAND']
    self.path   = '/home/marek/Dropbox/Data/OHLC stiahnute/'
    self.stiahni_data_pre_OHLC()
  
  def stiahni_data_pre_OHLC(self):
    """
    Kompletne spracovanie stahovanych dat a ich ulozenie do vytvorenej zlozky.
    """
    for i in self.datumy:
      os.mkdir(self.path+i)
      for j in self.burzy:
        app = IBapi()
        app.connect('127.0.0.1', 7497, 123)
        
        def run_loop():
          app.run()
        
        api_thread = threading.Thread(target=run_loop, daemon=True)
        api_thread.start()
        time.sleep(7)
        
        amd = Contract()
        amd.symbol = 'AMD'
        amd.secType = 'STK'
        amd.exchange = '{}'.format(j)
        amd.currency = 'USD'
        
        datum = i.replace('_','')
        app.reqHistoricalData(1,amd, datum+'-21:00:00', '23400 S', '5 secs', 'TRADES', 0, 2, False, [])
        time.sleep(7)
        
        np.save(self.path+i+'/'+'AMD_'+j+'.npy', app.data)
        
        app.disconnect()
        time.sleep(11)



stahovanie = Stahovanie_OHLC()
















































