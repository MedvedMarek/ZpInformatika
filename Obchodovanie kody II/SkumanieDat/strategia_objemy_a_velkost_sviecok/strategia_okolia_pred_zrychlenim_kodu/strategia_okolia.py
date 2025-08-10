# Skumanie strategie, ak je pravdepodobnost, ze ak je sviecka nejakej velkosti a je obchodovana s nejakym
# objemom, tak aka je prevdepodobnost, ze v buducnosti ked nastane takato ista situacia, bude obchod uspesny.
# Pri skumani strategie sa kombinuju objem, burza, velkost sviecky.

import numpy as np
import pandas as pd
import os
import datetime

from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

Base = declarative_base()

user = 'marek'
password = '138'
host = 'localhost'
database = 'obchodna_strategia'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

akcia = 'AAPL'
path = f'/media/marek/zaloha/Data/OHLC_TWS/{akcia}/5s/trades/'
nazov_tabulky = 'aapl_okolie_20'
okolie = 0.20


class Strategia(Base):
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
    true: int, kolko bolo dobre identifikovanych obchodov
    false: int, kolko bolo nie dobre identifikovanych obchodov
    suma: int, kolko bolo skumanych obchodov (true+false)
    pr: float, prevdepodobnost spravneho rozhodnutia, ak budu aj v dalsom obchode rovnake parametre
    """
    __tablename__ = nazov_tabulky
    id     = Column(Integer, primary_key=True, autoincrement=True)
    burza  = Column(String)
    ob_min = Column(Integer)
    ob_max = Column(Integer)
    sv_min = Column(Float)
    sv_max = Column(Float)
    true   = Column(Integer)
    false  = Column(Integer)
    suma   = Column(Integer)
    pr     = Column(Float)


def nacitaj_data(datum, burza) -> pd.DataFrame:
    """
    Primarne nacitava smart, aby sa mohli skumat sviecky a potom doplna jednu burzu na ktorej
    sa deju ostatne predikcie.
    
    Parameters
    ----------
    datum: str
    burza: str, pre aku burzu sa bude predikovat
    
    Returns
    -------
    data: dataFrame
    """    
    dtype1 = {'time': 'datetime64[ns]', 'open': 'float','close': 'float'}
    dtype2 = {'time': 'datetime64[ns]', f'{burza}': 'int'}

    smart = np.load(f'{path}{datum}/SMART.npy')
    bur = np.load(f'{path}{datum}/{burza.upper()}.npy')
    smart = pd.DataFrame(smart[:, [0,1,4]], columns=['time', 'open', 'close'])
    bur = pd.DataFrame(bur[:, [0,5]], columns=['time', burza])
    smart = smart.astype(dtype=dtype1)
    bur = bur.astype(dtype=dtype2)
    data = pd.merge(smart, bur, how='left',on='time')
    data[burza] = data[burza].fillna(0)
    
    return data[['open', 'close', f'{burza}']]


def vypocitaj_strategiu(datum, objem, okolie, velkost_sviecky, burza) -> pd.DataFrame:
    """
    Vypocet uspesnosti strategie.
    
    Parameters
    ----------
    datum: str, napr. '2024_03_22'
    objem: int, aka minimalna hranica objemu bude pre burza
    okolie: int, ake okolie bodu od spustaca sa ma pocitat
    velkost_sviecky: [int, int], je to interval v ktorom sa ma pohybovat sviecka
    burza: str, aka doplnkova burza ku smart sa bude davat

    Returns
    -------
    data: dataFrame
    
    Pozor!!!
    --------
    Nacitane data su orezane z konca obchodneho dna. Je to z dovodu, ze nie vzdy sa dokazu 
    pohnut v rozmedzi okolia. Preto nebude spustany falosny trigger.
    """
    dt = nacitaj_data(datum,burza)
    dt1 = dt[360:-720]
    
    data = dt1[(dt1[burza] > objem[0]) & (dt1[burza] <= objem[1])].copy()
    data['sviecka'] = np.where(data['open'] < data['close'], 0, 1)
    data['velkost_sv'] = np.where(data['sviecka'] == 0, data['close'] - data['open'], data['open'] - data['close'])    
    data = data[(data['velkost_sv'] > velkost_sviecky[0]) & (data['velkost_sv'] < velkost_sviecky[1])]
    data['trigger'] = int(0)
    index = data.index

    for i in index:
        if data.loc[i,'sviecka'] == 0:
            if (dt.loc[i:, ['close']] > (dt.loc[i, 'close']+okolie)).any(axis=1).any():
                data.loc[i, 'trigger'] = int(1)
            else:
                pass
        else:
            if (dt.loc[i:, ['close']] < (dt.loc[i,'close']-okolie)).any(axis=1).any():
                data.loc[i, 'trigger'] = int(1)
            else:
                pass

    return data


datum = os.listdir(f'{path}')
datum.sort()
velkost_sviecky = [[0.01, 0.02], [0.02, 0.03], [0.03, 0.04], [0.04, 0.05], [0.05, 0.06], [0.06, 0.07], [0.07, 0.08], [0.08, 0.09], [0.09, 0.1], [0.1, 0.12], [0.12, 0.14], [0.14, 0.16], [0.16, 0.18], [0.18, 0.2], [0.2, 0.22], [0.22, 0.25], [0.25, 0.3]]
burzy = ['arca', 'bats', 'drctedge', 'edgea', 'iex', 'memx', 'nasdaq', 'nyse', 'pearl', 'psx', 'smart']
objem = [[0,3], [3,6], [6,9], [9,12], [12,15], [15,18], [18,21], [21,24], [24,27], [27,30], [30,35], [35,40], [40,45], [45,50], [50,55], [55,60], [60,65], [65,75], [75,85], [85,100], [100,120], [120,150], [150,180], [180,210], [210,250], [250,300], [300, 3000]]


for m in burzy:
    for i in objem:
        for l in velkost_sviecky:
            true = 0
            false = 0
            
            for k in datum:
                data = vypocitaj_strategiu(k, i, okolie, l, m)
                velkost = data.shape[0]
                suma = data['trigger'].sum()
                true = true + suma
                false = false + (velkost - suma)
                    
                if true+false == 0:
                    pravdep = 0
                else:
                    pravdep = true/(true+false)

            zapis = Strategia(burza=m, ob_min=i[0], ob_max=i[1], sv_min=l[0], sv_max=l[1], true=true, false=false, suma=true+false, pr=pravdep)
            session.add(zapis)
            session.commit()
            session.close()
            print(f'burza: {m:<8}  objem: [{i[0]:<3} {i[1]:<3}]  sviecka: [{l[0]:<4} {l[1]:<4}]  ture: {true:<5}  false: {false:<5}  pr: {pravdep:.4f}')
        print('')





