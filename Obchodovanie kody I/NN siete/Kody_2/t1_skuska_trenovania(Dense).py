import numpy as np
import pandas as pd
import time
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras import layers, Input
from tensorflow.keras.optimizers import RMSprop


path = '/home/marek/Data/AMD/10m/'
data = pd.read_csv(path+'AMD_10m')


def generuj_data(data, min_index, max_index,batch_size,dni):
  dni = dni*39
  min_index = (min_index//dni)*dni
  max_index = min(max_index, data.shape[0])
  max_index = ((max_index - dni)//dni)*dni
  i = min_index

  while 1:
    if i+dni+batch_size*39 >= max_index:
      i = min_index
    samples = np.zeros((batch_size,dni,data.shape[-1]-1))
    targets = np.zeros((batch_size,1))

    for j in range(batch_size):
      samples[j] = data[i:i+dni].drop(['co'],axis=1).to_numpy()
      targets[j] = data['co'][i+dni-1]
      i  = i+39
    yield samples, targets


batch_size = 1
dni = 6
train = generuj_data(data,0,30000,batch_size,dni)
val   = generuj_data(data,30000,35000,batch_size,dni)
test  = generuj_data(data,35000,43000,1,dni)


vstup = Input(shape=(39*dni,data.shape[-1]-1), batch_size=batch_size)
x1 = layers.Flatten()(vstup)
x2 = layers.Dense(1000,activation='elu')(x1)
vystup = layers.Dense(1)(x2)

model = Model(vstup, vystup)

model.summary()
model.compile(optimizer='nadam', loss='mse')
history = model.fit(train,steps_per_epoch=128,epochs=200,validation_data=val,validation_steps=21)
