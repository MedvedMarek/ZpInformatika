from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import numpy as np
import time
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
from datetime import datetime
import random
from memory_profiler import profile


Base = declarative_base()
user = 'marek'
password = '138'
host = 'localhost'
database = 'AAPL'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

class Arca(Base):
    __tablename__ = 'arca'
    time = Column(Integer, primary_key=True)
    close= Column(Float)
    volume=Column(Integer)
    count =Column(Integer)
    def to_dict(self):
        return {'arca_time': self.time, 'arca_close': self.close, 'arca_volume': self.volume}

class Bats(Base):
    __tablename__ = 'bats'
    time = Column(Integer, primary_key=True)
    close= Column(Float)
    volume=Column(Integer)
    count =Column(Integer)
    def to_dict(self):
        return {'bats_time': self.time, 'bats_close': self.close, 'bats_volume': self.volume}

class Drctedge(Base):
    __tablename__ = 'drctedge'
    time = Column(Integer, primary_key=True)
    close= Column(Float)
    volume=Column(Integer)
    count =Column(Integer)
    def to_dict(self):
        return {'drctedge_time': self.time, 'drctedge_close': self.close, 'drctedge_volume': self.volume}

class Edgea(Base):
    __tablename__ = 'edgea'
    time = Column(Integer, primary_key=True)
    close= Column(Float)
    volume=Column(Integer)
    count =Column(Integer)
    def to_dict(self):
        return {'edgea_time': self.time, 'edgea_close': self.close, 'edgea_volume': self.volume}

class Iex(Base):
    __tablename__ = 'iex'
    time = Column(Integer, primary_key=True)
    close= Column(Float)
    volume=Column(Integer)
    count =Column(Integer)
    def to_dict(self):
        return {'iex_time': self.time, 'iex_close': self.close, 'iex_volume': self.volume}

class Memx(Base):
    __tablename__ = 'memx'
    time = Column(Integer, primary_key=True)
    close= Column(Float)
    volume=Column(Integer)
    count =Column(Integer)
    def to_dict(self):
        return {'memx_time': self.time, 'memx_close': self.close, 'memx_volume': self.volume}


class Nasdaq(Base):
    __tablename__ = 'nasdaq'
    time = Column(Integer, primary_key=True)
    close= Column(Float)
    volume=Column(Integer)
    count =Column(Integer)
    def to_dict(self):
        return {'nasdaq_time': self.time, 'nasdaq_close': self.close, 'nasdaq_volume': self.volume}

class Nyse(Base):
    __tablename__ = 'nyse'
    time = Column(Integer, primary_key=True)
    close= Column(Float)
    volume=Column(Integer)
    count =Column(Integer)
    def to_dict(self):
        return {'nyse_time': self.time, 'nyse_close': self.close, 'nyse_volume': self.volume}

class Pearl(Base):
    __tablename__ = 'pearl'
    time = Column(Integer, primary_key=True)
    close= Column(Float)
    volume=Column(Integer)
    count =Column(Integer)
    def to_dict(self):
        return {'pearl_time': self.time, 'pearl_close': self.close, 'pearl_volume': self.volume}

class Psx(Base):
    __tablename__ = 'psx'
    time = Column(Integer, primary_key=True)
    close= Column(Float)
    volume=Column(Integer)
    count =Column(Integer)
    def to_dict(self):
        return {'psx_time': self.time, 'psx_close': self.close, 'psx_volume': self.volume}

class Smart(Base):
    __tablename__ = 'smart'
    time = Column(Integer, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low  = Column(Float)
    close= Column(Float)
    volume=Column(Integer)
    count =Column(Integer)
    def to_dict(self):
        return {'smart_time': self.time, 'open': self.open, 'high': self.high, 'low': self.low,
                'smart_close': self.close, 'smart_volume': self.volume}


burzy = {'arca':Arca, 'bats':Bats, 'drctedge':Drctedge, 'edgea':Edgea, 'iex':Iex, 'memx':Memx, 'nasdaq':Nasdaq, 'nyse':Nyse, 'pearl':Pearl, 'psx':Psx, 'smart':Smart}
cas = np.repeat(1708112475, 11)
velkost = 100

def prevod(unix_time):
    dt = datetime.utcfromtimestamp(unix_time)
    formatovany_cas = dt.strftime('%Y-%m-%d %H:%M:%S')
    return formatovany_cas

@profile
def update_data():
    global cas
    
    while True:
        time.sleep(1)
        data = {}
        dt = None
        
        with Session() as session:
            for index, x in enumerate(burzy.keys()):
                dt = session.query(burzy[x]).filter(burzy[x].time > cas[index]).all()

                if len(dt) > 0:
                    if x == 'smart':
                        data.update(dt[-1].to_dict())
                        cas[index] = dt[-1].to_dict()[f'{x}_time']
                        data[f'{x}_time'] = prevod(data[f'{x}_time'])
                    else:
                        if dt[-1].to_dict()[f'{x}_volume'] > velkost:
                            data.update(dt[-1].to_dict())
                            data[f'{x}_time'] = prevod(data[f'{x}_time'])
                            data[f'{x}_close'] = data[f'{x}_close'] + random.uniform(-0.03, 0.03)
                            data[f'{x}_volume'] = data[f'{x}_volume'] # /10
                        
                        cas[index] = dt[-1].to_dict()[f'{x}_time']
        if len(data)>0:
            socketio.emit('my_data', data)


@app.route('/')
def index():
    return render_template('vykreslovanie.html')


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    thread = Thread(target=update_data)
    thread.start()


if __name__ == '__main__':
    socketio.run(app, debug=True)
