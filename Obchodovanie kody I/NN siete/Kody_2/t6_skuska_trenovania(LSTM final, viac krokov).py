import numpy as np
import pandas as pd
import time
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras import layers, Input


data = pd.read_csv('/home/marek/Data/AMD/5m/5m_dva_kroky.csv')
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
        samples = np.zeros((batch_size, lookback, data.shape[-1]-2))
        targets = np.zeros((batch_size,2))
        for k in np.arange(batch_size):
          samples[k] = data[_min+k:_max+k,:-2]
          targets[k] = data[_max+k,-2:]
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
lookback = 10
interval = 5

test  = generuj_data(data,lookback,38000,42000,1,interval)

encoder_inputs = Input(shape=(lookback,data.shape[-1]-2), batch_size=batch_size)
encoder_layers = layers.LSTM(70,return_sequences=True, stateful=True)(encoder_inputs)
vystup1 = layers.TimeDistributed(layers.Dense(50, activation='elu'))(encoder_layers)
vystup1 = layers.Flatten()(vystup1)
vystup1 = layers.Dense(1)(vystup1)

decoder = layers.LSTM(70,return_sequences=True,stateful=True)(encoder_layers)
vystup2 = layers.TimeDistributed(layers.Dense(50, activation='elu'))(decoder)
vystup2 = layers.Flatten()(vystup2)
vystup2 = layers.Dense(1)(vystup2)


inputs  = encoder_inputs
outputs = [vystup1,vystup2]

model = Model(inputs, outputs)
model.summary()
model.compile(optimizer='nadam', loss='mse')
model.load_weights('/home/marek/Data/Vahy/5m/5m_dva_kroky')


for i in range(300):
  x,y = test.__next__()
  a = model.predict(x)
  print(y)
  print(a[0][0][0],a[1][0][0])
  # xx.append(model.predict(x))
  # yy.append(y)
  time.sleep(3)





