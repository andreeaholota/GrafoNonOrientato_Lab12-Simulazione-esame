from datetime import date
import networkx as nx
from database.DAO import DAO


class Actor:

    def __init__(self, actor_id:int, name:str, eta:int):
        self._actor_id = actor_id
        self._name = name
        self._eta = eta

    @property
    def actor_id(self):
        return self._actor_id

    @property
    def name(self):
        return self._name

    @property
    def eta(self):
        return self._eta

    def __eq__(self,other):
        if not isinstance(other,Actor):
            return False
        return self._actor_id == other.actor_id

    def __hash__(self):
        return hash(self._actor_id)

    def __str__(self):
        return self._name

    def __repr__(self):
        return f"Actor({self.actor_id},{self.name},{self.eta})"


def _pulisci_incasso(testo_incasso):
    if testo_incasso is None:
        return 0.0

    try:
        pulito = "".join(carattere for carattere in str(testo_incasso) if carattere.isdigit() or carattere == ".")
        if pulito == "":
            return 0.0
        return float(pulito)
    except (ValueError, TypeError):
        return 0.0


def _calcola_eta(data_nascita):

    if data_nascita is None:
        return None # Dato anagrafico inesistente

    try:
        oggi = date.today()
        eta = oggi.year -data_nascita.year

        if (oggi.month, oggi.day) < (data_nascita.month, data_nascita.day):
            eta -= 1
    except (AttributeError, TypeError):
        return None # Data di nascita non è un oggetto valido

    if eta < 0 or eta > 120:
        return None  # età non plausibile

    return eta


class Model:
    def __init__(self):
        self._grafo = None
        self._id_map = {}
        self._migliore = []
        self._parziale = []

    # Converte la stringa di incasso in float

    def crea_grafo(self, rating_min, rating_max):
        self._grafo = nx.Graph() # NON ORIENTATO
        self._id_map = {}

        # 1. VERTICI

        lista_attori = DAO.get_attori_per_range(rating_min, rating_max)

        for actor_id, nome, data_nascita in lista_attori:
            eta = _calcola_eta(data_nascita)
            if eta is None:
                continue #età non valida: non lo inseriamo nel vertica

            self._id_map[actor_id] = Actor(actor_id, nome, eta)

        self._grafo.add_nodes_from(self._id_map.values())

        # 2. ARCHI

        righe = DAO.get_incassi_film_comuni(rating_min, rating_max)

        pesi_per_coppia = {}

        for id1, id2, incasso_testo in righe:
            if id1 not in self._id_map or id2 not in self._id_map:
                continue # uno dei due non è un vertice valido

            valore = _pulisci_incasso(incasso_testo)
            chiave = (id1, id2)
            pesi_per_coppia[chiave] = pesi_per_coppia.get(chiave, 0.0) + valore

        for (id1,id2), peso_totale in pesi_per_coppia.items():
            a1= self._id_map[id1]
            a2= self._id_map[id2]
            self._grafo.add_edge(a1, a2, weight=peso_totale)

        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def get_top_5_archi(self):
        if self._grafo is None:
            return []

        lista_archi = list(self._grafo.edges(data=True))
        lista_archi.sort(key=lambda arco: arco[2]['weight'], reverse=True)

        return lista_archi[:5]

    def get_componenti_connesse(self):
        if self._grafo is None or self._grafo.number_of_nodes() == 0:
            return 0, []

        componenti = list(nx.connected_components(self._grafo))

        numero_componenti = len(componenti)
        componente_piu_grande = max(componenti, key=len)

        return numero_componenti, list(componente_piu_grande)

    def get_voti(self):
        return DAO.get_all_rating()

