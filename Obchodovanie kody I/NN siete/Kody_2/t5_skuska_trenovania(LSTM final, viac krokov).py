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
encoder_outputs,encoder_s,encoder_h = layers.LSTM(100, return_state=True,return_sequences=False)(encoder_inputs)
encoder_outputs = tf.expand_dims(encoder_outputs,axis=-1)

decoder1_layer  = layers.LSTM(100, return_state=True)
decoder1_layer.states = [encoder_s,encoder_h]
decoder1_outputs,decoder1_s,decoder1_h = decoder1_layer(encoder_outputs)
decoder1_final = layers.Dense(1)(decoder1_outputs)
decoder1_outputs = tf.expand_dims(decoder1_outputs,axis=-1)

decoder2_layer = layers.LSTM(100,return_state=False)
decoder2_layer.states = [decoder1_s,decoder1_h]
decoder2_outputs = decoder2_layer(decoder1_outputs)
decoder2_final = layers.Dense(1)(decoder2_outputs)

inputs  = encoder_inputs
outputs = [decoder1_final,decoder2_final]

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




train = generuj_data(data,lookback,38000,42000,2,interval)

x = layers.LSTM(3,return_sequences=False,return_state=True)
x(train.__next__()[0])

y = layers.LSTM(3,return_sequences=True,return_state=True)
y(train.__next__()[0])


