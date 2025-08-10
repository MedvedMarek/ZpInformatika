# Stahuje a prepisuje data, ktore neboli stiahnute hned na prvy krat. Je to z dovodu, ze sa 
# asi prerusilo stahovacie vlakno alebo spojenie so serverom.

import pandas as pd
import numpy as np
import os
import time
import sys
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading


# zistujem velkost suborov a ak ma niektory menej ako 1M tak ho budem stahovat znova. Lebo
# pravdepodobne, ze sa prerusilo stahovanie v danom pripade.
def najdi_neuplne_stiahnute_data():
  """
  Funkcia zistuje velkost suborov a ak ma niektory menej ako 1M, tak je zapisany do premennej.
  
  Returns
  -------
  data: list
    Vystup je list, kde kazdy prvok obsahuje dva udaje ('datum', burza).
  """
  path   = '/media/marek/zaloha/Data/OHLC_TWS/AAPL/5s/bid/' #------------------------------------------------------
  zlozky = os.listdir(path)
  x = []
  for i in zlozky:
    for j in os.listdir(path+i):
      if os.path.getsize(path+i+'/'+j) < 2900000: #--------------------------------------------------------------------
        # rfind najde bodku v stringu (jeho poziciu) a potom index je pouzity ako hranica pre nacitanie stringu.
        # Tymto som odstranil bodku a priponu suboru a ostal mi len nazov burzy.
        x.append([i.replace('_','-'),j[:j.rfind('.')]])
  x.sort()
  return(x)


class IBapi(EWrapper, EClient):
	def __init__(self):
	  EClient.__init__(self, self)
	  self.data = [] #Initialize variable to store candle
	
	def historicalData(self, reqId, bar):
	  self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close]) #---------------------------------


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
    self.datum_a_burza = najdi_neuplne_stiahnute_data()
    self.path   = '/media/marek/zaloha/Data/OHLC_TWS/AAPL/5s/bid/' #---------------------------------------------
    self.stiahni_data_pre_OHLC()
  
  def stiahni_data_pre_OHLC(self):
    """
    Kompletne spracovanie stahovanych dat a ich ulozenie do vytvorenej zlozky.
    """
    for i,j in self.datum_a_burza:
      print(i,j)
      app = IBapi()
      app.connect('127.0.0.1', 7497, 1)
      
      def run_loop():
        app.run()
      
      api_thread = threading.Thread(target=run_loop, daemon=True)
      api_thread.start()
      time.sleep(2)
      
      amd = Contract()
      amd.symbol = 'AAPL' #--------------------------------------------------------------------------------------------
      amd.secType = 'STK'
      amd.exchange = '{}'.format(j)
      amd.currency = 'USD'
      
      datum = i.replace('-','')
      app.reqHistoricalData(1,amd, datum+'-21:00:00', '23400 S', '5 secs', 'BID', 1, 1, False, []) #---------------
      time.sleep(2)
      
      np.save(self.path+i.replace('-','_')+'/'+j+'.npy', app.data)
      
      app.disconnect()
      time.sleep(15)



stahovanie = Stahovanie_OHLC()




























