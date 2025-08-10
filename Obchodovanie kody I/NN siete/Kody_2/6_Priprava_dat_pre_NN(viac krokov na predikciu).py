# priprava dat pre trenovanie NN sieti. Je to kod kopirujuci predchadzajuce funkcie. Ale je tu rozdiel,
# lebo tu sa dokaze urcit, ktore data sa budu upravovat 1,2,5,10, min.

import numpy as np
import pandas as pd
import os
from datetime import timedelta


class Priprava_dat:
  def __init__(self, tick):
    """
    Parameters
    ----------
    tick: int
      Urcuje, aky tick sa pouzije v datach, napriklad (1,2,5,10, atd. ...)
    
    Atributs
    --------
    burzy
    path
    tick: int
      Vo vysledku sa to premiena na str. Je to z dovodu, ze castejsie sa toto pouziva ako sucast
      cesty do zlozky.
    pocet: dict
      Zobrazuje pocet tickov v jednom obchodnom dni pre dany casovy ramec.
    """
    self.burzy  = ['ARCA','BATS','DRCTEDGE','IEX','NYSE','SMART','ISLAND']
    self.path   = '/media/marek/zaloha/Data/OHLC_TWS/AMD/'
    self.tick   = str(tick)+'m/'
    self.datumy = self.__nacitaj_datumy()
    self.pocet  = {'1m/':390, '2m/':195, '5m/':78, '10m/':39}
    
  def __nacitaj_datumy(self):
    datumy = os.listdir(self.path+self.tick)
    datumy.sort()
    return datumy
  
  def __nacitaj_obchodny_den(self, datum):
    """
    Nacitava sa den z uvedeneho datumu. Najskor sa nacitava vsetko pre burzu SMART. A potom
    ku datam sa pridavaju uz iba hodnoty volume pre ostatne burzy.
    
    Parameters
    ----------
    datum: str, napriklad '2021_01_04'
    """
    def uprav_na_typ(data,burza):
      """
      Upravuje typ dat v stlpcoch. Str prevadza na datetime alebo na int.
      Funkcia je pouzita iba v cykle for.
      """
      data['time'] = pd.to_datetime(data['time'])
      data[burza] = data[burza].astype('float')
      return data
    
    def skontroluj_cas_otvorenia(otvorenie_smart,data):
      """
      Kontroluje cas, ci je rovnaky ako je cas pre burzu SMART. Lebo niektore burzy maju posunuty
      cas aj o hodinu. Preto ho treba zarovnat s burzou SMART. Taktiez je potrebne brat v uvahu,
      za sa moze menit cas (letny, zimny). Preto sa neda orientovat iba jednyn casom 15:30 - 22:00.
      Ale treba brat v uvahu, ked europa a amerika maju dva tyzdne v roku nie rovnaky letny alebo
      zimny cas.
      """
      otvorenie_burza = data['time'][0]
      if otvorenie_burza >= otvorenie_smart+timedelta(hours=1):
        data['time'] = data['time']-timedelta(hours=1)
      
      return data
    
    path = self.path+self.tick+datum
    data = np.load(path+'/SMART.npy')
    data = pd.DataFrame(data[:,:-1], columns=['time','o','h','l','c'])
    
    # Prevedenie time na datatime a ostatne data na float
    data['time'] = pd.to_datetime(data['time'])
    data['o'] = data['o'].astype('float')
    data['h'] = data['h'].astype('float')
    data['l'] = data['l'].astype('float')
    data['c'] = data['c'].astype('float')
    otvorenie_smart = data['time'][0] #Toto sluzi na porovnanie otvaracieho casu pre ostatne burzy 
    data['c'] = data['c'].fillna(0) 
    
    # Testovanie, ci je cena vyzsia ako 0. Lebo v jednom datume to tak bolo
    if min(data['c']) < 10:
      print('cena akcie je mensia ako 10')
      return None
    
    # Pripajanie stlpcov s volume k datam.
    for i in self.burzy:
      dt = np.load(self.path+self.tick+datum+'/'+i+'.npy')
      dt = pd.DataFrame(dt[:,[0,5]], columns=['time',i])
      dt = uprav_na_typ(dt,i)
      dt = skontroluj_cas_otvorenia(otvorenie_smart, dt)
      data = pd.merge(data,dt, how='left', on='time')
    
    data = data.fillna(0)
    key  = data.keys()
    # Toto je posunutie dat nahor o dany tick. Je to z dovodu, ze data zacinali uz od 15:30:00. A to nie je
    # pravda. Lebo sviecka sa vyvija a ukoncuje na konci casoveho kroku. A nie na zaciatku. Preto je to 
    # posunute vsetko o dany tick.
    data.time = data.time+timedelta(minutes=int(self.tick[:self.tick.index('m')]))
    return data
  
  def __spoj_dni(self):
    """
    Spaja vsetko do jedneho dataframu.
    """
    data = self.__nacitaj_obchodny_den(self.datumy[0]) # nacitanie prveho dna
    dni = []
    for i in self.datumy[1:]:
      d = self.__nacitaj_obchodny_den(i)
      data = pd.concat([data,d], ignore_index=True)
      data = data.reset_index(drop=True, inplace=False)
    return data
  
  def __dopln_min_max_predch_dna(self):
    """
    Doplna min, max, close predchadzajuceho dna. Su to zakladne klasicke hladiny, ktore 
    sa kreslia este pred zacatim obchodneho dna. Ale stlpce min, max, close sa odpocitavaju
    od otvaracej ceny. Je to z dovodu, aby to nebolo zavisle na cene akcie, ale len na 
    vyvoji ceny cez den.
    """
    data = self.__spoj_dni()
    data.insert(data.shape[1],'min',0)
    data.insert(data.shape[1],'max',0)
    data.insert(data.shape[1],'close',0)
    
    # Vytiahnutie dat z prveho dna. A tento den sa vo vypoctoch aj tak nebude pouzivat, lebo 
    # v trenovani sa zacina az druhym dnom.
    for i in self.datumy[1:]:
      datum = pd.to_datetime(i.replace('_',''))
      mask = ((data['time'] > datum) & (data['time'] < datum+timedelta(days=1))) # dnesny den
      index = data[mask].index              # dnesny den
      index1= index - self.pocet[self.tick] # predchadzajuci den. Odcitanie preto, lebo datumy nejdu zaradom. Su aj sviatky.
      _close= data['c'][index[0]-1]
      _min  = data['c'][index1].min()
      _max  = data['c'][index1].max()
      
      data.loc[index,'close'] = data.loc[index,'o'] - _close
      data.loc[index,'min']   = data.loc[index,'o'] - _min
      data.loc[index,'max']   = data.loc[index,'o'] - _max
    return data
  
  def __dopln_predikciu(self):
    """
    Doplna stlpec, do ktoreho budu ulozene data, ktore budu sluzit ako data na predikciu.
    Doplnam este jeden stlpec na predikciu dvoch casovych krokov.
    """
    data = self.__dopln_min_max_predch_dna()
    data.insert(data.shape[1],'co1',0)
    data.insert(data.shape[1],'co2',0)
    
    for i in self.datumy[1:]:
      datum = pd.to_datetime(i.replace('_',''))
      mask = ((data['time'] > datum) & (data['time'] < datum+timedelta(days=1)))
      index = data[mask].index
      
      data.loc[index[:-1],'co1'] = data.loc[index[1:],'o'].to_numpy()
      data.loc[index[-1],'co1'] = data.loc[index[-1],'c']
      
      data.loc[index[:-2],'co2'] = data.loc[index[2:],'o'].to_numpy()
      data.loc[index[-2],'co2'] = data.loc[index[-2],'c']
      data.loc[index[-1],'co2'] = data.loc[index[-1],'c']
    return data
  
  def __uprav_ohlc(self):
    """
    V ohlc sa upravuju stlpce samostatne. Najskor sa upravuju hlc. Tie reprezentuju 
    samotnu sviecku. To znamena ze 'h' a 'l' su knoty a 'c' reprezentuje velkost
    tela sviecky. 'o' reprezentuje relativnu cenu v priebehu dna. Teda, zacina od
    nuly a postupne sa vyvyja tak, ako rastie/klesa cena akcie.
    """
    data = self.__dopln_predikciu()
    for i in range(data.shape[0]):
      if data.loc[i,'o'] <= data.loc[i,'c']:
        data.loc[i,'h'] = data.loc[i,'h'] - data.loc[i,'c']
        data.loc[i,'l'] = data.loc[i,'o'] - data.loc[i,'l']
        data.loc[i,'c'] = data.loc[i,'c'] - data.loc[i,'o']
      else:
        data.loc[i,'h'] = data.loc[i,'h'] - data.loc[i,'o']
        data.loc[i,'l'] = data.loc[i,'c'] - data.loc[i,'l']
        data.loc[i,'c'] = data.loc[i,'c'] - data.loc[i,'o']
    
    for i in self.datumy:
      datum = pd.to_datetime(i.replace('_',''))
      mask = ((data['time'] > datum) & (data['time'] < datum+timedelta(days=1)))
      index = data[mask].index
      _open = data['o'][index[0]]
      
      for co in ['co1','co2']:
        data.loc[index,co] = data.loc[index,co] - _open
        data.loc[index[:1],co] = 0
        data.loc[index[-1],co] = data.loc[index[-2],co]
      
      data.loc[index,'o'] = data.loc[index,'o'] - _open
      data.loc[index[0],'o'] = 0
    
    datum = pd.to_datetime(self.datumy[0].replace('_',''))
    mask = ((data['time'] > datum) & (data['time'] < datum+timedelta(days=1)))
    index = data[mask].index
    data.loc[index,'co1'] = 0
    data.loc[index,'co2'] = 0
    
    return data
  
  def __dopln_hm(self):
    """
    Doplnaju sa stlpce h,m (hodiny, minuty). Je to vybrate zo stlpca time. A potom je
    stlpec time odstraneny. Hodnoty h,m su potom normalizovane.
    """
    data = self.__uprav_ohlc()
    
    data.insert(1,'minute',None)
    data.insert(1,'hour',None)
    
    data['minute'] = data['time'].apply(lambda x: (x.minute)/60) # Hned to aj normalizujem
    data['hour']   = data['time'].apply(lambda x: (x.hour)/24)   # Hned to aj normalizujem
    
    del(data['time']) # Odstranenie time. Uz tento stlpec nebude potrebny.
    return data
  
  def __normalizuj_volume(self):
    """
    Normalizacia je realizovana predelenim maximalnej hodnoty pre danu burzu.
    """
    data = self.__dopln_hm()
    volume = {x:int(data[x].max()) for x in self.burzy}
    
    for i in volume:
      data[i] = data[i]/volume[i]
    
    return data
  
  def dodaj_data(self):
    data = self.__normalizuj_volume()
    return data 



priprava = Priprava_dat(5)
data = priprava.dodaj_data()
data.to_csv('/home/marek/Data/AMD/5m/5m_dva_kroky.csv', index=False)

















