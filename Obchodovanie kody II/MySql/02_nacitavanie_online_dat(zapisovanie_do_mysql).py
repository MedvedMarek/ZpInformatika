# Dany kod sa viaze na kod 02_nacitavanie_online_dat(upravene).py. Tento kod zapisuje data do
# mysql.
from sqlalchemy import create_engine, Column, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
import numpy as np
import os
from datetime import datetime
import time
import random

path = '/media/marek/zaloha/Data/OHLC_TWS/AAPL/5s/trades/2021_01_04/'
ns = np.load(f'{path}NASDAQ.npy')
ny = np.load(f'{path}NYSE.npy')
sm = np.load(f'{path}SMART.npy')

def prevodDatumu(datum):
    prevod = datetime.strptime(datum, '%Y%m%d %H:%M:%S')
    prevod = int(prevod.timestamp())
    return prevod


vec_prevodDatumu = np.vectorize(prevodDatumu)
ns[:,0] = vec_prevodDatumu(ns[:,0])
ny[:,0] = vec_prevodDatumu(ny[:,0])
sm[:,0] = vec_prevodDatumu(sm[:,0])

Base = declarative_base()

user = 'marek'
password = '138'
host = 'localhost'
database = 'Skusobny'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Nasdaq(Base):
    __tablename__ = 'nasdaq'
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

class Smart(Base):
    __tablename__ = 'smart'
    time = Column(Integer, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low  = Column(Float)
    close= Column(Float)
    volume=Column(Integer)

triedy = {0: Nasdaq, 1:Nyse, 2:Smart}
burzy = {0:ns, 1:ny, 2:sm}

for i in range(200):
    for j in range(3):
        dt = triedy[j](time=burzy[j][i][0], open=burzy[j][i][1], high=burzy[j][i][2], low=burzy[j][i][3], close=burzy[j][i][4], volume=burzy[j][i][5])
        session.add(dt)
        session.commit()
        time.sleep(random.randint(1,6))
    time.sleep(random.randint(1,6))


session.close()


