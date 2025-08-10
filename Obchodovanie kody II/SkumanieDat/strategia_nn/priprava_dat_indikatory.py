# Subor pripravuje data pre trenovanie NN.
import os
import numpy as np
import pandas as pd
import pickle
from numba import jit
import ta

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


# Pouzitie pri vypocte indikatorov vo funkcii nacitaj_smart
def calculate_rsi(data, window):
    """
    Parameters
    ----------
    data: DataFrame, iba so stlpcom close
    window: int, ake dlhe okno sa bude pocitat
    """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    rsi[:window] = 50
    
    return rsi


# Výpočet Stochastic Oscillator
def calculate_stochastic_oscillator(data, window=60):
    low_min = data['low'].rolling(window=window).min()
    high_max = data['high'].rolling(window=window).max()
    stoch_k = 100 * ((data['close'] - low_min) / (high_max - low_min))
    stoch_d = stoch_k.rolling(window=3).mean()  # Kĺzavý priemer %K

    return stoch_k, stoch_d


def chande_momentum_oscillator(df, window=14):
    close = df
    diff = close.diff(1)
    gain = (diff.where(diff > 0, 0)).rolling(window=window).sum()
    loss = (-diff.where(diff < 0, 0)).rolling(window=window).sum()
    cmo = 100 * (gain - loss) / (gain + loss)
    return cmo


# Funkcie nacitaj_smart, nacitaj_burzu a zluc_data su doplnene funkcie do kodu. Je to na urychlenie vypoctov. Data sa nacitavaju
# do ramky a nemusia sa stale nacitavat z disku. Nacitanie a uprava dat trva cca 5 minut, ale potom kod ide bez problemov.
def nacitaj_smart(smart_df, vstup_stop_loss):
    """
    Nacitava vsetky datumy pre burzu smart do ramky. 

    Parameters
    ----------
    smart_df: DataFrame, stlpce ['time', 'open', 'high', 'low', 'close', 'sviecka', 'knot_up', 'knot_down', 'open_close', 'market', 'stop_loss']
    vstup_stop_loss: int, aka je hranica pre uzatvorenie obchodu, teda stop loss
    
    time: prevedeny cas na int. Vy sa mohol lahko aplikovat ako kluc
    open, high, low, close: klasicke OHLC udaje
    sviecka: rozmer sviecky (open - close)
    knot_up: velkost horneho knotu
    knot_down: velkost dolneho knotu
    open_close: aky je rozdiel v otvaracej cene a momentalnej cene
    market: je len 0, alebo 1. To znamena, ci cena prekroci cenu okolia, ktore je nastavene
    stop_loss: je len 0, alebo 1. Ci cena klesne pod uroven stop_loss, ktore je nastavene

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
        smart_df['volume'] = sm[:,5].astype(int)

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

        # vypocet pomocou jit
        smart_df['market'], smart_df['stop_loss'] = vypocitaj_okolie_a_stop_loss(pd_sviecka, pd_close, market, stop_loss, vstup_okolie, vstup_stop_loss, vstup_rozsah)

        # Doplnenie indikatorov. Ale pozor. Niektore indikatory sa budu pocitat od nulovej hondoty pre kazdy den, teda od open_close
        # a niektore indikatory sa budu pocitat z uzatvaracej ceny.
        #
        #EMA
        smart_df['EMA_24'] = smart_df['open_close'].ewm(span=24, adjust=False).mean()  # 2 minúty
        smart_df['EMA_60'] = smart_df['open_close'].ewm(span=60, adjust=False).mean()  # 5 minút

        # RSI
        smart_df['RSI_60'] = calculate_rsi(smart_df['close'], 60)

        # MACD
        smart_df['MACD'] = smart_df['EMA_24'] - smart_df['EMA_60']
        smart_df['Signal_line'] = smart_df['MACD'].ewm(span=18, adjust=False).mean()  # Signálová línia

        # Bolinger
        smart_df['SMA_24'] = smart_df['open_close'].rolling(window=24).mean()
        smart_df['STDDEV_24'] = smart_df['open_close'].rolling(window=24).std()
        smart_df['Upper_band'] = smart_df['SMA_24'] + (smart_df['STDDEV_24'] * 2)
        smart_df['Lower_band'] = smart_df['SMA_24'] - (smart_df['STDDEV_24'] * 2)

        smart_df.loc[:24, 'SMA_24'] = 0
        smart_df.loc[:24, 'STDDEV_24'] = 0
        smart_df.loc[:24, 'Upper_band'] = 0
        smart_df.loc[:24, 'Lower_band'] = 0

        # TR a ATR_24
        smart_df['TR'] = np.maximum((smart_df['high'] - smart_df['low']), np.maximum(abs(smart_df['high'] - smart_df['close'].shift()), abs(smart_df['low'] - smart_df['close'].shift())))
        smart_df['ATR_24'] = smart_df['TR'].rolling(window=24).mean()
        smart_df.loc[0, 'TR'] = 0
        smart_df.loc[:24, 'ATR_24'] = 0

        # OBV
        smart_df['OBV'] = (np.sign(smart_df['close'].diff()) * smart_df['volume']).fillna(0).cumsum()

        # stochastic indicator
        smart_df['Stoch_k'], smart_df['Stoch_d'] = calculate_stochastic_oscillator(smart_df, window=60)
        smart_df['Stoch_k'] = smart_df['Stoch_k'].bfill().ffill()
        smart_df['Stoch_d'] = smart_df['Stoch_d'].bfill().ffill()

        # Parabolic SAR
        high_0 = smart_df.loc[0, 'high']
        low_0 = smart_df.loc[0, 'low']
        close_0 = smart_df.loc[0, 'close']
        high_rel = smart_df['high']-high_0
        low_rel = smart_df['low']-low_0
        close_rel = smart_df['close']-close_0
        
        smart_df['Parabolic_sar'] = ta.trend.PSARIndicator(high=high_rel, low=low_rel, close=close_rel, step=0.02, max_step=0.2).psar()

        # CCI - skrátené okno na 20 periód pre 5-sekundové dáta
        smart_df['CCI'] = ta.trend.CCIIndicator(high=high_rel, low=low_rel, close=close_rel, window=20).cci()
        smart_df['CCI'] = smart_df['CCI'].bfill().ffill()

        # Ichimoku Cloud - okná prispôsobené pre 5-sekundové dáta
        indicator_ichimoku = ta.trend.IchimokuIndicator(high=high_rel, low=low_rel, window1=9, window2=26, window3=52)
        smart_df['Ichimoku_a'] = indicator_ichimoku.ichimoku_a()
        smart_df['Ichimoku_b'] = indicator_ichimoku.ichimoku_b()
        smart_df['Ichimoku_base_line'] = indicator_ichimoku.ichimoku_base_line()
        smart_df['Ichimoku_conversion_line'] = indicator_ichimoku.ichimoku_conversion_line()
        
        smart_df['Ichimoku_a'] = smart_df['Ichimoku_a'].bfill().ffill()
        smart_df['Ichimoku_b'] = smart_df['Ichimoku_b'].bfill().ffill()
        smart_df['Ichimoku_base_line'] = smart_df['Ichimoku_base_line'].bfill().ffill()
        smart_df['Ichimoku_conversion_line'] = smart_df['Ichimoku_conversion_line'].bfill().ffill()

        # VWAP - skrátené okno na 14 periód pre 5-sekundové dáta
        smart_df['VWAP'] = ta.volume.VolumeWeightedAveragePrice(high=high_rel, low=low_rel, close=close_rel, volume=smart_df['volume'], window=14).volume_weighted_average_price()
        smart_df['VWAP'] = smart_df['VWAP'].bfill().ffill()

        # Donchian Channels - skrátené okno na 20 periód pre 5-sekundové dáta
        smart_df['Donchain_high'] = ta.volatility.DonchianChannel(high=high_rel, low=low_rel, close=close_rel, window=20).donchian_channel_hband()
        smart_df['Donchain_low'] = ta.volatility.DonchianChannel(high=high_rel, low=low_rel, close=close_rel, window=20).donchian_channel_lband()
        smart_df['Donchain_middle'] = ta.volatility.DonchianChannel(high=high_rel, low=low_rel, close=close_rel, window=20).donchian_channel_mband()

        smart_df['Donchain_high'] = smart_df['Donchain_high'].bfill().ffill()
        smart_df['Donchain_low'] =  smart_df['Donchain_low'].bfill().ffill()
        smart_df['Donchain_middle'] = smart_df['Donchain_middle'].bfill().ffill()

        # CMO - skrátené okno na 14 periód pre 5-sekundové dáta
        smart_df['CMO'] = chande_momentum_oscillator(close_rel, window=14)
        smart_df['CMO'] = smart_df['CMO'].bfill().ffill()
        
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
    smart_df = pd.DataFrame(np.zeros((4680, 37)), columns=['time', 'open', 'high', 'low', 'close', 'sviecka', 'knot_up', 'knot_down', 'open_close', 'market', 'stop_loss',
                                                           'EMA_24', 'EMA_60', 'RSI_60', 'MACD', 'Signal_line', 'SMA_24', 'STDDEV_24', 'Upper_band', 'Lower_band', 'TR', 'ATR_24',
                                                           'volume', 'OBV', 'Stoch_k', 'Stoch_d', 'Parabolic_sar', 'CCI', 'Ichimoku_a', 'Ichimoku_b', 'Ichimoku_base_line',
                                                           'Ichimoku_conversion_line', 'VWAP', 'Donchain_high', 'Donchain_low', 'Donchain_middle', 'CMO']
                            ).astype({'time': 'int', 'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float', 'sviecka': 'float', 'knot_up': 'float', 'knot_down': 'float',
                                      'open_close': 'float', 'market': 'int', 'stop_loss': 'int', 'EMA_24': 'float', 'EMA_60': 'float', 'RSI_60': 'float', 'MACD': 'float',
                                      'Signal_line': 'float', 'SMA_24': 'float', 'STDDEV_24': 'float', 'Upper_band': 'float', 'Lower_band': 'float', 'TR': 'float', 'ATR_24': 'float',
                                      'volume': 'int', 'OBV': 'float', 'Stoch_k': 'float', 'Stoch_d': 'float', 'Parabolic_sar': 'float', 'CCI': 'float', 'Ichimoku_a': 'float',
                                      'Ichimoku_b': 'float', 'Ichimoku_base_line': 'float', 'Ichimoku_conversion_line': 'float', 'VWAP': 'float', 'Donchain_high': 'float',
                                      'Donchain_low': 'float', 'Donchain_middle': 'float', 'CMO': 'float'})
    # Nacitanie smart cez vsetky datumy.
    smart_open_close = nacitaj_smart(smart_df, vstup_stop_loss)
    # Nacitanie burz cez vsetky datumy
    data_burzy = {i: nacitaj_burzu(i) for i in ['arca', 'bats', 'drctedge', 'edgea', 'iex', 'memx', 'nasdaq', 'nyse', 'pearl', 'psx', 'smart']}

    zlucene_data = {}
    
    for i in datum:
        data = smart_open_close[i]
        for j in data_burzy.keys():
            data = pd.merge(data, data_burzy[j][i], how='left', on='time')
            data[j] = data[j].fillna(0)
        zlucene_data[i] = data[['time', 'sviecka', 'knot_up', 'knot_down', 'open_close', 'market', 'stop_loss', 'EMA_24', 'EMA_60', 'RSI_60', 'MACD', 'Signal_line',
                                'SMA_24', 'STDDEV_24', 'Upper_band', 'Lower_band', 'TR', 'ATR_24', 'OBV', 'Stoch_k', 'Stoch_d', 'Parabolic_sar', 'CCI',
                                'Ichimoku_a', 'Ichimoku_b', 'Ichimoku_base_line', 'Ichimoku_conversion_line', 'VWAP', 'Donchain_high', 'Donchain_low', 'Donchain_middle', 'CMO',
                                'arca', 'bats', 'drctedge', 'edgea', 'iex', 'memx', 'nasdaq', 'nyse', 'pearl', 'psx', 'smart']].astype(
                                    {'time': 'int', 'sviecka': 'float', 'knot_up': 'float', 'knot_down': 'float', 'open_close': 'float', 'market': 'int', 'stop_loss': 'int',
                                     'EMA_24': 'float', 'EMA_60': 'float', 'RSI_60': 'float', 'MACD': 'float', 'Signal_line': 'float', 'SMA_24': 'float', 'STDDEV_24': 'float',
                                     'Upper_band': 'float', 'Lower_band': 'float', 'TR': 'float', 'ATR_24': 'float', 'OBV': 'float', 'Stoch_k': 'float', 'Stoch_d': 'float',
                                     'Parabolic_sar': 'float', 'CCI': 'float', 'Ichimoku_a': 'float', 'Ichimoku_b': 'float', 'Ichimoku_base_line': 'float',
                                     'Ichimoku_conversion_line': 'float', 'VWAP': 'float', 'Donchain_high': 'float', 'Donchain_low': 'float', 'Donchain_middle': 'float', 'CMO': 'float',
                                     'arca': 'int', 'bats': 'int', 'drctedge': 'int', 'edgea': 'int', 'iex': 'int', 'memx': 'int', 'nasdaq': 'int', 'nyse': 'int',
                                     'pearl': 'int', 'psx': 'int', 'smart': 'int'})

    return zlucene_data





vstup_rozsah = 500


# for akcia in ['MU']:
#     path = f'/media/marek/zaloha/Data/OHLC_TWS/{akcia}/5s/trades/'
#     datum = os.listdir(path)
#     datum.sort()
#     for vstup_stop_loss in [0.25, 0.30, 0.35, 0.40, 0.50]:
#         for vstup_okolie in [0.12, 0.14, 0.16, 0.18, 0.20, 0.22]:
#             data = zluc_data(vstup_stop_loss)
#             path1 = f'/media/marek/zaloha/Data/data_pre_nn/{akcia.lower()}_{int(vstup_okolie*100)}_{int(vstup_stop_loss*100)}.pkl'
#             os.makedirs(os.path.dirname(path1), exist_ok=True)
            
#             with open(path1, 'wb') as f:
#                 pickle.dump(data, f)


# dtm = '2022_01_05'
# akcia = 'AAPL'
# path = f'/media/marek/zaloha/Data/OHLC_TWS/{akcia}/5s/trades/'
# datum = os.listdir(path)
# datum.sort()
# datum = datum[:3]
# vstup_stop_loss = 0.25
# vstup_okolie = 0.12
# data = zluc_data(vstup_stop_loss)


for akcia in ['TSLA']:
    path = f'/media/marek/zaloha/Data/OHLC_TWS/{akcia}/5s/trades/'
    datum = os.listdir(path)
    datum.sort()
    for vstup_stop_loss in [0.30]:
        for vstup_okolie in [0.20]:
            data = zluc_data(vstup_stop_loss)
            path1 = f'/media/marek/zaloha/Data/data_pre_nn/{akcia.lower()}_{int(vstup_okolie*100)}_{int(vstup_stop_loss*100)}.pkl'
            os.makedirs(os.path.dirname(path1), exist_ok=True)
            
            with open(path1, 'wb') as f:
                pickle.dump(data, f)



