import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
path = '/home/marek/Dropbox/Programovanie kody/RStudio/Obchodovanie kody/Kody statistika/data_zakladne_skusobne.csv'

"""
xxx_ch_0 = change rano
xxx_ch_1 = change vecer
xxx_s_0  = shortable shares rano
xxx_s_1  = shortable shares vecer
"""

data = pd.read_csv(path)

x = np.arange(22)
y1 = data.spy_ch_0
y2 = data.spy_ch_1
y3 = data.aapl_ch_0
y4 = data.aapl_ch_1
y5 = data.amd_ch_0
y6 = data.amd_ch_1
y7 = data.msft_ch_0
y8 = data.msft_ch_1
y9 = data.nvda_ch_0
y10 = data.nvda_ch_1

yy1 = data.spy_s_0
yy2 = data.spy_s_1
yy3 = data.aapl_s_0
yy4 = data.aapl_s_1
yy5 = data.amd_s_0
yy6 = data.amd_s_1
yy7 = data.msft_s_0 
yy8 = data.msft_s_1
yy9 = data.nvda_s_0 
yy10= data.nvda_s_1


plt.clf()
plt.plot(x,y1,linewidth=0.5,color='magenta',label='poobede')
plt.plot(x,y2,linewidth=0.5,color='blue',label='vecer')
plt.legend()
plt.show()


def plot1(x,y1,y2):
  plt.clf()
  plt.plot(x,y1, linewidth=0.5, color='magenta', label='poobede')
  plt.plot(x,y2, linewidth=0.5, color='blue', label='vecer')
  plt.legend()
  plt.tight_layout()
  plt.show()

def plot2(x,y1,y2,yy1,yy2):
  plt.clf()
  
  plt.subplot(2,1,1)
  plt.plot(x,y1, linewidth=0.5, color='magenta', label='poobede')
  plt.plot(x,y2, linewidth=0.5, color='blue', label='vecer')
  plt.legend()
  
  plt.subplot(2,1,2)
  plt.plot(x,yy1, linewidth=0.5, color='magenta', label='poobede')
  plt.plot(x,yy2, linewidth=0.5, color='blue', label='vecer')
  plt.legend()
  
  plt.tight_layout()
  plt.show()

plot1(x,yy1,yy2)
plot2(x,y1,y2,yy1,yy2)
plot2(x,y3,y4,yy3,yy4)
plot2(x,y5,y6,yy5,yy6)
plot2(x,y7,y8,yy7,yy8)
plot2(x,y9,y10,yy9,yy10)





y2.to_numpy()

np.correlate(y1.to_numpy(), yy1.to_numpy())
np.corrcoef(y1.to_numpy(), yy1.to_numpy())











