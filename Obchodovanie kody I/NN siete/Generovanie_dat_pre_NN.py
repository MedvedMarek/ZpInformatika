from importlib import reload
import numpy as np
import pandas as pd
import sys
sys.path.append('/home/marek/Dropbox/Programovanie kody/RStudio/Obchodovanie kody/NN siete/')
# import Uprava_dat_pre_NN_povodne as upravaNN
import Uprava_dat_pre_NN_nove as upravaNN
reload(upravaNN)

import time

class Generator_dat_pre_NN:
  # V triede je vytvorena funkcia na generovanie dat pre NN siete. Vytvarenie triedy je dlhsie, lebo
  # nacitava vela dat. Moze to trvat aj dve minuty.
  def __init__(self):
    __uprava     = upravaNN.Priprava_dat()
    self.data    = __uprava.data
    self.columns = __uprava.columns
    self.datumy  = __uprava.datumy
    self.otvaracie_ceny = __uprava.otvaracie_ceny
  
  def generuj_data(self, data, lookback, delay, min_index, max_index, batch_size):
    """
    Generuje data dopredu. Pocet dat dopredu je dany parametrom delay.
    
    Parameters
    ----------
    data: numpy
      Dana z ktorych sa generuje
    lookback: int
      Kolko casovych udajov ma ist dozadu
    delay: int
      kolko krokov ma predikovat dopredu
    min_index: int
      spodna hranica ktora bude pouzita pri rezani dat
    max_index: int
      horna hranica, ktora bude pouzita pri rezani datt
    batch_size: int
      velkost davky
    
    Return
    ------
    samples: numpy
    targets: numpy
    """
    i = min_index+lookback
    
    while 1:
      if i+batch_size+delay >= max_index:
        i = min_index+lookback
      rows = np.arange(i, min(i+batch_size, max_index))
      i+=len(rows)
      samples = np.zeros((len(rows), lookback, data.shape[-1]))
      targets = np.zeros((len(rows), delay))
      
      for j, row in enumerate(rows):
        indices = range(rows[j] - lookback, rows[j])
        samples[j] = data[indices]
        targets[j] = data[rows[j] : rows[j] + delay, self.columns.index('SMAc')]
      yield samples, targets


































