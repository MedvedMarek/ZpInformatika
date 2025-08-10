# nacitanie dat pre obchodnu strategiu. Data su ulozene v databaze. 

import pandas as pd
from typing import Dict, List, Tuple
from sqlalchemy import create_engine
import pymysql

user = 'marek'
password = '138'
host = 'localhost'
database = 'obchodna_strategia'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')



def zluc_intervaly(intervaly) -> List[List[float]]:
    """
    Zlucuje intervaly dokopy. Ak su zasebov dva intervaly napriklad [0.1, 0.2], [0.2, 0.5], tak
    tieto dva intervaly zluci do jedneho intervalu [0.1, 0.5].

    Parameters
    ----------
    intervaly: list, napriklad [[0.1, 0.2], [0.2, 0.5], [0.7, 0.8]]
    
    Returns
    -------
    zlucene_intervaly: list
    """
    
    # Zoradenie intervalov podľa ich začiatočných hodnôt
    zoradene_intervaly = sorted(intervaly, key=lambda x: x[0])
    
    # Výsledný zoznam zlúčených intervalov
    zlucene_intervaly = [zoradene_intervaly[0]]
    
    for aktualny in zoradene_intervaly[1:]:
        posledny_v_zlucene = zlucene_intervaly[-1]
        
        # Ak koncová hodnota posledného intervalu v zlúčenom zozname sa rovná
        # začiatočnej hodnote aktuálneho intervalu, zlúč ich
        if posledny_v_zlucene[1] == aktualny[0]:
            # Aktualizuj koncovú hodnotu posledného intervalu v zlúčenom zozname
            zlucene_intervaly[-1] = [posledny_v_zlucene[0], aktualny[1]]
        else:
            # Inak, pridaj aktuálny interval do výsledného zoznamu
            zlucene_intervaly.append(aktualny)
            
    return zlucene_intervaly



def nacitaj_strategiu(minimum, strategia) -> Dict[str, Dict[Tuple[int, int], List[List[float]]]]:
    """
    Obsahuje data pre objemy a velkost sviecok. Sluzi na porovnavanie dat, ci ma
    byt spusteny trigger, alebo nie.

    Parameters
    ----------
    minimum: int, to je dolna hranica pre akceptovanu pravdepodobnost.
    strategia: str, napr: 'okolie_16' strategia podla ktorej sa ma ist

    Returns
    -------
    slovnik: dict, slovnik obsahujuci burzy, objem, velkost sviecok.
    """

    # Zadavam prikaz na selektovanie dat z databazy. V pripade potreby sa moze minimum upravit.
    sql_prikaz = f"""
    SELECT burza, ob_min, ob_max, sv_min, sv_max, suma, pr FROM {strategia}
    WHERE pr > {minimum} AND suma > 20
    ORDER BY burza ASC
    """
    data = pd.read_sql(sql_prikaz, con=engine)
    
    burzy = data['burza'].unique()
    objem_unique = {}
    slovnik = {}
    
    for i in burzy:
        objem_unique[i] = data[data['burza'] == i]['ob_min'].unique()
        slovnik[i] = {}

    # vytvorenie slovnika ktory vytiahne objem a velkost sviecok pre danu pravdepodobnost
    for i in burzy:
        for j in objem_unique[i]:
            dt = data[data['burza'] == i]
            for index, row in dt[dt['ob_min'] == j].iterrows():
                if not (row['ob_min'], row['ob_max']) in slovnik[i]:
                    slovnik[i][(row['ob_min'], row['ob_max'])] = [[row['sv_min'], row['sv_max']]]
                else:
                    slovnik[i][(row['ob_min'], row['ob_max'])].append([row['sv_min'], row['sv_max']])

    # Zoradenie prvkov (velkosti sviecok) aby mohli byt intervaly zlucene do jedneho, ako je to mozne.
    # je to na rychlejsie iterovanie. Lebo takto sa to zmensi skoro o tretinu.
    for i in slovnik.keys():
        for j in slovnik[i].keys():
            slovnik[i][j] = sorted(slovnik[i][j])
            slovnik[i][j] = zluc_intervaly(slovnik[i][j])
    
    return slovnik








data = nacitaj_strategiu(0.9, 'aapl_okolie_14')

for i in data.keys():
    print(data[i])


