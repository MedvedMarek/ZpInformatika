import numpy as np
import pandas as pd
import pickle
import random
import sys
sys.path.append('/home/marek/Dropbox/Programovanie/TWS/obchodovanie_opcie/')
from strategia import nacitaj_strategiu


def nacitaj_data(akcia, okolie, stop_loss):
    """
    Parameters
    ----------
    akcia: str, napriklad 'aapl'
    okolie: int. Je to uz hodnota, ktora je prenasobena 100.
    stop_loss: int. Je to uz hodnota, ktora je prenasobena 100.
    """
    path = f'/media/marek/zaloha/Data/data_pre_nn/{akcia}_{okolie}_{stop_loss}.pkl'
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data


def vypocitaj_index(akcia, data, pravdepodobnost, okolie, burzy):
    """
    Vypocitava ktore riadky z dataframe su vhodne pouzit na trenovanie. Navracia index
    ktory bude pouzity pri generovani dat.
    
    Parameters
    ----------
    akcia: str, napriklad 'aapl'
    data: DataFrame, dataframe jedneho dna, pre ktory sa bude hladat index
    pravdepodobnost: float. HOdnota je pouzita na nacitanie strategie z mysql.
    okolie: int
    burzy: list, pre ktore burzy sa bude pocitat index. Lebo nie vsetky burzh budu zahrnute
           do vypoctov. Niektore burzy pri trenovani nn budu odstranene z dat.
    
    Returns
    -------
    index: list
    """
    strategia = nacitaj_strategiu(pravdepodobnost, f'{akcia}_okolie_{okolie}')
    data = data[720:-720]
    burzy_final = list(set(strategia.keys()) & set(burzy))
    index = set()
    
    for burza in burzy_final:
        for objem in strategia[burza].keys():
            for sviecka in strategia[burza][objem]:
                podmienka = (data[burza] >= objem[0]) & (data[burza] < objem[1]) & (data['sviecka'] >= sviecka[0]) & (data['sviecka'] < sviecka[1])
                index = index | set(data[podmienka].index)

    index = list(index)
    index.sort()
    
    return index


# pravdepodobnost = 0.95 # dolna hranica pravdepodobnosti pri nacitani dat z sql
# okolie = 12 # pre ake okolie sa maju nacitavat data z sql
# stop_loss = 50 # pre aky stop loss sa maju nacitat data z disku
# akcia = 'aapl'


def generuj_data(akcia, pravdepodobnost, okolie, stop_loss, burzy, lookback):
    """
    Generuje data na zaklade strategie ktora je v sql.

    Parameters
    ----------
    akcia: str, napriklad 'aapl'
    pravdepodobnost: float, dolna hranica pravdepodobnosti pri nacitani dat z sql
    okolie: int, pre ake okolie sa maju nacitavat data z sql
    stop_loss: int, pre aky stop loss sa maju nacitavat data z disku
    burzy: list, ktore burzy sa maju zapocitat do trenovania
    lookback: int, kolko krokov sa ma ist do minulosti

    Returns
    -------
    tuple: (np.array (.., 360, 16), np.array (..)), alebo (.., 360, 9) vygenerovane data, predikovane data
    """
    data = nacitaj_data(akcia, okolie, stop_loss)
    datumy = list(data.keys())
    random.shuffle(datumy) # zamiesanie datumov, aby nesli za sebou
    
    # Index dat, ktore boli detekovane strategiou ako potencialne uspesne na 95%.
    ind = {x: vypocitaj_index(akcia, data[x], pravdepodobnost, okolie, burzy) for x in datumy}

    pocet_riadkov = 0
    for i in datumy:
        if len(ind[i]) > 0:
            pocet_riadkov = pocet_riadkov + len(ind[i])


    vygenerovane_buy = []
    pocitadlo = 0
    final_column = ['sviecka', 'knot_up', 'knot_down', 'open_close', 'EMA_24', 'EMA_60', 'RSI_60', 'MACD', 'Signal_line', 'SMA_24',
                    'STDDEV_24', 'Upper_band', 'Lower_band', 'TR', 'ATR_24', 'OBV', 'Stoch_k', 'Stoch_d', 'Parabolic_sar', 'CCI',
                    'Ichimoku_a', 'Ichimoku_b', 'Ichimoku_base_line', 'Ichimoku_conversion_line', 'VWAP', 'Donchain_high', 'Donchain_low',
                    'Donchain_middle', 'CMO']

    vygenerovane_data = np.zeros(shape=(pocet_riadkov, lookback, len(final_column)+len(burzy)))
    
    for x in burzy:
        final_column.append(x)

    for datum in datumy:
        if len(ind[datum]) > 0:
            for index in ind[datum]:
                try:
                    vygenerovane_data[pocitadlo] = data[datum][index-(lookback-1):index+1][final_column].to_numpy()
                    vygenerovane_buy.append(int(data[datum]['market'].loc[index]))
                    pocitadlo += 1
                except Exception as e:
                    print(f'nepriraduje sa datum {datum} a chyba je {e}')

    return vygenerovane_data, vygenerovane_buy



# data = generuj_data('tsla', 0.95, 20, 30, ['arca', 'smart'], 700)

