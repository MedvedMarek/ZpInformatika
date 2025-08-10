# Spustaj to iba na konzole, alebo vo visualstudiu. Tu v Rku to nejde. Lebo nevie iteravat graf v okne

import numpy as np
import time 
import threading
import matplotlib.pyplot as plt
import matplotlib.animation

data = {'x':[0], 'y':[0]}


class Generator_dat:
  """
  V triede sa iba generuju data. Generuju sa kazdych 5s. A generuju sa vo svojom vlakne, aby neboli
  viazane na hlavny kod. Data su ukladane do globalnej premennej data.
  """
  def __init__(self):
    vlakno = threading.Thread(target=self.generuj_data)
    vlakno.start()
  
  def generuj_data(self):
    while True:
      data['x'].append(data['x'][-1]+1)
      data['y'].append(data['y'][-1]+np.random.normal())
      time.sleep(1)


class Vykreslovanie_dat:
  """
  V triede sa vykresluju data vo svojom vlakne. Funkcia dodaj_data ide v svojom vlastnom vlakne. Je to
  z dovodu, ze musi stale skumat, ci sa nenachadzaju nove data v premennej.
  """
  def __init__(self):
    self.id_data = 0
    vlakno = threading.Thread(target=self.dodaj_data)
    vlakno.start()
    
    # Vytvorenie okna (Canvas) do ktoreho su posielane streamovane data.
    fig, ax = plt.subplots()
    anim = matplotlib.animation.FuncAnimation(fig=fig, func=self.vykresluj_data, frames=self.dodaj_data, repeat=False, cache_frame_data=False)
    plt.show()
  
  def dodaj_data(self):
    """
    Funkcia ide v nekonecnej slucke. Ale je prerusovana na 0.3s. Funkcia stale kontroluje, ce neboli
    pridane nejake nove udaje do premennej x,y. A ak boli vykonane zmeny v premennej, tak sa data
    dalej posuvaju na vykreslovanie. 
    """
    while True:
      if self.id_data != data['x'][-1:][0]:
        yield data['x'], data['y']
      self.id_data = data['x'][-1:][0]
      time.sleep(0.3)
  
  def vykresluj_data(self, data_xy):
    """
    Toto je funkcia ktora je ako argument do funkcie na vykreslovanie streamovanych dat.
    Parameters
    ----------
    data_xy: list
      Preto je tu list, lebo funkcia dodaj_data vracia udaje vo forme yield. A to uklada do listu.
      Teda prvy udaj data['x'] a druhy udaj['y'].
    """
    plt.plot(data_xy[0], data_xy[1], color='firebrick')



generator = Generator_dat()
vykreslovanie_dat = Vykreslovanie_dat()







