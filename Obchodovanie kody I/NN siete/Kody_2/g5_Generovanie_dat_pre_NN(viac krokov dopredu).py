# Rozdiel oproti predchadzajucemu kodu je ten, ze tu sa generuju vsetky data pre 1,2,5,10 min.


import numpy as np
from importlib import reload
import pandas as pd
import time

data = pd.read_csv('/home/marek/Data/AMD/5m/5m_dva_kroky.csv')
data = data.to_numpy()

def generuj_data(data, lookback, min_index, max_index, batch_size, minuty):
  inte = {1:390, 2:195, 5:78, 10:39}
  
  min_index = int(((min_index//inte[minuty])+1)*inte[minuty])
  max_index = int((max_index//inte[minuty])*inte[minuty])
  print(min_index,max_index)
  
  while 1:
    interval = np.arange(min_index, max_index+1, inte[minuty])
    kroky = ((inte[minuty]-(lookback+batch_size))//batch_size)+1
    
    for i in interval:
      _min = i
      _max = _min+lookback
      for j in np.arange(kroky):
        samples = np.zeros((batch_size, lookback, data.shape[-1]-2))
        targets = np.zeros((batch_size,2))
        for k in np.arange(batch_size):
          samples[k] = data[_min+k:_max+k,:-2]
          targets[k] = data[_max+k,-2:]
        _min = _min+batch_size
        _max = _max+batch_size
        print(_min, _max)
        yield samples, targets


def steps(min_index,max_index,lookback,batch_size,minuty):
  inte = {1:390, 2:195, 5:78, 10:39}
  kroky = ((inte[minuty]-(lookback+batch_size))//batch_size)+1
  min_index = int(((min_index//inte[minuty])+1)*inte[minuty])
  max_index = int((max_index//inte[minuty])*inte[minuty])
  interval = (max_index - min_index)//inte[minuty]
  return kroky*interval

steps = steps(0,12304,300,20,1)


generator = generuj_data(data,60,0,1560,2,1)  
generator.__next__()

for i in range(400):
  print(i,'------------------------------------')
  generator.__next__()






