import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP Baseball Manager 2026"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#ebf4f4"
        self._page.window_height = 800
        page.window_center()
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._txt_name = None
        self._txt_result = None

        self._anno = None
        self._salario = None
        self._btnCreaGrafo = None
        self._btnConnesse = None
        self._btnGradoMax = None
        self._btnDreamTeam = None

    def load_interface(self):
        # title
        self._title = ft.Text("Simulazione", color="blue", size=24)
        self._page.controls.append(self._title)

        self._anno = ft.TextField(label = "Anno")
        self._salario = ft.TextField(label = "Salario (M$)")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo)

        row1 = ft.Row([self._anno, self._salario, self._btnCreaGrafo],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._btnConnesse = ft.ElevatedButton(text="Calcola Connesse",
                                              on_click=self._controller.handleCalcolaConnesse,
                                              disabled=True)
        self._btnGradoMax = ft.ElevatedButton(text="Grado Massimo",
                                              on_click=self._controller.handleGradoMassimo,
                                              disabled=True)
        self._btnDreamTeam = ft.ElevatedButton(text="Dream Team",
                                               on_click=self._controller.handleDreamTeam,
                                               disabled=True)

        row2 = ft.Row([self._btnConnesse, self._btnGradoMax, self._btnDreamTeam],
                      alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.END)

        self._page.controls.append(row1)
        self._page.controls.append(row2)

        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(ft.Container(self._txt_result))
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()