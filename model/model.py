from database.meteo_dao import MeteoDao
import copy

class Model:

    def __init__(self):
        self._sequenza_ottima = []
        self._costo_min = -1

    def get_all_situazioni(self):
        return MeteoDao.get_all_situazioni()

    def get_situazioni_mese(self, mese):
        situazioni = self.get_all_situazioni()
        situazioni_mese = []
        for situazione in situazioni:
            if situazione.data.month == mese:
                situazioni_mese.append(situazione)
        return situazioni_mese

    def get_umidita_media_mese(self, mese):
        situaz_mese = self.get_situazioni_mese(mese)
        diz_citta_um_media = {}
        somma_torino = 0
        count_torino = 0
        somma_milano = 0
        count_milano = 0
        somma_genova = 0
        count_genova = 0
        for situazione in situaz_mese:
            if situazione.localita == "Genova":
                somma_genova += situazione.umidita
                count_genova += 1
            if situazione.localita == "Torino":
                somma_torino += situazione.umidita
                count_torino += 1
            if situazione.localita == "Milano":
                somma_milano += situazione.umidita
                count_milano += 1
        if count_genova != 0:
            diz_citta_um_media["Genova"] = somma_genova / count_genova
        if count_torino != 0:
            diz_citta_um_media["Torino"] = somma_torino / count_torino
        if count_milano != 0:
            diz_citta_um_media["Milano"] = somma_milano / count_milano
        return diz_citta_um_media

    def trova_sequenza_citta(self, mese):
        self._sequenza_ottima = []
        self._costo_min = -1
        lista_situaz = MeteoDao.get_situazioni_meta_mese(mese)
        self._ricorsione([], lista_situaz)
        return self._sequenza_ottima, self._costo_min



    def _ricorsione(self, parziale, lista_situazioni):
        if len(parziale) == 15:
            print(parziale)
            costo = self._calcola_costo(parziale) #--> dovrebbe calcolare somma umidita delle situazioni messe nel parziale + 100*n_spostamenti
            if (self._costo_min == -1) or (costo < self._costo_min):
               self._costo_min = costo
               self._sequenza_ottima = copy.deepcopy(parziale)
        else:
            #passo al giorno successivo (primo giorno è 1)
            giorno = len(parziale)+1
            for situazione in lista_situazioni: # oppure situazione in situazioni[(giorno-1)*3:giorno*3], senza mettere l'if sotto
                # con questo if controllo solo il giorno che mi interessa, cioè un giorno diverso ogni iterazione, e le altre condizioni
                if situazione.data.day == giorno and self._vincoli_soddisfatti(parziale, situazione):
                    parziale.append(situazione)
                    self._ricorsione(parziale, lista_situazioni)
                    # SI FARA' IL pop() SOLO DOPO CHE VIENE SODDISFATTA LA CONDIZIONE INIZIALE, MOMENTO NEL QUALE
                    # VIENE CREATA UNA SOLUZIONE (IN QUESTO CASO QUANDO VENGONO INDIVIDUATI 15 EVENTI ADATTI),
                    # CHE VERRA' PRIMA SALVATA IN UNA VAR, POI ESCO DALL'ULTIMO RICHIAMO DELLA RICORSIONE ED ELIMINO
                    # DAL PARZIALE L'ULTIMO ELEMENTO APPENA TROVATO, FACCIO UN PASSO AVANTI NEL FOR DELLA RICORSIONE
                    # PRECEDENTE (GRAZIE A QUESTO TROVO SEMPRE SOLUZIONI DIVERSE) E SI PASSERA' QUINDI ALLA SOLUZIONE
                    # SUCCESSIVA (HO 14 ELEMENTI E DEVO TROVARE IL 15°), POI APPENA TROVO IL 15° SE LA SOLUZ E'
                    # MIGLIORE (COSTO MINORE) SALVO NUOVA SOLUZIONE, ESCO DALL'ULTIMA RICORSIONE E FACCIO pop()
                    # DELL'ULTIMO ELEM, PASSO AL PROSSIMO ELEMENTO DEL for DELLA RICORSIONE PRECEDENTE E COSI FINO A
                    # CHE NON FINISCE LA LISTA SITUAZIONI DELLA 14a RICORSIONE; DOPO DI CHE ESCO DAL for,
                    # QUINDI TERMINA ANCHE LA 14a RICORSIONE E PASSO ALL'ELEMENTO SUCCESSIVO DEL FOR DELLA 13a
                    # RICORSIONE, ECC.
                    parziale.pop()


    def _calcola_costo(self, parziale):
        costo = 0
        for i in range(len(parziale)):
            # corso umidità
            costo += parziale[i].umidita
            # costo spostamento
            if len(parziale) > 3:
                if parziale[i] != parziale[i-1]:
                    costo += 100
        return costo

    def _vincoli_soddisfatti(self, parziale, situazione):
        # Vincolo 1) check che non sia stato gia 6 giorni nella citta
        counter = 0
        for fermata in parziale:
            if fermata.localita == situazione.localita:
                counter += 1
        if counter >= 6:
            return False

        # Vincolo 2) check che abbia trascorso almeno 3 giorni nella stessa citta
        if len(parziale) <= 2 and len(parziale) > 0:
            if parziale[0].localita != situazione.localita:
                return False
        elif len(parziale) > 2:
            seq_finale = parziale[-3:] # <- ultimi 3 giorni in parziale
            # se NON sono gia passati 3 giorni nella stessa citta
            if seq_finale[0].localita != seq_finale[1].localita or seq_finale[1].localita != seq_finale[2].localita:
                # e se la città che stiamo valutando è diversa dalla città precedente
                if situazione.localita != seq_finale[2].localita:
                    return False
        # Ho soddisfatto tutti i vincoli
        return True

