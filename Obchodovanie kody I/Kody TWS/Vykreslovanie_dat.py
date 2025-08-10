import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import os


def najvacsie_obchody_burza(akcia, data, volume, burza, zobrazenie):
  """
  Vykresluje cenovy graf pre jednu burzu. Volume udava, aka hranica pre volume je zaujimava na
  vykreslenie.
  
  Parameters
  ----------
  akcia: str, 'AMD'
      Oznacuje, pre aku akciu sa to realizuje.
  data: DataFrame
  volume: int
      Zadava sa, od akej hranice volume sa ma vykreslit bod na grafe.
  burza: str, ('AMEX, ARCA, atd... )
      Pre aku konkretnu burzu sa to ma vykreslit.
  zobrazenie: str, ('graf', 'subor')
      Vykresluje graf do suboru, alebo na obrazovku. Ak je to do suboru, tak je to do zakladneho
      priecinku (/home/marek/grafy/)
  
  Returns
  -------
  plot: vykresleny graf. A je vykresleny bud do Rka, alebo je ulozeny do suboru 'grafy'.
  """
  burza = burza[:3]+'v'
  
  plt.clf()
  plt.figure(figsize=(36, 1440/96), layout='tight') # figure je v incoch. 1inch = 96px.
  nakup = data[burza].sort_values(ascending=False)[data[burza] >= volume]
  plt.plot(data.time, data.SMAc, color='firebrick', linewidth=0.5)
  plt.scatter(data.time[nakup.index], data.SMAc[nakup.index], color='black')
  if zobrazenie == 'graf':
    plt.tight_layout()
    plt.show()
  else:
    plt.savefig('./grafy/najvacsie_obchody_burza/'+akcia+'  '+str(burza)+'  '+str(data.time[0])[:11], format='png')


def najvacsie_obchody_cez_den(akcia, data, volume, zobrazenie):
  """
  Vykresluje do jedneho cenoveho grafu najvacisie obchody cez den kazdej burzy. Burzy maju svoje
  volume upravene podla najvacsich priemernych 20-tich obchodov. Je to dane len od oka. Je to mozne 
  este upravit.
  
  Parameters
  ----------
  akcia: str
      napr9klad 'AMD', 'AAPL', atd... .
  data: DataFrame
      Je to daraframe vsetkych burz za dany den
  volume: dict, {'ARCA': 20, 'AMEX': 100, ...}
      Slovnik, v ktorom su dane hranice pre volume
  zobrazenie: str, ('graf', 'subor')
      Vykresluje graf do suboru, alebo na obrazovku. Ak je to do suboru, tak je to do zakladneho
      priecinku (/home/marek/grafy/)
  """
  den = {0:'pondelok', 1:'utorok', 2:'streda', 3:'stvrtok', 4:'piatok'}
  
  plt.clf()
  plt.figure(figsize=(36, 1440/96), layout='tight')
  plt.plot(data.time, data.SMAc, color='firebrick', linewidth=0.5)
  
  for i in volume:
    burza = i[:3]+'v'
    nakup = data[burza].sort_values(ascending=False)[data[burza] >= volume[i]]
    plt.scatter(data.time[nakup.index] + pd.Timedelta('{}m'.format(np.random.uniform())), data.SMAc[nakup.index]+np.random.rand()/20, s = (data[burza][nakup.index]/volume[i])*30, linewidth=0.5, edgecolors = 'black', label=i)
  
  if zobrazenie == 'graf':
    plt.tight_layout()
    plt.legend()
    plt.show()
  else:
    plt.legend()
    plt.savefig('./grafy/najvacsie_obchody_cez_den/'+akcia+'  '+str(data.time[0])[:11]+ '  '+ den[data.time[0].day_of_week], format='png')


def najvacsie_obchody_cez_den_vw(akcia, data, volume, zobrazenie):
  """
  Vykresluje do jedneho cenoveho grafu najvacisie obchody cez den kazdej burzy. Ale velkost obchodov je
  pocitana ako podiel velkost obchodov/pocet obcodov. Burzy maju svoje volume upravene podla najvacsich priemernych 
  20-tich obchodov. Je to dane len od oka. Je to mozne este upravit.
  
  Parameters
  ----------
  akcia: str
      napriklad 'AMD', 'AAPL', atd... .
  data: DataFrame
      Je to daraframe vsetkych burz za dany den
  volume: dict, {'ARCA': 20, 'AMEX': 100, ...}
      Slovnik, v ktorom su dane hranice pre volume
  zobrazenie: str, ('graf', 'subor')
      Vykresluje graf do suboru, alebo na obrazovku. Ak je to do suboru, tak je to do zakladneho
      priecinku (/home/marek/grafy/)
  """
  den = {0:'pondelok', 1:'utorok', 2:'streda', 3:'stvrtok', 4:'piatok'}
  
  plt.clf()
  plt.figure(figsize=(36, 1440/96), layout='tight')
  plt.plot(data.time, data.SMAc, color='firebrick', linewidth=0.5)
  
  for i in volume:
    burza = i[:3]+'v
    w = i[:3]+'w'
    vw = (data[burza] / data[w])
    nakup = data[burza].sort_values(ascending=False)[data[burza] >= volume[i]]
    marker = {x:'${}$'.format(int(vw[x])) for x in nakup.index}
    plt.scatter(data.time[nakup.index] + pd.Timedelta('{}m'.format(np.random.uniform())), data.SMAc[nakup.index]+np.random.rand()/20, s = (data[burza][nakup.index]/volume[i])*30, linewidth=0.5, edgecolors = 'black', label=i)
    for i in marker:
      if vw[i] <= 3:
        plt.scatter(data.time[i] - pd.Timedelta('2m'), data.SMAc[i], marker = marker[i], s = 200, color = 'black')
  
  if zobrazenie == 'graf':
    plt.tight_layout()
    plt.legend()
    plt.show()
  else:
    plt.legend()
    plt.savefig('./grafy/najvacsie_obchody_cez_den_vw/'+akcia+'  '+str(data.time[0])[:11]+ '  '+ den[data.time[0].day_of_week], format='png')


def najvacsie_obchody_cez_den_2(akcia, data1, data2, volume1, volume2, zobrazenie):
  """
  Toto je to iste ako predchadzajuca funkcia, iba su vlozene dve akcie do jedneho grafu.
  """
  den = {0:'pondelok', 1:'utorok', 2:'streda', 3:'stvrtok', 4:'piatok'}
  
  plt.clf()
  fig, ax1 = plt.subplots(figsize=(36, 1440/96), layout='tight')
  ax2 = ax1.twinx()
  
  ax1.plot(data1.time, data1.SMAc, color='firebrick', linewidth=0.8, label='AMD')
  ax2.plot(data2.time, data2.SMAc, color='sienna', linewidth=0.5, label='SPY')
  
  for i in volume1:
    burza = i[:3]+'v'
    nakup = data1[burza].sort_values(ascending=False)[data1[burza] >= volume1[i]]
    ax1.scatter(data1.time[nakup.index], data1.SMAc[nakup.index]+np.random.rand()/20, s = (data1[burza][nakup.index]/volume1[i])*30, linewidth=0.5, edgecolors = 'black', label=i)
  
  for i in volume2:
    burza = i[:3]+'v'
    nakup = data2[burza].sort_values(ascending=False)[data2[burza] >= volume2[i]]
    ax2.scatter(data2.time[nakup.index], data2.SMAc[nakup.index]+np.random.rand()/20, s = (data2[burza][nakup.index]/volume2[i])*30, linewidth=0.5, edgecolors = 'black', label=i)
    ax2.grid(False)
  
  if zobrazenie == 'graf':
    fig.tight_layout()
    plt.legend()
    plt.show()
  else:
    plt.legend()
    plt.savefig('./grafy/najvacsie_obchody_cez_den_2/'+akcia+'  '+str(data1.time[0])[:11]+ '  '+ den[data1.time[0].day_of_week], format='png')
  

def najvacsie_obchody_cez_tyzden(akcia, data, tyzden, datumy, volume, zobrazenie):
  """
  Vykresluje do jedneho cenoveho grafu najvacsie bochody cez tyzden pre kazdu budzu. Burzy maju svoje
  volume upravene podla najvacsich priemernych 20-tich obchodov. Je to dane len od oka. Je mozne to
  este upravovat
  
  Parameters
  ----------
  akcia: str
      napriklad 'AMD', 'AAPL', atd... .
  data: DataFrame
      Je to daraframe vsetkych dat pre danu akciu
  tyzden: int
      To pre ktory tyzden chcem zobrazit data
  datumy: list
      To su vsetky datumy, ktore mam k dispozicii v datach
  volume: dict, {'ARCA': 20, 'AMEX': 100, ...}
      Slovnik, v ktorom su dane hranice pre volume
  zobrazenie: str, ('graf', 'subor')
      Vykresluje graf do suboru, alebo na obrazovku. Ak je to do suboru, tak je to do zakladneho
      priecinku (/home/marek/grafy/)
  """
  den = {0:'pondelok', 1:'utorok', 2:'streda', 3:'stvrtok', 4:'piatok'}
  tyz = [x for x in datumy if pd.Timestamp(x.replace('_', '-')).week == tyzden]
  dt = np.arange(9400).reshape(200,47) # (200,47) je na medzeru medzi grafmi
  dt = pd.DataFrame(dt, columns=data[datumy[0]].columns)
  dt[:] = None
  data = [pd.concat([data[x],dt]) for x in tyz ]
  data = pd.concat(data)
  data.index = np.arange(data.shape[0])
  
  plt.clf()
  plt.figure(figsize=(36, 1440/96), layout='tight')
  plt.plot(data.index, data.SMAc, color='firebrick', linewidth=0.5)
  
  for i in volume:
    burza = i[:3]+'v'
    nakup = data[burza].sort_values(ascending=False)[data[burza] >= volume[i]]
    plt.scatter(data.index[nakup.index], data.SMAc[nakup.index]+np.random.rand()/20, s = (data[burza][nakup.index]/volume[i])*30, linewidth=0.5, edgecolors = 'black', label=i)
  
  if zobrazenie == 'graf':
    plt.tight_layout()
    plt.legend()
    plt.show()
  else:
    plt.legend()
    plt.savefig('./grafy/najvacsie_obchody_cez_tyzden/'+akcia+'  - tyzden  '+str(tyzden)+'  od: '+tyz[0]+'   do: '+tyz[-1:][0], format='png')


def najvacsie_obchody_cez_tyzden_vw(akcia, data, tyzden, datumy, volume, zobrazenie):
  """
  Vykresluje do jedneho cenoveho grafu najvacsie bochody cez tyzden pre kazdu budzu. Ale velkost obchodov je
  pocitana ako podiel velkost obchodov/pocet obcodov.Burzy maju svoje volume upravene podla najvacsich 
  priemernych 20-tich obchodov. Je to dane len od oka. Je mozne to este upravovat
  
  Parameters
  ----------
  akcia: str
      napriklad 'AMD', 'AAPL', atd... .
  data: DataFrame
      Je to daraframe vsetkych dat pre danu akciu
  tyzden: int
      To pre ktory tyzden chcem zobrazit data
  datumy: list
      To su vsetky datumy, ktore mam k dispozicii v datach
  volume: dict, {'ARCA': 20, 'AMEX': 100, ...}
      Slovnik, v ktorom su dane hranice pre volume
  zobrazenie: str, ('graf', 'subor')
      Vykresluje graf do suboru, alebo na obrazovku. Ak je to do suboru, tak je to do zakladneho
      priecinku (/home/marek/grafy/)
  """
  den = {0:'pondelok', 1:'utorok', 2:'streda', 3:'stvrtok', 4:'piatok'}
  tyz = [x for x in datumy if pd.Timestamp(x.replace('_', '-')).week == tyzden]
  dt = np.arange(9400).reshape(200,47)
  dt = pd.DataFrame(dt, columns=data[datumy[0]].columns)
  dt[:] = None
  data = [pd.concat([data[x],dt]) for x in tyz ]
  data = pd.concat(data)
  data.index = np.arange(data.shape[0])
  
  plt.clf()
  plt.figure(figsize=(36, 1440/96), layout='tight')
  plt.plot(data.index, data.SMAc, color='firebrick', linewidth=0.5)
  
  for i in volume:
    burza = i[:3]+'v'
    w = i[:3]+'w'
    vw = data[burza] / data[w]
    nakup = data[burza].sort_values(ascending=False)[data[burza] >= volume[i]]
    marker = {x:'${}$'.format(int(vw[x])) for x in nakup.index}
    plt.scatter(data.index[nakup.index], data.SMAc[nakup.index]+np.random.rand()/20, s = (data[burza][nakup.index]/volume[i])*30, linewidth=0.5, edgecolors = 'black', label=i)
    for i in marker:
      if vw[i] <= 3:
        plt.scatter(data.index[i] - 100, data.SMAc[i], marker = marker[i], s = 200, color = 'black')
  
  if zobrazenie == 'graf':
    plt.tight_layout()
    plt.legend()
    plt.show()
  else:
    plt.legend()
    plt.savefig('./grafy/najvacsie_obchody_cez_tyzden_vw/'+akcia+'  - tyzden  '+str(tyzden)+'  od: '+tyz[0]+'   do: '+tyz[-1:][0], format='png')

































