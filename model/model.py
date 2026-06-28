import copy
import itertools
import random

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._teams = []
        self._idMapTeams = {}

        self._bestPath = []
        self._bestObjVal = 0

    def getPath(self, source): # questo e l'altro sempre per ricorsione
        # input: solo nodo di partenza
        # output: lista nodi da attraversare, valore peso massimo
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [source]
        for v in self._grafo.neighbors(source):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

    def getPath2(self, source):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [source]

        listaVicini = self.getVicini(parziale[-1])
        parziale.append(listaVicini[0][0]) # miglior nodo che posso aggiungere, il primo della lista
        self._ricorsioneV2(parziale)
        parziale.pop()

        return self._bestPath, self._bestObjVal

    def _ricorsione(self, parziale):
        # ricorsione molto lunga e complicata: decine di anni
        # quindi faccio in modo che sia più breve
        # non provo tutti i miei vicini, ma quello con peso maggiore

        # 1) condizione ottimalità: verifico se parziale migliore del best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        # 2) condizione di terminazione: verifico se posso continuare (quando non ha più senso continuare)
        # qua non c'è limite

        # 3) faccio ricorsione
        for v in self._grafo.neighbors(parziale[-1]):
            # devo verificare che arco sia crescente rispetto ad arco di prima
            pesoE = self._grafo[parziale[-1]][v]["weight"]
            if self._grafo[parziale[-2]][parziale[-1]]["weight"] > pesoE and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def _ricorsioneV2(self, parziale):
        # non provo tutti i miei vicini, ma quello con peso maggiore

        # 1) condizione ottimalità: verifico se parziale migliore del best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        # 2) condizione di terminazione: verifico se posso continuare (quando non ha più senso continuare)
        # qua non c'è limite

        # 3) faccio ricorsione
        # rispetto a prima però prendo come primo tentativo il maggiore (così forse ci metto meno)
        # listaVicini = []
        # for v in self._grafo.neighbors(parziale[-1]):
            # edgeV = self._grafo[parziale[-1]][v]["weight"] # peso che ha portato da parziale[-1] a v
            # listaVicini.append((v, edgeV))
         # listaVicini.sort(key=lambda x: x[1], reverse=True)

        # uso metodo che avevo già creato
        listaVicini = self.getVicini(parziale[-1])
        for v in listaVicini:
            if v[0] not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > v[1]:
                parziale.append(v[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return # nel momento in cui trovo miglior arco, esco

        # non ho garanzie di trovare soluzione ottima, perchè completamente connesso
        # 1. soluzione migliore, ma questa più veloce

    def _score(self, parziale):
        # siamo sicuri che nodi siano connessi, ottenuti da vicini
        score = 0
        for i in range(0, len(parziale)-1):
            score += self._grafo[parziale[i]][parziale[i+1]]["weight"]
        return score

    def buildGraph(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)

        # arco tra ogni nodo del grafo
        # for u in self._grafo.nodes():
            # for v in self._grafo.nodes():
                # if u != v:
                    # self._grafo.add_edge(u, v)

        # in alternativa usa combinations (libreria python)
        myEdges = list(itertools.combinations(self._teams, 2)) # prendo team 2 a 2 -> restituisce lista di tuple
        self._grafo.add_edges_from(myEdges) # add_edges_from vuole lista di tuple

        mapSalary = DAO.getSalariesTeam(year, self._idMapTeams)

        for e in self._grafo.edges():
            salario1 = mapSalary[e[0]]
            salario2 = mapSalary[e[1]]
            peso = salario1 + salario2
            self._grafo[e[0]][e[1]]["weight"] = peso # eventualmente tutta una riga

    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)
        self._idMapTeams = {t.ID: t for t in self._teams}
        return self._teams

    def getGraphDetails(self):
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def getVicini(self, source):
        vicini = self._grafo.neighbors(source)
        viciniTuple = []
        for v in vicini:
            viciniTuple.append((v, self._grafo[source][v]["weight"]))

        viciniTuple.sort(key=lambda x: x[1], reverse=True)
        return viciniTuple

    # per testare ricorsione
    def getRandomNode(self):
        index = random.randint(0, len(self._teams))
        return self._teams[index]