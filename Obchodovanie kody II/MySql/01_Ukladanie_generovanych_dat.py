from sqlalchemy import create_engine, Column, Float, Integer, Timestamp
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

Base = declarative_base()

user = 'marek'
password = '138'
host = 'localhost'
database = 'AAPL'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

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


jedna = Smart(time=2, open=10, high=10, low=10, close=10, volume=10)
session.add(jedna)
session.commit()
session.close()


