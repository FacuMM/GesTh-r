import flet as ft
from home import Home_
from settings import Setting_
from Formulario_CL import FormularioCliente_
from Formulario_PROD import FormularioPROD_
from Formulario_MOV import FormularioMOV_
from Formulario_VE import FormularioVE_

class SafeArea(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        
        
        self.main_content_area= None
    
    def build(self):
        
        self.titulo = ft.Text("Bienvenido", size=16)
        self.navbar = ft.Row(height=55,scroll=ft.ScrollMode.HIDDEN,visible=True, expand=True,spacing=45,alignment= ft.MainAxisAlignment.CENTER,
            controls=[
                ft.IconButton(ft.icons.HOME_ROUNDED, on_click=self.show_home,scale=2,tooltip="Inicio",icon_color=ft.colors.AMBER),
                ft.IconButton(ft.icons.MONETIZATION_ON_ROUNDED, on_click=self.show_sales,scale=2,tooltip="Registro de ventas",icon_color=ft.colors.GREEN),
                ft.IconButton(ft.icons.PORTRAIT_ROUNDED, on_click=self.show_customers,scale=2,tooltip="Clientes",icon_color=ft.colors.BLUE),
                ft.IconButton(ft.icons.PRODUCTION_QUANTITY_LIMITS_ROUNDED, on_click=self.show_products,scale=2,tooltip="Productos",icon_color=ft.colors.TEAL),
                ft.IconButton(ft.icons.REQUEST_QUOTE_ROUNDED, on_click=self.show_movements,scale=2,tooltip="Presupuestos",icon_color=ft.colors.CYAN),
                ft.IconButton(ft.icons.SETTINGS_ROUNDED, on_click=self.show_settings,scale=2,tooltip="Ajustes",icon_color=ft.colors.RED)
            ])

        
        self.main_content_area = ft.Column(controls=[],expand=True)#Pantalla Principal
        
        return ft.Column(controls=[
          
            
            
            self.navbar,
            
            self.titulo,
            self.main_content_area,
                                   ])
    
    def update_content(self,new_content):#Funcion Principal
        self.page.clean()
        self.page.add(self.navbar)
        self.page.add(ft.Divider(thickness=1,opacity=1,color="black"))
        
        self.page.add(self.main_content_area)
        self.main_content_area.controls.clear()#Para actualizar el contenido principal
        
        self.main_content_area.controls.append(new_content)#Debemos pasa el nuevo contenido
        self.update()#Actualizamos pantalla principal
    
    def show_home(self,e):#Con update_content actualizamos la pantalla principal
        home_ = Home_() #Se llama self()
        self.update_content(home_)       
    
    def show_sales(self,e):
        form_vent = FormularioVE_(venta_id=None)
        self.update_content(form_vent)
    
    def show_customers(self,e):
        form_CL = FormularioCliente_()
        self.update_content(form_CL)
    
    def show_products(self,e):
        form_prod = FormularioPROD_(cliente_id=None)
        self.update_content(form_prod)
    
    def show_movements(self,e):
        form_movs = FormularioMOV_(presupuesto_id=None)
        self.update_content(form_movs)
    
    def show_settings(self,e):
        form_set = Setting_()
        self.update_content(form_set)
        