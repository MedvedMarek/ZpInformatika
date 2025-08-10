# Rozdiel oproti predchadzajucemu kodu je ten, ze tu sa generuju vsetky data pre 1,2,5,10 min.


import numpy as np
from importlib import reload
import pandas as pd
import time

data = pd.read_csv('/home/marek/Data/SPY/2m/2m.csv')
data2 = pd.read_csv('/home/marek/Data/SPY/1m/1m.csv')
data = data.to_numpy()
data2 = data2.to_numpy()

def generuj_data(data, data2, lookback, min_index, max_index, batch_size, minuty):
  inte = {1:390, 2:195, 5:78, 10:39}
  
  min_index = int(((min_index//inte[minuty])+1)*inte[minuty])
  max_index = int((max_index//inte[minuty])*inte[minuty])
  nasobok = 2
  
  while 1:
    interval = np.arange(min_index, max_index+1, inte[minuty])
    kroky = ((inte[minuty]-(lookback+batch_size))//batch_size)+1
    
    for i in interval[:-1]:
      _min = i
      _max = _min+lookback
      _min2 = i*nasobok
      _max2 = _min2+(lookback*nasobok)
      print(_min,_max)
      print(_min2,_max2)
      for j in np.arange(kroky):
        samples = np.zeros((batch_size, lookback, data.shape[-1]-1))
        samples2= np.zeros((batch_size, lookback*nasobok, data.shape[-1]-1))
        targets = np.zeros((batch_size,1))
        for k in np.arange(batch_size):
          samples[k] = data[_min+k:_max+k,:-1]
          samples2[k]= data2[_min2+nasobok*k:_max2+nasobok*k,:-1]
          targets[k] = data[_max+k,-1:]
        _min = _min+batch_size
        _max = _max+batch_size
        _min2= _min2+batch_size*nasobok
        _max2= _max2+batch_size*nasobok
        yield samples, samples2, targets



def steps(min_index,max_index,lookback,batch_size,minuty):
  inte = {1:390, 2:195, 5:78, 10:39}
  kroky = ((inte[minuty]-(lookback+batch_size))//batch_size)+1
  min_index = int(((min_index//inte[minuty])+1)*inte[minuty])
  max_index = int((max_index//inte[minuty])*inte[minuty])
  interval = (max_index - min_index)//inte[minuty]
  return kroky*interval


steps = steps(0,12304,300,20,1)


generator = generuj_data(data,data2,10,0,500,3,2)  


for i in range(400):
  print(i,'------------------------------------')
  generator.__next__()


generator.__next__()


for i in range(50):
  generator.__next__()





x = np.ndarray(10)






































