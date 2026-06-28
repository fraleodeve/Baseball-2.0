from model.model import Model

mymodel = Model()

mymodel.buildGraph(2000, 5)
nodi, archi = mymodel.getDetails()

print(f"Grafo Creato! Il grafo ha {nodi} nodi e {archi} archi.")

percorso, costo = mymodel.getBestScore()
print(costo)
# for el in percorso:
    # print(el)

