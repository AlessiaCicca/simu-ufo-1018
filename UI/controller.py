import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_grafo(self, e):
        forma = self._view.dd_shape.value
        if forma is None:
            self._view.create_alert("Selezionare una forma")
            return
        anno = self._view.dd_anno.value
        if anno is None:
            self._view.create_alert("Selezionare un Anno")
            return
        grafo = self._model.creaGrafo(forma, int(anno))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))
        analisi = self._model.analisi()
        for nodo in analisi.keys():
            self._view.txt_result.controls.append(ft.Text(f"NODO {nodo}, somma pesi su archi= {analisi[nodo]}"))
        self._view.update_page()

    def handle_percorso(self, e):
        costo, listaNodi = self._model.getBestPath()
        self._view.txt_result.controls.append(ft.Text(f"Peso cammino massimo: {costo} "))
        for i in range(0,len(listaNodi)-1):
            self._view.txt_result.controls.append(ft.Text(f"{listaNodi[i].id} --> {listaNodi[i+1].id}: weight {self._model.grafo[listaNodi[i]][listaNodi[i+1]]["weight"]}, distanza={self._model.dista[f"{listaNodi[i].id}-{listaNodi[i+1].id}"]}"))
        self._view.update_page()


    def fillDDanno(self):
            anni=self._model.getAnni
            for anno in anni:
                self._view.dd_anno.options.append(ft.dropdown.Option(
                    text=anno))

    def fillDDforme(self,e):
        self._view.dd_shape.options=[]
        forme=self._model.getForme(int(self._view.dd_anno.value))
        for forma in forme:
            self._view.dd_shape.options.append(ft.dropdown.Option(
                text=forma))
        self._view.update_page()

