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
def najdi_neuplne_stiahnute_data(cas_vstup,zlozka):
  """
  Funkcia zistuje velkost suborov a ak ma niektory menej ako je potrebne, tak je zapisany do zoznamu.

  Parameters
  ----------
  cas_vstup: Casovy usek, pre ktory sa budu stahovat data.
             Akceptovane hodnoty: (5s,10s,15s,30s,1m,2m,3m,5m,10m,15m,20m,30m,1h,2h)
  zlozka:    Zlozka reprezentuje, do ktorej zlozky sa maju data stahovat. Akceptuju sa hodnoty:
             (trades, midpoint, bid, ask, bid_ask, option_implied_volatility)
  mb:        dict. Je to slovnik, udrzujuci hodnoty pre velkosti suborov, ktore sa maju testovat. Ak je niektory
             subor mensi, ako je subor ktory je uplne stiahnuty, tak je zapisany do zoznamu a bude stiahnuty znova.
  
  
  Returns
  -------
  data: list
    Vystup je list, kde kazdy prvok obsahuje dva udaje ('datum', burza).
  """
  mb = {'5s': 1000,
        '10s':1000,
        '15s':1000,
        '30s':1000,
        '1m': 1000,
        '2m': 1000,
        '3m': 1000,
        '5m': 1000,
        '10m':1000,
        '15m':1000,
        '20m':1000,
        '30m':1000,
        '1h': 1000,
        '2h': 1000,
        '4h': 1000}
  path   = f'/media/marek/zaloha/Data/OHLC_TWS/AAPL/{cas_vstup}/{zlozka}/'
  zlozky = os.listdir(path)
  x = []
  for i in zlozky:
    # for j in os.listdir(f'{path}/{i}/'):
    for j in ['ARCA.npy','BATS.npy','DRCTEDGE.npy','EDGEA.npy','IEX.npy','MEMX.npy','NASDAQ.npy','NYSE.npy','PEARL.npy','PSX.npy','SMART.npy']:
      if os.path.getsize(f'{path}/{i}/{j}') < mb[cas_vstup]:
        # rfind najde bodku v stringu (jeho poziciu) a potom index je pouzity ako hranica pre nacitanie stringu.
        # Tymto som odstranil bodku a priponu suboru a ostal mi len nazov burzy.
        x.append([i.replace('_','-'),j[:j.rfind('.')]])
  x.sort()
  return(x)


class IBapi(EWrapper, EClient):
	def __init__(self,zlozka):
	  EClient.__init__(self, self)
	  self.data = [] #Initialize variable to store candle
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
               Akceptovane hodnoty: (5s,10s,15s,30s,1m,2m,3m,5m,10m,15m,20m,30m,1h,2h)
    cas_int:   Slovnik v ktorom su ulozene hodnoty, ktore su potrebne ako vstupy do funkcii TWS.
    zlozka: Zlozka reprezentuje, do ktorej zlozky sa maju data stahovat. Akceptuju sa hodnoty:
            (trades, midpoint, bid, ask, bid_ask, option_implied_volatility)
    typ:    Typ dat ktore sa budu stahovat.
    interval: String. Je to iba vypichnute zo slovnika, aby sa to nemuselo konvertovat priamo vo funkcii.
    zlozka_typ: Strint. Je to iba vypichnute zo slovnika, aby sa to nemusel konvertovat priamo vo funkcii.
    
    
    datumy: tu su ulozene vsetky datumy pre ktore sa dubu stahovat udaje. Je to spravene tak, ze boli stiahnute
            historicke data z yahoo financial. Tam su zaznamenane vsetky obchodne dni. A potom bol nacitany 
            stlpec Date, z ktore holi vytiahnute datumy, podla ktorych sa stahuju historicke data.
    burzy:  tu su ulozene vsetky burzy, z ktorych sa budu stahovat udaje
    path:   uplna cesta do zlozky, kde sa budu vytvarat zlozky z datumov a ukladanie do nich
    """
    self.cas_vstup = cas_vstup
    self.cas_int   = {'5s':'5 secs', '10s':'10 secs', '15s':'15 secs', '30s':'30 secs',
                      '1m':'1 min', '2m':'2 mins', '3m':'3 mins', '5m':'5 mins', '10m':'10 mins', '15m':'15 mins',
                      '20m':'20 mins', '30m':'30 mins', '1h':'1 hour', '2h':'2 hours', '4h':'4 hours'}
    self.interval = self.cas_int[self.cas_vstup]
    self.zlozka = zlozka
    self.typ    = {'trades':'TRADES', 'midpoint':'MIDPOINT', 'bid':'BID', 'ask':'ASK', 'bid_ask':'BID_ASK',
                   'option_implied_volatility':'OPTION_IMPLIED_VOLATILITY'}
    self.interval_stahovanie = interval_stahovanie
    self.datum_a_burza = najdi_neuplne_stiahnute_data(cas_vstup,zlozka)
    self.path   = f'/media/marek/zaloha/Data/OHLC_TWS/AAPL/{cas_vstup}/{zlozka}/'
    self.stiahni_data_pre_OHLC()
  
  def stiahni_data_pre_OHLC(self):
    """
    Kompletne spracovanie stahovanych dat a ich ulozenie do vytvorenej zlozky.
    """
    for i,j in self.datum_a_burza:
      print(i,j)
      app = IBapi(self.zlozka)
      time.sleep(1)
      app.connect('127.0.0.1', 7497, 1)
      time.sleep(1)
      def run_loop():
        app.run()
      
      api_thread = threading.Thread(target=run_loop, daemon=True)
      api_thread.start()
      time.sleep(1)
      
      amd = Contract()
      amd.symbol = 'AAPL'
      amd.secType = 'STK'
      amd.exchange = '{}'.format(j)
      amd.currency = 'USD'
      
      datum = i.replace('-','')
      time.sleep(2) 
      app.reqHistoricalData(1,amd, datum+'-21:00:00', '23400 S', self.interval, self.zlozka, 1, 1, False, [])
      time.sleep(1) 
      path1 = self.path+i.replace('-','_')+'/'+j+'.npy'
      time.sleep(1) 
      
      dt = app.data
      app.disconnect()
      time.sleep(1)
      np.save(path1,dt)
      if np.asarray(dt).nbytes < 1000:
        print('nestiahnute')
      else:
        print('stiahnute')
      time.sleep(self.interval_stahovanie)


# navrhy pre cakanie:
# 5s  - 20
# 10s - 3
# 1m  - 1

#for i in ['5s','10s','15s','30s','1m','2m','3m','5m','10m','15m']:
#   print (i)
#   Stahovanie_OHLC(i,'trades',10)

#Toto su zapisane hodnoty, ktore boli prejdene v cykle 5x. A ak sa nestiahli, tak nebudu dostupne.
# trades - 5s,10s,15s,30s,1m,  

for j in range(5):
  for i in ['5s']:
    print(f'{i} - {j} krat')
    Stahovanie_OHLC(i,'trades',15)


