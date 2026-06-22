import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # POPOLA LE 2 TENDINE
    def fillDDsRating(self):
        lista_voti = self._model.get_voti()
        self._view.popola_dropdown_voti(lista_voti)

    # CLICK SUL GRAFO
    def handleCreaGrafo(self, e):
        voto_min_str = self._view.get_voto_min_selezionato()
        voto_max_str = self._view.get_voto_max_selezionato()

        # 1. L'utente deve aver selezionato entrambi i valori
        if voto_min_str is None or voto_max_str is None:
            self._view.mostra_errore("Seleziona entrambi i voti prima di procedere")
            return

        # 2. devono essere numeri validi
        try:
            voto_min = float(voto_min_str)
            voto_max = float(voto_max_str)

        except (ValueError, TypeError):
            self._view.mostra_errore("Valori di voto non validi.")
            return

        # 3. il range deve essere coerente
        if voto_min > voto_max:
            self._view.mostra_errore("il voto minimo non può essere maggiore del voto massimo.")
            return

        # 4. costruzione del grafo
        num_nodi, num_archi = self._model.crea_grafo(voto_min, voto_max)

        if num_nodi == 0:
            self._view.mostra_errore("Nessun attore trovato per il range selezionato.")
            return

        # 5. Statistiche derivate
        top_5 = self._model.get_top_5_archi()
        num_componenti, componente_max = self._model.get_componenti_connesse()

        # 6. passo tutto alla view
        self._view.mostra_risultati_grafo(num_nodi, num_archi, top_5, num_componenti, componente_max)



    def handleCammino(self, e):
        pass