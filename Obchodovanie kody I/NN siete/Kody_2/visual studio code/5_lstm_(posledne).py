import numpy as np
import pandas as pd
import time
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras import layers, Input
from tensorflow.keras.regularizers import l1


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
        yield [samples, samples2], targets


def steps(min_index,max_index,lookback,batch_size,minuty):
  inte = {1:390, 2:195, 5:78, 10:39}
  kroky = ((inte[minuty]-(lookback+batch_size))//batch_size)+1
  min_index = int(((min_index//inte[minuty])+1)*inte[minuty])
  max_index = int((max_index//inte[minuty])*inte[minuty])
  interval = (max_index - min_index)//inte[minuty]
  return kroky*interval


batch_size = 4
lookback = 5
interval = 2
train = generuj_data(data,data2,lookback,0,60000,batch_size,interval)
val   = generuj_data(data,data2,lookback,60000,70000,batch_size,interval)
test  = generuj_data(data,data2,lookback,70000,77000,1,interval)
train_steps = steps(0,60000,lookback,batch_size,interval)
val_steps   = steps(60000,70000,lookback,batch_size,interval)


vstup = Input(shape=(lookback,  data.shape[-1]-1), batch_size=batch_size)
vstup1= Input(shape=(lookback*2,data.shape[-1]-1), batch_size=batch_size)

x1 = layers.LSTM(128, return_sequences=True, unroll=False, stateful=True)(vstup)
x1 = layers.Dropout(0.1)(x1)

x2 = layers.LSTM(128, return_sequences=True, unroll=False, stateful=True)(vstup1)
x2 = layers.Dropout(0.1)(x2)

x = layers.concatenate([x1,x2], axis=1)
x = layers.LSTM(128,return_sequences=True,stateful=True)(x)
x = layers.Dropout(0.1)(x)

x = layers.TimeDistributed(layers.Dense(128, activation='elu'))(x)
x = layers.Flatten()(x)
x = layers.Dense(64, activation='elu')(x)
vystup = layers.Dense(1)(x)

model = Model([vstup,vstup1], vystup)

model.summary()
model.compile(optimizer='nadam', loss='mse')
model.load_weights('/home/marek/Data/Vahy/2m/2m')

for i in range(500):
  print(i)
  history = model.fit(train,steps_per_epoch=train_steps,epochs=5,validation_data=val,validation_steps=val_steps)
  model.save_weights('/home/marek/Data/Vahy/2m/2m', save_format='tf')

