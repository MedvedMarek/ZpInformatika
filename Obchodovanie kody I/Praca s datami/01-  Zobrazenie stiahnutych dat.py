import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sklearn.preprocessing as sk
from matplotlib.gridspec import GridSpec


path = '/home/marek/Dropbox/Data/TWS/amd_22_12_20/'
amex      = pd.read_csv(path+'AMEX.csv', index_col=0)
arca      = pd.read_csv(path+'ARCA.csv', index_col=0)
bats      = pd.read_csv(path+'BATS.csv', index_col=0)
bex       = pd.read_csv(path+'BEX.csv', index_col=0)
byx       = pd.read_csv(path+'BYX.csv', index_col=0)
chx       = pd.read_csv(path+'CHX.csv', index_col=0)
drctedge  = pd.read_csv(path+'DRCTEDGE.csv', index_col=0)
edgea     = pd.read_csv(path+'EDGEA.csv', index_col=0)
iex       = pd.read_csv(path+'IEX.csv', index_col=0)
memx      = pd.read_csv(path+'MEMX.csv', index_col=0)
nyse      = pd.read_csv(path+'NYSE.csv', index_col=0)
psx       = pd.read_csv(path+'PSX.csv', index_col=0)
smart     = pd.read_csv(path+'SMART.csv', index_col=0)
ibkrats   = pd.read_csv(path+'IBKRATS.csv', index_col=0) # Je to asi to iste ako smart
pearl     = pd.read_csv(path+'PEARL.csv', index_col=0)
island    = pd.read_csv(path+'ISLAND.csv', index_col=0)

# cboe
# edgx
# ise
# ltse
# nysenat
# phlx
# tplus1
# inet
# nsx
# pink
# pse
# etmm
# bzx




# slovnik do ktoreho su vlozene vsetky buzry. Sluzi to ako parameter pre funkcie na 
# vypis riadkov a pocet obchodov. Dalej sluzi ako parameter pre funkciu na vytvorenie
# jedneho dataframu
data_burzy = {'amex':amex, 'arca':arca, 'bats':bats, 'bex':bex, 'byx':byx, 'chx':chx, 'drctedge':drctedge,
              'edgea':edgea, 'iex':iex, 'memx':memx, 'nyse':nyse, 'psx':psx, 'smart':smart, 'pearl':pearl,
              'island':island}



# ------------------------------------ Funkcie ---------------------------------------

# zobrazenie poctu riadkov
def riadky(data):
  for i in data:
    print('{0:8}'.format(i), data[i].shape)


# pocet obchodov
# prva hodnota je pocet zobchodovanych akcii
# druha hodnota je kolko krat sa nezobchodovalo nic
# tretia hodnota je kolko krat sa obchodovalo
def pocet_obchodov(data):
  for i in data:
    print('{0:8}'.format(i), '{0:8}'.format(sum(data[i].Volume)), '{0:8}'.format(sum(data[i].Volume==0)),
          '{0:8}'.format(sum(data[i].Volume>0)))


# uprava datumu na rano. Odpocitanie 21600 je odpocitanie 6 hodin, aby som sa dostal
# na uroven otvorenia burzy. To je na rano 8:30. Lepsie sa to potom pozera aj do grafu na cenu.
def uprava_datum(data):
  for i in data:
    data[i].DateTime = data[i].DateTime - 21600
    data[i].DateTime = pd.to_datetime(data[i].DateTime, unit='s')
  return(data)



# zlucene data do jedneho dataframu. Ponechane je OHLC z ARCA a doplnene su potom
# vsetky Volume z ostatnych burz
def data(data):
  ohlc = data['arca']
  ohlc = ohlc.drop(labels='Volume', axis=1)
  
  for i in data.keys():
    # spajanie po stlpcoch. Referencny stlpec je DateTime. Pozri CheatSheet pre pandas v dropboxe
    ohlc = pd.merge(ohlc, data[i][['DateTime', 'Volume']], how='left', on='DateTime')
    # premenovavanie je tu preto, lebo muselo stale nejako inak nazvat novy stlpec. A pri velkom pocte
    # novych stlpcov to robilo sarapatu.
    ohlc.columns = list(ohlc.columns[:-1]) + [i]
  
  # pomenovanie pridanych stlpcov podla danych burz
  ohlc.columns = list(data['arca'].columns[:5]) + list(data.keys())
  # vytvorenie noveho stlpca Volume a pridanie do dataframu
  ohlc = ohlc.assign(Volume = ohlc[ohlc.columns[5:]].apply(np.sum, axis=1)) 
  # prenasobenie stlpca Volume, aby sa hodnota rovnala grafom z TWS (je to prehladnejsie)
  ohlc[ohlc.columns[5:]] = ohlc[ohlc.columns[5:]].apply(lambda x: x*100, axis=1) 
  return(ohlc)


# vykreslenie ceny 
def plot_cena(data):
  x = np.arange(data.shape[0])
  y = data['High']
  plt.clf()
  plt.plot(x,y, linewidth=0.5)
  plt.tight_layout()
  plt.show()


# vykresluje graf, kde na akej cene sa uskutocnil obchod
def plot_cena_a_burza(data, burza):
  x = np.arange(data.shape[0])
  y = data['High']
  xb = data[data[burza]>0].index
  yb = data['High'][data[burza]>0]
  plt.clf()
  plt.plot(x,y, linewidth=0.5)
  plt.scatter(xb,yb, s=2.5, color='red')
  plt.title(burza)
  plt.tight_layout()
  plt.show()


# vykresluje nejvacsie obchody
def plot_naj_obchod(data, burza, pocet):
  '''
  data = DataFrame, je to dataframe, kde su zlucene vsetky volume na burzach
  burza = string
  pocet = int, je to cislo, ktore urcuje, kolko sa ma zobrat najlepsich obchodov
  '''
  x = np.arange(data.shape[0])
  y = data['High']
  xb = data.sort_values(by=burza, ascending=False).index[:pocet]
  yb = data['High'][xb]
  
  plt.clf()
  plt.plot(x,y, linewidth=0.5)
  plt.scatter(xb,yb, s=8, color='red')
  plt.title(burza)
  plt.tight_layout()
  plt.show()


# vykresluje kedy sa neobchoduje, alebo kedy sa najmenej obchoduje
def plot_nulove_obchody(data, burza):
  '''
  vykresluje, kedy sa vobec neobchodovalo.
  '''
  x = np.arange(data.shape[0])
  y = data['High']
  xb = data[burza][data[burza]==0].index
  yb = data['High'][xb]
  
  plt.clf()
  plt.plot(x,y, linewidth=0.5)
  plt.scatter(xb,yb, s=8, color='red')
  plt.title(burza)
  plt.tight_layout()
  plt.show()


# vykresluje kedy sa obchoduje
def plot_nenulove_obchody(data, burza):
  '''
  vykresluje, kedy sa obchodovalo.
  '''
  x = np.arange(data.shape[0])
  y = data['High']
  xb = data[burza][data[burza]>0].index
  yb = data['High'][xb]
  
  plt.clf()
  plt.plot(x,y, linewidth=0.5)
  plt.scatter(xb,yb, s=8, color='red')
  plt.title(burza)
  plt.tight_layout()
  plt.show()



# vykresluje nejvacsie obchody
def plot_naj_obchod_mriezka(data, pocet):
  burza = list(data_burzy.keys())
  
  def graf(burza):
    x = np.arange(data.shape[0])
    y = data['High']
    xb = data.sort_values(by=burza, ascending=False).index[:pocet]
    yb = data['High'][xb]
    
    plt.plot(x,y, linewidth=0.5)
    plt.scatter(xb,yb, s=12, color='red')
    plt.title(burza)
  
  G = GridSpec(4,4)
  plt.clf()
  i = 0
  for j in np.arange(4):
    for k in np.arange(4):
      plt.subplot(G[j,k])
      graf(burza[i])
      i = i+1
      if i==15:
        break
  
  plt.tight_layout()
  plt.show()




plot_naj_obchod_mriezka(data,10)





riadky(data_burzy)
pocet_obchodov(data_burzy)
data_burzy = uprava_datum(data_burzy)
data = data(data_burzy)
data
plot_cena(data)

data2 = data[list(data.columns[:1]) + list(data.columns[5:])]




for i in data_burzy.keys():
  plot_cena_a_burza(data, i)


for i in data_burzy.keys():
  plot_naj_obchod(data, i, 20)


for i in data_burzy.keys():
  plot_nulove_obchody(data, i)

for i in data_burzy.keys():
  plot_nenulove_obchody(data, i)













