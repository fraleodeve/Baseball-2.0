import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceTeam = None

    def handleCreaGrafo(self, e):
        listaAnni = self._model.getAllYears()
        annoStr = self._view._anno.value
        salarioStr = self._view._salario.value

        try:
            anno = int(annoStr)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Attenzione! Inserire un valore intero per l'anno", color = "red"))
            self._view.update_page()
            return

        if anno not in listaAnni:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Attenzione! L'anno inserito non è presente nel database", color = "red"))
            self._view.update_page()
            return

        try:
            salario = int(salarioStr)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Attenzione! Inserire un valore intero per il salario", color = "red"))
            self._view.update_page()
            return

        self._model.buildGraph(anno, salario)
        nodi, archi = self._model.getDetails()

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato!", color = "red"))
        self._view._txt_result.controls.append(ft.Text(f"Ci sono {nodi} vertici."))
        self._view._txt_result.controls.append(ft.Text(f"Ci sono {archi} archi."))

        self._view._btnConnesse.disabled = False
        self._view._btnGradoMax.disabled = False
        self._view._btnDreamTeam.disabled = False

        self._view.update_page()


    def handleCalcolaConnesse(self, e):
        n = self._model.getComponentiConnesse()
        self._view._txt_result.controls.append(ft.Text())
        self._view._txt_result.controls.append(ft.Text(f"Ci sono {n} componenti connesse."))
        self._view.update_page()

    def handleGradoMassimo(self, e):
        nodo, peso = self._model.getNodoMassimo()
        self._view._txt_result.controls.append(ft.Text())
        self._view._txt_result.controls.append(ft.Text(f"Nodo di grado massimo: ", color = "red"))
        self._view._txt_result.controls.append(ft.Text(f"- {nodo}"))
        self._view._txt_result.controls.append(ft.Text(f"- Grado: {peso}"))
        self._view.update_page()

    def handleDreamTeam(self, e):
        pass
