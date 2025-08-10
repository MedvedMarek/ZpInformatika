import numpy as np
from importlib import reload
import pandas as pd


class Generator_dat_pre_NN:
  """
  V triede je vytvorena funkcia na generovanie dat pre NN siete. 
  """"
  
  def __init__(self, data):
    """
    Parameters
    ----------
    data: DataFrame
      Data su nacitane vo forme dataframe. Z tychto dat sa potom stahuju udaje o stlpcovh. Nacitavane
      data su vacsinou ulozene na disku, aby sa nemuseli stale upravovat a transformovat. Je to tak 
      rychlejsie.
    
    Atributs
    --------
    columns: list
      Zoznam vsetkych stlpcov, lebo pri vypoctoch sa pouziva numpy. A tam nie su stlpce.
    data: numpy
      Data su prevedene z dataframu do numpy pola. Prevod az teraz je preto, lebo je potrebne
      dataframu vytiahnut columns.
    """
    self.columns = data.columns
    self.data    = data.to_numpy()
  
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
        targets[j] = data[rows[j] : rows[j] + delay, self.columns.index('o')] # 'o' je stlpec pre otvaraciu cenu
      yield samples, targets


































