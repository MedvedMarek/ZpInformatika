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

generator = generovanie.Generator_dat_pre_NN()
data = generator.data
columns = generator.columns
smac = columns.index('SMAc')
otvaracie_ceny = generator.otvaracie_ceny

lookback = 550
delay = 1
batch_size = 300
train = generator.generuj_data(data,lookback,delay,0,150000,batch_size)
val   = generator.generuj_data(data,lookback,delay,150001,200000,batch_size)
test  = generator.generuj_data(data,lookback,delay,200001,240000,1)


vstup = Input(shape=(lookback,data.shape[-1]), batch_size=batch_size)
x1 = layers.GRU(32, return_sequences=True, unroll=True, stateful=True)(vstup)
x2 = layers.TimeDistributed(layers.Dense(35, activation='relu'))(x1)
x3 = layers.Flatten()(x2)
vystup = layers.Dense(1)(x3)
model = Model(vstup, vystup)

model.compile(optimizer='adam', loss='mse')
history = model.fit(train,steps_per_epoch=500,epochs=5,validation_data=val,validation_steps=160)
model.save_weights('/home/marek/Dropbox/Programovanie kody/RStudio/Obchodovanie kody/NN siete/Vahy/04 - Siet GRU (04 subor)/vahy', save_format='tf')



# ---------------------------------------------------------------------------------------
# predikovanie a vykreslenie odhadnutych dat

vstup1 = Input(shape=(lookback,data.shape[-1]), batch_size=1)
x1a = layers.GRU(32, return_sequences=True, unroll=True, stateful=True)(vstup1)
x2a = layers.TimeDistributed(layers.Dense(35, activation='relu'))(x1a)
x3a = layers.Flatten()(x2a)
vystup1 = layers.Dense(delay)(x3a)
model1 = Model(vstup1, vystup1)

model1.load_weights('/home/marek/Dropbox/Programovanie kody/RStudio/Obchodovanie kody/NN siete/Vahy/04 - Siet GRU (04 subor)/vahy')


while True:
  i = test.__next__()
  osx1 = np.arange(lookback)
  osx2 = np.arange(lookback-1,lookback+1,1)
  osx3 = np.arange(lookback,lookback+1,1)
  x = i[0][0,:,smac]
  y = [i[0][0,-1:,smac].flatten(),i[1].flatten()]
  predict = model1.predict(tf.convert_to_tensor(i[0], dtype=tf.float32))
  plt.clf()
  plt.plot(osx1,x, color='red')
  plt.plot(osx2,y, color='black')
  plt.scatter(osx3,predict.flatten()[-1:], color='green')
  plt.show()
  print(i[1])
  print(predict.flatten()[-1:])
  time.sleep(0.5)













