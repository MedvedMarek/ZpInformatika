# Online stahovanie dat a ich ukladanie do databazy. 
import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
import threading
import time
import numpy as np

#----------------------------------------------------------------------
from sqlalchemy import create_engine, Column, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError
import pymysql

Base = declarative_base()

vlakno = 9
user = 'marek'
password = '138'
host = 'localhost'
akcia = 'SPY'
database = 'x_SPY'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
Base.metadata.create_all(engine)


class Arca(Base):
    __tablename__ = 'arca'
    time = Column(Integer, primary_key=True)
    volume=Column(Integer)

class Bats(Base):
    __tablename__ = 'bats'
    time = Column(Integer, primary_key=True)
    volume=Column(Integer)

class Drctedge(Base):
    __tablename__ = 'drctedge'
    time = Column(Integer, primary_key=True)
    volume=Column(Integer)

class Edgea(Base):
    __tablename__ = 'edgea'
    time = Column(Integer, primary_key=True)
    volume=Column(Integer)

class Iex(Base):
    __tablename__ = 'iex'
    time = Column(Integer, primary_key=True)
    volume=Column(Integer)

class Memx(Base):
    __tablename__ = 'memx'
    time = Column(Integer, primary_key=True)
    volume=Column(Integer)

class Nasdaq(Base):
    __tablename__ = 'nasdaq'
    time = Column(Integer, primary_key=True)
    volume=Column(Integer)

class Nyse(Base):
    __tablename__ = 'nyse'
    time = Column(Integer, primary_key=True)
    volume=Column(Integer)

class Pearl(Base):
    __tablename__ = 'pearl'
    time = Column(Integer, primary_key=True)
    volume=Column(Integer)

class Psx(Base):
    __tablename__ = 'psx'
    time = Column(Integer, primary_key=True)
    volume=Column(Integer)

class Smart(Base):
    __tablename__ = 'smart'
    time = Column(Integer, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low  = Column(Float)
    close= Column(Float)
    volume=Column(Integer)


triedy = {1:Arca, 2:Bats, 3:Drctedge, 4:Edgea, 5:Iex, 6:Memx, 7:Nasdaq, 8:Nyse, 9:Pearl, 10:Psx, 11:Smart}


#--------------------------------------------------------------------
class IBApi(EWrapper, EClient):
  def __init__(self):
    EClient.__init__(self,self)
  
  def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
    super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
    bot.on_bar_update(reqId, time, open_, high, low, close, volume)


class Bot:
  ib = None
  
  def __init__(self):
    self.ib = IBApi()
    self.ib.connect("127.0.0.1", 7497, vlakno)

    self.session_factory = sessionmaker(bind=engine)
    self.session = scoped_session(self.session_factory)
    
    ib_thread = threading.Thread(target=self.run_loop, daemon=True)
    ib_thread.start()
    time.sleep(1)
            
    contract1 = Contract()
    contract1.symbol = akcia
    contract1.secType = "STK"
    contract1.exchange = "ARCA"
    contract1.currency = "USD"
    
    contract2 = Contract()
    contract2.symbol = akcia
    contract2.secType = "STK"
    contract2.exchange = "BATS"
    contract2.currency = "USD"
    
    contract3 = Contract()
    contract3.symbol = akcia
    contract3.secType = "STK"
    contract3.exchange = "DRCTEDGE"
    contract3.currency = "USD"
    
    contract4 = Contract()
    contract4.symbol = akcia
    contract4.secType = "STK"
    contract4.exchange = "EDGEA"
    contract4.currency = "USD"
    
    contract5 = Contract()
    contract5.symbol = akcia
    contract5.secType = "STK"
    contract5.exchange = "IEX"
    contract5.currency = "USD"
    
    contract6 = Contract()
    contract6.symbol = akcia
    contract6.secType = "STK"
    contract6.exchange = "MEMX"
    contract6.currency = "USD"

    contract7 = Contract()
    contract7.symbol = akcia
    contract7.secType = "STK"
    contract7.exchange = "NASDAQ"
    contract7.currency = "USD"

    contract8 = Contract()
    contract8.symbol = akcia
    contract8.secType = "STK"
    contract8.exchange = "NYSE"
    contract8.currency = "USD"
    
    contract9 = Contract()
    contract9.symbol = akcia
    contract9.secType = "STK"
    contract9.exchange = "PEARL"
    contract9.currency = "USD"

    contract10 = Contract()
    contract10.symbol = akcia
    contract10.secType = "STK"
    contract10.exchange = "PSX"
    contract10.currency = "USD"
    
    contract11 = Contract()
    contract11.symbol = akcia
    contract11.secType = "STK"
    contract11.exchange = "SMART"
    contract11.currency = "USD"
    
    self.ib.reqRealTimeBars(1, contract1, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(2, contract2, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(3, contract3, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(4, contract4, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(5, contract5, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(6, contract6, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(7, contract7, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(8, contract8, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(9, contract9, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(10, contract10, 1, "TRADES", 1, [])
    self.ib.reqRealTimeBars(11, contract11, 1, "TRADES", 1, [])
    
    
  def run_loop(self):
    self.ib.run()
  
  def on_bar_update(self, reqId, time, open_, high, low, close, volume):
    try:
        if reqId != 11:
            ulozenie = triedy[reqId](time=time, volume=volume)
        else:
            ulozenie = triedy[11](time=time, open=open_, high=high, low=low, close=close, volume=volume)
        self.session.add(ulozenie)
        self.session.commit()
    except IntegrityError:
        print(f'Pokus o prepis udajov: {reqId} {time}')
        self.session.rollback()
    finally:
        self.session.remove()


bot = Bot()


