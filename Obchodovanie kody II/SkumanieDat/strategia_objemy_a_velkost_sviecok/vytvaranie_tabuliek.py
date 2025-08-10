from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


username = 'marek'
password = '138'
hostname = 'localhost'
database = 'obchodna_strategia_sma'


# Pripojenie k databáze
engine = create_engine(f'mysql+pymysql://{username}:{password}@{hostname}/{database}')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


burzy = ['aapl','amd','amzn','baba','googl','msft','mu','spy','tsla','tsm']
interval = ['12','14','16','18','20','22']
table_names = [f'{i}_okolie_{j}' for j in interval for i in burzy]


# Dynamické vytvorenie tabuliek
for table_name in table_names:
    # Dynamicky vytvorenie triedy tabuľky
    NewTableClass = type(table_name, (Base,), {
        '__tablename__': table_name,
        'id': Column(Integer, primary_key=True, autoincrement=True),
        'burza': Column(String(255)),
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

# Vytvorenie všetkých definovaných tabuliek
Base.metadata.create_all(engine)

