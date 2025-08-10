from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


username = 'marek'
password = '138'
hostname = 'localhost'
database = 'obchodna_strategia_stop_loss'


# Pripojenie k databáze
engine = create_engine(f'mysql+pymysql://{username}:{password}@{hostname}/{database}')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


table_names = ['aapl','amd','amzn','baba','googl','msft','mu','spy','tsla','tsm']


# Dynamické vytvorenie tabuliek
for table_name in table_names:
    # Dynamicky vytvorenie triedy tabuľky
    NewTableClass = type(table_name, (Base,), {
        '__tablename__': table_name,
        'id': Column(Integer, primary_key=True, autoincrement=True),
        'burza': Column(String(255)),
        'okolie': Column(Integer),
        'stop_loss': Column(Integer),
        'poc_ob': Column(String(255)),
        'pravd': Column(Float)
    })

# Vytvorenie všetkých definovaných tabuliek
Base.metadata.create_all(engine)

