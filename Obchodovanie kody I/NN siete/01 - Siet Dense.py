import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.optimizers import RMSprop
from importlib import reload
import sys
sys.path.append('/home/marek/Dropbox/Programovanie kody/RStudio/Obchodovanie kody/NN siete/')
import Generovanie_dat_pre_NN as generovanie
reload(generovanie)


generator = generovanie.Generator_dat_pre_NN()
data = generator.data
columns = generator.columns
smac = columns.index('SMAc')
otvaracie_ceny = generator.otvaracie_ceny

lookback = 120
delay = 10
batch_size = 200
train = generator.generuj_data(data,lookback,delay,0,100000,batch_size)
val   = generator.generuj_data(data,lookback,delay,100001,150000,batch_size)
test  = generator.generuj_data(data,lookback,delay,150001,200000,1)

model = Sequential()
model.add(layers.Flatten(input_shape=(lookback,data.shape[-1])))
model.add(layers.Dense(2048, activation='relu'))
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(delay))

model.compile(optimizer='adam', loss='mae')
history = model.fit_generator(train,steps_per_epoch=200,epochs=5,validation_data=val,validation_steps=(100000-lookback)/batch_size)
model.save_weights('/home/marek/Dropbox/Programovanie kody/RStudio/Obchodovanie kody/NN siete/Vahy/01 - Siet Dense (01 subor)/vahy', save_format='tf')
# model.load_weights('/home/marek/Dropbox/Programovanie kody/RStudio/Obchodovanie kody/NN siete/Vahy/01 - Siet Dense (01 subor)/vahy')

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
import matplotlib.pyplot as plt

while True:
  i = test.__next__()
  osx1 = np.arange(120)
  osx2 = np.arange(121,131,1)
  x = i[0][0,:,44]
  y = i[1]
  predict = model.predict(tf.convert_to_tensor(i[0], dtype=tf.float32))
  plt.clf()
  plt.plot(osx1,x, color='red')
  plt.plot(osx2,y.flatten(), color='black')
  plt.plot(osx2,predict.flatten(), color='green')
  plt.show()
  print(i[1])
  time.sleep(0.2)



test.close()





















