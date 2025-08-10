import numpy as np
import pandas as pd
import time
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras import layers, Input


data = pd.read_csv('/home/marek/Data/AMD/10m/10m.csv')
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
lookback = 5
interval = 10
train = generuj_data(data,lookback,0,18000,batch_size,interval)
val   = generuj_data(data,lookback,18000,22000,batch_size,interval)
test  = generuj_data(data,lookback,22000,24000,1,interval)
train_steps = steps(0,30000,lookback,batch_size,interval)
val_steps   = steps(30000,38000,lookback,batch_size,interval)


print(train_steps, val_steps)

vstup = Input(shape=(lookback,data.shape[-1]-1), batch_size=batch_size)
x1 = layers.LSTM(50, return_sequences=True, unroll=False, stateful=True, dropout=0.1)(vstup)
x = layers.TimeDistributed(layers.Dense(200, activation='elu'))(x1)
x = layers.Flatten()(x)
x = layers.Dense(100, activation='elu')(x)
vystup = layers.Dense(1)(x)

model = Model(vstup, vystup)

model.summary()
model.compile(optimizer='nadam', loss='mse')
# model.load_weights('/home/marek/Data/Vahy/10m/10m')

for i in range(100):
  print(i)
  history = model.fit(train,steps_per_epoch=train_steps,epochs=5,validation_data=val,validation_steps=val_steps)
  model.save_weights('/home/marek/Data/Vahy/10m/10m', save_format='tf')
