import numpy as np
import pandas as pd
import time
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras import layers, Input


data = pd.read_csv('/home/marek/Data/AMD/1m/1m_vsetko.csv')
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
        samples = np.zeros((batch_size, lookback, data.shape[-1]-4))
        targets = np.zeros((batch_size,4))
        for k in np.arange(batch_size):
          samples[k] = data[_min+k:_max+k,:-4]
          targets[k] = data[_max+k,-4:]
        _min = _min+batch_size
        _max = _max+batch_size
        yield samples, targets


def steps(min_index,max_index,lookback,batch_size):
  kroky = ((390-(lookback+batch_size))//batch_size)+1
  min_index = int(((min_index//390)+1)*390)
  max_index = int((max_index//390)*390)
  interval = (max_index - min_index)//390
  return kroky*interval


batch_size = 10
lookback = 120
train = generuj_data(data,lookback,0,150000,batch_size)
val   = generuj_data(data,lookback,150000,200000,batch_size)
test  = generuj_data(data,lookback,200000,241000,1)
train_steps = steps(0,150000,lookback,batch_size)
val_steps   = steps(150000,200000,lookback,batch_size)

print(train_steps, val_steps)

vstup = Input(shape=(lookback,data.shape[-1]-4), batch_size=batch_size)
x1 = layers.LSTM(80, return_sequences=True, unroll=False, stateful=True)(vstup)
x2 = layers.LSTM(80, return_sequences=True, unroll=False, stateful=True)(x1)
x3 = layers.LSTM(80, return_sequences=True, unroll=False, stateful=True)(x2)
x4 = layers.LSTM(80, return_sequences=True, unroll=False, stateful=True)(x3)

x = layers.Add()([x1,x2,x3,x4])
x = layers.TimeDistributed(layers.Dense(100, activation='elu'))(x)
x = layers.Flatten()(x)
x = layers.Dense(50)(x)
vystup = layers.Dense(4)(x)

model = Model(vstup, vystup)

model.summary()
model.compile(optimizer='nadam', loss='mse')
# model.load_weights('/home/marek/Data/Vahy/1m/1m_vsetko')
history = model.fit(train,steps_per_epoch=train_steps,epochs=5,validation_data=val,validation_steps=val_steps)

model.save_weights('/home/marek/Data/Vahy/1m/1m_vsetko', save_format='tf')

