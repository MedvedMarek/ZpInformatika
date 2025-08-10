import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras import layers, Input
from tensorflow.keras.optimizers import RMSprop
from importlib import reload
import sys
sys.path.append('/home/marek/Dropbox/Programovanie kody/RStudio/Obchodovanie kody/NN siete/')
import Generovanie_dat_pre_NN as generovanie
reload(generovanie)
import matplotlib.pyplot as plt

# generator = generovanie.Generator_dat_pre_NN()
data = generator.data
columns = generator.columns
smac = columns.index('SMAc')
otvaracie_ceny = generator.otvaracie_ceny

lookback = 120
delay = 1
batch_size = 200
train = generator.generuj_data(data,lookback,delay,0,150000,batch_size)
val   = generator.generuj_data(data,lookback,delay,105001,200000,batch_size)
test  = generator.generuj_data(data,lookback,delay,200001,240000,1)

vstup = Input(shape=(lookback,data.shape[-1]), batch_size=batch_size)
x1 = layers.LSTM(64, return_sequences=True, unroll=True, stateful=True)(vstup)
# x2 = layers.LSTM(32, return_sequences=True, unroll=True, stateful=True)(x1)
# x3 = layers.LSTM(32, return_sequences=True, unroll=True, stateful=True)(x2)
# x = layers.TimeDistributed(layers.Dense(lookback))(x[:,-1:,:])
# x = layers.Add()([x1,x2,x3])
# x = layers.Flatten()(x)
x = layers.TimeDistributed(layers.Dense(delay))(x1)
# x = layers.Flatten()(x)
vystup = layers.TimeDistributed(layers.Dense(delay))(x[:,-1:,:])

model = Model(vstup, vystup)

model.compile(optimizer='adam', loss='mse')
history = model.fit(train,steps_per_epoch=750,epochs=5,validation_data=val,validation_steps=250)
model.save_weights('/home/marek/Dropbox/Programovanie kody/RStudio/Obchodovanie kody/NN siete/Vahy/03 - Siet GRU (03 subor)/vahy', save_format='tf')
# model.load_weights('/home/marek/Dropbox/Programovanie kody/RStudio/Obchodovanie kody/NN siete/Vahy/03 - Siet GRU (03 subor)/vahy')

loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1,len(loss)+1)

plt.clf()
plt.plot(epochs, loss, 'bo', label='Trenovacie data')
plt.plot(epochs, val_loss, 'b',label='Validacne data')
plt.legend()
plt.show()



# ---------------------------------------------------------------------------------------
# predikovanie a vykreslenie odhadnutych dat

vstup1 = Input(shape=(lookback,data.shape[-1]), batch_size=1)
x11 = layers.LSTM(64, return_sequences=True, unroll=True, stateful=True)(vstup1)
x12 = layers.TimeDistributed(layers.Dense(delay))(x11)
vystup1 = layers.TimeDistributed(layers.Dense(delay))(x12[:,-1:,:])

model2 = Model(vstup1,vystup1)
model2.load_weights('/home/marek/Dropbox/Programovanie kody/RStudio/Obchodovanie kody/NN siete/Vahy/03 - Siet GRU (03 subor)/vahy')


while True:
  i = test.__next__()
  osx1 = np.arange(lookback)
  osx2 = np.arange(lookback-1,lookback+1,1)
  osx3 = np.arange(lookback,lookback+1,1)
  x = i[0][0,:,44]
  y = [i[0][0,-1:,44].flatten(),i[1].flatten()]
  predict = model2.predict(tf.convert_to_tensor(i[0], dtype=tf.float32))
  plt.clf()
  plt.plot(osx1,x, color='red')
  plt.plot(osx2,y, color='black')
  plt.scatter(osx3,predict.flatten(), color='green')
  plt.show()
  print(i[1])
  print(predict.flatten())
  time.sleep(0.5)




