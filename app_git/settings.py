import flet as ft

class Setting_(ft.Column):
    def __init__(self):
        super().__init__()
        self.main_content_area = None
        self.titulo = ft.Text("Ajustes")
    
    def build(self):
        self.main_content_area = ft.Column()
        self.main_content_area.controls.append(self.titulo)

        return ft.Column(
            controls=[
                self.main_content_area
            ]
        )