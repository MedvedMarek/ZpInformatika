# Upravujem data, z TWS na data, ktore budu nacitavane do tensorflow

import numpy as np
import pandas as pd
import os
import sys


class Priprava_dat:
  """
  Upravuje data pre neuronove siete. Data su vo vystupe vylucne ako numpy polia. Je to
  podmienka pre tensorflow. Nacitavane data zo zloziek, nie su upravovane. Su len spojene
  z viac nacitavani. Treba ich utriedit, lebo sa mozu vyskytovat duplicitne udaje. A taktiez
  je potrebne ich zoradit a orezat na obchodne hodiny. Na vsetky upravy je pouzity pandas.
  Je lepsie citatelny (stlpce, riadky, vystup). A az potom v zavere je vsetko prevedene na
  numpy pole.
  
  Nasledovne funkcie idu v poradi tak, ako su volane pri uprave dat. Poradie funkcie je
  aj v popise nad funkciou.
  """
  def __init__(self):
    """
    Atributs
    --------
    datumy: list
      Datumy nacitane zo zlozky, kde su ulozene data na stahovanie.
    path: str
      Cesta do slozky, kde su ulozene data.
    burzy: list
      Ktore burzy su ulozene v stiahnutych datach. A ktore burzy budu pouzite pri uprave dat.
    ohlc: DataFrame
      Denne ohlc, ktore je pouzite pri uprave dat. je to z dovodu, ze nie su stiahnute vsetky 
      obchodne dni. Teda nie su obchodne dni v poradi, tak ako idu. Preto sa nedalo vycitat 
      zo stiahnutych dat (min, max, close) predchadzajuce hotnoty.
    columns: list
      Stlpce, tak ako idu v numpy poli. Je to ulozene z dvovodu, aby bolo mozne pohodlne
      prehliadat numpy pole a vediet, ktory stlpec je ktory.
    otvaracie_ceny: DataFrame
      Dataframe na ulozenie dat pre otvaracie ceny. Dany dataframe je potrebny pri trenovani
      NN sieti. Je to potrebne na spatnu normalizaciu dat.
    data: DataFrame
      Finalne upravene data.
    """
    self.datumy = os.listdir('/home/marek/Dropbox/Data/TWS/')
    self.path   = '/home/marek/Dropbox/Data/TWS/'
    self.datumy.sort()
    # self.burzy  = ['AMEX','ARCA','BATS','BEX','BYX','CHX','DRCTEDGE','EDGEA','IEX','MEMX','NYSE','PSX','SMART','PEARL','ISLAND']
    # Tu su odobrane burzy : Amex, Bex, Byx, Edgea, Chx, Psx, Pearl. Je to z dovodu, ze neboli tak casto obchodovane. Preto
    # bolo vyhovujuce ich nedavat do dat, aby sa zbytocne nezahlcovala pamat a vypoctova narocnost.
    self.burzy  = ['ARCA','BATS','DRCTEDGE','IEX','MEMX','NYSE','SMART','ISLAND']
    self.ohlc   = pd.read_csv('/home/marek/Dropbox/Data/OHLC/AMD.csv')
    self.columns= None # Skutocne stlpce v numpy poli. Budu pouzite potom pri trenovani NN sieti.
    self.otvaracie_ceny = None
    self.mov_av = 40 # Hodnota pre moving average
    print('Pozor! Hodnotu moving average mas danu na 40. Je to stanovene pre hodnotu\
    lookback 200. V pripade, ze sa to bude menit, tak je potrebne zmenit aj hodnotu MA.')
    self.data   = self.__preved_data_na_numpy()
  
  # Prva funkcia v poradi
  def __nacitaj_a_spoj_burzy_za_jeden_den(self,den):
    """
    Nacitava burzy z jedneho dna a spaja ich do jedneho DataFramu. Ako vystup su upravene
    a spojene data, ktore su zaroven orezane na jeden obchodny den. To je od 8:30-15:00.
    
    Parameters
    ----------
    den: str
      Je to nazov zlozky, z ktorej chcem nacitavat den. 
    
    Returns
    -------
    data: DataFrame
      Je to uz upraveny a orezenay dataframe.
    
    Examples
    -------
    >>> nacitaj_a_spoj_burzy_za_jeden_den('2023_01_19')
    """
    data = np.load(self.path+den+'/AMD_ARCA.npy')
    data = pd.DataFrame(data[:,[1,2,3,4]], columns=['time', 'ARCc','ARCv','ARCw'])
    data['time'] = data['time'].astype('int')
    data = data[data['time']>1]
    data = data.drop_duplicates(subset=['time'], ignore_index=True)
    data = data.sort_values(by='time', ignore_index=True)
    
    for i in self.burzy[1:]:
      d = np.load(self.path+den+'/AMD_'+i+'.npy')
      d = pd.DataFrame(d[:,[1,2,3,4]], columns=['time', i[:3]+'c', i[:3]+'v', i[:3]+'w'])
      d['time'] = d['time'].astype('int')
      d = d[d['time']>1]
      d = d.drop_duplicates(subset=['time'], ignore_index=True)
      d = d.sort_values(by='time', ignore_index=True)
      
      data = pd.merge(data, d, how='outer', on='time')
      data = data.fillna(0)
    
    data = data.drop_duplicates(subset=['time'], ignore_index=True)
    data = data.sort_values(by='time', ignore_index=True)
    data.time = data.time-21600
    data.time = pd.to_datetime(data.time, unit='s')
    data = self.__orez_na_obchodne_hodiny(data)
    
    return(data)
  
  # Druha funkcia v poradi
  def __orez_na_obchodne_hodiny(self, data):
    """
    Orezanie dat na obchodny den. To je 8:30-15:00. Zaroven odstranuje nulove hodnoty v cene. Lebo
    ked sa prerusilo stahovanie streamovanych dat, tak ako cenu zaznacilo 0. A ked sa vykresloval 
    graf, tak cenovy graf skakal do nulovej pozicie. Ale ako referencnu hodnotu pre prerusenie 
    stahovania streamovanych dat berem len udaje z burzy SMART. Lebo to je hlavna burza, ktora
    je plne poskytovana InteractiveBrokers. To je vlastne ich interny darkpool. Preto ak tato
    burza je v cenovom grafe prerusena, tak sa moze predpokladat, ze sa prerusil tok dat. Inak
    nie. Niektore burzy maju nulove hodnoty, ale to je z dobodu, ze neposkytli udaje o trhu. 
    A nie preto, ze by bolo prerusene stahovanie dat. Na vykreslovanie sa stale budu pouzivat
    iba data zo SMARTu.
    
    Parameters
    ----------
    data: DataFrame
      DataFrame spojenych burz v jednom dni.
    
    Returns
    -------
    data: DataFrame
      Orezany dataframe iba na obchodne hodiny.
    """
    
    date = str(data.time[0])[:11]
    start = '08:30:00'
    end   = '15:00:00'
    start = pd.Timestamp(date+start)
    end   = pd.Timestamp(date+end)
    mask  = (data.time >= start) & (data.time <= end)
    data  = data[mask]
    
    data  = data.drop(labels=data[data['SMAc'] == 0].index)
    index = {x[1]:x[0] for x in enumerate(data.index)}
    data  = data.rename(index)
    
    return(data)
  
  # Tretia funkcia v poradi
  def __spoj_data_do_celku(self):
    """
    Spaja vsetky dni do jedneho DataFramu.
    
    Returns
    -------
    data: DataFrame
      Data su spojene do celku.
    """
    
    data = self.__nacitaj_a_spoj_burzy_za_jeden_den(self.datumy[0])
    
    for i in self.datumy[1:]:
      d = self.__nacitaj_a_spoj_burzy_za_jeden_den(i)
      data = pd.concat([data,d], ignore_index=True)
    
    return(data)
  
  # Stvrta funkcia v poradi
  def __pridaj_odober_stlpce(self):
    """
    Odobera niektore stlpce (napriklad time) a doplna nove stlpce. Je tu este stale ponechany
    dataframe, aby bolo mozne skontrolovat stlpce. Ci su dobre popisane a zoradene. Lebo ak sa
    prevedu do numpy pola, tak to uz neskontrolujem.
    
    Returns
    -------
    data: DataFrame
    """
    # Doplnenie stlpcov pre D,H,M,S (dni, hodiny, minuty, sekundy).
    data = self.__spoj_data_do_celku()
    data.insert(1,'second',None)
    data.insert(1,'minute',None)
    data.insert(1,'hour',None)
    data.insert(1,'day',None)
    data.day    = data.time.apply(lambda x: x.day_of_week)
    data.hour   = data.time.apply(lambda x: x.hour)
    data.minute = data.time.apply(lambda x: x.minute)
    data.second = data.time.apply(lambda x: x.second)
    
    # Doplnenie stlpcov pre min, max ceny v predchadzajucom obchodnom dni. A uzatvaraciu cenu
    # v predchadzajucom obchodnom dni. Toto su hlavne oporne hranice, ktore sa kreslia pri 
    # day tradingu.
    data.insert(5,'uzavretie',None)
    data.insert(5,'max',None)
    data.insert(5,'min',None)
    
    start = ' 01:00:00' # Pozor medzery. Pred hodinou musi ostat medzera, lebo pri spajani by sa to zlucilo.
    end   = ' 23:00:00' # Pozor medzery. Pred hodinou musi ostat medzera, lebo pri spajani by sa to zlucilo.
    
    for i in self.datumy:
      datum = i.replace('_','-')
      st    = pd.Timestamp(datum+start) # start v novom cykle
      en    = pd.Timestamp(datum+end)   # end v novom cykle
      mask  = (data.time >= st) & (data.time <= en)
      
      # Hladam index v ohlc pre tento den.
      index = self.ohlc[self.ohlc['Date'] == i.replace('_','-')].index[0]
      
      # Hodnoty min, max, close, budu zadavane uz z predchadzajuceho obchodneho dna. Teda je to index-1.
      _min  = (self.ohlc.loc[index-1,'Low']).__round__(4)
      _max  = (self.ohlc.loc[index-1,'High']).__round__(4)
      close = (self.ohlc.loc[index-1,'Close']).__round__(4)
      data.loc[mask,['min','max','uzavretie']] = [_min, _max, close]
    
    # Doplnenie stlpca "sviecka". Bude to nahrada za klasicku sviecku. Bude to rozdiel medzi
    # terajsou cenou a cenou o jeden tick pred. To bude znamenat, ze ako dynamicky sa cena
    # vyvija. Ale je to spravene len na priemernej cene. Lebo data OHLC sa nestahuju.
    data.insert(8,'sviecka',None)
    
    # Doplnenie stlpca "MA" moving average. MA bude pocitana ako desatina z dlzky lookback.
    data.insert(9,'MA',None)
    
    return(data)
  
  # Piata funkcia v poradi
  def __normalizuj_data(self):
    """
    Normalizuje data do intervalu [0,1], alebo do co najvacsej tesnosti k intervalu [0,1]. 
    Jednotlive stlpce, ktore su rovnake v kazdej burze, su dane ako samostatny list, aby 
    to bolo mozne lahsie upravovat v pripade potreby zmenit nejaku hodnotu, ktora je 
    zodpovedna za normalizovanie.
    
    Returns
    -------
    data: DataFrame
    """
    # Ak budes chciet realizovat nejake upravy a budu potrebne nahlady na povodne data, tak staci
    # ked zakomentujes vsetky transformacie a vystup bude funkcia __pridaj_odober_stlpce().
    data = self.__pridaj_odober_stlpce()
    
    # Vytvorenie noveho dataframu, ktory bude podporny pri trenovani NN sieti.
    self.otvaracie_ceny = pd.DataFrame(data[['SMAc','ISLv']], columns=('SMAc','otvaracia_cena'))
    
    # dhms (den, hoidna, minuta, sekunda)
    dhms = {'day':4, 'hour':24, 'minute':60, 'second':60}
    for i in dhms:
      data[i] = data[i]/dhms[i]
      data[i] = data[i].apply(lambda x: x.__round__(3))
    
    # Volume je vypocitane nasledovne. Su zoradne stlpce a potom som zobral poslednych 400 
    # najvacsich hodnot. Je to priblizne parovane ako som mal hodnoty pre pat burz, ktore su
    # vykreslene do grafov. V pripade potreby je mozne hodnotu 400 zmenit na nejaku inu. Len pre
    # ukazku:
    #   for i in [x[:3]+'v' for x in  self.burzy]:
    #     print( '{}: {}'.format(i, int(np.mean(sorted(data[i])[-400:]))))
    # 
    # >>> AMEv: 13
    # >>> ARCv: 169
    # >>> BATv: 98
    # >>> BEXv: 15
    # ...
    volume = {'ARCv':170,'BATv':100,'DRCv':260,'IEXv':60,'MEMv':70,'NYSv':55,'SMAv':1300,'ISLv':500}
    for i in volume:
      data[i] = data[i]/volume[i]
      data[i] = data[i].apply(lambda x: x.__round__(6))
    
    # Pocet obchodov je totozne s volume. Je predpoklad, ze pocet obchodov je rovnaky ako je volume. 
    # Iba v par pripadoch su zrealizovane velke bolokove objednavky.
    ww     = {'ARCw':170,'BATw':100,'DRCw':260,'IEXw':60,'MEMw':70,'NYSw':55,'SMAw':1300,'ISLw':500}
    for i in ww:
      data[i] = data[i]/ww[i]
      data[i] = data[i].apply(lambda x: x.__round__(6))
    
    # Uprava vsetkych cien burz, ktore sa vztahuju ku burze SMART. Burza SMART sa berie ako referencka
    # burza, od ktorej sa odrazaju ostatne burzy. Predpoklad je, ze pri predaji, alebo nakupe sa 
    # sa preferuje burza ktora ma mensiu cenu, alebo vacsiu cenu ako burza SMART. To zalezi od toho,
    # ci cena akcie stupa, alebo klesa. Zoberme burzu ISLAND. Teda vsetky ceny pre ISLAND budu
    # ako SMART-ISLAND. A toto bude platiti pre kazdu dalsiu burzu. Jedine obmedzenie je to, ze 
    # niekedy burzy nezapisuju vsetky svoje ceny. Preto v datach je zaznacena 0. Preto pri upravach
    # dat, je potrebne kontrolovat, ci v danom riadku sa nenachadza 0. Ak ano, tak tento riadok preskocit.
    burzy_bez_SMART = self.burzy
    burzy_bez_SMART.remove('SMART')
    for i in burzy_bez_SMART:
      mask = data[i[:3]+'c']>0
      data.loc[mask,i[:3]+'c'] = data[mask][i[:3]+'c'] - data[mask]['SMAc']
      data.loc[mask,i[:3]+'c'] = data[mask][i[:3]+'c'].apply(lambda x: x.__round__(6))
    
    # Uprava min, max, uzavretie. Hlavne nastavenie je vo funkcii pridaj_odober_stlpce(). Tam su dane 
    # hlavne ceny z cenoveho grafu. V tomto kroku bude od cien odcitana hodnota SMAc. Je to z dovodu,
    # aby graf nebol viazany na cenu akcie, ale aby boli reflektovane iba cenove pohyby v ramci dna.
    # Ceny min, max, uzavretie su hlavne hladiny, ktore sa klasicky kreslia pre day tradingu.
    # Upravy budu nasledovne min-SMAc, max-SMAc, uzavretie-SMAc.
    start = ' 01:00:00' # Pozor medzery. Pred hodinou musi ostat medzera, lebo pri spajani by sa to zlucilo.
    end   = ' 23:00:00' # Pozor medzery. Pred hodinou musi ostat medzera, lebo pri spajani by sa to zlucilo.
    for i in self.datumy:
      datum = i.replace('_','-')
      st    = pd.Timestamp(datum+start) # start v novom cykle
      en    = pd.Timestamp(datum+end)   # end v novom cykle
      mask  = (data.time >= st) & (data.time <= en)
      data.loc[mask,'min'] = data[mask]['min'] - data[mask]['SMAc']
      data.loc[mask,'min'] = data[mask]['min'].apply(lambda x: x.__round__(3))
      data.loc[mask,'max'] = data[mask]['max'] - data[mask]['SMAc']
      data.loc[mask,'max'] = data[mask]['max'].apply(lambda x: x.__round__(3))
      data.loc[mask,'uzavretie'] = data[mask]['uzavretie'] - data[mask]['SMAc']
      data.loc[mask,'uzavretie'] = data[mask]['uzavretie'].apply(lambda x: x.__round__(3))
    
    # Doplnenie hodnoty pre "sviecku". Stlpec "sviecka" bol vytvoreny vo funkcii __pridaj_odober_stlpce().
    # Hodnota je tvorena rozdielom terajcieho a predchadzajuceho ticku. Ako prva hodnota v kazcom novom 
    # obchodnom dni, bude hodnota 0.
    start = ' 01:00:00' # Pozor medzery. Pred hodinou musi ostat medzera, lebo pri spajani by sa to zlucilo.
    end   = ' 23:00:00' # Pozor medzery. Pred hodinou musi ostat medzera, lebo pri spajani by sa to zlucilo.
    for i in self.datumy:
      datum = i.replace('_','-')
      st    = pd.Timestamp(datum+start) # start v novom cykle
      en    = pd.Timestamp(datum+end)   # end v novom cykle
      mask  = (data.time >= st) & (data.time <= en)
      index = data[mask].index
      for i,j in enumerate(index):
        if i == 0:
          data.loc[j,'sviecka'] = 0
        else:
          data.loc[j,'sviecka'] = (data.loc[j,'SMAc'] - data.loc[j-1,'SMAc']).__round__(4)
    
    # Uprava ceny pre burzu SMART
    # Cena. Ako referencna miera sa berie cena z burzy SMART. Je to zakladna burza pre InteractiveBrokers.
    # Aby nebola cena viazana na hodnoty "skutocnu cenu akcie", tak je upravena tak, ze cena sa vyvyja 
    # od otvaracej ceny v danom obchodnom dni. Cena v kazdom dni je viazana iba na otvorenie burzy. 
    start = ' 01:00:00' # Pozor medzery. Pred hodinou musi ostat medzera, lebo pri spajani by sa to zlucilo.
    end   = ' 23:00:00' # Pozor medzery. Pred hodinou musi ostat medzera, lebo pri spajani by sa to zlucilo.
    for i in self.datumy:
      datum = i.replace('_','-')
      st    = pd.Timestamp(datum+start) # start v novom cykle
      en    = pd.Timestamp(datum+end)   # end v novom cykle
      mask  = (data.time >= st) & (data.time <= en)
      otvaracia_cena = float(data[mask]['SMAc'][:1]) # otvaracia cena v novom dni
      data.loc[mask,'SMAc'] = data[mask]['SMAc'].apply(lambda x: x-otvaracia_cena)
      data.loc[mask,'SMAc'] = data[mask]['SMAc'].apply(lambda x: x.__round__(6))
      # Dany dataframy sluzi potom pri trenovani NN sieti na spatnu normalizaciu dat. Aby sa vratili do 
      # povodneho stavu.
      self.otvaracie_ceny.loc[mask,'otvaracia_cena'] = otvaracia_cena 
    
    # Uprava hodnoty pre 'MA'. Stlpec 'MA' bol vytvoreny vo funkcii __pridaj_odober_stlpce(). Hodnota "MA"
    # je tvorena ako klzavy priemer. Hodnota okna pre klzavy priemer sa berie ako desatina z lookback.
    # Najskor sa vypocita klzavy priemer a potom sa hodnota MA obpocita od SMAc
    for i in range(data.shape[0]):
      if i <= self.mov_av:
        data.loc[i,'MA'] = data.loc[i,'SMAc']
      else:
        data.loc[i,'MA'] = sum(data.loc[i-self.mov_av:i,'SMAc'])/self.mov_av
    data['MA'] = data['MA']-data['SMAc'] #Odcitanie ceny burzy od klzaveho priemeru
    data['MA'] = data['MA'].apply(lambda x: x.__round__(6))
    
    # Odstranenie stlpca time
    del(data['time'])
    
    # Zapisanie stlpcov do "self.columns" v konstruktore. Je to potrebne pre lepsiu orientaciu v numpy poli.
    # Pouziva sa to v inych triedach, kde je k dispozicii uz iba numpy pole.
    self.columns = list(data.keys())
    
    return(data)
  
  # siesta funkcia v poradi
  def __preved_data_na_numpy(self):
    """
    Posledna uprava na numpy pole
    
    Returns
    -------
    data: numpy
    """
    data = self.__normalizuj_data()
    return(data.to_numpy())



