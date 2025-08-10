import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import sklearn.preprocessing as sk


# ------------------------- Nacitanie dat zo suboru -------------------------------------
day   = '2023_02_17'
path  = '/home/marek/Dropbox/Data/TWS/'+ day +'/'
burzy = ['AMEX','ARCA','BATS','BEX','BYX','CHX','DRCTEDGE','EDGEA','IEX','MEMX','NYSE',
         'PSX','SMART','PEARL','ISLAND']

def nacitaj_akciu(path, akcia):
  """
  Nacitava z disku uz upravene data a prevadza ich na DataFrame.
  """
  
  data = np.load(path+akcia+'_AMEX.npy')
  data = pd.DataFrame(data[:,[1,2,3,4]], columns=['time','AMEc','AMEv','AMEw'])
  data['time'] = data['time'].astype('int')
  data = data.drop(0, axis=0)
  data = data[data.time >1]
  data = data.drop_duplicates(subset=['time'], ignore_index=True)
  data = data.sort_values(by='time', ignore_index=True)
  data = data.drop_duplicates(subset=['time'], ignore_index=True)
  
  for j in burzy[1:]:
    d = np.load(path+akcia+'_'+j+'.npy')
    d = pd.DataFrame(d[:,[1,2,3,4]], columns=['time',j[:3]+'c',j[:3]+'v', j[:3]+'w'])
    
    d['time'] = d['time'].astype('int')
    d = d.drop(0, axis=0)
    d = d[d.time >1]
    d = d.drop_duplicates(subset=['time'], ignore_index=True)
    d = d.sort_values(by='time', ignore_index=True)
    d = d.drop_duplicates(subset=['time'], ignore_index=True)
    
    data = pd.merge(data,d, how='outer', on='time')
    data = data.fillna(0)
  
  data = data.drop_duplicates(subset=['time'], ignore_index=True)
  data = data.sort_values(by='time', ignore_index=True)
  data.time = data.time-21600
  data.time = pd.to_datetime(data.time, unit='s')
  xx = [i[:3]+'v' for i in burzy]
  data['volume'] = data[xx].apply(sum, axis=1)
  
  return(data)

amd = nacitaj_akciu(path, 'AMD')


# ------------------------- Orezanie dat iba na obchodne hodiny -------------------------
start = day.replace('_','-') + ' 08:30:00'
stop  = day.replace('_','-') + ' 15:00:00'
start = pd.Timestamp(start)
stop  = pd.Timestamp(stop)
mask  = (amd.time >= start) & (amd.time <= stop)
data  = amd[mask]
index = {x[1]:x[0] for x in enumerate(data.index)}
data = data.rename(index)


# ------------------------- Uprava dat pre moznost zobrazit ich -------------------------

# Nahlad na data, ake ma maximalne a minimalne hodnoty cien. Lebo niekedy, ked je 
# pri stahovani dat prerusene vlakno, tak ma tendneciu davat namiesto ceny iba nulu. 
# A to potom zle vykresluje graf, ked sa normalizuju data pomocou funkcie minmaxscaler.
for i in burzy:
  mi = min(data[i[:3]+'c'])
  ma = max(data[i[:3]+'c'])
  print('{:10}'.format(i), '{:5.2f}'.format(mi), '  {:5.2f}'.format(ma))

# Vypisanie, ktore riadky su nulove. A ak ich nie je vela, tak su odstranene.
for i in burzy:
  data[data[i[:3]+'c'] == 0]

# Nezaradenie nulovych riadkov do dat. Nulovych riadkov bolo malo a aj to iba na konci 
# dat. Preto su nie zahrnute.
for i in burzy:
  data = data[data[i[:3]+'c'] != 0]
  data.index = np.arange(data.shape[0])


# ------------------------- Statistika kolko obchodov bolo spravenych -------------------

# Nahlad na pocet zrelizovanych obchodov (volume). Je to az po upravach a orezani dat. 
# Lebo maximalne hodnoty pri otvoreni a uzatvarani nie su velmi doverihodne.
for i in burzy:
  print('{:10}'.format(i), '{:7}'.format(int(sum(data[i[:3]+'v']))), '{:5}'.format(int(max(data[i[:3]+'v']))))


# ------------------------- Transformacia dat -------------------------------------------

# Transformujem to na MinMaxScaler. Je to z dovodu, ze do grafu potom chcem vykreslovat
# cenovy graf a aj graf pre volume.
def min_max_scaler(data):
  dt = data.copy()
  
  for i in data.columns.drop('time'):
    x = data[i].to_numpy().reshape(data.shape[0],1)
    dt[i] = sk.minmax_scale(x)
  
  return(dt)

data_tr = min_max_scaler(data)


# ------------------------- Vykreslovanie dat -------------------------------------------

# Vykreslovanie cenoveho grafu a aj volume zaroven.
date  = str(data_tr.time[0])[:11]
start = pd.Timestamp(date+'10:45:00')
stop  = pd.Timestamp(date+'11:08:00')
mask  = (data_tr.time >= start) & (data_tr.time <= stop)
dt    = data_tr[mask]
x     = np.arange(dt.volume.shape[0])
burzy2 = ['ARCA', 'BATS', 'DRCTEDGE', 'EDGEA', 'IEX', 'MEMX', 'NYSE', 'SMART', 'ISLAND']
burzyCVW = []
sc    = sk.MinMaxScaler()
# View(data[['time']+[x[:3]+j for x in burzy2 for j in ['c','v','w']]+['volume']])

# plt.clf()
# for i in enumerate(burzy, start=1):
#   sc.fit(data[i[1][:3]+'c'].to_numpy().reshape(data.shape[0],1))
#   plt.subplot(4,4,i[0])
#   plt.bar(x, dt.SMAv, width=0.8, color='blue', alpha = 0.3)
#   plt.bar(x, dt[i[1][:3]+'v'], width=0.8, color='black', alpha=0.7)
#   plt.axhline(sc.transform([[77.89]]), color='grey', linewidth=1)
#   plt.axhline(sc.transform([[77.45]]), color='grey', linewidth=1)
#   plt.axhline(sc.transform([[77.45]]), color='grey', linewidth=1)
#   plt.plot(x,dt[i[1][:3]+'c'], color='firebrick', linewidth=2)
#   plt.title(i[1], size=9)
# 
# plt.show()


plt.clf()
for i in enumerate(burzy2, start=1):
  sc.fit(data[i[1][:3]+'c'].to_numpy().reshape(data.shape[0], 1))
  plt.subplot(3,3,i[0])
  plt.bar(x, dt.SMAv, width=0.8, color='blue', alpha = 0.3)
  plt.bar(x, dt[i[1][:3]+'v'], width=0.8, color='black', alpha=0.7)
  plt.axhline(sc.transform([[77.64]]), color='grey', linewidth=1)
  # plt.axhline(sc.transform([[77.64]]), color='grey', linewidth=1)
  # plt.axhline(sc.transform([[77.45]]), color='grey', linewidth=1)
  # plt.axhline(sc.transform([[77.45]]), color='grey', linewidth=1)
  plt.plot(x,dt[i[1][:3]+'c'], color='firebrick', linewidth=2)
  plt.title(i[1], size=9)

plt.show()


plt.clf()
for i in enumerate(burzy2, start=1):
  nakup = data[i[1][:3]+'v'].sort_values(ascending=False)[:20]
  plt.subplot(3,3,i[0])
  plt.plot(data.index, data.SMAc, color='firebrick', linewidth=0.5)
  plt.scatter(nakup.index, data.SMAc[nakup.index], color='black')
  plt.title(i[1])

plt.show()



for i in burzy2:
  data[i[:3]+'v'].sort_values(ascending=False)[:20]

































