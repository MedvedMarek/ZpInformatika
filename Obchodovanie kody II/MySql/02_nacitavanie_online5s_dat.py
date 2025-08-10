import time
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

user = 'marek'
password = '138'
host = 'localhost'
database = 'AAPL'


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
    wap = Column(Integer)
    count = Column(Integer)

# Nastavenie engine a reťazca pripojenia
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

# Vytvorenie Session
Session = sessionmaker(bind=engine)
session = Session()

cas = 1707510255

for i in range(5):
    session.expire_all()
    
    # Dotaz na načítanie dát novších ako určitý timestamp
    data = session.query(Smart).filter(Smart.time > cas)
    print(data, cas)
    # Vykonanie dotazu a získanie výsledkov
    new_data = data.all()

    if len(new_data) > 0:
        # Práca s načítanými dátami
        for j in new_data:
            print(j.time, j.open, j.high, j.low, j.close, j.volume, j.wap, j.count)

    if len(new_data) > 0:
        cas = new_data[-1].time
        print(f'cas je: {cas}')
        print('\n')
        
    time.sleep(10)

# Zatvorenie session
session.close()
