# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Priprava dat, ktore budu vstupovat do generatora pri trenovani RNN sieti.
Pri priprave dat je vynechany prvy den. Je to z dovodu, ze z neho boli pocitane
rozne udaje. Ako napriklad ema a min/max nasledujuceho dna. Tymto padom nie je 
potrebne, aby boli k dispozicii nejake inde udaje. Vsetko je pocitane zo stiahnutych
dat.
"""
import numpy as np
import pandas as pd
import os
import time
from datetime import timedelta

class UpravaDat:
  def __init__(self):
    """
    Atributs
    --------
    path: str
      Cesta do zlozky, kde zu ulozene data.
    datumy: list
      Zoradene datumy pre ktore su k dispozicii data.
    burzy: list
      Vsetky burzy pre ktore su stiahnute data.
    ema: int
      Hodnota parametra pre klzavy priemer. Je to nastavene na hodnotu 600. Hodnota je prevzata z nahladu na
      minutovy graf, kde sa osvedcila EMA 50. To potom pre 5s graf znamena 50*12=600.
        
    """
    self.path   = '/media/marek/zaloha/Data/OHLC_TWS/'
    self.datumy = self.__nacitaj_datumy()
    # self.burzy = ['AMEX','ARCA','BATS','BEX','BYX','CHX','DRCTEDGE','EDGEA','IEX','MEMX','NYSE','PSX','SMART','PEARL','ISLAND']
    # Tu su odobrane burzy : Amex, Bex, Byx, Edgea, Chx, Psx, Pearl. Je to z dovodu, ze neboli tak casto obchodovane. Preto
    # bolo vyhovujuce ich nedavat do dat, aby sa zbytocne nezahlcovala pamat a vypoctova narocnost.
    self.burzy = ['ARCA','BATS','DRCTEDGE','IEX','MEMX','NYSE','SMART','ISLAND']
    self.ema   = 600
    
  def __nacitaj_datumy(self):
    """
    Nacitava datumy zo zlozky, kde su ulozene data. Datumy su nasledne zoradene.
    
    Returns
    -------
    datumy: list
    """
    datumy = os.listdir(self.path)
    datumy.sort()
    return(datumy)
  
  def __spoj_burzy(self, datum):
    """
    Spaja vsetky burzy z obchodneho dna do jedneho dataframu. Burzy su spojene tak, ze 
    ohlc je ponechane len pre burzu SMART. Od ostatnych burz je prevzate len volume.
    
    Parameters
    ----------
    datum: str
      Datum, pre ktory sa maju stiahnut a spojit burzy.
    
    Returns
    -------
    data: DataFrame
      Spojeny dataframe. Stlpce v daraframe su nasledovne: time,o,h,l,c,AMEX,ARCA,... . 
      Time a ohlc su data zobrate z burzy smart. Burza smart v prvom kroku nie je zaradena
      do dataframu. Je zaradena az v druhom kroku, kde sa doplna volume pre kazdu burzu. 
      Teda potom dalej burzy reprezentuju volume. 
    """
    def uprav_na_typ(data,burza):
      """
      Upravuje typ dat v stlpcoch. Str prevadza na datetime alebo na int.
      Funkcia je pouzita iba v cykle for.
      """
      data['time'] = pd.to_datetime(data['time'])
      data[burza] = data[burza].astype('float')
      return(data)
    
    def skontroluj_cas_otvorenia(otvorenie_smart,data):
      """
      Kontroluje cas, ci je rovnaky ako je cas pre burzu SMART. Lebo niektore burzy maju posunuty
      cas aj o hodinu. Preto ho treba zarovnat s burzou SMART. Taktiez je potrebne brat v uvahu,
      za sa moze menit cas (letny, zimny). Preto sa neda orientovat iba jednyn casom 15:30 - 22:00.
      Ale treba brat v uvahu, ked europa a amerika maju dva tyzdne v roku nie rovnaky letny alebo
      zimny cas.
      
      Parameters
      ----------
      otvorenie_smart: pd.TimeStamp
        Toto je otvaraci cas pre burzu Smart. Tento cas bude referencny.
      data: Dataframe
      
      Returns
      -------
      data: DataFrame
        V pripade potreby upraveny dataframe na rovnaky cas ako ma burza SMART.
      """
      otvorenie_burza = data['time'][0]
      if otvorenie_burza >= otvorenie_smart+timedelta(hours=1):
        data['time'] = data['time']-timedelta(hours=1)
      
      return(data)
    
    data = np.load(self.path+datum+'/SMART.npy')
    data = pd.DataFrame(data[:,:5], columns=['time','o','h','l','c'])
    data['time'] = pd.to_datetime(data['time'])
    data['o'] = data['o'].astype('float')
    data['h'] = data['h'].astype('float')
    data['l'] = data['l'].astype('float')
    data['c'] = data['c'].astype('float')
    otvorenie_smart = data['time'][0] #Toto sluzi na porovnanie otvaracieho casu pre ostatne burzy 
    
    for i in self.burzy:
      dt = np.load(self.path+datum+'/'+i+'.npy')
      dt = pd.DataFrame(dt[:,[0,5]], columns=['time',i])
      dt = uprav_na_typ(dt,i)
      dt = skontroluj_cas_otvorenia(otvorenie_smart, dt)
      data = pd.merge(data,dt, how='outer', on='time')
    
    data = data.fillna(0)
    return(data)
  
  def __spoj_dni(self):
    """
    Spaja dni do jedneho dataframu.
    
    Returns
    -------
    data: DataFrame
    """
    data = self.__spoj_burzy(self.datumy[0])
    
    for i in self.datumy[1:]:
      print(i)
      d = self.__spoj_burzy(i)
      data = pd.concat([data,d], ignore_index=True)
    
    return(data)
  
  def __vypocitaj_EMA(self):
    """
    EMA je pocitana z kompletneho balika dat. Prve hodnoty pre EMA su ponechane povodne otvaracie ceny. Preto 
    aby sa predislo zmatocnym udajom pre trenovanie NN sieti, tak prve hodnoty, z ktorych sa pocitala prva
    hodnota pre EMA budu odstranene v nasledujucej funkcii. Lebo cely jeden den bude odstraneny.
    
    Returns
    -------
    data: DataFrame
      Do dataframu je doplneny stlpec pre EMA.
    """
    data = self.__spoj_dni()
    k  = 2/(self.ema+1)
    k1 = 1-k
    data.insert(5,'ema',None)
    data.loc[:self.ema, 'ema'] = data['c'][:self.ema]
    
    for i in range(self.ema, data.shape[0]):
      data.loc[i,'ema'] = (data.loc[i,'c']*k + data.loc[(i-1), 'ema']*k1)
    
    # data = data[self.ema:].reset_index(drop=True)
    return(data)
  
  def __vypocitaj_sklon_EMA(self):
    """
    Pocita sklon EMA. Lebo aj toto je udaj, ktory sa sleduje v day tradingu. A sklon je jedna z veci
    ktora urcuje, ci je predpoklad rastu alebo klesania ceny.
    Sposob vypoctu sklonu je, ze sa berie rozdiel dvoch po sebe iducich ema a vynasobi sa to 1000. 
    Nasobenie je z toho dovodu, ze rozdiel dvoch ema je velmi malicky. Preto prenasobenim 1000 to viem
    dostat aspon ku jednotke.
    sklon_ema[t] = (ema[t]-ema[t-1])*1000
    
    Returns
    -------
    data: Dataframe
    """
    data = self.__vypocitaj_EMA()
    data.insert(6,'sklon_ema',None)
    
    for i in range(1,data.shape[0]):
      data.loc[i,'sklon_ema'] = (data['ema'][i] - data['ema'][i-1])*1000
    
    data.loc[0,'sklon_ema'] = data['sklon_ema'][1] # Nultu hodnotu davam rovnaku ako je prva hodnota
    return(data)
  
  def __dopln_min_max_close_predchadzajuceho_dna(self):
    """
    Doplna stlpce min, max a close z predchadzajuceho dna. Lebo toto su udaje, ktore su dolezite 
    pre day trading. Vystupne data su mensie o jeden obchodny den. Odobraty je prvy obchodny den,
    lebo ten sluzi ako vstupne udaje pre min,max,close pre nasledujuci den. A pre prvy den nie su
    k dispozicii data. Bolo by mozne ich doplnit z nejakeho externeho suboru, ale je lepsie 
    nespoliehat sa na dalsie vstupy.
    
    Returns
    -------
    data: DataFrame
      Rozsireny dataframe o stlpce min,max,close.
    """
    data = self.__vypocitaj_sklon_EMA()
    data.insert(7,'close',None)
    data.insert(7,'max',None)
    data.insert(7,'min',None)
    
    # Prevzatie min,max,close z prveho dna
    datum = pd.to_datetime(self.datumy[0].replace('_','-'))
    mask = ((data['time'] >= datum) & (data['time'] < datum+timedelta(days=1)))
    _min = min(data[mask]['c'])
    _max = max(data[mask]['c'])
    close = float(data[mask]['c'][-1:])
    
    for i in self.datumy[1:]:
      datum = pd.to_datetime(i.replace('_','-'))
      mask = ((data['time'] >= datum) & (data['time'] < datum+timedelta(days=1)))
      data.loc[mask,'min'] = _min
      data.loc[mask,'max'] = _max
      data.loc[mask,'close'] = close
      
      _min = min(data[mask]['c'])
      _max = max(data[mask]['c'])
      close = float(data[mask]['c'][-1:])
    
    # V tomto kroku odstranujem prvy den, z ktoreho sa brali prve hodnoty pre min,max,close.
    data = data[data['time'] > pd.to_datetime(self.datumy[1].replace('_','-'))]
    data = data.reset_index(drop=True)
    
    return(data)
    
  def __uprav_min_max_close_ema(self):
    """
    Uprava sa realizuje tak, ze hodnota min,max,close sa odpocita od ceny open. Je potrebne
    aby hodnota nebola viazana na nejaku konkretnu cenu, ale len na cenu otvorenia. 
    data['min'] = data['o']-data['min']
    data['max'] = data['o']-data['max']
    data['close'] = data['o']-data['close']
    
    Uprava EMA sa realizuje:
    data['ema'] = data['ema'] - data['o']
    
    Returns
    -------
    data: DataFrame
      Upravene data min,max,close.
    """
    data = self.__dopln_min_max_close_predchadzajuceho_dna()
    data['min'] = data['o'] - data['min']
    data['max'] = data['o'] - data['max']
    data['close'] = data['o'] - data['close']
    data['ema'] = data['ema'] - data['o']
    
    return(data)
  
  def __uprav_ohlc(self):
    """
    V ohlc sa upravuju iba stlpce hlc. Stlpec o sa iba predeli 100, aby sa dostal do intervalu 0-1. Teda
    bude ponechana skutocna cena aktiva. Data hcl budu odrazat skutocne rozmery sviecky. 
    'h' - ukazuje na velkost horneho knotu
    'l' - ukazuje na velkost spodneho knotu
    'c' - bude reprezentovat velkost sviecky bez knotov. Teda data['c']-data['o']
    """
    data = self.__uprav_min_max_close_ema()
    
    for i in range(data.shape[0]):
      if data['o'][i] <= data['c'][i]:
        data.loc[i,'h'] = data['h'][i] - data['c'][i]
        data.loc[i,'l'] = data['o'][i] - data['l'][i]
        data.loc[i,'c'] = data['c'][i] - data['o'][i]
      else:
        data.loc[i,'h'] = data['h'][i] - data['o'][i]
        data.loc[i,'l'] = data['c'][i] - data['l'][i]
        data.loc[i,'c'] = data['c'][i] - data['o'][i]
    
    data['o'] = data['o']/100
    
    return(data)
  
  def __dopln_h_m_s(self):
    """
    Doplnaju sa stlpce h,m,s (hodiny, minuty, sekundy). Je to vybrate zo stlpca time. A potom je
    stlpec time odstraneny. Hodnoty h,m,s su potom normalizovane.
    
    Return
    ------
    data: DataFrame
    """
    data = self.__uprav_ohlc()
    
    data.insert(1,'second',None)
    data.insert(1,'minute',None)
    data.insert(1,'hour',None)
    
    data['second'] = data['time'].apply(lambda x: (x.second)/60) # Hned to aj normalizujem
    data['minute'] = data['time'].apply(lambda x: (x.minute)/60) # Hned to aj normalizujem
    data['hour']   = data['time'].apply(lambda x: (x.hour)/22)   # Hned to aj normalizujem
    
    del(data['time']) # Odstranenie time. Uz tento stlpec nebude potrebny.
    return(data)
  
  def __normalizuj_volume(self):
    data = self.__dopln_h_m_s()
    volume = {'ARCA':200,'BATS':150,'DRCTEDGE':300,'IEX':100,'MEMX':130,'NYSE':100,'SMART':2000,'ISLAND':1000}
    
    for i in volume:
      data[i] = data[i]/volume[i]
    
    return(data)
  
  def vrat_data_pre_nn(self):
    """
    Vrati upravene data, ktore budu pouzite ako vstup do trenovania NN sieti.
    """
    # data = self.__normalizuj_volume()
    data = self.__spoj_dni()
    return(data)


uprava = UpravaDat()
data = uprava.vrat_data_pre_nn()

# train 1.9 - 14.9
# train 20.9 - 23.11
# val 28.11 - 30.12
# test 1.1 - 31.1
data.to_csv('/home/marek/Dropbox/Data/TWS/data_neupravene.csv', index=False)













