# Kod je upravou zakladneho kodu, ktory nacitaval data z disku, upravoval a manipuloval v pandas.
# Potom bol kod zrychleny pomocnou numba. Teraz su data nacitavane do ram a pracuje sa pomotou numba.

# Skumanie strategie, ak je pravdepodobnost, ze ak je sviecka nejakej velkosti a je obchodovana s nejakym
# objemom, tak aka je prevdepodobnost, ze v buducnosti ked nastane takato ista situacia, bude obchod uspesny.
# Pri skumani strategie sa kombinuju objem, burza, velkost sviecky.

import numpy as np
import pandas as pd
import os
import datetime
from numba import jit

from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

Base = declarative_base()

user = 'marek'
password = '138'
host = 'localhost'
database = 'obchodna_strategia_sma'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

akcia = 'AAPL'
rozsah = 300 
burzy = ['arca', 'bats', 'drctedge', 'edgea', 'iex', 'memx', 'nasdaq', 'nyse', 'pearl', 'psx', 'smart']
path = f'/media/marek/zaloha/Data/OHLC_TWS/{akcia}/5s/trades/'

datum = os.listdir(f'{path}')
datum.sort()

okolie = [12,14,16,18,20,22] # pre ake okolia sa bude pocitat strategia
triedy = {} # sem sa budu ukladat triedy, ktore sa vytvorili dynamicky 

def nazov_tabulky(okolie):
    return f'{akcia.lower()}_okolie_{okolie}'


def vytvor_triedu_tabulky(name, table_name):
    """
    Trieda na posielanie dat do databazy pre tabulku strategia_velkost_sviecok_okolia_objemu_niektore_burzy_2.
    
    Parameters
    ----------
    id: je to zakladny udaj pre tabulku do databazy. Toto sa nebude tu aktualizovat.
    burza: str
    ob_min: int, objem minimum
    ob_max: int, objem maximum
    okolie: float, pri akom okoli sa zrealizuje zisk
    sv_min: float, minimalna velkost sviecky
    sv_max: float, maximalna velkost sviecky
    cls_sma_min: float, kolko je nad alebo pod urovnou mean 50. Je to rozdiel close - sma. 
    sklon_min: float, ci akcia rastie, alebo klesa. Je to pocitane ako rozdiel sma, ktore su od seba vzdialene 50
    true: int, kolko bolo dobre identifikovanych obchodov
    false: int, kolko bolo nie dobre identifikovanych obchodov
    suma: int, kolko bolo skumanych obchodov (true+false)
    pr: float, prevdepodobnost spravneho rozhodnutia, ak budu aj v dalsom obchode rovnake parametre
    """
    return type(name, (Base,), {
        '__tablename__': table_name,
        'id': Column(Integer, primary_key=True, autoincrement=True),
        'burza': Column(String),
        'ob_min': Column(Integer),
        'ob_max': Column(Integer),
        'sv_min': Column(Float),
        'sv_max': Column(Float),
        'cls_sma_min': Column(Float),
        'cls_sma_max': Column(Float),
        'sklon_min': Column(Float),
        'sklon_max': Column(Float),
        'true': Column(Integer),
        'false': Column(Integer),
        'suma': Column(Integer),
        'pr': Column(Float)
    })


for i in okolie:
    nazov_triedy = f'Strategia_{i}'
    nazov_tab = nazov_tabulky(i)
    trieda = vytvor_triedu_tabulky(nazov_triedy, nazov_tab)
    triedy[i] = trieda

     
def extract_time_as_int(x) -> int:
    """
    Toto je na upravu casu v nasledujucej funkcii. Vstup je str napriklad 2024-02-03 15:30:25 a iba casova zlozka sa
    prevadza na int a to sposobom, ze sa string oreze a prevedie na int. Toto bude sluzit ako kluc pre porovnavanie v pandas.

    Parameters
    ----------
    x: str

    Returns
    -------
    int
    """
    return int(x[10:12] + x[13:15] + x[16:18])


# Funkcie nacitaj_smart, nacitaj_burzu a zluc_data su doplnene funkcie do kodu. Je to na urychlenie vypoctov. Data sa nacitavaju
# do ramky a nemusia sa stale nacitavat z disku. Nacitanie a uprava dat trva cca 5 minut, ale potom kod ide bez problemov.
def nacitaj_smart():
    """
    Nacitava vsetky datumy pre burzu smart do ramky.
    """
    smart = {}
    for i in datum:
        sm = np.load(f'{path}{i}/SMART.npy')
        sm[:,0] = np.array([extract_time_as_int(t) for t in sm[:,0]])
        smart_df['time'] = sm[:, 0].astype(int)
        smart_df['open'] = sm[:, 1].astype(float)
        smart_df['close'] = sm[:, 4].astype(float)
        smart_df['sviecka'] = (sm[:, 4].astype(float) - sm[:, 1].astype(float)).astype(float)
        smart[i] = smart_df.copy()
    return smart


def nacitaj_burzu(burza):
    """
    Nacitava vsetky datumy pre danu burzu do ramky.
    """
    burza_slovnik = {}
    
    for i in datum:
        br = np.load(f'{path}{i}/{burza.upper()}.npy')
        br[:,0] = np.array([extract_time_as_int(t) for t in br[:,0]])
        bur_df = pd.DataFrame(br[:,[0,5]], columns=['time', burza]).astype({'time': 'int', burza: 'int'})
        burza_slovnik[i] = bur_df.copy()

    return burza_slovnik


@jit(nopython=True)
def vypocitaj_sma(close, sma, lookup) -> np.array:
    """
    Pocita jednoduchy klzavy priemer. Bude sluzit na zistenie, ako velmi sa cena lisi od priemeru.

    Parameters
    ----------
    close: np.array, cena close prevedena na array
    sma: np.array, je to pole nul
    lookup: int, ako daleko sa ma pocitat sma

    Return
    ------
    sma: np.array
    """
    for i in np.arange(lookup, 4680):
        sma[i] = sum(close[i-lookup:i])/lookup

    return sma


@jit(nopython=True)
def vypocitaj_sklon(sma, data_zero) -> np.array:
    """
    Pocita, ci je akcia rastuca, alebo klesajuca. Je to pocitane ako rozdiel dvoch sma, ktore su vzdialene od seba 50.

    Parameters
    ----------
    sma: np.array, prevedeny pandas na array
    data_zero: np.array, nulove hodnoty v array

    Returns
    -------
    data_zeros: np.array, rozdiel medzi sma
    """
    for i in np.arange(50, 4680):
        data_zero[i] = sma[i] - sma[i-50]

    return data_zero


def zluc_data(burza) -> pd.DataFrame:
    """
    Spaja smart a konkretnu burzu v danom dni do jedneho dataframe.
    """
    zlucene_data = {}
    
    for i in datum:
        data = pd.merge(smart_open_close[i], data_burzy[burza][i], how='left', on='time')
        data[burza] = data[burza].fillna(0)
        zlucene_data[i] = data[['open', 'close', 'sviecka', burza]]
        
        zlucene_data_close = zlucene_data[i]['close'].to_numpy() 
        zlucene_data_sma = np.zeros(data.shape[0], dtype=float) 
        zlucene_data[i]['sma_200'] = vypocitaj_sma(zlucene_data_close, zlucene_data_sma, 200) 
        zlucene_data[i]['sma_50'] = vypocitaj_sma(zlucene_data_close, zlucene_data_sma, 50) 
        zlucene_data[i]['cls_sma'] = zlucene_data[i]['close'] - zlucene_data[i]['sma_50'] 
        zlucene_data_zero = np.zeros(data.shape[0], dtype=float)
        zlucene_data_sma_200 = zlucene_data[i]['sma_200'].to_numpy()
        zlucene_data[i]['sklon'] = vypocitaj_sklon(zlucene_data_sma_200, zlucene_data_zero)

    return zlucene_data


# Alokovanie pandas dat na to, aby sa to nemusel stale alokovat nanovo.
smart_df = pd.DataFrame(np.zeros((4680, 4)), columns=['time', 'open', 'close', 'sviecka']).astype({'time': 'int', 'open': 'float','close': 'float', 'sviecka': 'float'})
# Nacitanie smart cez vsetky datumy.
smart_open_close = nacitaj_smart()
# Nacitanie burz cez vsetky datumy
data_burzy = {i: nacitaj_burzu(i) for i in ['arca', 'bats', 'drctedge', 'edgea', 'iex', 'memx', 'nasdaq', 'nyse', 'pearl', 'psx', 'smart']}
# finalne upravene data ktore budu pouzite v algoritme.
nacitaj_data = {i: zluc_data(i) for i in ['arca', 'bats', 'drctedge', 'edgea', 'iex', 'memx', 'nasdaq', 'nyse', 'pearl', 'psx', 'smart']}


@jit(nopython=True)
def najdi_trigger(close_price, data_index, triggers, data_close, data_sviecka, okolie) -> np.array:
    """
    Hladanie spustaca na vypocet strategie. V pripade, ze trigger vyhovuje podmienkam, ta je nastaveny
    na 1. Inak nadobuda 0.

    Funkcia je dekorovana pre NUMBA. Je to spustanie na urovni procesora a vynechava sa standardne prekladanie
    do python prekladaca. Je to na urychlenie kodu.

    Parameters
    ----------
    close_price: np.array, prevedeny pandas na array
    data_index: np.array, prevedeny pandas na array
    triggers: np.array, nulove hodnoty
    data_close: np.array, prevedeny pandas na array
    data_sviecka: np.array, prevedeny pandas na array
    okolie: pre ake okolie sa bude pocitat uspesnost strategie

    Returns
    -------
    triggers: np.array
    """
    for idx, i in enumerate(data_index):
        if data_sviecka[idx] > 0:
            for p in range(rozsah):
                if close_price[i+p] > close_price[i] + okolie:
                    triggers[idx] = 1
                    break
        else:
            for p in range(rozsah):
                if close_price[i+p] < close_price[i] - okolie:
                    triggers[idx] = 1
                    break
    return triggers


def vypocitaj_strategiu(datum, objem, okolie, velkost_sviecky, burza, close_sma, sklon_sma) -> pd.DataFrame:
    """
    Vypocet uspesnosti strategie.
    
    Parameters
    ----------
    datum: str, napr. '2024_03_22'
    objem: int, aka minimalna hranica objemu bude pre burza
    okolie: int, ake okolie bodu od spustaca sa ma pocitat
    velkost_sviecky: [int, int], je to interval v ktorom sa ma pohybovat sviecka
    burza: str, aka doplnkova burza ku smart sa bude davat
    close_sma: [float, float], interval v ktorom sa pohybuje sma
    sklon_sma: [float, float], interval v ktorom sa pohybuje sklon grafu

    Returns
    -------
    data: dataFrame
    
    Pozor!!!
    --------
    Nacitane data su orezane z konca obchodneho dna. Je to z dovodu, ze nie vzdy sa dokazu 
    pohnut v rozmedzi okolia. Preto nebude spustany falosny trigger.
    """
    dt = nacitaj_data[burza][datum]
    dt1 = dt[360:-720]
    
    # Toto je zretazene pre rychlejsie spracovanie
    data = dt1[
        (dt1[burza] > objem[0]) & (dt1[burza] <= objem[1]) &
        (dt1['sviecka'] >= velkost_sviecky[0]) & (dt1['sviecka'] < velkost_sviecky[1]) &
        (dt1['cls_sma'] >= close_sma[0]) & (dt1['cls_sma'] < close_sma[1]) &
        (dt1['sklon'] >= sklon_sma[0]) & (dt1['sklon'] < sklon_sma[1])
    ].copy()

    # Optimalizacia pre rychlejsi chod kodu
    close_price = dt['close'].to_numpy()
    data_index = data.index.to_numpy()
    triggers = np.zeros(data.shape[0], dtype=int)
    data_close = data['close'].to_numpy()
    data_sviecka = data['sviecka'].to_numpy()
    data['trigger'] = najdi_trigger(close_price, data_index, triggers, data_close, data_sviecka, okolie)

    return data


velkost_sviecky = [[-0.3, -0.25], [-0.25, -0.22], [-0.22, -0.2], [-0.2, -0.18], [-0.18, -0.16], [-0.16, -0.14],
                   [-0.14, -0.12], [-0.12, -0.1], [-0.1, -0.09], [-0.09, -0.08], [-0.08, -0.07], [-0.07, -0.06],
                   [-0.06, -0.05], [-0.05, -0.04], [-0.04, -0.03], [-0.03, -0.02], [-0.02, -0.01],
                   [0.01, 0.02], [0.02, 0.03], [0.03, 0.04], [0.04, 0.05], [0.05, 0.06], [0.06, 0.07], [0.07, 0.08],
                   [0.08, 0.09], [0.09, 0.1], [0.1, 0.12], [0.12, 0.14], [0.14, 0.16], [0.16, 0.18], [0.18, 0.2],
                   [0.2, 0.22], [0.22, 0.25], [0.25, 0.3]]

objem = [[0,3], [3,6], [6,9], [9,12], [12,15], [15,18], [18,21], [21,24], [24,27], [27,30], [30,35], [35,40],
         [40,45], [45,50], [50,55], [55,60], [60,65], [65,75], [75,85], [85,100], [100,120], [120,150], [150,180],
         [180,210], [210,250], [250,300], [300, 3000]]


close_sma = [[-2, -1], [-1, -0.8], [-0.8, -0.6], [-0.6, -0.4], [-0.4, -0.2], [-0.2, 0],
             [0, 0.2], [0.2, 0.4], [0.4, 0.6], [0.6, 0.8], [0.8, 1], [1, 2]]


sklon_sma = [[-1, -0.6], [-0.6, -0.5], [-0.5, -0.4], [-0.4, -0.3], [-0.3, -0.2], [-0.2, -0.1], [-0.1, 0],
             [0, 0.1], [0.1, 0.2], [0.2, 0.3], [0.3, 0.4], [0.4, 0.5], [0.5, 0.6], [0.6, 1]]



session = Session()

for n in okolie:
    oko = n/100 # aby som dostal okolie v desatinom mieste. Ako napriklad 0.12.
    for m in burzy:
        for i in objem:
            for l in velkost_sviecky:
                for sma in close_sma:
                    for sklon in sklon_sma:
                        false = 0
                        true = 0
                        
                        for k in datum:
                            data = vypocitaj_strategiu(k, i, oko, l, m, sma, sklon)
                            velkost = data.shape[0]
                            suma = data['trigger'].sum()
                            true = true + suma
                            false = false + (velkost - suma)

                        pravdep = true/(true+false) if true+false != 0 else 0    
                        zapis = triedy[n](burza=m, ob_min=i[0], ob_max=i[1], sv_min=l[0], sv_max=l[1], cls_sma_min=sma[0], cls_sma_max=sma[1],
                                          sklon_min=sklon[0], sklon_max=sklon[1], true=true, false=false, suma=true+false, pr=pravdep)
                        session.add(zapis)
                        session.commit()
            
                        print(f'burza: {m:<8}  objem: [{i[0]:<3} {i[1]:<3}]  sviecka: [{l[0]:<5} {l[1]:<5}]  cls: [{sma[0]:<4} {sma[1]:<4}]  sklon: [{sklon[0]:<4} {sklon[1]:<4}]  ture: {true:<5}  false: {false:<5}  pr: {pravdep:.4f}')
                    print('')

session.close()
