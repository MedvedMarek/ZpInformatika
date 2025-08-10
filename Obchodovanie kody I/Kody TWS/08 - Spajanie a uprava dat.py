import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = '/home/marek/Dropbox/Data/TWS Docasne prelozene  data/2023_05_26/'
paths = [path+'w1/', path+'wx/']

burzy = ['AMEX','ARCA','BATS','BEX','BYX','CHX','DRCTEDGE','EDGEA','IEX','MEMX','NYSE','PSX','SMART','PEARL','ISLAND']
akcie = ['AMD']

def zluc_data(paths): 
  """
  Zlucuje data, ktore su ulozene vo viacerych zlozkach, lebo bolo prerusene stahovanie. Staci zadat cesty ku 
  zlozkam a kod spoji jednotlive akcie a burzy a ulozi to nanovo do cesty /home/marek.
  
  Parameters
  ----------
  paths:  list
          Je to list v ktorom je ulozena kazda cesta k danej zlozke.
  
  Returns
  -------
  data:   dict
          Je to slovnik v ktorom su ulozene vsetky spojene data.
  """
  data = {}
  
  for i in burzy:
    for j in akcie:
      data[j+'_'+i] = np.load(paths[0]+j+'_'+i+'.npy')
  
  if len(paths)>1:
    for i in paths[1:]:
      for j in burzy:
        for k in akcie:
          data[k+'_'+j] = np.concatenate((data[k+'_'+j], np.load(i+k+'_'+j+'.npy')), axis=0)
    
  for i in burzy:
    for j in akcie:
      np.save(path+j+'_'+i+'.npy',data[j+'_'+i])
        
  return(data)

zluc_data(paths)

