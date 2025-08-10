import numpy as np
import pandas as pd

burzy = ['AMEX','ARCA','BATS','BEX','BYX','CHX','DRCTEDGE','EDGEA','IEX','MEMX','NYSE','PSX','SMART','PEARL','ISLAND']
burzy2 = ['AMEX','BATS','BEX','BYX','CHX','EDGEA','IEX','MEMX','NYSE','PSX','PEARL']


def nacitaj_akciu(path, akcia):
  """
  Nacitava z disku uz upravene data a prevadza ich na DataFrame.
  
  Parameters
  ----------
  path:   str, uplna cesta k suboru
  akcia:  str, nazov celej akcie (AMD, AAPL, atd... .)
  
  Returns
  -------
  data:   DataFrame
  
  Examples
  --------
  >>> nacitaj_akciu('/home/marek/Dropbox/Data/TWS/', 'AMD')
  """
  
  data = np.load(path+akcia+'_AMEX.npy')
  data = pd.DataFrame(data[:,[1,2,3,4]], columns=['time','AMEc','AMEv','AMEw'])
  data['time'] = data['time'].astype('int')
  data = data.drop(0, axis=0)
  data = data[data.time >1]
  data = data.drop_duplicates(subset=['time'], ignore_index=True)
  data = data.sort_values(by='time', ignore_index=True)
  data = data.drop_duplicates(subset=['time'], ignore_index=True)
  
  for j in burzy[1:]:
    d = np.load(path+akcia+'_'+j+'.npy')
    d = pd.DataFrame(d[:,[1,2,3,4]], columns=['time',j[:3]+'c',j[:3]+'v', j[:3]+'w'])
    
    d['time'] = d['time'].astype('int')
    d = d.drop(0, axis=0)
    d = d[d.time >1]
    d = d.drop_duplicates(subset=['time'], ignore_index=True)
    d = d.sort_values(by='time', ignore_index=True)
    d = d.drop_duplicates(subset=['time'], ignore_index=True)
    
    data = pd.merge(data,d, how='outer', on='time')
    data = data.fillna(0)
    
  data = data.drop_duplicates(subset=['time'], ignore_index=True)
  data = data.sort_values(by='time', ignore_index=True)
  data.time = data.time-21600
  data.time = pd.to_datetime(data.time, unit='s')
  xx = [i[:3]+'v' for i in burzy]
  data['volume'] = data[xx].apply(sum, axis=1)
  
  return(data)


def orez_na_obchodne_hodiny(data):
  """
  Orezanie dat na interval obchodnych hodin.
  Zaroven odstranuje nulove hodnoty v cene. Lebo, niekedy sa stalo, ze sa prerusilo vlakno 
  a nezaznamenala sa cena. A potom to robilo v grafe neplechu.
  
  Parameters
  ----------
  data: DataFrame
  
  Returns
  -------
  data: DataFrame
    
  """
  
  date  = str(data.time[0])[:11]
  start = '08:30:00'
  end   = '15:00:00'
  start = pd.Timestamp(date+start)
  end   = pd.Timestamp(date+end)
  mask  = (data.time >= start) & (data.time <= end)
  data  = data[mask]
  
  for i in burzy:
    data = data.drop(labels = data[data['SMAc'] == 0].index)
  
  index = {x[1]:x[0] for x in enumerate(data.index)}
  data = data.rename(index)
  
  return(data)


def vypis_max_volume(data, datumy, burza, pocet):
  """
  Vypise najvacisie volume pre dany pocet a danu burzu. Je to na zorientovanie, ake su priemerne
  najvacsie nakupy pre danu burzu. Dany vystup sluzi na nastavenie poctu obchodov pre vykreslenie
  v grafe. Napriklad je to: vykresluj hodnoty iba nad volume 100, atd... . 
  
  Hodnoty, datumy a data su prevzate ako globalne premenne.
  
  Parameters
  ----------
  data: dict
      Je to slovnik v ktorom su ulozene aktualne data pre danu akciu
  datumy: list
      Tam su ulozene datumy, pre ktore sa to ma zobrazit. Lebo len pre niektore datumy mam vsetky data.
  burza: str, ('AMEX', 'ARCA', atd... ). Je to uplny nazov burzy. V kode sa upravy na pozadovany tvar.
  pocet: int, je to pocet prvych najvacsich obchodov.
  
  Returns
  -------
  dt: DataFrame, je to zobrazenie najvacsich obchodov podla datumu
  """
  
  datum = [x[5:] for x in datumy]
  dt = pd.DataFrame(index=np.arange(pocet), columns=datum)
  burza = burza[:3]+'v'
  
  for i in enumerate(datum, start=0):
    dt[i[1]] = data[datumy[i[0]]].iloc[data[datumy[i[0]]][burza].sort_values(ascending=False).index][burza][:pocet].to_numpy()
  return(dt)



def zluc_ostatne_burzy(data):
  """
  Zluci ostatne burzy, ktore nie su zahrnute v hlavnom zobrazovani. Nie su zahrnute z dovodu, ze maju
  male objemy v nakupoch. A ich zobrazovanie bolo zavadzajuce. Ale ked sa scitaju, tak maju jeden
  velky objem nakupov, porovnatelny so SMART, ARCA, atd... .

  Parameters
  ----------
  data: dict
    Je to slovnik, v ktorom su ulozene aktualne data pre danu akciu.

  Returns
  -------
  dt: dict
    Je to rovnaky slovnik, ako bol na vstupe, ale zmenseny o dane 'nepotrebne' burzy, ktore su zlucene
    do jednej burzy nazvanej 'ostatne'.
  """
  datumy = data.keys()
  dt = {x:data[x].copy(deep=True) for x in data.keys()}
  
  for i in datumy:
    for j in burzy2:
      del(dt[i][j[:3]+'c'])
      del(dt[i][j[:3]+'v'])
      del(dt[i][j[:3]+'w'])
  
  v = [x[:3]+'v' for x in burzy2]
  w = [x[:3]+'w' for x in burzy2]
  
  for i in datumy:
    dt[i]['OSTv'] = data[i][v].apply(sum, axis=1)
    dt[i]['OSTw'] = data[i][w].apply(sum, axis=1)
  
  return(dt)













