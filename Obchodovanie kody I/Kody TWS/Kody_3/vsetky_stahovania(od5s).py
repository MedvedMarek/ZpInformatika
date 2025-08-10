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
	def __init__(self,zlozka):
	  EClient.__init__(self, self)
	  self.data = []
	  self.zlozka = zlozka
	
	def historicalData(self, reqId, bar):
	  if self.zlozka == 'trades':
	    self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])
	  else:
	    self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close])




class Stahovanie_OHLC:
  """
  Stahovanie OHLC dat z TWS. 
  """
  def __init__(self,cas_vstup,zlozka,interval_stahovanie):
    """
    Parameters
    ----------
    cas_vstup: Casovy usek, pre ktory sa budu stahovat data.
               Akceptovane hodnoty: (5s,10s,15s,30s,1m,2m,3m,5m,10m,15m,20m,30m,1h,2h,4h)
    cas_int:   Slovnik v ktorom su ulozene hodnoty, ktore su potrebne ako vstupy do funkcii TWS.
    zlozka: Zlozka reprezentuje, do ktorej zlozky sa maju data stahovat. Akceptuju sa hodnoty:
            (trades,midpoint,bid,ask,bid_ask,option_implied_volatility)
    typ:    Typ dat ktore sa budu stahovat.
    interval: String. Je to iba vypichnute zo slovnika, aby sa to nemuselo konvertovat priamo vo funkcii.
    zlozka_typ: Strint. Je to iba vypichnute zo slovnika, aby sa to nemusel konvertovat priamo vo funkcii.
    datumy: tu su ulozene vsetky datumy pre ktore sa dubu stahovat udaje. Je to spravene tak, ze boli stiahnute
            historicke data z yahoo financial. Tam su zaznamenane vsetky obchodne dni. A potom bol nacitany 
            stlpec Date, z ktore holi vytiahnute datumy, podla ktorych sa stahuju historicke data.
    burzy:  tu su ulozene vsetky burzy, z ktorych sa budu stahovat udaje
    path:   uplna cesta do zlozky, kde sa budu vytvarat zlozky z datumov a ukladanie do nich
    interval_stahovanie: int Je to interval kolko ma byt pauza pri odpojeni sa z vlakna.
    """
    self.cas_vstup = cas_vstup
    self.cas_int   = {'5s':'5 secs', '10s':'10 secs', '15s':'15 secs', '30s':'30 secs',
                      '1m':'1 min', '2m':'2 mins', '3m':'3 mins', '5m':'5 mins', '10m':'10 mins', '15m':'15 mins',
                      '20m':'20 mins', '30m':'30 mins', '1h':'1 hour', '2h':'2 hours', 
                      '4h':'4 hours','1d':'1 day'}
    self.zlozka = zlozka
    self.typ    = {'trades':'TRADES', 'midpoint':'MIDPOINT', 'bid':'BID', 'ask':'ASK', 'bid_ask':'BID_ASK',
                   'option_implied_volatility':'OPTION_IMPLIED_VOLATILITY'}
    self.interval = self.cas_int[self.cas_vstup]
    self.zlozka_typ = self.typ[self.zlozka]
    self.datumy = list(pd.read_csv('/home/marek/Desktop/AAPL.csv')['Date'])
    # self.burzy  = ['ARCA', 'BATS', 'CHX', 'DRCTEDGE', 'IEX', 'MEMX', 'NYSE', 'PSX', 'SMART', 'PEARL', 'ISLAND'] if zlozka != 'option_implied_volatility' else ['SMART']
    # self.burzy = ['ARCA','BATS','DRCTEDGE', 'EDGEA', 'IEX', 'ISLAND', 'MEMX', 'NASDAQ', 'NYSE', 'PEARL', 'PSX', 'SMART'] if zlozka != 'option_implied_volatility' else ['SMART']
    self.burzy = ['ARCA', 'BATS', 'DRCTEDGE', 'EDGEA', 'IEX', 'MEMX', 'NASDAQ', 'NYSE', 'PEARL', 'PSX', 'SMART']
    self.path   = '/media/marek/zaloha/Data/OHLC_TWS/AAPL/'+cas_vstup+'/'+zlozka+'/'
    self.interval_stahovanie = interval_stahovanie
    self.stiahni_data_pre_OHLC()
  
  def stiahni_data_pre_OHLC(self):
    """
    Kompletne spracovanie stahovanych dat a ich ulozenie do vytvorenej zlozky.
    """
    for i in self.datumy:
      os.mkdir(self.path+i.replace('-','_'))
      for j in self.burzy:
        app = IBapi(self.zlozka)
        # time.sleep(1) # nad 10s toto vypnut
        app.connect('127.0.0.1', 7497, 123)
        time.sleep(1)
        def run_loop():
          app.run()
        
        api_thread = threading.Thread(target=run_loop, daemon=True)
        api_thread.start()
        # time.sleep(1) # nad 10s toto vypnut
        
        amd = Contract()
        amd.symbol = 'AAPL'
        amd.secType = 'STK'
        amd.exchange = '{}'.format(j)
        amd.currency = 'USD'
        
        datum = i.replace('-','')
        # time.sleep(1) #nad 5s toto vypnut
        app.reqHistoricalData(1,amd, datum+'-21:00:00', '23400 S', self.interval, self.zlozka_typ, 1, 1, False, [])
        time.sleep(1) 
        path1 = self.path+i.replace('-','_')+'/'+j+'.npy'
        # time.sleep(1) 
        
        dt = app.data
        # time.sleep(1) # nad 5s toto vypnut
        app.disconnect()
        time.sleep(self.interval_stahovanie)
        np.save(path1,dt)


# parametre:
# aky casovy usek sa stahuje, do ktorej zlozky sa uklada, kolko sa caka na konci po odpojeni vlakna

# navrhy pre cakanie:
# 5s  - 20
# 10s - 3
# 30s - 3
# 1m  - 1

for i in ['5s']:
        for j in ['trades']:
                Stahovanie_OHLC(i,j,15)


#for i in ['15m']:
#   for x in ['ask','bid_ask']:
#      Stahovanie_OHLC(i,x,2)







































