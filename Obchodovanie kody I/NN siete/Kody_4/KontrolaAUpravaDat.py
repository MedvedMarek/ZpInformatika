import os

class KontrolaAUpravaDat:
    """
    Kontroluje zlozky, kde su ulozene data. Kontroluje ich obsah a ci su dobre stiahnute. Referencna hodnota
    je burza SMART. Vsetko sa odvyja od nej. Trieda je pouzita len na upravu a kontrolu dat. V dalsom postupe
    pre trenovanie NN sieti je uz nevyuzivana
    """
    def __init(self):
        pass

    def kontrola_smart_velkost_dat(self):
        """
        Testuje, ci subor v danej zlozke, je vacsi, ako 128 bytes. Je to z dovodu, ze numpy pole, ak aj nema
        ziadne prvky, tak jeho velkost je 128 bytes. Lebo obsahuje aj inaksie informacia o numpy poli. 
        """
        pass

    def kontrola_smart_open_close(self):
        """
        Testovanie, ci otvaracia-zatvaracia doba je podla burzovych otvaracich hodin. 
        """
        pass

    def kontrola_smart_eur_usa_cas(self):
        """
        Testovanie, ci nie je nahodou posunuty obchodny cas v ramci posunu letneho-zimneho casu. V USA sa 
        cas posuva skor ako v Europe. 
        """
        pass

    def kontrola_smart_pocet_tickov(self):
        """
        Kontrola, ci ulozene udaje maju taky isty rozsah tickov ako maju ticky obchodneho dna.
        """
        pass







