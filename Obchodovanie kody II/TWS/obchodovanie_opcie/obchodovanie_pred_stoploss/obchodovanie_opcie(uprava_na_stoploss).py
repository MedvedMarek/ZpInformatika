# Subor na automatizovany nakup opcie podla strategie.
# V prvom odstavci je inicializacia pre tws. V druhom je nacitavanie dat z databazy.
import sys
import threading
import time
import numpy as np
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
# import vlastnych funkcii
sys.path.append('/home/marek/Dropbox/Programovanie/TWS/obchodovanie_opcie/')
from strategia import nacitaj_strategiu

# ----------------------------------------------------------------------------------------------------
# ------------------------------------ Priprava tws --------------------------------------------------
# ----------------------------------------------------------------------------------------------------

vlakno = 6  # vlakno je potrebne mat rozne  pri viacerych otvorenych suboroch tws
burza = 'AMD'

class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.orderId = None  # index pre kazdy nakup. Nakup v danom dni je jedinecny a musi mat unikatne cislo.
        self.execution_price = 0  # cena opcie v aktualnom prebehnutom obchode. Pouziva sa v nastaveni pre limitnu cenu.
        self.order_status = False  # sluzi na spustanie predaja opcie ak je nastaveny na True
        self.order_status_inactive = False  # sluzi na ukoncenie vypisania limitnej objednavky, lebo nakup nebol zrealizovany. Nakup bol v rozpore s obchodnymi podmienkami tws.
        self.order_status_submitted = False
        self.pocitadlo_pre_opcie = []  # sem sa budu ukladat este nezrealizovane limitne objednavky. A pokial ich bude viac ako nejaka hranica, tak sa nebude dalej kupovat. Aby nebolo otvorenych vela objednavok.

    def nextValidId(self, orderId: int):
        """Táto metóda je volaná automaticky od TWS s najvyšším platným orderId."""
        self.orderId = orderId

    def nextOrderId(self):
        # Zvýši orderId o jedna a vráti jeho hodnotu. Je to na indexaciu kazdeho obchodu.
        self.orderId += 1
        return self.orderId

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        """
        Toto je automaticka funkcia v tws. Pri kazdej zmene objednavky sa odosielaju udaje z tws o stave objednavky. Pre mna je v tomto
        momente dolezita len filled. Je to kompletne vyplnenie objednavky. Teda ak je tam nakup napriklad 3 opcii, tak status odosle
        filled len v pripade, ze vsetky objednavky boli vyplnene.
        Cakanie na filled je hlavne z dovodu, ze ak by sa automaticky spustiel predaj opcie za limitnu cenu a nebol by este zrealizovany
        cely obchod, tak potom pri predaji by sa bralo, ze ak by neboli vyplnene vsetky obchody, tak by nemalo co predat a potom by sa
        vypisovala opcia.
        """
        self.order_status = False
        self.order_status_inactive = False
        self.order_status_submitted = False

        print(f"Order: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, clientId: {clientId}")
        # print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

        # Filled – príkaz bol kompletne vyplnený.
        # Inactive – príkaz je neaktívny.
        # Cancelled – príkaz bol zrušený.
        # Submitted – príkaz bol odoslaný na burzu a je aktívny.
        # PreSubmitted – príkaz bol odoslaný na burzu, ale ešte nebol vyplnený.
        # PendingSubmit – príkaz bol prijatý systémom, ale ešte nebol odoslaný na burzu.
        # PendingCancel – požiadavka na zrušenie príkazu bola odoslaná, ale ešte nebola potvrdená.
        
        if status == 'Filled':
            # toto je skumanie, ci sa nachadza v pocitadle id pre limitnu objednavku. Ak ano, tak sa z pocitadla id odstrani, lebo objednavka
            # uz bola zrealizovana a mam otovrenych objednavok o jednu menej.
            if orderId in self.pocitadlo_pre_opcie:
                self.pocitadlo_pre_opcie.remove(orderId)
            else:
                self.order_status = True

        if status == 'Cancelled':
            # Cancelled - toto znamena, ze objednavka bola zrusena. Je to v pripade bracet orders. kedy jedna z objednavok (limitna, stoploss) je
            # zrusena, lebo protistrana bola zrealizovana.
            if orderId in self.pocitadlo_pre_opcie:
                self.pocitadlo_pre_opcie.remove(orderId)

        if status == 'Inactive':
            # inactive - toto znamena, ze objednavka bola vyhodena, lebo je v kolizii s obchodnymi podmienkami.
            self.order_status_inactive = True

        if status in ['Submitted', 'PendingSubmit', 'PendingCancel', 'PartiallyFilled', 'PreSubmitted']:
            # toto znamena, ze objednavka je este v rezime, kde sa nieco vykonava
            self.order_status_submitted = True

    def execDetails(self, orderId, contract, execution):
        """
        Vypisuje udaje o prebehnutom obchode a uklada cenu, za aku sa obchod zrealizoval. Cena sluzi ako
        zaklad pre vypocet limitnej ceny pre predaj opcie. Cena je pocitana automaticky. Je to potomok
        EWrapper a EClient. Dana funkcia sa nikde nevola, ale udaje sa aktualizuju okamzite pri zmene.
        """
        self.execution_price = execution.price

    def nakup_opcie(self, expiracia, strike, right, quantity):
        """
        Parameters
        ----------
        expiracia: str, datum vyprsania, napr: "20240419"
        strike: int, strike cena
        right: str, 'C' alebo 'P', call, put
        quantity: int, pocet opcii
        """
        contract = Contract()
        contract.symbol = burza
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = expiracia
        contract.strike = strike
        contract.right = right
        contract.multiplier = "100"

        order = Order()
        order.action = "BUY"
        order.totalQuantity = quantity
        order.orderType = "MKT"
        order.eTradeOnly = ''  # Toto je iba osetrenie vynimky. Vyhadzovalo to a podla netu to staci takto osetrit.
        order.firmQuoteOnly = ''  # Toto je to iste ako v predchadzajucom riadku.
        self.placeOrder(self.nextOrderId(), contract, order)  # Poslanie objednávky

    def predaj_opcie(self, expiracia, strike, right, quantity):
        """
        Parameters
        ----------
        expiracia: str, datum vyprsania, napr: "20240419"
        strike: int, strike cena
        right: str, 'C' alebo 'P', call, put
        quantity: int, pocet opcii
        """
        contract = Contract()
        contract.symbol = burza
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = expiracia
        contract.strike = strike
        contract.right = right
        contract.multiplier = "100"

        limit_order = Order()
        limit_order.action = "SELL"
        limit_order.totalQuantity = quantity
        limit_order.orderType = "LMT"
        limit_order.lmtPrice = self.execution_price + 0.07  # execution_price je pocitane automaticky. hodnota 0.15 je o kolko sa ma navysit cena aby sa predala opcia.
        limit_order.eTradeOnly = ''  # Toto je iba osetrenie vynimky. Vyhadzovalo to a podla netu to staci takto osetrit.
        limit_order.firmQuoteOnly = ''  # Toto je to iste ako v predchadzajucom riadku.

        stop_loss_order = Order()
        stop_loss_order.action = "SELL"
        stop_loss_order.totalQuantity = quantity
        stop_loss_order.orderType = "STP"
        stop_loss_order.auxPrice = self.execution_price - 0.10
        stop_loss_order.eTradeOnly = ''
        stop_loss_order.firmQuoteOnly = ''

        limit_order_id = self.nextOrderId()  # toto sluzi v pocitadle pre pocet otvorenych objednavok
        stop_loss_order_id = self.nextOrderId() 

        self.pocitadlo_pre_opcie.append(limit_order_id) # tu sa uchovavaju id pre limitne objednavky. Podla toho sa bude urcovat, ze ak bude viac objednavok ako hranica, tak sa objednavka nezrealizuje.
        self.pocitadlo_pre_opcie.append(stop_loss_order_id) # tu sa tiez uchovavaju limitne objednavky.

        self.placeOrder(limit_order_id, contract, limit_order)  # Poslanie objednávky
        self.placeOrder(stop_loss_order_id, contract, stop_loss_order) # Poslanie objednavky


class Bot:
    ib = None
    running = True

    def __init__(self):
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", 7497, vlakno)

        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)

    def run_loop(self):
        while self.running:
            self.ib.run()

    def stop(self):
        self.running = False
        self.ib.disconnect()


# ----------------------------------------------------------------------------------------------------
# --------------------------------- Nacitavanie online dat z databazy --------------------------------
# ----------------------------------------------------------------------------------------------------

Base = declarative_base()
user = 'marek'
password = '138'
host = 'localhost'
database = f'x_{burza}'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class Arca(Base):
    __tablename__ = 'arca'
    time = Column(Integer, primary_key=True)
    volume = Column(Integer)

    def to_dict(self):
        return {'arca_time': self.time, 'arca_volume': self.volume}


class Bats(Base):
    __tablename__ = 'bats'
    time = Column(Integer, primary_key=True)
    volume = Column(Integer)

    def to_dict(self):
        return {'bats_time': self.time, 'bats_volume': self.volume}


class Drctedge(Base):
    __tablename__ = 'drctedge'
    time = Column(Integer, primary_key=True)
    volume = Column(Integer)

    def to_dict(self):
        return {'drctedge_time': self.time, 'drctedge_volume': self.volume}


class Edgea(Base):
    __tablename__ = 'edgea'
    time = Column(Integer, primary_key=True)
    volume = Column(Integer)

    def to_dict(self):
        return {'edgea_time': self.time, 'edgea_volume': self.volume}


class Iex(Base):
    __tablename__ = 'iex'
    time = Column(Integer, primary_key=True)
    volume = Column(Integer)

    def to_dict(self):
        return {'iex_time': self.time, 'iex_volume': self.volume}


class Memx(Base):
    __tablename__ = 'memx'
    time = Column(Integer, primary_key=True)
    volume = Column(Integer)

    def to_dict(self):
        return {'memx_time': self.time, 'memx_volume': self.volume}


class Nasdaq(Base):
    __tablename__ = 'nasdaq'
    time = Column(Integer, primary_key=True)
    volume = Column(Integer)

    def to_dict(self):
        return {'nasdaq_time': self.time, 'nasdaq_volume': self.volume}


class Nyse(Base):
    __tablename__ = 'nyse'
    time = Column(Integer, primary_key=True)
    volume = Column(Integer)

    def to_dict(self):
        return {'nyse_time': self.time, 'nyse_volume': self.volume}


class Pearl(Base):
    __tablename__ = 'pearl'
    time = Column(Integer, primary_key=True)
    volume = Column(Integer)

    def to_dict(self):
        return {'pearl_time': self.time, 'pearl_volume': self.volume}


class Psx(Base):
    __tablename__ = 'psx'
    time = Column(Integer, primary_key=True)
    volume = Column(Integer)

    def to_dict(self):
        return {'psx_time': self.time, 'psx_volume': self.volume}


class Smart(Base):
    __tablename__ = 'smart'
    time = Column(Integer, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

    def to_dict(self):
        return {'smart_time': self.time, 'open': self.open, 'high': self.high, 'low': self.low,
                'close': self.close, 'smart_volume': self.volume}


burzy = {'arca': Arca, 'bats': Bats, 'drctedge': Drctedge, 'edgea': Edgea, 'iex': Iex, 'memx': Memx, 'nasdaq': Nasdaq, 'nyse': Nyse, 'pearl': Pearl, 'psx': Psx, 'smart': Smart}
cas = np.repeat(1714118018, 11)
strategia = f'{burza.lower()}_okolie_12'
strategia_opcie = nacitaj_strategiu(0.85, strategia)
strike_ceny = [150, 152.5, 155, 157.5, 160, 162.5, 165, 167.5, 170, 172.5, 175, 177.5, 180, 182.5, 185, 187.5, 190, 192.5, 195, 197.5, 200, 202.5, 205, 207.5, 210]
sviecka = 0.01  # velkost sviecky je len na inicializaciu
cena_akcie = 0.01  # cena kcie je dana len na inicializaciu
cp = ''
strike = 0

def limitny_predaj_opcie(trigger):
    if trigger:
        bot.ib.predaj_opcie(expiracia_opcie, strike, cp, 1)


def bot_opcie():
    """
    Automatizovanie obchodovania opcii na zaklade strategie.

    Globals
    -------
    cas: je to na ukladanie casu, aby sa nestahovali stale stare data z databazy
    sviecka: velkost sviecky
    cena akcie: aktualna hodnota akcie, teda cena podkladoveho aktiva
    cp: je to na urcenie co kupit. Ci Call alebo Put
    strike: je to realizacna cena opcie ktora bude pouzita pri nakupe opcie
    """
    global cas
    global sviecka
    global cena_akcie
    global cp
    global strike
    print('bot_opcie je aktivny')
    burzy_po_strategii = list(strategia_opcie.keys())
    
    while True:
        time.sleep(0.5)
        data = {}
        dt = None
        pocitadlo = int(0)

        with Session() as session:
            for index, x in enumerate(burzy_po_strategii):
                # dt je instancia triedy pre konkretnu burzu. A ak sa nachadza viac riadkov, ktore splnaju podmienku
                # tak tam pre kazdy riadok bude jedna instancia triedy. Preto potom nizsie sa pouziva dt[-1]. To aby
                # sa zobrala iba posledna instanicia. Teda najnovsi zapis do databazy.
                dt = session.query(burzy[x]).filter(burzy[x].time > cas[index]).all()

                if len(dt) > 0:
                    if x == 'smart':
                        data.update(dt[-1].to_dict())
                        cas[index] = data['smart_time']
                        sviecka = abs(data['close'] - data['open'])
                        cena_akcie = data['close']
                        cp = 'C' if data['open'] < data['close'] else 'P'
                        strike = min(strike_ceny, key=lambda x: abs(x - cena_akcie))

                        for i in strategia_opcie['smart'].keys():
                            if data['smart_volume'] > i[0] and data['smart_volume'] <= i[1]:
                                for j in strategia_opcie['smart'][i]:
                                    if sviecka > j[0] and sviecka <= j[1]:
                                        pocitadlo = pocitadlo + 1

                    else:
                        data.update(dt[-1].to_dict())
                        cas[index] = data[f'{x}_time']
                        for i in strategia_opcie[x].keys():
                            if data[f'{x}_volume'] > i[0] and data[f'{x}_volume'] <= i[1]:
                                for j in strategia_opcie[x][i]:
                                    if sviecka > j[0] and sviecka <= j[1]:
                                        pocitadlo = pocitadlo + 1

        # na nakup musia byt nejake spustace a nesmia byt otvorenych viac limitnych objednavok ako 2.
        # Preto je tam 5, lebo do pocitadle pre opcie su ukladane aj stoploss id. Teda potom jedna objednavka ma
        # v zozname dve id. A ked sa zrealizuje, tak sa tieto dve ide odstrania zo zonamu.
        if (pocitadlo > 0) and (len(bot.ib.pocitadlo_pre_opcie) < 5):
            # pocitadlo = pocitadlo if pocitadlo <= 3 else 3
            pocitadlo = 1  # zatial som dal pocitadlo na jdna. Lebo podla neho sa kupuju opcie.
            bot.ib.nakup_opcie(expiracia_opcie, strike, cp, pocitadlo)
            time.sleep(0.5)

            # caka sa pokial nebude vyplneny obchod
            while ((bot.ib.order_status is False) and (bot.ib.order_status_inactive is False)) or (bot.ib.order_status_submitted is True):
                time.sleep(0.5)
                print(f'{bot.ib.order_status}, {bot.ib.order_status_inactive}, {bot.ib.order_status_submitted}')

            time.sleep(0.2)
            limitny_predaj_opcie(bot.ib.order_status)

        bot.ib.order_status = False
        bot.ib.order_status_inactive = False
        bot.ib.order_status_submitted = False




expiracia_opcie = '20240531'
bot = Bot()
bot_opcie()

