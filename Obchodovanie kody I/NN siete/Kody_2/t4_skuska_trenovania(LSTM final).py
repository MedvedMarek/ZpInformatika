import numpy as np
import pandas as pd
import time
# import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras import layers, Input
from tensorflow.keras.regularizers import l1

data = pd.read_csv('/media/marek/zaloha/Data/CSV/SPY/5m/5m.csv')
data = data.to_numpy()

def generuj_data(data, lookback, min_index, max_index, batch_size, minuty):
  inte = {1:390, 2:195, 5:78, 10:39}
  
  min_index = int(((min_index//inte[minuty])+1)*inte[minuty])
  max_index = int((max_index//inte[minuty])*inte[minuty])
  
  while 1:
    interval = np.arange(min_index, max_index+1, inte[minuty])
    kroky = ((inte[minuty]-(lookback+batch_size))//batch_size)+1
    
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

def steps(min_index,max_index,lookback,batch_size,minuty):
  inte = {1:390, 2:195, 5:78, 10:39}
  kroky = ((inte[minuty]-(lookback+batch_size))//batch_size)+1
  min_index = int(((min_index//inte[minuty])+1)*inte[minuty])
  max_index = int((max_index//inte[minuty])*inte[minuty])
  interval = (max_index - min_index)//inte[minuty]
  return kroky*interval


batch_size = 1
lookback = 24
interval = 5

test  = generuj_data(data,lookback,27000,30000,1,interval)

vstup = Input(shape=(lookback,data.shape[-1]-1), batch_size=batch_size)

# d = layers.Dense(50,activation='elu')(vstup)
x1 = layers.LSTM(256, return_sequences=True, unroll=False, stateful=True)(vstup)
#x2 = layers.LSTM(128, return_sequences=True, unroll=False, stateful=True)(x1)
#x3 = layers.LSTM(256, return_sequences=True, unroll=False, stateful=True)(x2)
#x4 = layers.LSTM(128, return_sequences=True, unroll=False, stateful=True)(x3)
#x5 = layers.LSTM(128, return_sequences=True, unroll=False, stateful=True)(x4)
#x6 = layers.LSTM(128, return_sequences=True, unroll=False, stateful=True)(x5)

#x = layers.Add()([x1,x2])
x = layers.TimeDistributed(layers.Dense(128, activation='elu'))(x1)
x = layers.Flatten()(x)
x = layers.Dense(64, activation='elu')(x)
vystup = layers.Dense(1)(x)

model = Model(vstup, vystup)

model.summary()
model.compile(optimizer='nadam', loss='mse')
# model.load_weights('/home/marek/Data/Vahy/5m/5m')

x = []
y = []

for i in range(500):
  xx,yy = test.__next__()
  # print('od ',model.predict(x)[0][0])
  # print('sk ',y[0][0])
  x.append(model.predict(xx)[0][0])
  y.append(yy[0][0])
  # time.sleep(3)




import matplotlib.pyplot as plt

def plot():
  plt.plot(x, color='red')
  plt.plot(y, color='black')
  plt.scatter(range(len(x)),x,s=5,c='red')
  plt.scatter(range(len(y)),y,s=5,c='black')
  plt.show()
















