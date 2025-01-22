#Sector de productos para vender
import flet as ft
import sqlite3
import datetime 
from Formulario_MOV import FormularioMOV_#De aca va a presupuestos 
from Formulario_VE import FormularioVE_#De aca debe ir a movimientos de venta


#clase para venta directa
class FormularioPROD_(ft.Column):
    def __init__(self, cliente_id):
        super().__init__()
        #Agregar lista_productos
        # searchbar para buscar_servicios
        # usando la funcion filtrar_servicios
        # en mostrar_tabla ocultamos tabla procutos
        # mostramos tabla servicios actualizada con filtrar_servicio
        # para lista_servicios en el return, limpiamos content_row_resultados,
        # al seleccionar debe sumarse tambien a la lista de venta o presupuesto,
        # tener en cuenta la otra clase
        # servicio debe ser un formulario, esconder todo, casi como editar cliente
        # al igual que productos..:
        self.lista_productos = []  
        self.cliente_id = cliente_id 
        self.total_venta = 0.0  
        self.main_content_area = None
        self.main_content_button = None
        
        self.search_bar = ft.TextField(
            label="Buscar producto",
            on_change=self.buscar_producto,
            expand=True,)
        self.boton_vender = ft.IconButton(
            icon=ft.icons.CHECK_ROUNDED,
            scale=2.15,
            tooltip="Realizar venta",
            on_click=self.realizar_venta,#Terminar forma de pago mercado pago, :
            #Descontar stock y guardar registro con btn efectivo
            #Descontar stock con estado de pago ok , estado pendiente no descuenta, :
            #Con mp pedir link, y generar estado de venta, hacer query sobre
            #el estado para actualizar el estado y terminar proseso. :
            style=ft.ButtonStyle(color=ft.colors.GREEN),
        )
        self.boton_cancelar = ft.IconButton(
            icon=ft.icons.DELETE_ROUNDED,
            scale=2.15,
            tooltip="Cancelar venta",
            on_click=self.cancelar_venta,
            style=ft.ButtonStyle(color=ft.colors.RED,),
        )
        self.resultados = ft.DataTable(
            horizontal_margin=0.4, column_spacing=5, data_row_max_height=80,scale=1, visible=True,expand=True,
            border_radius=5,width="adaptative",
            bgcolor="lightgrey",
            border=ft.border.all(4, "lightblue"),
            vertical_lines=ft.border.BorderSide(3, "lightblue"),
            horizontal_lines=ft.border.BorderSide(3, "lightblue"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.LIGHT_BLUE,
            heading_row_height=23,
            data_row_color={"hovered": "0x30FF0000"},
            #show_checkbox_column=True,
            divider_thickness=0,
            columns=[
                ft.DataColumn(label=ft.Text("ID", size=16)),
                ft.DataColumn(label=ft.Text("Nombre", size=16)),
                ft.DataColumn(label=ft.Text("Categoría", size=16)),
                ft.DataColumn(label=ft.Text("Precio", size=16)),
                ft.DataColumn(label=ft.Text("Stock", size=16)),
                ft.DataColumn(label=ft.Text("Añadir", size=16)),
            ],
            rows=[],
        )
        self.resultados_seleccionados = ft.DataTable(
            horizontal_margin=0.4, column_spacing=5, scale=1, visible=True,expand=True,
            border_radius=10,width="adaptative",
            bgcolor="lightgrey",
            border=ft.border.all(4, "lightblue"),
            data_row_max_height=80,
 
            
            
            vertical_lines=ft.border.BorderSide(3, "lightblue"),
            horizontal_lines=ft.border.BorderSide(3, "lightblue"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.LIGHT_BLUE,
            heading_row_height=23,
            data_row_color={"hovered": "0x30FF0000"},
            #show_checkbox_column=True,
            divider_thickness=0,
            columns=[
                ft.DataColumn(label=ft.Text("ID", size=16)),
                ft.DataColumn(label=ft.Text("Nombre", size=16)),
                ft.DataColumn(label=ft.Text("Precio", size=16)),
                ft.DataColumn(label=ft.Text("Cantidad", size=16)),
                ft.DataColumn(label=ft.Text("Subtotal", size=16)),
                ft.DataColumn(label=ft.Text("Borrar", size=15)),
            ],
            rows=[],
        )
        self.label_total = ft.Text(f"Total: ${self.total_venta:.2f}", size=18, weight="bold")
        self.content_Row_button = ft.Row(scroll=ft.ScrollMode.HIDDEN,visible=True, expand=True,
            alignment= ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
            ft.TextButton("Exportar",tooltip="Exporte un archivo.csv\na la carpeta /descargas"),#Tabla Productos y servicios
            ft.TextButton("Importar",tooltip="Importe un archivo.cvs\nde la carpeta /descargas"),
            ft.TextButton("Escanear",tooltip="En desarrollo"),
            ft.TextButton("Productos",tooltip="Agregue o edite un producto(desarrollo)"),#Formulario productos
            ft.TextButton("Servicios",tooltip="Agregue o edite un servicio(desarrollo)")#Formulario servicios
            ],)
        self.content_detalle_pag = ft.Text("Productos y Servicios",size=28,weight="bold",theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.row_buttons_area = ft.Row(expand=True,alignment=ft.MainAxisAlignment.CENTER,
                                       vertical_alignment="C",
            controls=[ft.Text("Aceptar"),self.boton_vender,ft.Text("Eliminar"), self.boton_cancelar])
        self.content_Row_resultados = ft.Row(visible=True, expand=True,controls=[self.resultados])
        self.content_Row_resultados_seleccionados = ft.Row(visible=True, expand=True,controls=[self.resultados_seleccionados])
        self.row_text_id_cliente = ft.Row()
        self.row_text_id_cliente.controls.append(ft.Text(f"Venta para id: {self.cliente_id}"))
        self.row_botones_ocultar = ft.Row()
        self.boton_ocultar_tabla = ft.ElevatedButton("Ocultar", on_click=self.ocultar_tabla)
        self.boton_mostrar_tabla = ft.ElevatedButton("Mostrar", on_click=self.mostrar_tabla, visible=False)
        self.boton_buscar_tabla = ft.ElevatedButton("Buscador", on_click=self.focus_on)

        self.row_botones_ocultar.controls.append(self.boton_ocultar_tabla)
        self.row_botones_ocultar.controls.append(self.boton_mostrar_tabla)
        self.row_botones_ocultar.controls.append(self.boton_buscar_tabla)
        #Cliente id None


    def build(self):
        
        self.row_buttons_up = ft.Row()
        self.titulo_content = ft.Column()
        self.main_content_button = ft.Column()
        self.content_tabla = ft.Column()
        self.main_content_area = ft.Column()
        self.text_producto_up = ft.Text("Tabla de selección", size=20,expand=True)
        self.divisor_seleccion = ft.Text("Detalles de selección", size=20,expand=True)
        self.titulo_content.controls.append(self.content_detalle_pag)
        '''self.titulo_content.controls.append(self.detalles_pagina)'''
        self.row_buttons_up.controls.append(self.content_Row_button)
        #self.titulo_content.controls.append(self.detalle_buscadoor)
        self.row_buttons_area.controls.append(self.main_content_button)
        self.main_content_area.controls.append(self.titulo_content)
        self.main_content_area.controls.append(self.search_bar)
        self.main_content_area.controls.append(self.row_buttons_up)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="grey"))
        self.main_content_area.controls.append(self.text_producto_up)
        self.main_content_area.controls.append(self.content_Row_resultados)
        self.main_content_area.controls.append(self.row_botones_ocultar)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="grey"))
        self.main_content_area.controls.append(self.divisor_seleccion)
        self.main_content_area.controls.append(self.content_Row_resultados_seleccionados)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="grey"))
        self.main_content_area.controls.append(self.label_total)
        self.main_content_area.controls.append(self.row_text_id_cliente)
        self.main_content_area.controls.append(ft.Divider(thickness=2,opacity=0))
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="grey"))
        self.main_content_area.controls.append(self.row_buttons_area)
        self.main_content_area.controls.append(ft.Divider(thickness=10,opacity=0))
        self.main_content_area.controls.append(ft.Divider(thickness=10,opacity=0))  
                                                
        self.main_content_area.controls.append(ft.Text("Al presionar aceptar debera seleccionar el metodo de pago.\nOpciones:\n  -Efectivo\n  -Mercado Pago",size=12,weight="bold"))
        self.main_content_area.controls.append(ft.Divider(thickness=5,opacity=0))
        return ft.Column(
            controls=[
                
                self.main_content_area
            ],
            expand=True,
        )   
    
    def ocultar_tabla(self,e):
        self.content_Row_resultados.visible = False
        self.boton_mostrar_tabla.visible = True
        self.boton_ocultar_tabla.visible = False
        snackbar = ft.SnackBar(content=ft.Text("Tabla de productos oculta",weight="bold"),
                               action="mostrar",
                               on_action=self.mostrar_tabla,
                                bgcolor="Grey400")
        snackbar.open = True
        self.page.add(snackbar)
        self.update()
    def mostrar_tabla(self,e):
        self.content_Row_resultados.visible = True
        self.boton_mostrar_tabla.visible = False
        self.boton_ocultar_tabla.visible = True 
        self.update()

    def focus_on(self,e):
        self.search_bar.focus()
        self.update()

    def buscar_cliente(self,e):
        self.txtFld = ft.TextField(label="Hola",on_change=self.filtrar_cliente)  
        cliente = self.txtFld.value.strip()
        cliente = self.filtrar_cliente(cliente)  
        print(f"nombre {cliente}")              
        self.dialog = ft.AlertDialog(
            title=ft.Text("Puedes agrear el nombre del cliente"),
            )
        
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
        for resultado_cliente in cliente:
            texto =ft.Text(f"Sera?{resultado_cliente}")
            self.dialog.content(ft.Column(texto,self.txtFld))
            self.dialog.update()
        self.page.update()
    
    def filtrar_cliente(self,cliente):
        self.mostrar_tabla      
        print(f"cliente id {cliente}")
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM clientes WHERE id LIKE ?",(f"%{cliente}%",))
        resultado = cursor.fetchall()
        conexion.close()
        return resultado   
    #codigo nuevo arriba
    
    def ocultar_row_buttons(self):
        self.main_content_button.visible = True
        self.update()
    
    def buscar_producto(self, e):
        """Buscar productos en la base de datos según el texto ingresado."""
        filtro = self.search_bar.value.strip()
        self.productos = self.filtrar_productos(filtro)

        self.resultados.rows = []  # Limpiar resultados anteriores

        if self.productos:
            for producto in self.productos:
                self.resultados.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(producto[0],tooltip=f"{producto[1]}")),
                            ft.DataCell(ft.Text(producto[1],tooltip=f"{producto[1]}")),
                            ft.DataCell(ft.Text(producto[3],tooltip=f"{producto[1]}")),
                            ft.DataCell(ft.Text(f"{producto[4]:.2f}",tooltip=f"{producto[1]}")),
                            ft.DataCell(ft.Text(producto[5],tooltip=f"{producto[1]}")),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.icons.ADD_SHOPPING_CART_ROUNDED,
                                    on_click=lambda e, p=producto: self.agregar_producto(p),
                                )
                            ),
                        ]
                    )
                )
        self.update()
    
    def filtrar_productos(self, filtro):
        """Consultar productos en la base de datos según el filtro."""
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_producto, nombre_producto, descripcion, categoria, precio_unitario, stock 
            FROM productos 
            WHERE id_producto LIKE ? OR nombre_producto LIKE ? OR categoria LIKE ? OR codigo_barras LIKE ?
        """, (f"%{filtro}%", f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"))
        resultados = cursor.fetchmany(15)
        conexion.close()
        return resultados
    
    def agregar_producto(self, producto):
        snackbar = ft.SnackBar(content=ft.Text(f"Añadido; {producto[1]}"),
                                bgcolor="Green400")
        snackbar.open = True
        self.page.add(snackbar)
        
        """Agregar un producto a la lista seleccionada."""
        cantidad = 1
        subtotal = producto[4] * cantidad
        for p in self.lista_productos:
            if p[0] == producto[0]:
                p[3] += cantidad
                p[4] += subtotal
                self.total_venta += producto[4]
                self.actualizar_tabla_seleccionados()
                return

        self.lista_productos.append([producto[0], producto[1], producto[4], cantidad, subtotal])
        self.total_venta += subtotal
        self.actualizar_tabla_seleccionados()
    
    def actualizar_tabla_seleccionados(self):
        """Actualizar tabla de productos seleccionados."""
        self.resultados_seleccionados.rows.clear()

        for producto in self.lista_productos:
            self.resultados_seleccionados.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(producto[0]))),
                        ft.DataCell(ft.Text(producto[1])),
                        ft.DataCell(ft.Text(f"{producto[2]:.2f}")),
                        ft.DataCell(ft.Text(str(producto[3]))),
                        ft.DataCell(ft.Text(f"{producto[4]:.2f}")),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                on_click=lambda e, p=producto: self.eliminar_producto(p),
                            )
                        ),
                    ]
                )
            )
        self.label_total.value = f"Total: ${self.total_venta:.2f}"
        self.update()
    
    def eliminar_producto(self, producto):
        """Eliminar un producto de la lista seleccionada."""
        self.lista_productos.remove(producto)
        self.total_venta -= producto[4]
        self.actualizar_tabla_seleccionados()
        snackbar = ft.SnackBar(content=ft.Text(f"Eliminado; {producto[1]}"),
                                bgcolor="Red400")
        snackbar.open = True
        self.page.add(snackbar)
    
    def realizar_venta(self, e):
        #mejoras para tener en cuenta
        #Crear la tabla de estados de venta, guardar el insert 
        #Cuando se eliga el metodo de pago.
        #Quitar el insert de aca y ponerlo en btn Efectivo y Mercado pago
        #Al resionar efectivo se hace el commit y update, y en mp el commit espera
        #a que el estado de venta sea confirmado para update datos y commit venta:
        if not self.lista_productos:
            print("No hay productos seleccionados para realizar la venta.")
            snackbar = ft.SnackBar(content=ft.Text("No hay productos seleccionados"),
                                bgcolor="Red400")
            snackbar.open = True
            self.page.add(snackbar)
            return
        try:
            conexion = sqlite3.connect("database_empresa.db")
            cursor = conexion.cursor()
            # Insertar registro de la venta
            self.fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO ventas (fecha, cliente_id, total) VALUES (?, ?, ?)", (self.fecha,self.cliente_id, self.total_venta))
            venta_id = cursor.lastrowid
            # Insertar detalles de la venta
            for producto in self.lista_productos:
                cursor.execute("""
                    INSERT INTO detalles_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (venta_id, producto[0], producto[3], producto[2], producto[4]))
                #Cuando el estado de la venta es pago confirmado se actualiza el producto
                '''cursor.execute(
                "UPDATE productos SET stock = stock - ? WHERE id_producto = ?",
                (producto[3], producto[0]),)'''
            conexion.commit()
            
            # Limpiar la lista de productos seleccionados
            self.lista_productos.clear()
            self.total_venta = 0.0
            self.actualizar_tabla_seleccionados()
            self.resultados.rows.clear() 
            self.filtrar_productos(e)
            self.resultados.update()
            self.update()
            print(f"Aqui viene lo bueno! Como quiere recibir el pago de la venta nº: {venta_id}.")
            self.dialog = ft.AlertDialog(
                    title=ft.Text(f"Aqui viene lo bueno!\nComo quiere recibir el pago de la venta nº: {venta_id}.\nredireccion area VENTAS",size=17),
                    on_dismiss=[],
                    actions=[ft.TextButton(
                        text="Mercado Pago",#LLama toda la cuestion
                        tooltip="En desarrollo"),
                        ft.TextButton(
                        text="Efectivo",
                        tooltip="Efectivo",
                        on_click=lambda e, id=venta_id:self.ver_venta(id))])
            #Los movimientos deben cargar instancias para presupuestos, ventas etc...:
            self.page.dialog = self.dialog
            self.dialog.open=True            
            self.page.update()
        except sqlite3.Error as error:
            print(f"Error al guardar el pago: {error}")
            snackbar = ft.SnackBar(content=ft.Text(f"Error al guardar el pago: {error}"),
                                bgcolor="Red400")
            snackbar.open = True
            self.page.add(snackbar)            
        finally:
            conexion.close()
    
    def cancelar_venta(self, e):
        """Cancelar la venta actual."""
        self.lista_productos.clear()
        self.total_venta = 0.0
        self.actualizar_tabla_seleccionados()
        snackbar = ft.SnackBar(content=ft.Text(f"Total restaurado"),
                                bgcolor="Red400")
        snackbar.open = True
        self.page.add(snackbar)
        self.update()
    #Funciones dialogo
    def update_content(self,new_content):#Funcion Principal
        self.main_content_area.controls.clear()#Para actualizar el contenido principal
        
        self.main_content_area.controls.append(new_content)#Debemos pasa el nuevo contenido
        self.update()#Actualizamos pantalla principal
    
    def show_ventas(self, form_ve):
        self.update_content(form_ve)
    
    def abrir_ventas(self, ventas_id):
        print(f"Venta ID seleccionado: {ventas_id}")
        form_ve = FormularioVE_(ventas_id)
        self.show_ventas(form_ve)
    
    def ver_venta(self, ventas_id):
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()
        try:
            # Obtener los productos y cantidades de la venta
            cursor.execute(
                "SELECT producto_id, cantidad FROM detalles_ventas WHERE venta_id = ?",
                (ventas_id,)  # Correcta forma de pasar parámetros
            )
            productos = cursor.fetchall()

            # Actualizar el stock de cada producto
            for producto in productos:
                producto_id = producto[0]
                cantidad = producto[1]
                cursor.execute(
                    "UPDATE productos SET stock = stock - ? WHERE id_producto = ?",
                    (cantidad, producto_id),
                )

            # Confirmar cambios en la base de datos
            conexion.commit()

        except Exception as e:
            print(f"Error al procesar la venta: {e}")
            conexion.rollback()  # Deshacer cambios en caso de error
        finally:
            cursor.close()
            conexion.close()

        # Cerrar el diálogo y actualizar la página
        self.dialog.open = False
        self.page.update()

        # Llamar a abrir_ventas con el ID de la venta
        self.abrir_ventas(ventas_id)

    #Agregar un editador de producto o servicio, añadir un servicio a la base de datos:
    

    #Objetivo
    # Guardar una venta directa con cliente okis
    # Enviamos el id del cliente desde formCL_ a formPROD_ :
    #Para eso desde productos vamos a usar el boton clientes
    # Creamos otra instancia de fomrCL_??? O solo hacemos query desde venta directa?:

    #clase para crear presupuestos

#clase para clientes 
class FormularioPROD_Presupuesto(ft.Column):
    def __init__(self, cliente_id):
        super().__init__()
        self.lista_productos = []  
        self.cliente_id = cliente_id 
        self.total_venta = 0.0  
        self.total_presupuesto = 0.0
        self.main_content_area = None #para tablas
        self.main_content_button = None #para botones
        self.search_bar = ft.TextField(
            label="Buscar producto",
            on_change=self.buscar_producto,
            expand=True,
            autofocus=False
            
        )
        self.boton_aceptar_presupuesto = ft.ElevatedButton("Guardar Presupuesto", on_click= self.guardar_presupuesto)
        self.boton_cancelar_presupuesto = ft.ElevatedButton("Cancelar", on_click= self.cancelar_presupuesto)
        #Tabla de productos
        self.resultados = ft.DataTable(
            horizontal_margin=0.4, column_spacing=5, scale=1, visible=True,expand=True,
            border_radius=10,width="adaptative",
            bgcolor="lightgrey",data_row_max_height=80,
            border=ft.border.all(4, "lightblue"),
            vertical_lines=ft.border.BorderSide(3, "lightblue"),
            horizontal_lines=ft.border.BorderSide(3, "lightblue"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.LIGHT_BLUE,
            heading_row_height=23,
            data_row_color={"hovered": "0x30FFF600"},
            #show_checkbox_column=True,
            divider_thickness=0,
            columns=[
                ft.DataColumn(label=ft.Text("ID",size=16)),
                ft.DataColumn(label=ft.Text("Nombre",size=16)),
                ft.DataColumn(label=ft.Text("Categoría",size=16)),
                ft.DataColumn(label=ft.Text("Precio",size=16)),
                ft.DataColumn(label=ft.Text("Stock",size=16)),
                ft.DataColumn(label=ft.Text(spans=[ft.TextButton("Agregar")],size=16)),
            ],
            rows=[],
        )
        self.resultados_seleccionados = ft.DataTable(
            horizontal_margin=0.4, column_spacing=5, scale=1, visible=True,expand=True,
            border_radius=10,width="adaptative",
            data_row_max_height=80,
            bgcolor="lightgrey",
            border=ft.border.all(4, "lightblue"),
            vertical_lines=ft.border.BorderSide(3, "lightblue"),
            horizontal_lines=ft.border.BorderSide(3, "lightblue"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.LIGHT_BLUE,
            heading_row_height=23,
            data_row_color={"hovered": "0x30FFF600"},
            #show_checkbox_column=True,
            divider_thickness=0,
            columns=[
                ft.DataColumn(label=ft.Text("ID", size=16)),
                ft.DataColumn(label=ft.Text("Nombre", size=16)),
                ft.DataColumn(label=ft.Text("Precio", size=16)),
                ft.DataColumn(label=ft.Text("Cantidad", size=16)),
                ft.DataColumn(label=ft.Text("Subtotal", size=16)),
                ft.DataColumn(label=ft.Text(spans=[ft.TextButton("Eliminar")], size=16)),
            ],
            rows=[],
        )
        self.label_total = ft.Text(f"Total: ${self.total_venta:.2f}", size=18, weight="bold")
        '''self.resultados_selecccionados = ft.DataTable(
            horizontal_margin=0.4, column_spacing=10, scale=1, visible=True,expand=True,
            border_radius=10,
            columns=[
                ft.DataColumn(label=ft.Text("ID Venta", size=16)), 
                ft.DataColumn(label=ft.Text("Producto", size=16)),
                ft.DataColumn(label=ft.Text("Cantidad", size=16)), 
                ft.DataColumn(label=ft.Text("Subtotal", size=16)), 
            ],
            rows=[],
        )'''
        self.content_Row_button = ft.Row(scroll=ft.ScrollMode.HIDDEN,visible=True,expand=True,controls=[
            ft.TextButton("Exportar"),ft.TextButton("Importar"),
            ft.TextButton("Agregar",tooltip="Desarollo"),ft.TextButton("Opciones",tooltip="Desarollo"),
            ],alignment= ft.MainAxisAlignment.SPACE_AROUND,)
        self.Row_detalle_pag = ft.Text("Productos y Servicios ",size=28,weight="bold",theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.Row__resultados = ft.Row(visible=True,expand=True,
                                              controls=[self.resultados])
        self.Row__resultados_seleccionados = ft.Row(visible=True,expand=True,
                                              controls=[self.resultados_seleccionados])
        self.row_text_id_cliente = ft.Row()

        self.row_botones_ocultar = ft.Row()
        self.boton_ocultar_tabla = ft.ElevatedButton("Ocultar", on_click=self.ocultar_tabla)
        self.boton_mostrar_tabla = ft.ElevatedButton("Mostrar", on_click=self.mostrar_tabla)
        self.boton_buscar_tabla = ft.ElevatedButton("Buscador", on_click=self.focus_on)
        self.row_botones_ocultar.controls.append(self.boton_ocultar_tabla)
        self.row_botones_ocultar.controls.append(self.boton_mostrar_tabla)
        self.row_botones_ocultar.controls.append(self.boton_buscar_tabla)
        

    def build(self):
        self.row_buttons_up = ft.Row()
        self.row_buttons_bottom = ft.Row()
        self.row_buttons_bottom.controls.append(self.boton_aceptar_presupuesto)
        self.row_buttons_bottom.controls.append(self.boton_cancelar_presupuesto)
        self.row_text_id_cliente.controls.append(ft.Text(f"Presupuesto para id: {self.cliente_id}"))
               
        #self.main_content_button = ft.Column()
        self.main_content_area = ft.Column()
        self.row_buttons_area = ft.Row(
            expand=True,alignment=ft.MainAxisAlignment.END,
            controls=[self.boton_aceptar_presupuesto])
        self.divisor_seleccion_1 = ft.Text("Seleccionar producto o servicio Presupuesto", size=15)
        self.divisor_seleccion_resultados = ft.Text("Productos seleccionados", size=15)
        #self.row_buttons_area.controls.append(self.main_content_button)
        self.row_buttons_up.controls.append(self.content_Row_button)
        self.main_content_area.controls.append(self.Row_detalle_pag)
        self.main_content_area.controls.append(self.search_bar)
        self.main_content_area.controls.append(self.row_buttons_up)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="black"))
        self.main_content_area.controls.append(self.divisor_seleccion_1)
        self.main_content_area.controls.append(self.Row__resultados)
        self.main_content_area.controls.append(self.row_botones_ocultar)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="black"))
        self.main_content_area.controls.append(self.divisor_seleccion_resultados)
        self.main_content_area.controls.append(self.Row__resultados_seleccionados)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="black"))
        self.main_content_area.controls.append(self.row_buttons_bottom)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="black"))
        self.main_content_area.controls.append(self.label_total)
        self.main_content_area.controls.append(self.row_text_id_cliente)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="black"))
        return ft.Column(
            controls=[
                
                self.main_content_area,
                
               ],
            expand=True,
            )          

    def ocultar_tabla(self,e):
        self.Row__resultados.visible = False
        self.update()
    def mostrar_tabla(self,e):
        self.Row__resultados.visible = True
        self.update()

    def focus_on(self,e):
        self.search_bar.focus()
        self.update()


    def buscar_producto(self, e):
        """Buscar productos en la base de datos según el texto ingresado."""
        filtro = self.search_bar.value.strip()
        self.productos = self.filtrar_productos(filtro)

        self.resultados.rows = []  # Limpiar resultados anteriores

        if self.productos:
            for producto in self.productos:
                self.resultados.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(producto[0])),
                            ft.DataCell(ft.Text(producto[1],tooltip=f"{producto[1]}")),
                            ft.DataCell(ft.Text(producto[3],tooltip=f"{producto[3]}")),
                            ft.DataCell(ft.Text(f"{producto[4]:.2f}")),
                            ft.DataCell(ft.Text(producto[5])),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.icons.ADD_SHOPPING_CART_ROUNDED,
                                    on_click=lambda e, p=producto: self.agregar_producto(p),
                                )
                            ),
                        ]
                    )
                )
        self.update()
    
    def filtrar_productos(self, filtro):
        """Consultar productos en la base de datos según el filtro."""
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_producto, nombre_producto, descripcion, categoria, precio_unitario, stock 
            FROM productos 
            WHERE id_producto LIKE ? OR nombre_producto LIKE ? OR categoria LIKE ? OR codigo_barras LIKE ?
        """, (f"%{filtro}%", f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"))
        resultados = cursor.fetchmany(15)
        conexion.close()
        return resultados  
    
    def agregar_producto(self, producto):
        """Agregar un producto a la lista seleccionada."""
        cantidad = 1
        subtotal = producto[4] * cantidad
        for p in self.lista_productos:
            if p[0] == producto[0]:
                p[3] += cantidad
                p[4] += subtotal
                self.total_venta += producto[4]
                self.actualizar_tabla_seleccionados()
                return

        self.lista_productos.append([producto[0], producto[1], producto[4], cantidad, subtotal])
        self.total_venta += subtotal
        self.actualizar_tabla_seleccionados()
        snackbar = ft.SnackBar(content=ft.Text(f"Agregado; {producto[1]}"),
                                bgcolor="Green400")
        snackbar.open = True
        self.page.add(snackbar)
    
    def actualizar_tabla_seleccionados(self):
        """Actualizar tabla de productos seleccionados."""
        self.resultados_seleccionados.rows.clear()

        for producto in self.lista_productos:
            self.resultados_seleccionados.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(producto[0]))),
                        ft.DataCell(ft.Text(producto[1])),
                        ft.DataCell(ft.Text(f"{producto[2]:.2f}")),
                        ft.DataCell(ft.Text(str(producto[3]))),
                        ft.DataCell(ft.Text(f"{producto[4]:.2f}")),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                on_click=lambda e, p=producto: self.eliminar_producto(p),
                            )
                        ),
                    ]
                )
            )
        self.label_total.value = f"Total: ${self.total_venta:.2f}"
        self.update()
    
    def eliminar_producto(self, producto):
        """Eliminar un producto de la lista seleccionada."""
        self.lista_productos.remove(producto)
        self.total_venta -= producto[4]
        self.actualizar_tabla_seleccionados()
        snackbar = ft.SnackBar(content=ft.Text(f"Eliminado; {producto[1]}"),
                                bgcolor="Red400")
        snackbar.open = True
        self.page.add(snackbar)
        
    
    def guardar_presupuesto(self, e):
        
        if not self.lista_productos:
            print("No hay productos seleccionados para guardar el presupuesto.")
            snackbar = ft.SnackBar(content=ft.Text("No hay productos seleccionados"),
                                bgcolor="Red400")
            snackbar.open = True
            self.page.add(snackbar)
            return

        try:
            conexion = sqlite3.connect("database_empresa.db")
            cursor = conexion.cursor()
            import datetime
            self.fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO presupuestos (cliente_id, fecha, total) 
                VALUES (?, ?, ?)
            """, (self.cliente_id, self.fecha, self.total_venta))
            presupuesto_id = cursor.lastrowid

            # Insertar detalles de presupuesto
            for producto in self.lista_productos:
                cursor.execute("""
                    INSERT INTO detalles_presupuestos 
                    (presupuesto_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (presupuesto_id, producto[0], producto[3], producto[2], producto[4]))

            # Confirmar transacción
            conexion.commit()

            # Limpiar la lista de productos seleccionados y reiniciar la tabla
            self.lista_productos.clear()
            self.total_venta = 0.0 
            self.label_total
            self.total_presupuesto = 0.0
            self.actualizar_tabla_seleccionados()
            self.resultados.rows.clear()

            # Actualizar la interfaz
            self.label_total.value = f"Total: ${self.total_presupuesto:.2f}"
            self.resultados.update()
            self.update()

            print(f"Presupuesto guardado exitosamente con ID {presupuesto_id}.")
            self.dialog = ft.AlertDialog(
                    title=ft.Text(f"Presupuesto guardado id nº {presupuesto_id}",size=18),
                    on_dismiss=[],
                    actions=[  #on_click=self.editar_cliente), imprimir en un futuro
                             ft.TextButton(text="Ver Presupuesto",on_click=lambda e, id=presupuesto_id:self.ver_presupuesto(id))] #ir a movimientos y cargar presupuestos desde aca
                                    # on_click=lambda e, id=cliente_id: self.crear_presupuesto(id))
                                        )
            #Los movimientos deben cargar instancias para presupuestos, ventas etc...:
            self.page.dialog = self.dialog
            self.dialog.open=True            
            self.page.update()
            #Pasos para ir a mov
            # llamar una instancia que traiga formMOV_()
            # y crear la funcion update_content:
            # :
            

        except sqlite3.Error as error:
            print(f"Error al guardar el presupuesto: {error}")
            snackbar = ft.SnackBar(content=ft.Text(f"Error al guardar el presupuesto: {error}"),
                                bgcolor="Red400")
            snackbar.open = True
            self.page.add(snackbar)
        finally:
            conexion.close()

    def cancelar_presupuesto(self, e):
        """Cancelar la venta actual."""
        self.lista_productos.clear()
        self.total_venta = 0.0
        self.actualizar_tabla_seleccionados()
        snackbar = ft.SnackBar(content=ft.Text(f"Total restaurado"),
                                bgcolor="Red400")
        snackbar.open = True
        self.page.add(snackbar)
        self.update()

    def update_content(self,new_content):#Funcion Principal
        self.main_content_area.controls.clear()#Para actualizar el contenido principal
        
        self.main_content_area.controls.append(new_content)#Debemos pasa el nuevo contenido
        self.update()#Actualizamos pantalla principal
    
    def show_movements(self, form_movs):
        self.update_content(form_movs)
    
    def abrir_movimientos(self, presupuesto_id):
        print(f"Presupuesto ID seleccionado: {presupuesto_id}")
        form_movs = FormularioMOV_(presupuesto_id)
        self.show_movements(form_movs)
    
    def ver_presupuesto(self,presupuesto_id):
        self.dialog.open=False
        self.page.update()
        self.abrir_movimientos(presupuesto_id)
    


    
#Objetivo:
#Mejorar la interfaz de productos, tener un scroll en una columna
# par la tabla_productos y para la tabla_productos_seleccionados
# Para ambos formiularios
# mejorar el cambio a ventas, no encuentra nada :
#Terminar el filtro de feecha y cliente. Poner que solo busque con id de venta en
# el searchbar para que sea mas preciso para mostrar la venta
# CREAR UNA NUEVA TABLA DE SERVICIOS; CON una lista_servicios
# y un formulario_servicios para guardar nuevos servicios y colocar el detalle
# del servicio en el mismo formulario que debe ser multilinea true
# lo debemos hacer en presupuesto y productos venta
# para eso vamos a agregar la creacion de la tabla en funciones_tabla
# y hay que crearla con relacion a id venta id cliente id presupuesto
# porque es nueva informacion que entra directamente, no hay detalle_servicio
# directamente ahi se agrega el detalle de lo que se hizo, cliente, total
# y se agrega a la factura con el id del cliente o la fecha que es mas precisa
# pero deberia tener un sector servicios? es facil agregar
# pero vams por paso primero hacer el serach mas preciso
# :


