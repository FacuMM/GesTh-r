#Aplicacion de gestion para una pequeña o mediana empresa
import flet as ft
from funciones_tablas_sql import crear_tablas_empresa
from controls import SafeArea
from flet import PermissionHandler,PermissionType

def main(page: ft.Page):
    page.appbar =ft.AppBar(title= ft.Text("GesTh©r  comercial",weight="Bold"),
                           )#leading=ft.Text("GesTh©r",expand=True))
      
    page.title = "Aplicacion de Gestión "
    page.scroll = ft.ScrollMode.HIDDEN
    page.window.bgcolor = ft.colors.TRANSPARENT
    page.bgcolor = ft.colors.ON_PRIMARY
    #page.bgcolor = ft.colors.BACKGROUND
    page.window.prevent_close = True
    page.adaptive = True
    #page.bgcolor = ft.ColorScheme.on_surface
    ph = ft.PermissionHandler()
    contet_permissions = ft.Row()
    contet_permissions.controls.append(ph)
     
    page.add(ft.Column(controls=[ft.Text()],expand=True),
                        ft.Divider(opacity=0,thickness=30),
                        ft.TextButton("Permisos",on_click=lambda e: open_app_settings(e)),
                        contet_permissions,
                        ph,
                       ft.Text("Gestor de empresa",size=24),
                       ft.Divider(opacity=0,thickness=30))
    
    crear_tablas_empresa()
    
    def handle_window_event(e):
        if e.data == "close":
            page.open(confirm_dialog)

    page.window.prevent_close = True

    page.window.on_event = handle_window_event

    def handle_yes(e):
        page.window.destroy()

    def handle_no(e):
        page.close(confirm_dialog)

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to exit this app?"),
        actions=[
            ft.ElevatedButton("Yes", on_click=handle_yes),
            ft.OutlinedButton("No", on_click=handle_no),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def check_permission(e):
            o = ph.check_permission(e.control.data)
            page.add(ft.Text(f"Checked {e.control.data.name}: {o}"))

    def request_permission(e):
        o = ph.request_permission(e.control.data)
        page.add(ft.Text(f"Requested {e.control.data.name}: {o}"))

    def open_app_settings(e):
        o = ph.open_app_settings()
        contet_permissions.controls.append(ft.Text(f"App Settings: {o}"))
        if o == True:
                contet_permissions.controls.append(ft.Text("Permisos concedidos"))
                page.add()
        elif o == False:
            contet_permissions.controls.append(ft.OutlinedButton(
            "Open App Settings",
            on_click=open_app_settings,
            ))
            page.add(ft.OutlinedButton(
            "Check Storege Permission",
            data=ft.PermissionType.MANAGE_EXTERNAL_STORAGE,
            on_click=check_permission,
            ),
            ft.OutlinedButton(
            "Request Storage Permission",
            data=ft.PermissionType.MANAGE_EXTERNAL_STORAGE,
            on_click=request_permission,
            ))    
             
     
    
    page.add(SafeArea())#Agregamos el safe area() asi porque es self
    page.update()
    
if __name__ == "__main__":
    
    #ip_local = obtener_ip_local()
    ft.app(target=main,view=ft.AppView.WEB_BROWSER)



    #Terminar la gestion de la empres y ver si se puede crear una nueva migracion.
    #Vamos a necesitar nçmigrar todo lo que ya hicimnos a una pagina mas ordenada 
    # para poder convertirla en pagina web o algo mejor. Pero yo siempre pregferiria las
    # aplicaciones con todo esto sumando  a la nueva app, con las funciones que 
    # dejamos de lado en el otro codigo
    # Para eso debemos aprender a manejar las rutas
    # Tener control sobre flask, los controles, permisos de android
    # y aprender a manejar una pagina web desde una red local o desde github
    # 
    # Estoy conforme a lo que esta llegando la applicacion. Me gusta su formato.                                                                                    :