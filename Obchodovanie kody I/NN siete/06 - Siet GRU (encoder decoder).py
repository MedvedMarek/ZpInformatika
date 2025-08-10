# Toto je kus kodu, kde je zobrazene, ako nastavit encoder/decoder. Taktiez je znazornene, ako vypnut 
# trenovanie niektorych vrstiev. Treba dat pozor na vrstvy GRU a LSTM. Nemaju rovnaky pocet stavov.

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

lookback = 100
delay = 3
batch_size = 200
train = generator.generuj_data(data,lookback,delay,0,150000,batch_size)
val   = generator.generuj_data(data,lookback,delay,150001,200000,batch_size)
test  = generator.generuj_data(data,lookback,delay,200001,240000,1)

# treba si uvedomit, ze pocet krokov dopredu, by malo mat potrebny pocet vrstiev. Ak je napriklad
# predikovanych 5 krokov dopredu, tak by malo byt 5 vrstiev. V pripade, ze nebude rovnaka
# dimenzia vstupnej a vystupnej vrstvy, tak pri vypocte straty pre MSE si to model upravuje sam
# a upravuje mensi vektor do rovnakej dimenzie ako je vacsi vektor. Ale ci to bude dobre, tak to neviem.

# encoder
# Hlavny vstup, kde ide plna datova matica.
input_encoder = Input(shape=(lookback,data.shape[-1]), batch_size=batch_size)
x = layers.GRU(10, return_sequences=True, unroll=False, stateful=True, name='en1')(input_encoder)
# Tato vrstva navracia inicializaciu vah, ktore pojdu ako vstup do decodera. Je to z dovodu, ze tu
# je zachovana informacia casoveho radu. A aby tuto informasiu mal aj decoder.
x,state1 = layers.GRU(10, return_sequences=True, unroll=False, stateful=True, return_state=True, name='en2')(x)
encoder_output = layers.Dense(1, name='en3')(x)

# decoder
y1 = layers.GRU(10, return_sequences=True, stateful=True)(encoder_output,initial_state=state1)
y1,state2 = layers.GRU(10, return_sequences=True, stateful=True, return_state=True)(y1)
decoder1_output = layers.Dense(1, name='dec1')(y1)

y2 = layers.GRU(10, return_sequences=True, stateful=True)(decoder1_output,initial_state=state2)
decoder2_output = layers.Dense(1, name='dec2')(y2)

output = [encoder_output, decoder1_output, decoder2_output]

model = Model(input_encoder, output)
# Tu je ukazka toho, ze ak by som nechcel trenovat niektore vrstvy, lebo ich uz mam natrenovane.
# Funkcia model.layers[2] ma ako vstup cislo vrstvy. Preto ak neviem, ake cislo ma konkretna vrstva, tak
# to mozem zistit cez index.
# Ale vypnutie trenovania sa musi realizovat este pred kompilaciou.
model.layers[model.layers.index(model.get_layer('en1'))].trainable=False
model.compile(optimizer='adam', loss='mse')
history = model.fit(train,steps_per_epoch=50,epochs=2,validation_data=val,validation_steps=50)


# -----------------------------------------------------------------------------------------
# testovanie 

input_encoder1 = Input(shape=(lookback,data.shape[-1]), batch_size=1)
x1 = layers.GRU(10, return_sequences=True, unroll=False, stateful=True)(input_encoder1)
x1 = layers.GRU(10, return_sequences=True, unroll=False, stateful=True)(x1)
encoder_output1 = layers.Dense(1, name='en')(x1)

y11 = layers.GRU(10, return_sequences=True, stateful=True)(encoder_output1)
y11 = layers.GRU(10, return_sequences=True, stateful=True)(y11)
decoder1_output1 = layers.Dense(1, name='dec1')(y11)

y21 = layers.GRU(10, return_sequences=True, stateful=True)(decoder1_output1)
decoder2_output1 = layers.Dense(1, name='dec2')(y21)

output1 = [encoder_output1, decoder1_output1, decoder2_output1]

model1 = Model(input_encoder1, output1)
model1.set_weights(model.get_weights())

pred = model1.predict(test.__next__()[0])
pred[1].flatten()[0]











































