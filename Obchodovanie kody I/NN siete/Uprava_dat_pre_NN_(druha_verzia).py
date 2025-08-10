# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Upraveny kod pre upravu dat, ktore su pouzivane ako vstup do generatora pre trenovanie NN sieti.
Trieda SpajanieDat spaja data stiahnute z TWS a data pre OHLC. Je to z dovodu, ze pre prve data 
nebolo stahovane ohlc. Ale bola stahovana iba priemerna cena dat. Preto ohlc boli dodatocne
stiahnute a pripojene k povodnym datam. Vystup je taky isty, ako su nasledujuce stahovane data.
Preto tato trieda nebude mat dlhodobu vyuzitelnost.
"""

import numpy as np
import pandas as pd
import os
import time
from pytz import timezone


class SpajanieDat:
  """
  Trieda spaja data TWS a data OHLC. Data z TWS neobsahovali data pre ohlc. Preto OHLC boli 
  stiahnute separatne a touto triedou su pripojene k datam z TWS. Vystup z tejto triedy bude
  identicky ako budu stahovane data z TWS neskor. Teda, data z tejto triedy a data z buduceho
  stahovania TWS budu identicke.
  Postup pri spajani dat je:
    Nacitava data zo zloziek TWS a OHLC stiahnute a spaja ich dokopy. Ulozene su do zlozky
    Spojene data (OHLC a TWS). Niekedy je zlozka OHLC stiahnute presunuta na plochu. Je to 
    z dovodu, lebo je velka. Tak ju potom treba bud vratit do dropboxu, alebo upravit cestu
    ku zlozke tu v triede.
  """
  def __init__(self):
    """
    Arguments
    ---------
    burzy:  vsetky burzy pre ktore su dostupne data. V pripade potreby, je mozne zmensit pocet burz iba
            na potrebne burzy. Vsetky vypocty su realizovane cez funkciu. Teda, upravit argumenty je
            mozne aj po inicializacii triedy.
    cestaTWS, cestaOHLC, cesta_spojenie_data:
            toto su cesty pre dane data, alebo pre ulozenie dat
    datumy: toto su vsetky datumy, pre ktore bude pocitane spajanie
    """
    self.burzy = ['AMEX','ARCA','BATS','BEX','BYX','CHX','DRCTEDGE','EDGEA','IEX','MEMX','NYSE','PSX','SMART','PEARL','ISLAND']
    self.cestaTWS  = '/home/marek/Dropbox/Data/TWS/'
    self.cestaOHLC = '/home/marek/Dropbox/Data/OHLC stiahnute/'
    self.cesta_spojene_data = '/home/marek/Dropbox/Data/Spojene data (OHLC a TWS)/'
    self.datumy    = os.listdir(self.cestaTWS)
    self.datumy.sort()
  
  def zluc_data(self):
    """
    Zluci data z TWS a OHLC do jedneho celku a ulozi ich do suboru. Data su ulozene ako csv subor, kde su udane 
    aj stlpce.
    """
    for i in self.datumy:
      os.mkdir(self.cesta_spojene_data+i)
      for j in self.burzy:
        ohlc = np.load(self.cestaOHLC+i+'/'+'AMD_'+j+'.npy')
        tws  = np.load(self.cestaTWS+i+'/'+'AMD_'+j+'.npy')
        
        ohlc = pd.DataFrame(ohlc, columns=['time','open','high','low','close','vol'])
        ohlc['time'] = ohlc['time'].astype('float')
        ohlc = ohlc.drop_duplicates('time', ignore_index=True)
        ohlc.reset_index(drop=True)
        ohlc = ohlc.sort_values(by='time', ignore_index=True)
        
        data = pd.DataFrame(tws[1:,1:], columns=['time','wap','vol','count'])
        data = data.drop_duplicates('time', ignore_index=True)
        data = data.sort_values(by='time', ignore_index=True)
        data = data[data['wap']>20]
        data.reset_index(drop=True)
        data = pd.merge(ohlc[['time','open','high','low','close']], data, how='inner', on='time')
        data['time'] = pd.to_datetime(data['time'], unit='s')
        date = str(data['time'][0])[:11]
        mask = ((data['time'] >= pd.Timestamp(date+'15:30:00')) & (data['time'] <= pd.Timestamp(date+'22:00:00')))
        data = data[mask]
        data['time'] = data['time'].apply(lambda x: int(x.timestamp()))
        data.to_csv(self.cesta_spojene_data+i+'/'+'AMD_'+j+'.csv', index=False)


class UpravaDat:
  """
  Uprava dat nadvezuje na prvu upravu dat. Tu boli data rozsirene o OHLC a aj kod je priblizne
  pisany na urychlenie nacitavania dat. Ale samotne data kopiruju povodny kod (povodnu upravu).
  """
  def __init__(self):
    """
    Atributs
    --------
    path_data: str
      Cesta ku datam
    datumy: list
      Vsetky datumy, pre ktore su ulozene data
    burzy: list
      Burzy, pre ktore sa budu pocitat data. V stiahnutych data su nasledovne burzy, ktorych sa potom 
      mozu vybrat tie, ktore budu zaujimave pre trenovanie, alebo blizsie skumanie:
      AMEX, ARCA, BATS, BEX, BYX, CHX, DRCTEDGE, EDGEA, IEX, MEMX, NYSE, PSX, SMART, PEARL, ISLAND
    ohlc: DataFrame
      Denne ohlc, ktore je pouzite pri uprave dat. je to z dovodu, ze nie su stiahnute vsetky 
      obchodne dni. Teda nie su obchodne dni v poradi, tak ako idu. Preto sa nedalo vycitat 
      zo stiahnutych dat (min, max, close) predchadzajuce hotnoty.
    volume: dict
      Volume je vypocitane nasledovne. Su zoradne stlpce a potom som zobral poslednych 400 
      najvacsich hodnot. Je to priblizne parovane ako som mal hodnoty pre pat burz, ktore su
      vykreslene do grafov. V pripade potreby je mozne hodnotu 400 zmenit na nejaku inu. 
    count: dict
      Count je vypocitane nasledovne. Su zoradne stlpce a potom som zobral poslednych 400 
      najvacsich hodnot. Je to priblizne parovane ako som mal hodnoty pre pat burz, ktore su
      vykreslene do grafov. V pripade potreby je mozne hodnotu 400 zmenit na nejaku inu. 
    mov_av: int
      Moving average. Hodnota je stanovena pre lookback 200. V pripade, ze sa lookback budd menit
      tak je potrebne zmenit aj hodnotu movving average.
    """
    self.path_data = '/home/marek/Dropbox/Data/Spojene data (OHLC a TWS)/'
    self.datumy    = self.__zorad_datumy()
    self.burzy = ['AMEX','ARCA','BATS','BEX','BYX','CHX','DRCTEDGE','EDGEA','IEX','MEMX','NYSE','PSX','SMART','PEARL','ISLAND']
    self.ohlc  = pd.read_csv('/home/marek/Dropbox/Data/OHLC/AMD.csv')
    self.volume = {'AMEvo':13,'ARCvo':170,'BATvo':100,'BEXvo':15,'BYXvo':20,'CHXvo':11,'DRCvo':260,'EDGvo':25,'IEXvo':60,'MEMvo':70,'NYSvo':55,'PSXvo':20,'SMAvo':1300,'PEAvo':17,'ISLvo':500}
    self.count  = {'AMEco':13,'ARCco':170,'BATco':100,'BEXco':15,'BYXco':20,'CHXco':11,'DRCco':260,'EDGco':25,'IEXco':60,'MEMco':70,'NYSco':55,'PSXco':20,'SMAco':1300,'PEAco':17,'ISLco':500}
    self.mov_av = 40
    print('Pozor! Hodnota mov_av je stanovena pre lookback 200. V pripade zmeny lookback je potrebne mov_av prisposobit.')
  
  def __zorad_datumy(self):
    """
    Zoraduje datumy. Lebo v konstruktore sa to nedalo zrealizovat.
    """
    datumy = os.listdir(self.path_data)
    datumy.sort()
    return(datumy)
  
  def nacitaj_a_spoj_burzy_za_jeden_den(self,datum):
    """
    Nacitava burzy z jedneho dna a spaja ich horizontalne do jedneho DataFramu.
    
    Parameters
    ----------
    datum: str
      Je to nazov zlozky, z ktorej chcem nacitavat den.
    
    Returns
    -------
    data: DataFrame
      Je to uz upraveny a orezany dataframe.
    
    Examples
    --------
    >>> nacitaj_a_spoj_burzy_za_jeden_den('2023_01_19')
    """
    data = pd.read_csv(self.path_data+datum+'/AMD_'+self.burzy[0]+'.csv')
    data.columns = ['time', self.burzy[0][:3]+'o', self.burzy[0][:3]+'h', self.burzy[0][:3]+'l', self.burzy[0][:3]+'c', self.burzy[0][:3]+'wa', self.burzy[0][:3]+'vo', self.burzy[0][:3]+'co']
    data.sort_values(by='time', ignore_index=True)
    
    # Horizontalne spajanie burz v jednom dni
    for i in self.burzy[1:]:
      dt = pd.read_csv(self.path_data+datum+'/AMD_'+i+'.csv')
      dt.columns = ['time', i[:3]+'o', i[:3]+'h', i[:3]+'l', i[:3]+'c', i[:3]+'wa', i[:3]+'vo', i[:3]+'co']
      dt.sort_values(by='time', ignore_index=True)
      data = pd.merge(data, dt, how='outer', on='time')
    
    data = data.sort_values(by='time', ignore_index=True)
    data = data.drop_duplicates('time', ignore_index=True)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    
    # Nahradzanie NAN hodnot pre stlpce volume a count (vo, co). Nan hodnoty su vyplnane ako 0.
    for i in [x[:3]+'vo' for x in self.burzy], [x[:3]+'co' for x in self.burzy]:
      data[i] = data[i].fillna(0)
    
    # Nahradzanie NAN hodnoty v SMAo. Niekde nie su stiahnute data pre ohlc. To je nahradene nan hodnotou.
    # Preto je potrebne tuto hodnotu nahradit najblizsou hodnotou. Toto nahradenie je z dovodu, ze SMAo
    # sa pouziva na vyplnenie ostatnych nan hodnot v datach. JE to kod dolu.
    data['SMAo']  = data['SMAo'].fillna(method='ffill').fillna(method='bfill')
    data['SMAh']  = data['SMAh'].fillna(method='ffill').fillna(method='bfill')
    data['SMAl']  = data['SMAl'].fillna(method='ffill').fillna(method='bfill')
    data['SMAc']  = data['SMAc'].fillna(method='ffill').fillna(method='bfill')
    data['SMAwa'] = data['SMAwa'].fillna(method='ffill').fillna(method='bfill')
    
    # Nahradzanie NAN hodhot pre stlpce ohlc a wa. Ohlc a wa stlpce su nahradzane hodnotou SMAo.
    # Hodnota SMAo je dana preto, lebo bude vzdy k dispozicii. Lebo je stahovana z historickych dat
    # a burza SMART je stale v plnom rozsahu obchodnych hodin.
    for i in [x[:3]+'o' for x in self.burzy]:
      index = data[data[i].isna()].index
      data.loc[index,i[:3]+'o'] = data['SMAo'][index]
      data.loc[index,i[:3]+'h'] = data['SMAo'][index]
      data.loc[index,i[:3]+'l'] = data['SMAo'][index]
      data.loc[index,i[:3]+'c'] = data['SMAo'][index]
      data.loc[index,i[:3]+'wa']= data['SMAo'][index]
    
    return(data)
  
  def spoj_data_do_celku(self):
    """
    Vertikalne spajanie dat zo vsetkych datumov.
    
    Returns
    -------
    data: Dataframe
      Je to spojeny dataframe zo vsetkych obchodnych dni.
    """
    data = self.nacitaj_a_spoj_burzy_za_jeden_den(self.datumy[0])
    
    for i in self.datumy[1:]:
      d = self.nacitaj_a_spoj_burzy_za_jeden_den(i)
      data = pd.concat([data,d], ignore_index=True)
    
    return(data)
  
  def pridaj_odober_stlpce(self):
    """
    Pridavaju a odoberaju sa stlpce.
    
    Returns
    -------
    data: DataFrame
    """
    data = self.spoj_data_do_celku()
    
    # Doplnenie stlpcov H,M,S (hodiny, minuty, sekundy)
    data.insert(1,'second',None)
    data.insert(1,'minute',None)
    data.insert(1,'hour',None)
    data.second = data.time.apply(lambda x: x.second)
    data.minute = data.time.apply(lambda x: x.minute)
    data.hour   = data.time.apply(lambda x: x.hour)
    
    # Doplnenie stlpcov pre min, max ceny v predchadzajucom obchodnom dni. A uzatvaraciu cenu
    # v predchadzajucom obchodnom dni. Toto su hlavne oporne hranice, ktore sa kreslia pri 
    # day tradingu.
    data.insert(4,'uzavretie',None)
    data.insert(4,'max',None)
    data.insert(4,'min',None)
    
    start = ' 01:00:00' # Pozor medzery. Pred hodinou musi ostat medzera, lebo pri spajani by sa to zlucilo.
    end   = ' 23:00:00' # Pozor medzery. Pred hodinou musi ostat medzera, lebo pri spajani by sa to zlucilo.
    
    for i in self.datumy:
      datum = i.replace('_','-')
      st    = pd.Timestamp(datum+start) # start v novom cykle
      en    = pd.Timestamp(datum+end)   # end v novom cykle
      mask  = (data.time >= st) & (data.time <= en)
      
      # Hladam index v ohlc pre tento den.
      index = self.ohlc[self.ohlc['Date'] == i.replace('_','-')].index[0]
      
      # Hodnoty min, max, close, budu zadavane uz z predchadzajuceho obchodneho dna. Teda je to index-1.
      _min  = (self.ohlc.loc[index-1,'Low']).__round__(4)
      _max  = (self.ohlc.loc[index-1,'High']).__round__(4)
      close = (self.ohlc.loc[index-1,'Close']).__round__(4)
      data.loc[mask,['min','max','uzavretie']] = [_min, _max, close]
    
    # Doplnenie stlpca "MA" moving average. MA bude pocitana ako desatina z dlzky lookback.
    data.insert(7,'EMA',None)
    
    return(data)
  
  def normalizuj_data(self):
    """
    Normalizuje data do intervalu [0,1], alebo do co najvacsej tesnosti k intervalu [0,1]. 
    Jednotlive stlpce, ktore su rovnake v kazdej burze, su dane ako samostatny list, aby 
    to bolo mozne lahsie upravovat v pripade potreby zmenit nejaku hodnotu, ktora je 
    zodpovedna za normalizovanie.
    
    Returns
    -------
    data: DataFrame
    """
    
    data = self.pridaj_odober_stlpce()
    
    # hms (hoidna, minuta, sekunda)
    dhms = {'hour':24, 'minute':60, 'second':60}
    for i in dhms:
      data[i] = data[i]/dhms[i]
      data[i] = data[i].apply(lambda x: x.__round__(3))
    
    # Volume je vypocitane nasledovne. Su zoradne stlpce a potom som zobral poslednych 400 
    # najvacsich hodnot. Je to priblizne parovane ako som mal hodnoty pre pat burz, ktore su
    # vykreslene do grafov. V pripade potreby je mozne hodnotu 400 zmenit na nejaku inu. Len pre
    # ukazku:
    #   for i in [x[:3]+'v' for x in  self.burzy]:
    #     print( '{}: {}'.format(i, int(np.mean(sorted(data[i])[-400:]))))
    # 
    # >>> AMEv: 13
    # >>> ARCv: 169
    # >>> BATv: 98
    # >>> BEXv: 15
    # ...
    for i in self.burzy:
      burza = i[:3]+'vo'
      data[burza] = data[burza]/self.volume[burza]
      data[burza] = data[burza].apply(lambda x: x.__round__(6))
    
    # Pocet obchodov je totozne s volume. Je predpoklad, ze pocet obchodov je rovnaky ako je volume. 
    # Iba v par pripadoch su zrealizovane velke bolokove objednavky.
    for i in self.count:
      burza = i[:3]+'co'
      data[burza] = data[burza]/self.count[burza]
      data[burza] = data[burza].apply(lambda x: x.__round__(6))
    
    # Uprava vsetkych cien burz, ktore sa vztahuju ku burze SMART. Burza SMART sa berie ako referencka
    # burza, od ktorej sa odrazaju ostatne burzy. Predpoklad je, ze pri predaji, alebo nakupe sa 
    # preferuje burza ktora ma mensiu cenu, alebo vacsiu cenu ako burza SMART. To zalezi od toho,
    # ci cena akcie stupa, alebo klesa. Zoberme burzu ISLAND. Teda vsetky ceny pre ISLAND budu
    # ako SMART-ISLAND. A toto bude platiti pre kazdu dalsiu burzu. 
    burzy_bez_SMART = self.burzy
    burzy_bez_SMART.remove('SMART')
    for i in burzy_bez_SMART:
      burza = i[:3]+'wa'
      data[burza] = data[burza] - data['SMAwa']
      data[burza] = data[burza].apply(lambda x: x.__round__(6))
    
    # Uprava min, max, uzavretie. Hlavne nastavenie je vo funkcii pridaj_odober_stlpce(). Tam su dane
    # hlavne ceny z cenoveho grafu. V tomto kroku bude od cien odcitana hodnota SMAc. Je to z dovodu,
    # aby graf nebol viazany na cenu akcie, ale aby boli reflektovane iba cenove pohyby v ramci dna.
    # Ceny min, max, uzavretie su hlavne hladiny, ktore sa klasicky kreslia pre day tradingu.
    # Upravy budu nasledovne min-SMAwa, max-SMAwa, uzavretie-SMAwa.
    data['min'] = data['min'] - data['SMAwa']
    data['max'] = data['max'] - data['SMAwa']
    data['uzavretie'] = data['uzavretie'] - data['SMAwa']
    data['min'] = data['min'].apply(lambda x: x.__round__(6))
    data['max'] = data['max'].apply(lambda x: x.__round__(6))
    data['uzavretie'] = data['uzavretie'].apply(lambda x: x.__round__(6))
    
    # Uprava ceny pre burzu SMART
    # Cena. Ako referencna miera sa berie cena z burzy SMART. Je to zakladna burza pre InteractiveBrokers.
    # Aby nebola cena viazana na hodnoty "skutocnu cenu akcie", tak je upravena tak, ze cena sa vyvyja
    # od otvaracej ceny v danom obchodnom dni. Cena v kazdom dni je viazana iba na otvorenie burzy.
    start = ' 01:00:00' # Pozor medzery. Pred hodinou musi ostat medzera, lebo pri spajani by sa to zlucilo.
    end   = ' 23:00:00' # Pozor medzery. Pred hodinou musi ostat medzera, lebo pri spajani by sa to zlucilo.
    for i in self.datumy:
      datum = i.replace('_','-')
      st    = pd.Timestamp(datum+start) # start v novom cykle
      en    = pd.Timestamp(datum+end)   # end v novom cykle
      mask  = (data.time >= st) & (data.time <= en)
      otvaracia_cena = float(data[mask]['SMAwa'][:1]) # otvaracia cena v novom dni
      data.loc[mask,'SMAwa'] = data[mask]['SMAwa'].apply(lambda x: x-otvaracia_cena)
      data.loc[mask,'SMAwa'] = data[mask]['SMAwa'].apply(lambda x: x.__round__(6))

    # Uprava hodnoty pre 'MA'. Stlpec 'MA' bol vytvoreny vo funkcii __pridaj_odober_stlpce(). Hodnota "MA"
    # je tvorena ako klzavy priemer. Hodnota okna pre klzavy priemer sa berie ako desatina z lookback.
    # Najskor sa vypocita klzavy priemer a potom sa hodnota MA obpocita od SMAc
    k  = 2/(self.mov_av+1) # Toto je parameter zo vzorca
    k1 = 1-k               # Toto je parameter zo vzorca
    
    data.loc[:self.mov_av,'EMA'] = data.loc[:self.mov_av,'SMAwa']
    
    for i in range(self.mov_av+1, data.shape[0]):
      data.loc[i,'EMA'] = (data.loc[i,'SMAwa']*k + data.loc[(i-1),'EMA']*k1)
    
    data['EMA'] = data['EMA'] - data['SMAwa'] # Odcitanie ceny burzy od klzaveho priemeru
    data['EMA'] = data['EMA'].apply(lambda x: x.__round__(6))
    
    # Odstranenie stlpca time
    # del(data['time'])
    
    return(data)




# spajanieDat = SpajanieDat()
# spajanieDat.zluc_data()

upravaDat = UpravaDat()
dt = upravaDat.normalizuj_data()
dt

View(dt)


import matplotlib.pyplot as plt

a=dt['SMAwa'][:500]
b=dt['EMA'][:500]
c=range(500)

plt.clf()
plt.plot(c,a)
plt.plot(c,b)
plt.show()
















