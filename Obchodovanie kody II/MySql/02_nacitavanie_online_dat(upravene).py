# Dany kod sa viaze na kod 02_nacitavanie_online_dat(generovanie_dat).py. Ten kod generuje data
# v nejakom intervale a tu sa v nejakom intervale zobrazuju. Je to skusobny subor pre vykreslovanie
# streamovanych dat.
import time
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime

user = 'marek'
password = '138'
host = 'localhost'
database = 'Skusobny'


# Definícia základnej triedy pre modely
Base = declarative_base()

# Definícia modelu pre tabuľku
class Smart(Base):
    __tablename__ = 'smart'
    time = Column(Integer, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low  = Column(Float)
    close= Column(Float)
    volume=Column(Integer)

class Nyse(Base):
    __tablename__ = 'nyse'
    time = Column(Integer, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low  = Column(Float)
    close= Column(Float)
    volume=Column(Integer)

class Nasdaq(Base):
    __tablename__ = 'nasdaq'
    time = Column(Integer, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low  = Column(Float)
    close= Column(Float)
    volume=Column(Integer)


# Nastavenie engine a reťazca pripojenia
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

# Vytvorenie Session
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

cas = [0,0,0]

for i in range(200):
    session.expire_all()
    session = Session()

    # Dotaz na načítanie dát novších ako určitý timestamp
    smart  = session.query(Smart).filter(Smart.time > cas[0])
    nyse   = session.query(Nyse).filter(Nyse.time > cas[1])
    nasdaq = session.query(Nasdaq).filter(Nasdaq.time > cas[2])
    # Vykonanie dotazu a získanie výsledkov
    new_smart = smart.all()
    new_nyse = nyse.all()
    new_nasdaq = nasdaq.all()

    for new_data in [new_smart, new_nyse, new_nasdaq]:
        if len(new_data) > 0:
            # Práca s načítanými dátami
            for j in new_data:
                print(j.time, j.open, j.high, j.low, j.close, j.volume)

    for index, new_data in enumerate([new_smart, new_nyse, new_nasdaq]):
        if len(new_data) > 0:
            cas[index] = new_data[-1].time
        
    Session.remove()
    time.sleep(0.5)

# Zatvorenie session
session.close()







    
