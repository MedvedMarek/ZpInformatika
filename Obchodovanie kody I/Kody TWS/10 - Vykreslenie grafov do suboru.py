import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import sklearn.preprocessing as sk
import os
import sys

from importlib import reload
sys.path.append('/home/marek/Dropbox/Programovanie kody/RStudio/Obchodovanie kody/Kody TWS/')
import Nacitavanie_a_uprava_dat as fun
import Vykreslovanie_dat_dane_do_triedy as vykreslovanie
reload(vykreslovanie)
reload(fun)
path = '/home/marek/Dropbox/Data/TWS/'

# ------------------------- Nacitanie dat zo zlozky Data ---------------------------------------
datumy = os.listdir(path)
datumy.sort()
data = {x: fun.nacitaj_akciu(path+x+'/', 'AMD') for x in datumy}

# ------------------------- Uprava a transformacia dat -----------------------------------------
data = {x:fun.orez_na_obchodne_hodiny(data[x]) for x in datumy}


# ------------------------- Vykreslovanie dat --------------------------------------------------
vykresli = vykreslovanie.Vykreslovanie(data)

vykresli.najvacsie_obchody_burza()
vykresli.najvacsie_obchody_cez_den()
vykresli.najvacsie_obchody_cez_den_vw()
vykresli.najvacsie_obchody_cez_tyzden()
vykresli.najvacsie_obchody_cez_tyzden_vw()





# ------------------------- Docasne kody -------------------------------------------------------

# Vykreslenie vsetkych burz do jedneho grafu, kde sa zobrazuju dve akcie
for i in datumy:
  plot.najvacsie_obchody_cez_den_2('AMD', data[i], data_ap[i], volume_AMD, volume_AAPL, 'subor')








