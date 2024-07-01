import copy

import networkx as nx
from geopy import distance
from database.DAO import DAO


class Model:
    def __init__(self):
        self.getAnni=DAO.getAnni()
        self.grafo = nx.Graph()
        self._idMap = {}
        self.dista={}

    def getForme(self,anno):
        return DAO.getForme(anno)

    def creaGrafo(self, forma,anno):
        self.nodi = DAO.getNodi()
        self.grafo.add_nodes_from(self.nodi)
        for v in self.nodi:
            self._idMap[v.id] = v
        self.addEdges(forma, anno)
        return self.grafo

    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)
    def addEdges(self, forma,anno):
        self.grafo.clear_edges()
        allEdges = DAO.getConnessioni()
        for connessione in allEdges:
            nodo1 = self._idMap[connessione.v1]
            nodo2 = self._idMap[connessione.v2]
            if nodo1 in self.grafo.nodes and nodo2 in self.grafo.nodes:
                if self.grafo.has_edge(nodo1, nodo2) == False:
                    peso = DAO.getPeso(forma, anno, connessione.v1, connessione.v2)
                    self.grafo.add_edge(nodo1, nodo2, weight=peso)
    def analisi(self):
        dizio={}
        for nodo in self.grafo.nodes:
            somma=0
            for vicino in self.grafo.neighbors(nodo):
                somma+=self.grafo[nodo][vicino]["weight"]
            if somma!=0:
                dizio[nodo.id]=somma
        return dizio

    def getBestPath(self):
        self._soluzione = []
        self._costoMigliore = 0
        for nodo in self.grafo.nodes:
                parziale = [nodo]
                self._ricorsione(parziale)
        return self._costoMigliore, self._soluzione

    def _ricorsione(self, parziale):
        if self.distanza(parziale) > self._costoMigliore:
                self._soluzione = copy.deepcopy(parziale)
                self._costoMigliore = self.distanza(parziale)

        for n in self.grafo.neighbors(parziale[-1]):
            if n not in parziale:
                if len(parziale)>=2:
                    if self.grafo[parziale[-1]][n]["weight"]>self.grafo[parziale[-1]][parziale[-2]]["weight"]:
                        parziale.append(n)
                        self._ricorsione(parziale)
                        parziale.pop()
                else:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()

    def distanza(self,listaNodi):
        distanzaTot=0
        for i in range(0, len(listaNodi) - 1):
            stato1=listaNodi[i]
            stato2=listaNodi[i+1]
            posizione1=(stato1.Lat,stato1.Lng)
            posizione2 = (stato2.Lat, stato2.Lng)
            distanza = distance.geodesic(posizione1, posizione2).km
            distanzaTot+=distanza
            self.dista[f"{stato1.id}-{stato2.id}"]=distanza
        return distanzaTot