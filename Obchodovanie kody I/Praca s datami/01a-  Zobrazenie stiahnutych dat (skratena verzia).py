import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sklearn.preprocessing as sk
from matplotlib.gridspec import GridSpec


path = '/home/marek/Dropbox/Data/TWS/amd_22_12_21/'
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


data_burzy = {'amex':amex, 'arca':arca, 'bats':bats, 'bex':bex, 'byx':byx, 'chx':chx, 'drctedge':drctedge,
              'edgea':edgea, 'iex':iex, 'memx':memx, 'nyse':nyse, 'psx':psx, 'smart':smart, 'pearl':pearl,
              'island':island}


# ------------------------------------ Funkcie ---------------------------------------
def uprava_datum(data):
  for i in data:
    data[i].DateTime = data[i].DateTime - 21600
    data[i].DateTime = pd.to_datetime(data[i].DateTime, unit='s')
  return(data)

def data(data):
  ohlc = data['arca']
  ohlc = ohlc.drop(labels='Volume', axis=1)
  
  for i in data.keys():
    ohlc = pd.merge(ohlc, data[i][['DateTime', 'Volume']], how='left', on='DateTime')
    ohlc.columns = list(ohlc.columns[:-1]) + [i]
  
  ohlc.columns = list(data['arca'].columns[:5]) + list(data.keys())
  ohlc = ohlc.assign(Volume = ohlc[ohlc.columns[5:]].apply(np.sum, axis=1)) 
  ohlc[ohlc.columns[5:]] = ohlc[ohlc.columns[5:]].apply(lambda x: x*100, axis=1) 
  return(ohlc)

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


riadky(data_burzy)
pocet_obchodov(data_burzy)
data_burzy = uprava_datum(data_burzy)
data = data(data_burzy)

plot_naj_obchod_mriezka(data,100)
















