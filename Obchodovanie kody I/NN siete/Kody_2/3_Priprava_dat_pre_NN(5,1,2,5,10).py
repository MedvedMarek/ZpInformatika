# Priprava dat pre trenovanie NN siete. Data budu zlozene z 5s,1m,2m,5m,10m tickov.
# Spoznamkovane to nie je. Vsetky kody su prevzate priblizne z predchadzajuceho suboru,
# ktory je odkomentovany.

import numpy as np
import pandas as pd
import os
from datetime import timedelta


class Priprava_dat:
  def __init__(self,interval):
    """
    Parameters
    ----------
    interval: int
      Je to cislo, ktore reprezentuje, aky interval (tick) sa bude predikovat (1,2,5,10 minut).
      Interval je pouzity vo funkcii dopln_predikciu.
    """
    self.burzy  = ['ARCA','BATS','DRCTEDGE','IEX','NYSE','SMART','ISLAND']
    self.path   = '/media/marek/zaloha/Data/OHLC_TWS/AMD/'
    self.tick   = ['1m/','2m/','5m/','10m/']
    self.datumy = self.__nacitaj_datumy()
    self.interval = interval
  
  def __nacitaj_datumy(self):
    datumy = os.listdir(self.path+'1m/')
    datumy.sort()
    return datumy
  
  def __nacitaj_obchodny_den(self, datum, tick):
    """
    Nacitava sa den z uvedeneho datumu. Najskor sa nacitava vsetko pre burzu SMART. A potom
    ku datam sa pridavaju uz iba hodnoty volume pre ostatne burzy.
    
    Parameters
    ----------
    datum: str, napriklad '2021_01_04'
    tick: str, napriklad '1m/'
    
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
    
    path = self.path+tick+datum
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
      dt = np.load(self.path+tick+datum+'/'+i+'.npy')
      dt = pd.DataFrame(dt[:,[0,5]], columns=['time',i])
      dt = uprav_na_typ(dt,i)
      dt = skontroluj_cas_otvorenia(otvorenie_smart, dt)
      data = pd.merge(data,dt, how='left', on='time') # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    data = data.fillna(0)
    key  = data.keys()
    data.columns = [key[0]]+[i+tick[:tick.index('m')] for i in key[1:]] # pripisanie ticku do nazvu burzy
    data.time = data.time+timedelta(minutes=int(tick[:tick.index('m')]))
    return data
  
  def __spoj_ticky(self, datum):
    """
    Spaja data z tickov do jedneho celku. Tera ticky 1m,2m,5m,10m budu spojene do jedneho dataframu.
    """
    jedna_m = self.__nacitaj_obchodny_den(datum,'1m/')
    dva_m   = self.__nacitaj_obchodny_den(datum,'2m/')
    pat_m   = self.__nacitaj_obchodny_den(datum,'5m/')
    desat_m = self.__nacitaj_obchodny_den(datum,'10m/')
    
    data = pd.merge(jedna_m, dva_m, how='left', on='time')
    
    for x in [pat_m, desat_m]:
      data = pd.merge(data, x, how='left', on='time')
    
    data = data.fillna(method='ffill')
    data = data.fillna(value=0)
    
    return data
  
  def __spoj_dni(self):
    """
    Spaja vsetko do jedneho dataframu.
    """
    data = self.__spoj_ticky(self.datumy[0]) # nacitanie prveho dna
    
    for i in self.datumy[1:]:
      d = self.__spoj_ticky(i)
      data = pd.concat([data,d], ignore_index=True)
      data = data.reset_index(drop=True, inplace=False)
      data = data.drop_duplicates(ignore_index=True)
    
    return data
  
  def __dopln_predikciu(self):
    """
    Doplna stlpec, do ktoreho budu ulozene data, ktore budu sluzit ako data na predikciu.
    Na predikciu mozem pouzit rozne ticky 1,2,5,10.
    """
    data = self.__spoj_dni()
    data.insert(data.shape[1],'co',0)
    data.co = np.append(data['o'+str(self.interval)][1:].to_numpy(),0) # pripajam ku koncu nulu
    return data
  
  def __uprav_ohlc(self):
    """
    V ohlc sa upravuju stlpce samostatne. Najskor sa upravuju hlc. Tie reprezentuju 
    samotnu sviecku. To znamena ze 'h' a 'l' su knoty a 'c' reprezentuje velkost
    tela sviecky. 'o' reprezentuje relativnu cenu v priebehu dna. Teda, zacina od
    nuly a postupne sa vyvyja tak, ako rastie/klesa cena akcie.
    """
    data = self.__dopln_predikciu()
    for j in ['1','2','5','10']:
      for i in range(data.shape[0]):
        if data.loc[i,'o'+j] <= data.loc[i,'c'+j]:
          data.loc[i,'h'+j] = data.loc[i,'h'+j] - data.loc[i,'c'+j]
          data.loc[i,'l'+j] = data.loc[i,'o'+j] - data.loc[i,'l'+j]
          data.loc[i,'c'+j] = data.loc[i,'c'+j] - data.loc[i,'o'+j]
        else:
          data.loc[i,'h'+j] = data.loc[i,'h'+j] - data.loc[i,'o'+j]
          data.loc[i,'l'+j] = data.loc[i,'c'+j] - data.loc[i,'l'+j]
          data.loc[i,'c'+j] = data.loc[i,'c'+j] - data.loc[i,'o'+j]
    
    for i in self.datumy:
      datum = pd.to_datetime(i.replace('_',''))
      mask = ((data['time'] > datum) & (data['time'] < datum+timedelta(days=1)))
      index = data[mask].index
      _open = data['o1'][index[0]]
      data.loc[index,'co'] = data.loc[index,'co'] - _open
      data.loc[index[:self.interval],'co'] = 0
      data.loc[index[-1],'co'] = data.loc[index[-2],'co']
      for j in ['1','2','5','10']:
        data.loc[index,'o'+j] = data.loc[index,'o'+j] - _open
        data.loc[index[:int(j)], 'o'+j] = 0
    
    return data

  def __dopln_hms(self):
    """
    Doplnaju sa stlpce h,m,s (hodiny, minuty, sekundy). Je to vybrate zo stlpca time. A potom je
    stlpec time odstraneny. Hodnoty h,m,s su potom normalizovane.
    """
    data = self.__uprav_ohlc()

    # data.insert(1,'second',None)
    data.insert(1,'minute',None)
    data.insert(1,'hour',None)

    # data['second'] = data['time'].apply(lambda x: (x.second)/60) # Hned to aj normalizujem
    data['minute'] = data['time'].apply(lambda x: (x.minute)/60) # Hned to aj normalizujem
    data['hour']   = data['time'].apply(lambda x: (x.hour)/24)   # Hned to aj normalizujem

    del(data['time']) # Odstranenie time. Uz tento stlpec nebude potrebny.
    return data
  
  def __normalizuj_volume(self):
    """
    Normalizacia je realizovana predelenim maximalnej hodnoty pre danu burzu.
    """
    data = self.__dopln_hms()
    volume = {x+j:int(data[x+j].max()) for x in self.burzy for j in ['1','2','5','10']}
    
    for i in volume:
      data[i] = data[i]/volume[i]
    
    return data
  
  def dodaj_data(self):
    data = self.__normalizuj_volume()
    return data 



priprava = Priprava_dat(1)
data = priprava.dodaj_data()
data.to_csv('/home/marek/Data/AMD/1m/1m.csv', index=False)
View(data)










