import numpy as np
import pickle
import sys
sys.path.append('/home/marek/Dropbox/Programovanie/TWS/obchodovanie_opcie/')
from strategia import nacitaj_strategiu

from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

Base = declarative_base()
user = 'marek'
password = '138'
host = 'localhost'
database = 'obchodna_strategia_stop_loss'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind= engine)

akcia = 'aapl'


class AAPL(Base):
    __tablename__ = akcia
    id = Column(Integer, primary_key=True, autoincrement=True)
    burza = Column(String(255))
    okolie = Column(Integer)
    stop_loss = Column(Integer)
    poc_ob = Column(String(255))
    pravd = Column(Float)


def nacitaj_data(okolie, stop_loss):
    """
    Parameters
    ----------
    okolie: int. Je to uz hodnota, ktora je prenasobena 100.
    stop_loss: int. Je to uz hodnota, ktora je prenasobena 100.
    """
    path = f'/media/marek/zaloha/Data/data_pre_nn/{akcia}_{okolie}_{stop_loss}.pkl'
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data

def vypis_strategiu(data, okolie, stra, bur):
    index = set()
    sumar = []
    datumy = list(data[okolie].keys())
    for datum in datumy:
        data1 = data[okolie][datum][360:-720]
        # for burza in stra[okolie].keys():
        for burza in [bur]:
            # print(' ')
            for volume in stra[okolie][burza].keys():
                for sviecka in stra[okolie][burza][volume]:
                    podmienka = (data1[burza] > volume[0]) & (data1[burza] < volume[1]) & (data1['sviecka'] > sviecka[0]) & (data1['sviecka'] < sviecka[1])
                    if len(data1[podmienka].index) > 1:
                        sumar = sumar + list(data1[podmienka]['market'].values)
                    index = index | set(data1[podmienka].index)
    try:
        pravdepodobnost = round(sum(sumar)/len(sumar), 4)
        pocet_obchodov = len(index)
        print(f'percento uspesnosti pre okolie {okolie}: {pravdepodobnost} pocet obchodov: {pocet_obchodov}')

        return pravdepodobnost, pocet_obchodov
    except:
        pass


data_25 = {x: nacitaj_data(x,25) for x in [12, 14, 16, 18, 20, 22]}
data_30 = {x: nacitaj_data(x,30) for x in [12, 14, 16, 18, 20, 22]}
data_35 = {x: nacitaj_data(x,35) for x in [12, 14, 16, 18, 20, 22]}
data_40 = {x: nacitaj_data(x,40) for x in [12, 14, 16, 18, 20, 22]}
data_50 = {x: nacitaj_data(x,50) for x in [12, 14, 16, 18, 20, 22]}
stra_95 = {x: nacitaj_strategiu(0.95, f'amd_okolie_{x}') for x in [12, 14, 16, 18, 20, 22]}

dt = {25: data_25, 30: data_30, 35: data_35, 40: data_40, 50: data_50}
st = {'stra_95': stra_95}

session = Session()

for data in dt.keys():
    print('')
    print(data)
    for burza in ['arca','bats','drctedge','edgea','iex','memx','nasdaq','nyse','pearl','psx','smart']:
        print(burza)
        for stra in st.keys():
            for i in [12, 14, 16, 18, 20, 22]:
                try:
                    pravdepodobnost, pocet_obchodov = vypis_strategiu(dt[data], i, st[stra], burza)
                    zapis = AAPL(burza=burza, okolie=i, stop_loss=data, poc_ob=pocet_obchodov, pravd=pravdepodobnost)
                    session.add(zapis)
                    session.commit()
                except:
                    pass

session.close()

# index = list(index)
# index.sort()

