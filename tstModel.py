from model.model import Model

mymodel = Model()

mymodel.getTeamsOfYear(1988)
mymodel.buildGraph(1988)
nodi, archi = mymodel.getGraphDetails()

print(f"Grafo Creato! Il grafo ha {nodi} nodi e {archi} archi.")

v0 = mymodel.getRandomNode()
path, score = mymodel.getPath2(v0)

print(f"Trovato soluzione lunga {len(path)} con somma pesi archi pari a {score}")
for p in path:
    print(p)

