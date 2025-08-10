import numpy as np
from importlib import reload
import pandas as pd

data = pd.read_csv('/home/marek/Data/AMD/1m/1m.csv')
data = data.to_numpy()

def generuj_data(data, lookback, min_index, max_index, batch_size):
  min_index = int(((min_index//390)+1)*390)
  max_index = int((max_index//390)*390)
  print(min_index,max_index)
  
  while 1:
    interval = np.arange(min_index, max_index+1, 390)
    kroky = ((390-(lookback+batch_size))//batch_size)+1
    
    for i in interval:
      _min = i
      _max = _min+lookback
      for j in np.arange(kroky):
        samples = np.zeros((batch_size, lookback, data.shape[-1]-1))
        targets = np.zeros((batch_size,1))
        for k in np.arange(batch_size):
          samples[k] = data[_min+k:_max+k,:-1]
          targets[k] = data[_max+k,-1:]
        _min = _min+batch_size
        _max = _max+batch_size
        yield samples, targets

      
    
    
  
generator = generuj_data(data1,380,0,12304,2)  

generator.__next__()

def steps(min_index,max_index,lookback,batch_size):
  kroky = ((390-(lookback+batch_size))//batch_size)+1
  min_index = int(((min_index//390)+1)*390)
  max_index = int((max_index//390)*390)
  interval = (max_index - min_index)//390
  return kroky*interval































