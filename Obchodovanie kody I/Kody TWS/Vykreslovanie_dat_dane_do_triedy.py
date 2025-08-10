import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import os



class Vykreslovanie:
  def __init__(self, data):
    """
    Parameters
    ----------
    data: dict
        Slovnik je zlozeny z dataframov, kde kluce su datumy obchodnych dnov.
    """
    self.data = data
    self.volume = {'ARCA':140, 'DRCTEDGE':190, 'IEX':70, 'SMART':1100, 'ISLAND':260} #arca, smart, island
    self.datumy = list(self.data.keys())
    self.den = {0:'pondelok', 1:'utorok', 2:'streda', 3:'stvrtok', 4:'piatok'}
    self.burzy = ['AMEX','ARCA','BATS','BEX','BYX','CHX','DRCTEDGE','EDGEA','IEX','MEMX','NYSE','PSX','SMART','PEARL','ISLAND']
    self.cisla_tyzdnov = np.arange(4,pd.Timestamp.now().week+1,1) # stvorka je tam preto, lebo zacinam od stvrteho tyzdna
  
  def najvacsie_obchody_burza(self, zobrazenie='subor'):
    """
    Vykresluje cenovy graf jednej burzy. Ale vykresli vsetky grafy do suboru, alebo do R-ka.
    
    Parameters
    ----------
    zobrazenie: str, ('graf', 'subor'). Default je 'subor'.
        Vykresluje graf do suboru, alebo na obrazovku. Ak je to do suboru, tak je to do zakladneho
        priecinku (/home/marek/grafy/)
    
    Returns
    -------
    plot: vykresleny graf. A je vykresleny bud do Rka, alebo je ulozeny do suboru 'grafy'.
    """
    
    for i in self.datumy:
      for j in self.volume:
        burza = j[:3]+'v'
        plt.clf()
        plt.figure(figsize=(36, 1440/96), layout='tight') # figure je v incoch. 1inch = 96px.
        nakup = self.data[i][burza].sort_values(ascending=False)[self.data[i][burza] >= self.volume[j]]
        plt.plot(self.data[i].time, self.data[i].SMAc, color='firebrick', linewidth=0.5)
        plt.scatter(self.data[i].time[nakup.index], self.data[i].SMAc[nakup.index], color='black')
        if zobrazenie == 'graf':
          plt.tight_layout()
          plt.show()
        else:
          plt.savefig('./grafy/najvacsie_obchody_burza/AMD  '+str(burza)+'  '+str(self.data[i].time[0])[:11], format='png')
  
  
  def najvacsie_obchody_cez_den(self, zobrazenie='subor'):
    """
    Vykresluje do jedneho cenoveho grafu najvacisie obchody kazdej burzy v danom dni. Burzy maju svoje
    volume upravene podla najvacsich priemernych 20-tich obchodov. Je to dane len od oka. Je to mozne 
    este upravit.
    
    Parameters
    ----------
    zobrazenie: str ('graf', 'subor'). Default je 'subor'.
        Vykresluje graf do suboru, alebo na obrazovku. Ak je to do suboru, tak je to do zakladneho
        priecinku (/home/marek/grafy/)
    
    Returns
    -------
    plot: vykresleny graf. A je vykresleny bud do Rka, alebo je ulozeny do suboru 'grafy'
    """
    
    for i in self.datumy:
      plt.clf()
      plt.figure(figsize=(36, 1440/96), layout='tight')
      plt.plot(self.data[i].time, self.data[i].SMAc, color='firebrick', linewidth=0.5)
      
      for j in self.volume:
        burza = j[:3]+'v'
        nakup = self.data[i][burza].sort_values(ascending=False)[self.data[i][burza] >= self.volume[j]]
        plt.scatter(self.data[i].time[nakup.index] + pd.Timedelta('{}m'.format(np.random.uniform())), self.data[i].SMAc[nakup.index]+np.random.rand()/20, s = (self.data[i][burza][nakup.index]/self.volume[j])*30, linewidth=0.5, edgecolors = 'black', label=j)
      
      if zobrazenie == 'graf':
        plt.tight_layout()
        plt.legend()
        plt.show()
      else:
        plt.legend()
        plt.savefig('./grafy/najvacsie_obchody_cez_den/AMD  '+str(self.data[i].time[0])[:11]+ '  '+ self.den[self.data[i].time[0].day_of_week], format='png')
  
  
  def najvacsie_obchody_cez_den_vw(self, zobrazenie='subor'):
    """
    Vykresluje do jedneho cenoveho grafu najvacisie obchody cez den kazdej burzy. Ale velkost obchodov je
    pocitana ako podiel velkost obchodov/pocet obcodov. Burzy maju svoje volume upravene podla najvacsich priemernych 
    20-tich obchodov. Je to dane len od oka. Je to mozne este upravit.
  
    Parameters
    ----------
    zobrazenie: str ('graf', 'subor'). Default je 'subor'.
        Vykresluje graf do suboru, alebo na obrazovku. Ak je to do suboru, tak je to do zakladneho
        priecinku (/home/marek/grafy/)
    
    Returns
    -------
    plot: vykresleny graf. A je vykresleny bud do Rka, alebo je ulozeny do suboru 'grafy'
    """
    
    for i in self.datumy:
      plt.clf()
      plt.figure(figsize=(36, 1440/96), layout='tight')
      plt.plot(self.data[i].time, self.data[i].SMAc, color='firebrick', linewidth=0.5)
      
      for j in self.volume:
        burza = j[:3]+'v'
        w = j[:3]+'w'
        vw = (self.data[i][burza] / self.data[i][w])
        nakup = self.data[i][burza].sort_values(ascending=False)[self.data[i][burza] >= self.volume[j]]
        marker = {x:'${}$'.format(int(vw[x])) for x in nakup.index}
        plt.scatter(self.data[i].time[nakup.index] + pd.Timedelta('{}m'.format(np.random.uniform())), self.data[i].SMAc[nakup.index]+np.random.rand()/20, s = (self.data[i][burza][nakup.index]/self.volume[j])*30, linewidth=0.5, edgecolors = 'black', label=j)
        
        for k in marker:
          if vw[k] <= 3:
            plt.scatter(self.data[i].time[k] - pd.Timedelta('2m'), self.data[i].SMAc[k], marker = marker[k], s=200, color='black')
      
      if zobrazenie == 'graf':
        plt.tight_layout()
        plt.legend()
        plt.show()
      else:
        plt.legend()
        plt.savefig('./grafy/najvacsie_obchody_cez_den_vw/AMD  '+str(self.data[i].time[0])[:11]+ '  '+ self.den[self.data[i].time[0].day_of_week], format='png')
  
  
  def najvacsie_obchody_cez_tyzden(self, zobrazenie='subor'):
    """
    Vykresluje do tyzdnoveho cenoveho grafu najvacsie obchody kazdej burzy. Volume pre kazdu burzu je zvolene podla priemernej
    hodnoty 20-tich najvacsich obchodov. Je to dane len od oka. Je to mozne potom este upravit.
    
    Parameters
    ----------
    zobrazenie: str, ('graf', 'subor'). Default je 'subor'.
        Vykresluje graf do zuboru, alebo na obrazovku. Ak je to do suboru, tak je to do zakladneho
        priecinku (/home/marek/grafy/)
    
    Returns
    -------
    plot: vykresleny graf. A je vykresleny bud do Rka, alebo je ulozeny do suboru 'grafy'.
    """
    
    for i in self.cisla_tyzdnov:
      tyzden = [x for x in self.datumy if pd.Timestamp(x.replace('_','-')).week == i]
      dt = np.arange(9400).reshape(200,47) # Teraz som iba vytvoril medzeru 200 pat sekund medzi dennymi grafmi
      dt = pd.DataFrame(dt, columns = self.data[self.datumy[0]].columns)
      dt[:] = None
      data_tyzden = [pd.concat([self.data[x], dt]) for x in tyzden]
      data_tyzden = pd.concat(data_tyzden)
      data_tyzden.index = np.arange(data_tyzden.shape[0])
      
      plt.clf()
      plt.figure(figsize=(36, 1440/96), layout='tight')
      plt.plot(data_tyzden.index, data_tyzden.SMAc, color='firebrick', linewidth=0.5)
      
      for j in self.volume:
        burza = j[:3]+'v'
        nakup = data_tyzden[burza].sort_values(ascending=False)[data_tyzden[burza] >= self.volume[j]]
        plt.scatter(data_tyzden.index[nakup.index]+np.random.normal()*7, data_tyzden.SMAc[nakup.index]+np.random.normal()/10, s=(data_tyzden[burza][nakup.index]/self.volume[j])*30, linewidth=0.5, edgecolors='black', label=j)
      
      if zobrazenie == 'graf':
        plt.tight_layout()
        plt.legend()
        plt.show()
      else:
        plt.legend()
        plt.savefig('./grafy/najvacsie_obchody_cez_tyzden/AMD  - tyzden  '+str(i)+'  od: '+tyzden[0]+'   do: '+tyzden[-1:][0], format='png')
  
  
  def najvacsie_obchody_cez_tyzden_vw(self, zobrazenie='subor'):
    """
    Vykresluje do tyzdnoveho cenoveho grafu najvacsie obchody kazdej burzy. Volume pre kazdu burzu je zvolene podla priemernej
    hodnoty 20-tich najvacsich obchodov. Je to  dane len od oka. Je to mozne potom este upravit. A do toho vypisuje najmansi
    podiel velkost obchodov/pocet. To je z dovodu, ze sa sleduje obchod s najvacsou objednavkou.
    
    Parameters
    ----------
    zobrazenie: str, ('graf', 'subor'). Defaule je 'subor'.
        Vykresluje graf do suboru, alebo na obrazovku. Ak je to do suboru, tak je to do zakladneho
        priecinku (/home/marek/grafy/)
        
    Returns
    -------
    plot: vykresleny graf. A je vykresleny bud do Rka, alebo je ulozeny do suboru 'grafy'.
    """
    
    for i in self.cisla_tyzdnov:
      tyzden = [x for x in self.datumy if pd.Timestamp(x.replace('_','-')).week == i]
      dt = np.arange(9400).reshape(200,47) # Teraz som iba vytvoril medzeru 200 pat sekund medzi dennymi grafmi
      dt = pd.DataFrame(dt, columns = self.data[self.datumy[0]].columns)
      dt[:] = None
      data_tyzden = [pd.concat([self.data[x], dt]) for x in tyzden]
      data_tyzden = pd.concat(data_tyzden)
      data_tyzden.index = np.arange(data_tyzden.shape[0])
      
      plt.clf()
      plt.figure(figsize=(36, 1440/96), layout='tight')
      plt.plot(data_tyzden.index, data_tyzden.SMAc, color='firebrick', linewidth=0.5)
      
      for j in self.volume:
        burza = j[:3]+'v'
        w = j[:3]+'w'
        vw = data_tyzden[burza] / data_tyzden[w]
        nakup = data_tyzden[burza].sort_values(ascending=False)[data_tyzden[burza] >= self.volume[j]]
        marker = {x:'${}$'.format(int(vw[x])) for x in nakup.index}
        plt.scatter(data_tyzden.index[nakup.index]+np.random.normal()*7, data_tyzden.SMAc[nakup.index]+np.random.normal()/10, s=(data_tyzden[burza][nakup.index]/self.volume[j])*30, linewidth=0.5, edgecolors='black', label=j)
        
        for k in marker:
          if vw[k] <= 3:
            plt.scatter(data_tyzden.index[k] - 100, data_tyzden.SMAc[k], marker = marker[k], s=200, color='black')
      
      if zobrazenie == 'graf':
        plt.tight_layout()
        plt.legend()
        plt.show()
      else:
        plt.legend()
        plt.savefig('./grafy/najvacsie_obchody_cez_tyzden_vw/AMD  - tyzden  '+str(i)+'  od: '+tyzden[0]+'   do: '+tyzden[-1:][0], format='png')
  
  
    






















































