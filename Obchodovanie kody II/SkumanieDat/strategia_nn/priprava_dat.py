# Subor pripravuje data pre trenovanie NN.
import os
import numpy as np
import pandas as pd
import pickle
from numba import jit

# akcia = 'AMD'
# path = '/media/marek/zaloha/Data/OHLC_TWS/AMD/5s/trades/'
# datum = os.listdir(path)
# datum.sort()

# burzy = ['arca','bats','drctedge','edgea','iex','memx','nasdaq','nyse','pearl','psx','smart']

# # Stop_loss sa pouziva pri uprave dat pre smart. Je to pouzite v stlpci market. Kde sa pozera, ci
# # sa najskor zrealizuje stoploss, alebo market cena.
# vstup_stop_loss = 0.35
# vstup_rozsah = 300

def extract_time_as_int(x) -> int:
    """
    Toto je na upravu casu v nasledujucej funkcii. Vstup je str napriklad 2024-02-03 15:30:25 a iba casova zlozka sa
    prevadza na int a to sposobom, ze sa string oreze a prevedie na int. Toto bude sluzit ako kluc pre porovnavanie v pandas.

    Parameters
    ----------
    x: str

    Returns
    -------
    int
    """
    return int(x[10:12] + x[13:15] + x[16:18])


# vektorizovanie pre numpy pracu po riadkoch
vect_extract_time_as_int = np.vectorize(extract_time_as_int)


@jit(nopython=True)
def vypocitaj_okolie_a_stop_loss(sviecka, close, market, stop_loss, vstup_okolie, vstup_stop_loss, vstup_rozsah):
    """
    Vypocitava ci sa naplni limitna cena, alebo ci nebude aktivovany stop_loss.

    Parameters
    ----------
    sviecka: velkost sviecky
    close: stlpce z pandas
    market, stop_loss = np.zeros(4680, dtype=np.int32)
    okolie, cena_stop_loss: float
    rozsah: int, aky velky casovy krok do buducna sa ma brat pre pozeranie, ci sa naplni market, alebo stop_loss
            klasicky som daval 300. To je 25 minut.

    Returns
    -------
    market, stop_loss: np.array
    """
    # pocita sa, ci bude naplnena cena+okolie alebo ci bude naplneny skor stoploss. Podla toho co bude skor.
    for idx, i in enumerate(close):
        if sviecka[idx] > 0:
            for p in range(vstup_rozsah):
                if close[idx+p] > close[idx] + vstup_okolie:
                    market[idx] = 1
                    break
                if close[idx+p] < close[idx] - vstup_stop_loss:
                    stop_loss[idx] = 1
                    break
                
        else:
            for p in range(vstup_rozsah):
                if close[idx+p] < close[idx] - vstup_okolie:
                    market[idx] = 1
                    break
                if close[idx+p] > close[idx] + vstup_stop_loss:
                    stop_loss[idx] = 1
                    break
    
    return market, stop_loss
    


# Funkcie nacitaj_smart, nacitaj_burzu a zluc_data su doplnene funkcie do kodu. Je to na urychlenie vypoctov. Data sa nacitavaju
# do ramky a nemusia sa stale nacitavat z disku. Nacitanie a uprava dat trva cca 5 minut, ale potom kod ide bez problemov.
def nacitaj_smart(smart_df, vstup_stop_loss):
    """
    Nacitava vsetky datumy pre burzu smart do ramky. 

    Parameters
    ----------
    smart_df: DataFrame, stlpce [time, sviecka, up, down],
              sviecka je velkost sviecky
              up je velkost horneho knotu
              down je velkost dolneho knotu
    """
    smart = {}
    for i in datum:
        sm = np.load(f'{path}{i}/SMART.npy')
        sm[:,0] = vect_extract_time_as_int(sm[:,0])

        smart_df['time'] = sm[:, 0].astype(int)
        smart_df['sviecka'] = sm[:, 4].astype(float) - sm[:, 1].astype(float)
        smart_df['open'] = sm[:, 1].astype(float)
        smart_df['high'] = sm[:, 2].astype(float)
        smart_df['low'] = sm[:, 3].astype(float)
        smart_df['close'] = sm[:, 4].astype(float)
        smart_df['knot_up'] = 0.0
        smart_df['knot_down'] = 0.0

        mask_up = smart_df['sviecka'] >= 0
        mask_down = smart_df['sviecka'] < 0

        smart_df.loc[mask_up, 'knot_up'] = smart_df.loc[mask_up, 'high'] - smart_df.loc[mask_up, 'close']
        smart_df.loc[mask_up, 'knot_down'] = smart_df.loc[mask_up, 'open'] - smart_df.loc[mask_up, 'low']
        smart_df.loc[mask_down, 'knot_up'] = smart_df.loc[mask_down, 'high'] - smart_df.loc[mask_down, 'open']
        smart_df.loc[mask_down, 'knot_down'] = smart_df.loc[mask_down, 'close'] - smart_df.loc[mask_down, 'low']

        smart_df['open_close'] = sm[:,4].astype(float) - sm[0,4].astype(float)

        pd_sviecka = smart_df['sviecka'].to_numpy()
        pd_close = smart_df['close'].to_numpy()        
        market = np.zeros(4680, dtype=np.int32)
        stop_loss = np.zeros(4680, dtype=np.int32)
        
        smart_df['market'], smart_df['stop_loss'] = vypocitaj_okolie_a_stop_loss(pd_sviecka, pd_close, market, stop_loss, vstup_okolie, vstup_stop_loss, vstup_rozsah)
        smart[i] = smart_df.copy()
        
    return smart


def nacitaj_burzu(burza):
    """
    Nacitava vsetky datumy pre danu burzu do ramky.
    """
    burza_slovnik = {}
    
    for i in datum:
        br = np.load(f'{path}{i}/{burza.upper()}.npy')
        br[:,0] = vect_extract_time_as_int(br[:,0])
        bur_df = pd.DataFrame(br[:,[0,5]], columns=['time', burza]).astype({'time': 'int', burza: 'int'})
        burza_slovnik[i] = bur_df.copy()

    return burza_slovnik


def zluc_data(vstup_stop_loss) -> pd.DataFrame:
    """
    Spaja smart a konkretnu burzu v danom dni do jedneho dataframe.
    """
    # Alokovanie pandas dat na to, aby sa to nemusel stale alokovat nanovo.
    # time: prevedeny cas na int. Vy sa mohol lahko aplikovat ako kluc
    # open, high, low, close: klasicke OHLC udaje
    # sviecka: rozmer sviecky (open - close)
    # knot_up: velkost horneho knotu
    # knot_down: velkost dolneho knotu
    # open_close: aky je rozdiel v otvaracej cene a momentalnej cene
    # market: je len 0, alebo 1. To znamena, ci cena prekroci cenu okolia, ktore je nastavene
    # stop_loss: je len 0, alebo 1. Ci cena klesne pod uroven stop_loss, ktore je nastavene
    smart_df = pd.DataFrame(np.zeros((4680, 11)), columns=['time', 'open', 'high', 'low', 'close', 'sviecka', 'knot_up', 'knot_down', 'open_close', 'market', 'stop_loss']).astype({
        'time': 'int', 'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float', 'sviecka': 'float', 'knot_up': 'float', 'knot_down': 'float',
        'open_close': 'float', 'market': 'int', 'stop_loss': 'int'})
    # Nacitanie smart cez vsetky datumy.
    smart_open_close = nacitaj_smart(smart_df, vstup_stop_loss)
    # Nacitanie burz cez vsetky datumy
    data_burzy = {i: nacitaj_burzu(i) for i in ['arca', 'bats', 'drctedge', 'edgea', 'iex', 'memx', 'nasdaq', 'nyse', 'pearl', 'psx', 'smart']}

    zlucene_data = {}
    
    for i in datum:
        data = smart_open_close[i]
        for j in burzy:
            data = pd.merge(data, data_burzy[j][i], how='left', on='time')
            data[j] = data[j].fillna(0)
        zlucene_data[i] = data[['time', 'sviecka', 'knot_up', 'knot_down', 'open_close', 'market', 'stop_loss',
                                'arca', 'bats', 'drctedge', 'edgea', 'iex', 'memx', 'nasdaq', 'nyse', 'pearl', 'psx', 'smart']].astype(
                                    {'time': 'int', 'sviecka': 'float', 'knot_up': 'float', 'knot_down': 'float', 'open_close': 'float', 'market': 'int', 'stop_loss': 'int',
                                     'arca': 'int', 'bats': 'int', 'drctedge': 'int',
                                     'edgea': 'int', 'iex': 'int', 'memx': 'int', 'nasdaq': 'int', 'nyse': 'int', 'pearl': 'int', 'psx': 'int', 'smart': 'int'})

    return zlucene_data




# for vstup_okolie in [0.12, 0.14, 0.16, 0.18, 0.20, 0.22]:
#     data = zluc_data()
#     path1 = f'/media/marek/zaloha/Data/data_pre_nn/amd_{int(vstup_okolie*100)}_{int(vstup_stop_loss*100)}.pkl'
#     os.makedirs(os.path.dirname(path1), exist_ok=True)
    
#     with open(path1, 'wb') as f:
#         pickle.dump(data, f)






burzy = ['arca','bats','drctedge','edgea','iex','memx','nasdaq','nyse','pearl','psx','smart']
vstup_rozsah = 500



for akcia in ['MU']:
    path = f'/media/marek/zaloha/Data/OHLC_TWS/{akcia}/5s/trades/'
    datum = os.listdir(path)
    datum.sort()
    for vstup_stop_loss in [0.25, 0.30, 0.35, 0.40, 0.50]:
        for vstup_okolie in [0.12, 0.14, 0.16, 0.18, 0.20, 0.22]:
            data = zluc_data(vstup_stop_loss)
            path1 = f'/media/marek/zaloha/Data/data_pre_nn/{akcia.lower()}_{int(vstup_okolie*100)}_{int(vstup_stop_loss*100)}.pkl'
            os.makedirs(os.path.dirname(path1), exist_ok=True)
            
            with open(path1, 'wb') as f:
                pickle.dump(data, f)
