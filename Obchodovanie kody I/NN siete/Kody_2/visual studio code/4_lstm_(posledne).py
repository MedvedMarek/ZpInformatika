import numpy as np
import pandas as pd
import time
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras import layers, Input
from tensorflow.keras.regularizers import l1


data = pd.read_csv('//media/marek/zaloha/Data/CSV/SPY/5m/5m.csv')
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


batch_size = 5
lookback = 55
interval = 5
train = generuj_data(data,lookback,0,25000,batch_size,interval)
val   = generuj_data(data,lookback,25000,27000,batch_size,interval)
test  = generuj_data(data,lookback,27000,30000,1,interval)
train_steps = steps(0,25000,lookback,batch_size,interval)
val_steps   = steps(25000,27000,lookback,batch_size,interval)


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
#model.load_weights('/home/marek/Data/Vahy/5m/5m')

for i in range(500):
  print(i)
  history = model.fit(train,steps_per_epoch=train_steps,epochs=5,validation_data=val,validation_steps=val_steps)
  model.save_weights('/home/marek/Data/Vahy/5m/5m', save_format='tf')

