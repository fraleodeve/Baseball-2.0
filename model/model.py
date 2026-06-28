import copy
import itertools
import random
from collections import defaultdict

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._salario = 0
        self._anno = 0

        self._idMapPlayers = {}
        for el in DAO.getAllPlayers():
            self._idMapPlayers[el.playerID] = el

        self._bestPath = []
        self._bestScore = 0

    def getBestScore(self):
        self._bestPath = []
        self._bestScore = 0

        self.ricorsione([], [], 0)
        return self._bestPath, self._bestScore

    def ricorsione(self, parziale, squadre, salario):
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = salario
        elif len(parziale) == len(self._bestPath):
            if salario > self._bestScore:
                self._bestPath = copy.deepcopy(parziale)
                self._bestScore = salario

        for nodo in self._grafo.nodes():
            pID, tID, sal = "", "", 0
            for el in DAO.ricorsione(self._anno, self._salario):
                if el[0] == nodo.playerID:
                    if tID not in squadre:
                        pID, tID, sal = el

            if nodo not in parziale and tID not in squadre:
                parziale.append(nodo)
                squadre.append(tID)
                salario += sal
                self.ricorsione(parziale, squadre, salario)
                parziale.pop()

    def buildGraph(self, anno, sal):
        self._grafo.clear()
        salario = sal * 1000000

        self._salario = salario
        self._anno = anno

        nodi = DAO.getNodes(anno, salario)
        for el in nodi:
            self._grafo.add_node(self._idMapPlayers[el])

        archi = DAO.getEdges(anno, salario)
        for el in archi:
            self._grafo.add_edge(self._idMapPlayers[el[0]], self._idMapPlayers[el[1]])

    def getDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getNodoMassimo(self):
        nodiOrdinati = sorted(self._grafo.nodes(), key=lambda x: self._grafo.degree(x), reverse = True)
        return nodiOrdinati[0], self._grafo.degree(nodiOrdinati[0])

    def getComponentiConnesse(self):
        return nx.number_connected_components(self._grafo)

    def getAllYears(self):
        return DAO.getAllYears()