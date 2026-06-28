import networkx as nx
from database.DAO import DAO
class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMap = {}


    def getRatings(self):
        return DAO.getAllRatings()


    def buildGraph(self, rat1, rat2):
        self._graph.clear()
        self._actors = DAO.getAllActorsbyRange(rat1, rat2)
        for a in self._actors:
            self._idMap[a.ActorID] = a

        self._graph.add_nodes_from(self._actors)

        self._edges = DAO.getAllEdges(rat1, rat2)
        for e1, e2, w in self._edges:
            self._graph.add_edge(self._idMap[e1], self._idMap[e2], weight=w)

    def getTop5Edges(self):

        edges = sorted(
            self._graph.edges(data=True),
            key=lambda x: x[2]["weight"],
            reverse=True
        )

        return edges[:5]
    def getBestPath(self):

        self._bestPath = []

        for start in self._graph.nodes():
            partial = [start]
            self._ricorsione(partial)

        return self._bestPath

    def _ricorsione(self, partial):

        if len(partial) > len(self._bestPath):
            self._bestPath = list(partial)

        current = partial[-1]

        for _, successor in self._graph.edges(current):

            # vincolo: età decrescente
            if successor not in partial and successor.birth_date > current.birth_date:
                partial.append(successor)

                self._ricorsione(partial)

                partial.pop()

    def getConnectedComponents(self):
        components = list(nx.connected_components(self._graph))
        largest = max(components, key=len)
        return components, largest

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)