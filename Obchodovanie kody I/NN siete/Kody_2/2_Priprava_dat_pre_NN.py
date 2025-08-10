# Priprava dat pre trenovanie NN sieti. Cena akcie sa prevadza na relativnu cenu
# v ramci dna. Preto nie je viazana na momentalnu cenu akcie, ale iba na relativny
# pohyb v ramci dna.

import numpy as np
import pandas as pd
import os
from datetime import timedelta
path = '/media/marek/zaloha/Data/OHLC_TWS/AMD/1m/'


class Priprava_dat_pre_NN:
  """
  Pripravuje data pre trenovanie NN sieti.
  """
  def __init__(self,path):
    """
    Parameters
    ----------
    path = str
      Cesta ku datam
    
    Atributs
    ----------
    datumy = list
      Vsetky datumy, pre ktore su k dispozicii data.
    burzy  = list
      Vsetky burzy pre ktore su stiahnute data.
    path_data = str
      Cesta ku datam
    path_ohlc = str
      Cesta ku suboru .csv v ktorom su ulozene denne ohlc udaje.
    """
    self.burzy  = ['ARCA','BATS','DRCTEDGE','IEX','NYSE','SMART','ISLAND']
    self.path_data = path
    self.datumy = self.__nacitaj_datumy()
  
  def __nacitaj_datumy(self):
    """
    Data su stale ulozene na rovnakom mieste na disku. Odtial sa nacitavaju vsetky udaje.
    
    Returns
    -------
    datumy: list
      Zoznam vsetkych datumov, pre ktore su stiahnute data.
    """
    datumy = os.listdir(self.path_data)
    datumy.sort()
    datumy1 = datumy.copy()
    # Odstranovanie datumov, ktore nemaju uplne data v jednotlivych burzach. Ak nebude mat
    # nejaka burza uplne data, tak sa cely datum vyhodi prec.
    for i in datumy:
      for j in self.burzy:
        if os.path.getsize(self.path_data+'/'+i+'/'+j+'.npy') < 200: 
          datumy1.remove(i)
    
    rozdiel = [x for x in datumy if x not in datumy1]
    print('boli odstranene datumy:')
    for x in rozdiel:
      print(x)
    print('V pripade, ze by boli odstranene datumy mimo poradia')
    print('tak je potrebne prehodnotit tieto data kvoli trenovaniu gapu')
    
    return(datumy1)
  
  def __nacitaj_data_pre_obchodny_den(self, datum):
    """
    Nacitava sa den z uvedeneho datumu. Najskor sa nacitava vsetko pre burzu SMART. A potom
    ku datam sa pridavaju uz iba hodnoty volume pre ostatne burzy.
    
    Parameters
    ----------
    datum: str
      Je to jeden konkrety datum, pre ktory sa budu nacitavat data.
    
    Returns
    -------
    data: DataFrame
      Je to dataframe v ktorom su spojene data zo vsetkych burz do jedneho celku.
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
    
    try:
      # Osetrenie ci su k dispozicii nejake data. Ak je prazdne pole tak vyhodi vynimku.
      path = self.path_data+datum
      data = np.load(path+'/SMART.npy')
      data = pd.DataFrame(data[:,:-1], columns=['time','o','h','l','c'])
    except Exception as e:
      print('nenacitany datum: {}'.format(datum))
      print(e)
      return None
    
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
      return(None)
    
    # Pripajanie stlpcov s volume k datam.
    for i in self.burzy:
      try:
        dt = np.load(self.path_data+datum+'/'+i+'.npy')
        dt = pd.DataFrame(dt[:,[0,5]], columns=['time',i])
      except Exception as e:
        return None
      
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
    def nacitaj_prvy_den():
      for x in self.datumy:
        data = self.__nacitaj_data_pre_obchodny_den(x)
        if data is not None:
          return self.datumy.index(x)
    
    index = nacitaj_prvy_den()
    data = self.__nacitaj_data_pre_obchodny_den(self.datumy[index])
    
    for i in self.datumy[index+1:]:
      d = self.__nacitaj_data_pre_obchodny_den(i)
      data = pd.concat([data,d], ignore_index=True)
    # Odstranenie nulovych hodnot zo stlpca 'c'
    data = data[data['c'] > 0]
    data = data.reset_index(drop=True, inplace=False)
    
    return(data)
  
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
      index = data[mask].index # dnesny den
      index1= index - 390      # predchadzajuci den. Odcitanie preto, lebo datumy nejdu zaradom. Su aj sviatky.
      _close= data['c'][index[0]-1]
      _min  = data['c'][index1].min()
      _max  = data['c'][index1].max()
      
      data.loc[index,'close'] = data.loc[index,'o'] - _close
      data.loc[index,'min']   = data.loc[index,'o'] - _min
      data.loc[index,'max']   = data.loc[index,'o'] - _max
      
    return data
  
  def __dopln_predikciu(self):
    """
    Doplna sa stlpec, do ktoreho budu ulozene data, ktore budu sluzit ako data
    ktore sa chcu predikovat.
    """
    data = self.__dopln_min_max_predch_dna()
    data.insert(data.shape[1],'co',0)
    
    for i in self.datumy[:-1]:
      datum = pd.to_datetime(i.replace('_',''))
      mask = ((data['time'] > datum) & (data['time'] < datum+timedelta(days=1)))
      index = data[mask].index
      _open = data['o'][index[-1]+1]
      data.loc[index, 'co'] = _open - data['c'][index[-1]]
 
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
      # Niektore datumy nebudu v datach. Preto budu mat index 0. A ak maju nulovy index
      # potom vyhadzuje vynimku.
      try:
        _open = data['o'][index[0]]
        data.loc[index, 'o'] = data.loc[index,'o'] - _open
      except Exception:
        print('vynimka v uprav ohlc')
    
    return(data)
  
  def __dopln_hms(self):
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
    """
    Normalizacia je realizovana predelenim maximalnej hodnoty pre danu burzu.
    """
    data = self.__dopln_hms()
    volume = {x:int(data[x].max()) for x in self.burzy}
    
    for i in volume:
      data[i] = data[i]/volume[i]
    
    return(data)
  
  def dodaj_data(self):
    data = self.__normalizuj_volume()
    return(data)


priprava = Priprava_dat_pre_NN(path)
data = priprava.dodaj_data()
data.to_csv('/home/marek/Data/AMD/1m/1m.csv', index=False)
































  
