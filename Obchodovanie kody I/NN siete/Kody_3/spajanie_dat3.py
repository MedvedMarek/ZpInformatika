import numpy as np
import pandas as pd
import os

class KontrolaAUpravaDat:
    """
    Kontroluje a upravuje stiahnute data.
    Pre kazdu burzu je referencna burza SMART. To sa jedna o rozsah dat a aj o rozsah obchodnych hoidn. Burza SMART je
    stiahnuta a uplna. V pripade, ze nebola stiahnuta, tak bola manualne upravena podla najpodobnejsej burzy ku SMART.
    A to burzou: BATS, alebo ARCA. Data su kontrolovane vo svojich zlozkach a tam aj ostavaju. Po kontrole a uprave dat
    zlozky ostavaju pouzitelne pre dalsie pouzite. A to je spajanie dat do blokov pre nacitanie do NN sieti.
    """
    def __init__(self):
        pass











path = '/media/marek/zaloha/Data/OHLC_TWS/AAPL/5s/bid/2021_01_04/ARCA.npy'
x = np.load(path)

x
