import sys
sys.path.append('/home/marek/Dropbox/Programovanie/SkumanieDat/strategia_nn/')
from generovanie_dat import generuj_data


import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, BatchNormalization, Dropout, Flatten

# Kontrola dostupnosti GPU
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

burzy = ['arca', 'bats', 'drctedge', 'edgea', 'iex', 'memx', 'nasdaq', 'nyse', 'pearl', 'psx', 'smart']
akcie = ['aapl', 'amd', 'msft', 'tsm']


data = generuj_data('tsla', 0.95, 20, 30, ['arca', 'bats', 'drctedge', 'edgea', 'iex', 'memx', 'nasdaq', 'nyse', 'pearl', 'psx', 'smart'], 700)


def pomer(data):
    l = len(data[1])
    s = sum(data[1])
    print(f'celkom {l}   spravne {s}  pomer {s/l}')


pomer(data)


num_samples_train = round(data[0].shape[0]*0.9)
time_steps = data[0].shape[1]
num_features = data[0].shape[2]

X_train = data[0][:num_samples_train]
y_train = np.array(data[1][:num_samples_train])

X_test = data[0][num_samples_train:]
y_test = np.array(data[1][num_samples_train:])

model = Sequential([
    LSTM(256, input_shape=(time_steps, num_features), return_sequences=True),
    BatchNormalization(),
    Dropout(0.4),
    LSTM(128, return_sequences=True),
    BatchNormalization(),
    Dropout(0.3),
    Flatten (),
    Dense(64, activation='elu'),
    BatchNormalization(),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

model.fit(X_train, y_train, epochs=50, batch_size=8, validation_split=0.2)

test_loss, test_acc = model.evaluate(X_test, y_test)
print(f'Test accuracy: {test_acc}')

predictions = model.predict(X_test)
print(f'Predikcie pre prvú testovaciu vzorku: {predictions[0]}')


y_test[:10]
np.round(predictions[:10], 1)



for i in range(200):
    print((data[0][-i] == 0).all())
    







