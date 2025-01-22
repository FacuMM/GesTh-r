import sqlite3
import flet as ft
from Formulario_PROD import FormularioPROD_Presupuesto, FormularioPROD_
import os
import platform
import csv
import fpdf

class FormularioCliente_(ft.Column):
    def __init__(self):
        super().__init__()
        
        self.lista_clientes = []
        self.lista_datos_cliente = []
        self.lista_venta_cliente = []
        self.lista_presupuesto_cliente = []        
        self.main_content_area = None
        self.content_detalles = None
        self.main_content_button = None
        self.file_picker = ft.FilePicker()
        self.boton_abrir_form = ft.TextButton(
            "Agregar",
            tooltip="Abrir formulario\n Opción\n    -Guardar un cliente nuevo",
            on_click=self.abrir_formulario)
        self.searchbar = ft.TextField(
            label="Buscar cliente",
            on_change=self.buscar_cliente,
            autofocus=False
        )
        self.tabla_clientes = ft.DataTable(
            horizontal_margin=0.4,data_row_max_height=60, column_spacing=40, scale=1, visible=True,expand=True,
            width="adaptative",
            bgcolor="lightgrey",
            border=ft.border.all(4, "lightblue"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, "lightblue"),
            horizontal_lines=ft.border.BorderSide(3, "lightblue"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.LIGHT_BLUE,
            heading_row_height=23,
            data_row_color={"hovered": "0x30FFF600"},
            #show_checkbox_column=True,
            divider_thickness=0,
            #column_spacing=50,
            columns=[
                ft.DataColumn(label=ft.Text("ID", size=17)),
                ft.DataColumn(label=ft.Text("Nombre", size=17)),
                ft.DataColumn(label=ft.Text("Telefono",size=17)),
                
            ],
                #ft.DataColumn(label=ft.Text("Email")),
                #ft.DataColumn(label=ft.Text("CUIL")),
                #ft.DataColumn(label=ft.Text("DNI")),
                #ft.DataColumn(label=ft.Text("WhatsApp")),
            rows=[],
        )
        self.tabla_ventas_cliente = ft.DataTable(visible=False,
            horizontal_margin=0.4, column_spacing=10, scale=1,expand=True,
            border_radius=10,width="adaptative",
            data_row_max_height=60,
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
            #column_spacing=50,
            columns=[ft.DataColumn(label=ft.Text("id",size=17)),
                ft.DataColumn(label=ft.Text("cliente",size=17)),
                ft.DataColumn(label=ft.Text("Detalle",size=17)),
                ft.DataColumn(label=ft.Text("Total",size=17)),
                
                               
                ],
            rows=[],
                

        )
        self.tabla_presupuestos_cliente = ft.DataTable(visible=False,
            horizontal_margin=0.4, column_spacing=10, scale=1,expand=True,
            border_radius=10,width="adaptative",
            bgcolor="lightgrey",
            border=ft.border.all(4, "lightblue"),
            data_row_max_height=60,
            
            vertical_lines=ft.border.BorderSide(3, "lightblue"),
            horizontal_lines=ft.border.BorderSide(3, "lightblue"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.LIGHT_BLUE,
            heading_row_height=23,
            data_row_color={"hovered": "0x30FFF600"},
            #show_checkbox_column=True,
            divider_thickness=0,
            #column_spacing=50,
            columns=[ft.DataColumn(label=ft.Text("Id",size=17)),
                ft.DataColumn(label=ft.Text("Cliente",size=17)),
                ft.DataColumn(label=ft.Text("Detalle ",size=17)),
                ft.DataColumn(label=ft.Text("Presupuesto",size=17)),
                
                               
                ],
            rows=[],
                

        )
        self.boton_opcion_guardar = ft.Row(controls=[ft.TextButton("Guardar", on_click=self.guardar_cliente,)],visible=False)
        self.formulario_area = ft.Column(visible=False, controls=[
            ft.TextField(label="Nombre*",hint_text="Campo obligatorio",
                            bgcolor=ft.colors.RED_300,
                           keyboard_type=ft.KeyboardType.NAME,
                           on_submit=self.opcion_guardar,
                           tooltip="campo obligatorio",
                           
                           ),
            ft.TextField(label="Teléfono", keyboard_type=ft.KeyboardType.DATETIME),#, ref="telefono"),
            ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL),#, ref="email"),
            ft.TextField(label="CUIL",keyboard_type=ft.KeyboardType.DATETIME,value=None),#, ref="cuil"),
            ft.TextField(label="DNI",keyboard_type=ft.KeyboardType.DATETIME,value=None),#, ref="dni"),
            ft.TextField(label="WhatsApp", keyboard_type=ft.KeyboardType.DATETIME),#, ref="whatsapp"),
            ft.Text("""Revise bien los campos antes de guardar\nSe asigna un ID único por cliente\nPodrá modificar los datos del cliente en Editar\n\n*insertado el nombre oprima aceptar en el teclado\npara mostrar la opción de guardar""",size=14,weight="bold"),
            ft.Row(controls=[               
                ft.TextButton("Cancelar", on_click=self.cerrar_formulario),
                self.boton_opcion_guardar,
            ])
        ])
        self.row_button_bottom = ft.Row(visible=True,expand=True,alignment=ft.MainAxisAlignment.SPACE_AROUND)
        self.formulario_EDIT = ft.Column(visible=False, controls=[
            #ft.TextField(label="Nombre", keyboard_type=ft.KeyboardType.NAME),#, ref="nombre"),
            ft.TextField(label="Teléfono", keyboard_type=ft.KeyboardType.NUMBER),#, ref="telefono"),
            ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL),#, ref="email"),
            ft.TextField(label="CUIL",value=None),#, ref="cuil"),
            ft.TextField(label="DNI",value=None),#, ref="dni"),
            ft.TextField(label="WhatsApp", keyboard_type=ft.KeyboardType.NUMBER),#, ref="whatsapp"),
            ft.Text("Revise bien los campos antes de actualizar\nCampos vacios no se modifican",weight="bold",size=14)
        ])   
        self.content_Row_button = ft.Row(scroll=ft.ScrollMode.HIDDEN,visible=True,expand=True,
            controls=[
                self.boton_abrir_form,
                ft.TextButton("Exportar",tooltip="Exporte un archivo.csv\na la carpeta /descargas",
                            on_click= lambda e:
                                self.exportar_clientes_a_csv()),
                ft.TextButton("Importar",tooltip="Importe un archivo.csv\na la carpeta /descargas",
                            on_click=lambda e:
                                self.importar_tabla_clientes()),
                ft.TextButton("Ventas",tooltip="En desarrollo",
                              on_click=self.ventas_cliente),
                ft.TextButton("Presupuestos",tooltip="En desarrollo",
                              on_click=self.presupuesto_cliente),
                ft.TextButton("Opciones",tooltip="En desarrollo")]
            ,alignment= ft.MainAxisAlignment.SPACE_AROUND,)
                        #Objetivos boton ventas / algo parecido para presupuestos
        self.content_Row_detalle_pag = ft.Text("Clientes ",weight="bold",theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.row_tabla_clientes = ft.Row(expand=True,visible=True,alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                         )
        self.row_tabla_venta = ft.Row(expand=True)
        self.row_tabla_presupuesto = ft.Row(expand=True)
        
    
    def build(self):
        
        self.main_content_button = ft.Column(expand=False,adaptive=True,col=2)
        self.main_content_area = ft.Column(expand=True,adaptive=True) 
        self.row_buttons_up = ft.Row(expand=True)
        self.row_buttons_area = ft.Row(expand=True)
        self.row_tabla_clientes.controls.append(self.tabla_clientes)
        self.main_content_area.controls.append(self.content_Row_detalle_pag)
        self.row_buttons_up.controls.append(self.content_Row_button)
        self.main_content_area.controls.append(self.searchbar) 
        self.main_content_area.controls.append(self.row_buttons_up)   
        #self.row_buttons_up.controls.append(self.boton_abrir_form)    
        self.main_content_button.controls.append(self.row_buttons_area)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="grey"))   
        self.main_content_area.controls.append(ft.Text("Lista de clientes ",weight="bold",size=16))         
        self.main_content_area.controls.append(self.row_tabla_clientes)
        self.row_tabla_venta.controls.append(self.tabla_ventas_cliente)  
        self.row_tabla_presupuesto.controls.append(self.tabla_presupuestos_cliente)
        self.main_content_area.controls.append(ft.Text("Toque un cliente para ver más opciones ",weight="bold",size=14))
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="grey"))
        self.main_content_area.controls.append(ft.Text("Ventas y presupuestos con cliente; ",weight="bold",size=16))
       
        self.main_content_area.controls.append(self.file_picker)
        #self.formulario_area.controls.append(self.boton_opcion_guardar)
        return ft.Column(
            controls=[
                
                self.main_content_area,
                self.formulario_area,
                self.formulario_EDIT,
                self.main_content_button,
                self.row_tabla_venta,
                self.row_tabla_presupuesto
            ]) 
#nuevo codi
    def opcion_guardar(self,e):
        #ocultar boton guardar en row de formulario_area:
        self.boton_opcion_guardar.visible = True
        self.update()
#presupuesto_cliente #Mejorar 
    def presupuesto_cliente(self,e):
        self.tabla_clientes.visible = True
        self.tabla_ventas_cliente.visible = False
        self.tabla_presupuestos_cliente.visible = True
        self.main_content_area.update()
        self.filtrar_presupuestos()
        self.update()

    def filtrar_presupuestos(self):
        query = self.searchbar.value.strip()
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect("database_empresa.db")
            cursor = conexion.cursor()

            # Consulta combinada usando JOIN para optimizar
            cursor.execute("""
                SELECT 
                    c.id AS cliente_id, 
                    c.nombre, 
                    p.fecha, 
                    p.total
                FROM clientes c
                LEFT JOIN presupuestos p ON c.id = p.cliente_id
                WHERE c.nombre LIKE ? OR c.telefono LIKE ?
                ORDER BY p.fecha DESC
            """, (f"%{query}%", f"%{query}%"))

            # Guardar resultados
            self.lista_presupuesto_cliente = cursor.fetchall()

        except Exception as e:
            print(f"Error al filtrar presupuestos: {e}")
            self.lista_presupuesto_cliente = []  # Asegurarse de que esté vacía si hay un error

        finally:
            conexion.close()
        

        # Actualizar la tabla en la interfaz
        self.actualizar_tabla_presupuestos_clientes()

    def actualizar_tabla_presupuestos_clientes(self):
        # Crear filas para la tabla
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(presupuesto[0]),size=16)),  # ID del cliente
                    ft.DataCell(ft.Text(presupuesto[1], size=14)),       # Nombre del cliente
                    ft.DataCell(ft.Text(presupuesto[2] or "", size=14)), # Fecha de la presupuesto
                    ft.DataCell(ft.Text(str(presupuesto[3] or ""), size=14)), # Total de la presupuesto
                ],
                on_select_changed=lambda e, id=presupuesto[0],data=presupuesto[2]: self.mostrar_detalles_presupuesto(id,data),#Pasamos la fecha
            )
            for presupuesto in self.lista_presupuesto_cliente
        ]

        # Actualizar la tabla con las filas generadas
        self.tabla_presupuestos_cliente.rows = rows
        self.update()

    def mostrar_detalles_presupuesto(self, cliente_id, fecha_presupuesto):
        """Muestra un diálogo con los detalles de un presupuesto filtrado por cliente y fecha."""
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()

        try:
            cursor.execute(
                '''
                SELECT p.id_presupuesto, p.fecha, c.nombre, p.total
                FROM presupuestos p
                LEFT JOIN clientes c ON p.cliente_id = c.id
                WHERE p.cliente_id = ? AND p.fecha = ?
                ''',(cliente_id, fecha_presupuesto))
            presupuesto = cursor.fetchone()

            if not presupuesto:
                print(f"No se encontró un presupuesto para el cliente ID: {cliente_id} con fecha: {fecha_presupuesto}")
                return
            
            cursor.execute(
                '''
                SELECT pr.nombre_producto, dp.cantidad, dp.subtotal
                FROM detalles_presupuestos dp
                INNER JOIN productos pr ON dp.producto_id = pr.id_producto
                WHERE dp.presupuesto_id = ?
                ''',(presupuesto[0],))
            detalles = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error al consultar la base de datos: {e}")
            return
        
        finally:
            conexion.close()
        contenido = [#contenido para el control del dialogo
            ft.Text(f"ID Presupuesto: {presupuesto[0]}"),
            ft.Text(f"Fecha: {presupuesto[1]}"),
            ft.Text(f"Cliente: {presupuesto[2]}"),
            ft.Text(f"Total: ${presupuesto[3]:.2f}"),
            ft.Divider(),
            ft.Text("Detalles del Presupuesto:"),
        ]

        # Agregar los detalles al contenido
        for detalle in detalles:
            contenido.append(
                ft.Text(f"{detalle[0]} - Cantidad: {detalle[1]}, Subtotal: ${detalle[2]:.2f}")
            )

        # Mostrar diálogo
        self.dialogo = ft.AlertDialog(
            title=ft.Text("Detalles del Presupuesto"),
            content=ft.Column(controls=contenido),#agregamos el contenido
            actions=[ft.TextButton(
                "Generar PDF",
                tooltip="Generar un pdf del presupuesto",
                on_click=lambda e:
                  self.generar_pdf_presupuesto(presupuesto, detalles)),
                
                ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = self.dialogo
        self.dialogo.open = True
        self.page.update()

    def generar_pdf_presupuesto(self, presupuesto, detalles_presupuesto):
        self.dialogo.open=False
        self.page.update()
        
        #self.dismiss_dialog()
        """Generar el PDF con los datos de un presupuesto específico."""
        if not presupuesto:
            print("Datos del presupuesto no disponibles.")
            return None
        # Nombre del archivo PDF
        numero_presupuesto = str(presupuesto[0])
        nombre_pdf = f"presupuesto_{numero_presupuesto}.pdf"

        # Determinar el directorio de Descargas según el sistema operativo
        sistema = platform.system()
        if sistema == "Linux" or "ANDROID_STORAGE" in os.environ:  # Android o Linux
            directorio = os.path.join(os.getenv('EXTERNAL_STORAGE', '/storage/emulated/0'), "Download")
        elif sistema == "Windows":  # Windows
            directorio = os.path.join(os.getenv('USERPROFILE'), "Downloads")
        elif sistema == "Darwin":  # macOS
            directorio = os.path.join(os.path.expanduser("~"), "Downloads")
        else:
            raise Exception("No se puede determinar el directorio de Descargas.")

        # Crear la carpeta si no existe
        if not os.path.exists(directorio):
            os.makedirs(directorio)

        # Ruta completa del archivo PDF
        ruta_pdf = os.path.join(directorio, nombre_pdf)

        # Crear una instancia del objeto PDF
        pdf = fpdf.FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Encabezado
        pdf.set_font("Arial", size=17)
        pdf.cell(200, 10, txt="NOMBRE DE LA EMPRESA", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Fecha: {presupuesto[1]}", ln=True, align='C')
        pdf.ln(10)

        # Información del presupuesto
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt=f"Presupuesto ID: {presupuesto[0]}", ln=True)
        pdf.cell(200, 10, txt=f"Cliente: {presupuesto[2]}", ln=True)
        pdf.cell(200, 10, txt=f"Total: ${presupuesto[3]:.2f}", ln=True)
        pdf.ln(10)

        # Título de la tabla
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(80, 10, txt="Producto", border=1, align='C')
        pdf.cell(40, 10, txt="Cantidad", border=1, align='C')
        pdf.cell(40, 10, txt="Subtotal", border=1, align='C')
        pdf.ln()

        # Detalles de los productos
        pdf.set_font("Arial", size=12)
        for detalle in detalles_presupuesto:
            pdf.cell(80, 10, txt=detalle[0], border=1)  # Nombre del producto
            pdf.cell(40, 10, txt=str(detalle[1]), border=1, align='C')  # Cantidad
            pdf.cell(40, 10, txt=f"${detalle[2]:.2f}", border=1, align='R')  # Subtotal
            pdf.ln()

        # Pie de página con el total
        pdf.ln(10)
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(120, 10, txt="Total General", align='R')
        pdf.cell(40, 10, txt=f"${presupuesto[3]:.2f}", border=1, align='R')
        pdf.ln(20)

        # Guardar el PDF
        try:
            pdf.output(ruta_pdf)
            print(f"PDF guardado en: {ruta_pdf}")
        except Exception as e:
            print(f"Error al guardar el archivo PDF: {e}")
        alerta = f"PDF guardado en: {ruta_pdf}"
        print(alerta)
        #Dialogo para imprimir pdf presupuesto
        self.dialog_alert = ft.AlertDialog(
            title=ft.Text("PDF generado exitosamente"),
            content=ft.Text(alerta),
            actions=[],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dialog_alert
        self.dialog_alert.open = True
        self.page.update()    

#ventas_clientes
    def ventas_cliente(self,e):
        self.tabla_clientes.visible = True
        self.tabla_ventas_cliente.visible = True
        self.tabla_presupuestos_cliente.visible = False
        self.main_content_area.update()
        self.filtrar_ventas()
        self.update()
    
    def filtrar_ventas(self):
        query = self.searchbar.value.strip()
        try:
            # Conectar a la base de datos
            conexion = sqlite3.connect("database_empresa.db")
            cursor = conexion.cursor()

            # Consulta combinada usando JOIN para optimizar
            cursor.execute("""
                SELECT 
                    c.id AS cliente_id, 
                    c.nombre, 
                    v.fecha, 
                    v.total
                FROM clientes c
                LEFT JOIN ventas v ON c.id = v.cliente_id
                WHERE c.nombre LIKE ? OR c.telefono LIKE ?
                ORDER BY v.fecha DESC
            """, (f"%{query}%", f"%{query}%"))

            # Guardar resultados
            self.lista_venta_cliente = cursor.fetchall()

        except Exception as e:
            print(f"Error al filtrar ventas: {e}")
            self.lista_venta_cliente = []  # Asegurarse de que esté vacía si hay un error

        finally:
            conexion.close()
        

        # Actualizar la tabla en la interfaz
        self.actualizar_tabla_ventas_clientes()
    
    def actualizar_tabla_ventas_clientes(self):
        # Crear filas para la tabla
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(venta[0]), size=14)),  # ID cliente
                    ft.DataCell(ft.Text(venta[1], size=14)),       # Nombre del cliente
                    ft.DataCell(ft.Text(venta[2] or "", size=14)), # Fecha de la venta
                    ft.DataCell(ft.Text(str(venta[3] or ""), size=14)), # Total de la venta
                ],
                on_select_changed=lambda e, id=venta[0],data=venta[2]: self.mostrar_detalles_venta(id,data),
            )
            for venta in self.lista_venta_cliente
        ]

        # Actualizar la tabla con las filas generadas
        self.tabla_ventas_cliente.rows = rows
        self.update()

    def mostrar_detalles_venta(self, cliente_id, fecha_venta):
        """Muestra un diálogo con los detalles de una venta filtrada por cliente y fecha."""
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()

        try:
            # Obtener los datos principales de la venta y el cliente asociado
            cursor.execute(
                '''
                SELECT v.id, v.fecha, c.nombre, v.total
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                WHERE v.cliente_id = ? AND v.fecha = ?
                ''',
                (cliente_id, fecha_venta)
            )
            venta = cursor.fetchone()

            if not venta:
                print(f"No se encontró una venta para el cliente ID: {cliente_id} con fecha: {fecha_venta}")
                return

            # Obtener los detalles de la venta
            cursor.execute(
                '''
                SELECT pr.nombre_producto, dv.cantidad, dv.subtotal
                FROM detalles_ventas dv
                INNER JOIN productos pr ON dv.producto_id = pr.id_producto
                WHERE dv.venta_id = ?
                ''',
                (venta[0],)  # Usar venta_id del resultado
            )
            detalles = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error al consultar la base de datos: {e}")
            return
        finally:
            conexion.close()

        # Crear contenido del diálogo
        contenido = [
            ft.Text(f"ID Venta: {venta[0]}"),
            ft.Text(f"Fecha: {venta[1]}"),
            ft.Text(f"Cliente: {venta[2]}"),
            ft.Text(f"Total: ${venta[3]:.2f}"),
            ft.Divider(),
            ft.Text("Detalles de la Venta:"),
        ]

        # Agregar los detalles al contenido
        for detalle in detalles:
            contenido.append(
                ft.Text(f"{detalle[0]} - Cantidad: {detalle[1]}, Subtotal: ${detalle[2]:.2f}")
            )

        # Mostrar diálogo detalle venta
        self.dialogo = ft.AlertDialog(
            title=ft.Text("Detalles de la Venta"),
            content=ft.Column(controls=contenido),
            actions=[
                #ft.TextButton("Cerrar", on_click=lambda e: self.dismiss_dialog()),
                ft.TextButton("Generar PDF",
                tooltip="Generar un pdf de la venta",
                on_click=lambda e: 
                    self.generar_pdf_venta(venta, detalles)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = self.dialogo
        self.dialogo.open = True
        self.page.update()

    def generar_pdf_venta(self, venta, detalles_venta):
        self.dialogo.open = False
        self.page.update()
        if not venta:
            print("Datos de la venta no disponibles.")
            return None

        numero_venta = str(venta[0])
        nombre_pdf = f"venta_{numero_venta}.pdf"

        sistema = platform.system()
        if sistema == "Linux" or "ANDROID_STORAGE" in os.environ: 
            directorio = os.path.join(os.getenv('EXTERNAL_STORAGE', '/storage/emulated/0'), "Download")
        elif sistema == "Windows":  
            directorio = os.path.join(os.getenv('USERPROFILE'), "Downloads")
        elif sistema == "Darwin":  
            directorio = os.path.join(os.path.expanduser("~"), "Downloads")
        else:
            raise Exception("No se puede determinar el directorio de Descargas.")

        if not os.path.exists(directorio):
            os.makedirs(directorio)

        ruta_pdf = os.path.join(directorio, nombre_pdf)

        pdf = fpdf.FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font("Arial", size=17)
        pdf.cell(200, 10, txt="NOMBRE DE LA EMPRESA", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Fecha: {venta[1]}", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt=f"Venta ID: {venta[0]}", ln=True)
        pdf.cell(200, 10, txt=f"Cliente: {venta[2]}", ln=True)
        pdf.cell(200, 10, txt=f"Total: ${venta[3]:.2f}", ln=True)
        pdf.ln(10)

        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(80, 10, txt="Producto", border=1, align='C')
        pdf.cell(40, 10, txt="Cantidad", border=1, align='C')
        pdf.cell(40, 10, txt="Subtotal", border=1, align='C')
        pdf.ln()

        pdf.set_font("Arial", size=12)
        for detalle in detalles_venta:
            pdf.cell(80, 10, txt=detalle[0], border=1)
            pdf.cell(40, 10, txt=str(detalle[1]), border=1, align='C')
            pdf.cell(40, 10, txt=f"${detalle[2]:.2f}", border=1, align='R')
            pdf.ln()

        pdf.ln(10)
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(120, 10, txt="Total General", align='R')
        pdf.cell(40, 10, txt=f"${venta[3]:.2f}", border=1, align='R')
        pdf.ln(20)

        try:
            pdf.output(ruta_pdf)
            print(f"PDF guardado en: {ruta_pdf}")
        except Exception as e:
            print(f"Error al guardar el archivo PDF: {e}")
        alerta = f"PDF guardado en: {ruta_pdf}"
        print(alerta)
        self.dialog_alert = ft.AlertDialog(
            title=ft.Text("PDF generado exitosamente"),
            content=ft.Text(alerta),
            actions=[],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dialog_alert
        self.dialog_alert.open = True
        self.page.update()
#Area de venta final
    def cerrar_dialogo(self):
        self.page.dialog = self.dialogo_importar
        self.dialogo_importar = False
        self.update()

        """Cierra el diálogo de importación."""           
    
    def importar_datos_csv(self, ruta_archivo):
        """Importa los datos del archivo CSV a la tabla 'clientes'."""
        try:
            # Verificar si el archivo existe
            if not os.path.isfile(ruta_archivo):
                self.dialog = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text(f"El archivo no existe: {ruta_archivo}"),
                    on_dismiss=lambda e: print("Dialog cerrado")  # Reemplaza con una acción si es necesario
                )

                return

            # Leer el archivo CSV
            with open(ruta_archivo, newline='', encoding='utf-8') as archivo_csv:
                lector_csv = csv.reader(archivo_csv)

                # Conectar a la base de datos
                with sqlite3.connect("database_empresa.db") as conexion:
                    cursor = conexion.cursor()

                    # Iterar sobre las filas del CSV
                    for fila in lector_csv:
                        if len(fila) != 6:  # Validar que cada fila tenga 6 columnas
                            self.dialog = ft.AlertDialog(
                                title=ft.Text("Error"),
                                content=ft.Text(f"Formato incorrecto en la fila: {fila}"),
                            )

                            return

                        # Insertar la fila en la base de datos
                        cursor.execute(
                            "INSERT INTO clientes (nombre, telefono, email, cuil, dni, whatsapp) VALUES (?, ?, ?, ?, ?, ?)",
                            fila
                        )
                    conexion.commit()

            # Mostrar éxito
            self.dialog_2 = ft.AlertDialog(
                title=ft.Text("Éxito"),
                content=ft.Text("Datos importados correctamente."),
                on_dismiss=lambda e: self.cerrar_dialogo()  # Cerrar el diálogo al terminar
                )
            self.page.dialog = self.dialog_2
            self.dialog_2 = open()
            self.page.update()


        except Exception as e:
            # Manejo de errores
            self.dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text(f"Ocurrió un error al importar los datos: {str(e)}"),
            )
            self.page.dialog = self.dialog
            self.dialog = True
            self.page.update()
#mensaje
    def mostrar_alerta(self, titulo, mensaje):
        txt = titulo
        self.dialogo = ft.AlertDialog(
            title=ft.Text(f"{txt}"),
            content=ft.Column(controls=ft.Text(f"{mensaje}")),
            actions=[ft.TextButton("Cerrar")],
        )
        self.page.dialog = self.dialogo
        self.dialogo.open()
        self.page.update()
    
    def dimiss_import_alert(self):
        self.dialogo_importar.open = False
        self.page.update()       
    
    def exportar_tabla_clientes(self):
        self.dialogo = ft.AlertDialog(
            title=ft.Text("Desea exportar la lista de clientes?",size=16),
            content=ft.Column(),
                    actions=[
            ft.TextButton("Cerrar", on_click= self.dismiss_alert()),
            ft.TextButton("Exportar cvs", on_click=lambda e: self.crear_tabla_clientes()),
            ],
            
        )
        self.page.dialog = self.dialogo
        self.dialogo.open=True            
        self.page.update()
    
    def crear_tabla_clientes(self,):
        self.dialogo.open=False
        self.page.update()
        self.exportar_clientes_a_csv()
    
    def dimiss_alert(self):
        self.dialogo.open=False
        self.page.update()
    
    def buscar_cliente(self, e):
        self.ocultar_tablas()
        query = self.searchbar.value.strip()
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()
        cursor.execute("""SELECT id, nombre, telefono 
                        FROM clientes 
                        WHERE nombre LIKE ? OR telefono LIKE ?
                        ORDER BY id DESC """, (f"%{query}%",f"%{query}%",))
        self.lista_clientes = cursor.fetchmany(15)

            
        self.actualizar_tabla_clientes()
        
        
        conexion.close()
    
    def ocultar_tablas(self):
        self.tabla_ventas_cliente.visible = False
        self.tabla_presupuestos_cliente.visible = False
    
    def actualizar_tabla_clientes(self):
        rows = [
            ft.DataRow(
                
                cells=[
                    ft.DataCell(ft.Text(str(cliente[0]),weight="bold",size=14,tooltip=f"{cliente[1]}")),
                    ft.DataCell(ft.Text(cliente[1],weight="bold",size=14,tooltip=f"{cliente[1]}")),
                    ft.DataCell(ft.Text(cliente[2] or "",weight="bold",size=14,tooltip=f"{cliente[2]}")),
                              
                    #ft.DataCell(ft.Text(cliente[4] or "")),
                    #ft.DataCell(ft.Text(cliente[5] or "")),
                    #ft.DataCell(ft.Text(cliente[6] or "")),
                ],on_select_changed=lambda e, id=cliente[0]:self.ver_cliente(id),
                
            )
            for cliente in self.lista_clientes
        ]
        self.tabla_clientes.rows = rows
        self.update()
    
    def abrir_formulario(self, e):
        self.ocultar_tablas()
        self.row_buttons_area.visible = False
        self.main_content_area.visible = False
        self.formulario_area.visible = True
        self.formulario_area.update()
        self.update()
    
    def cerrar_formulario(self,e):
        self.row_buttons_area.visible = True
        self.main_content_area.visible = True
        self.boton_opcion_guardar.visible = False
        self.formulario_area.visible =False
        
        self.limpiar_formulario(e)
        self.update()
        
        self.update()
    
    def limpiar_formulario(self, e):
        """Limpiar todos los campos del formulario."""
        for field in self.formulario_area.controls :
            if isinstance(field, ft.TextField):
                field.value = ""
        self.update()
        for field in self.formulario_EDIT.controls :
            if isinstance(field, ft.TextField):
                field.value = ""
        self.update()
    
    def guardar_cliente(self, e):
        self.boton_opcion_guardar.visible = False
        
        if not self.formulario_area.controls[0].value.split():
            snackbar = ft.SnackBar(content=ft.Text(f"No hay datos para guardar",weight="bold"),
                                    bgcolor="Red400")
            snackbar.open = True
            self.page.add(snackbar)
            self.page.update()
            
            
        else:
            try:
                conexion = sqlite3.connect("database_empresa.db")
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO clientes (nombre, telefono, email, cuil, dni, whatsapp) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        self.formulario_area.controls[0].value,
                        self.formulario_area.controls[1].value,
                        self.formulario_area.controls[2].value,
                        self.formulario_area.controls[3].value,
                        self.formulario_area.controls[4].value,
                        self.formulario_area.controls[5].value,
                    )
                )
                conexion.commit()
                conexion.close()
                if conexion:
                    print("Cliente guardado")
                    '''dialog = ft.AlertDialog(
                            title=ft.Text("Acción realizada con éxito",size=14),
                            )
                    self.page.dialog = dialog
                    dialog.open=True'''
                    snackbar = ft.SnackBar(content=ft.Text(f"Se añadio un nuevo cliente"),
                                    bgcolor="Green400")
                    snackbar.open = True
                    self.page.add(snackbar)
                    self.page.update()
                    self.cerrar_formulario(e)
                    self.limpiar_formulario(e)
            except Exception as e:
                print(f"Error {e}")
                '''dialog = ft.AlertDialog(
                        title=ft.Text(f"Error {e}",size=14),
                        )
                self.page.dialog = dialog
                dialog.open=True'''
                snackbar = ft.SnackBar(content=ft.Text(f"Error {e}"),
                                    bgcolor="Red300")
                snackbar.open = True
                self.page.add(snackbar)
                self.page.update()
            
    def ver_cliente(self, cliente_id):
        
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id= ?",(cliente_id,) )    
        resultado = cursor.fetchall()
        conexion.close()
        if resultado:
            
            print(f"¨{resultado}")

        print("seleccionaste un cliente")
        self.dialog = ft.AlertDialog(
                    title=ft.Text(f"Opciones para Cliente: {cliente_id}",size=16),
                    on_dismiss=[],
                    actions=[ft.TextButton("Editar", 
                                    on_click=lambda e, id=cliente_id: self.editar_cliente(id)),
                            ft.TextButton(text="Crear Presupuesto",
                                    on_click=lambda e, id=cliente_id: self.crear_presupuesto(id)),
                            ft.TextButton(text="Vender Productos",
                                    on_click=lambda e, id=cliente_id: self.vender_producto(id))
                                ])
        self.page.dialog = self.dialog
        self.dialog.open=True            
        self.page.update()    
#Para cerrar el dialogo    
    def editar_cliente(self,cliente_id):
        self.ocultar_tablas()
        self.dialog.open=False
        self.page.update()
        self.abrir_formulario_edit(cliente_id)
        self.page.update()
   
    def abrir_formulario_edit(self, cliente_id): 
        print(f"Se editara {cliente_id}") 
        self.row_buttons_area.visible = False
        self.main_content_area.visible = False
        self.formulario_EDIT.visible = True
        
        
        
        self.row_button_bottom.controls.append(ft.ElevatedButton("Cancelar", on_click=lambda e: self.cerrar_formulario_EDIT(e)))
        self.row_button_bottom.controls.append(ft.ElevatedButton("Actualizar", on_click=lambda e, id=cliente_id: self.actualizar_cliente(id)))

        self.formulario_EDIT.controls.append(self.row_button_bottom)
        self.formulario_EDIT.update()
        
        self.update()
    
    def cerrar_formulario_EDIT(self,e):
        print("Cerrando formulario")
        #Revisar porque a la segunda no funciona mas la verguen esten:
        self.row_buttons_area.visible = True
        self.main_content_area.visible = True

        self.row_button_bottom.clean()
        self.formulario_EDIT.visible = False
        self.formulario_EDIT.update()
        self.limpiar_formulario(e)
        self.update()
        
    def actualizar_cliente(self, cliente_id):
        print(f"Se presionó actualizar con cliente ID: {cliente_id}")
        
        try:
            # Obtener los valores del formulario
            campos = [
                ("telefono", self.formulario_EDIT.controls[0].value),
                ("email", self.formulario_EDIT.controls[1].value),
                ("cuil", self.formulario_EDIT.controls[2].value),
                ("dni", self.formulario_EDIT.controls[3].value),
                ("whatsapp", self.formulario_EDIT.controls[4].value),
            ]
            
            # Filtrar campos llenos
            campos_actualizar = [(campo, valor) for campo, valor in campos if valor and valor.strip() != ""]
            
            if not campos_actualizar:
                snackbar = ft.SnackBar(content=ft.Text("No hay ningun campo para actualizar"),
                                bgcolor="Red400")
                snackbar.open = True
                self.page.add(snackbar)
                print("No se proporcionaron valores para actualizar.")
                #return
            else:
            # Construir dinámicamente la consulta SQL
                set_clause = ", ".join([f"{campo} = ?" for campo, _ in campos_actualizar])
                valores = [valor for _, valor in campos_actualizar]
                valores.append(cliente_id)  # Agregar el ID del cliente al final
                
                consulta = f"""
                UPDATE clientes
                SET {set_clause}
                WHERE id = ?
                """
                
                # Conexión segura usando 'with'
                with sqlite3.connect("database_empresa.db") as conexion:
                    cursor = conexion.cursor()
                    
                    # Ejecutar la actualización
                    cursor.execute(consulta, valores)
                    conexion.commit()
                
                print("Cliente actualizado correctamente.")
                '''dialog = ft.AlertDialog(
                    title=ft.Text("Acción realizada con éxito", size=14),
                )
                self.page.dialog = dialog
                dialog.open = True
                self.page.update()'''
                self.limpiar_formulario(cliente_id)
                self.cerrar_formulario_EDIT(cliente_id)
                
                snackbar = ft.SnackBar(content=ft.Text(f"Cliente actualizado con exito"),
                                bgcolor="Green400")
                snackbar.open = True
                self.page.add(snackbar)
                self.update()
                
        
        except Exception as e:
            print(f"Error: {e}")
            snackbar = ft.SnackBar(content=ft.Text(f"Error{e}"),
                                bgcolor="red400")
            snackbar.open = True
            self.page.add(snackbar)
            self.page.update()      
    
    def borrar_cliente(self, e):
        # Implementar lógica para borrar un cliente seleccionado
        pass
    
    def update_content(self,new_content):#Funcion Principal
        self.main_content_area.controls.clear()#Para actualizar el contenido principal
        self.main_content_button.controls.clear()
        self.main_content_area.controls.append(new_content)#Debemos pasa el nuevo contenido
        self.update()#Actualizamos pantalla principal
#Area Presupuestos   
    def show_products(self, form_prod):
        self.update_content(form_prod)
    
    def abrir_productos(self, cliente_id):#Pasamos desde crear_presupuesto cliente_id
        print(f"Cliente ID seleccionado: {cliente_id}")
        form_prod = FormularioPROD_Presupuesto(cliente_id)
        self.show_products(form_prod)
    
    def crear_presupuesto(self,cliente_id):#LLamamos desde el dialogo pasando por id=cliente_id: self.crear_prespuesto(id)
        self.dialog.open=False
        self.ocultar_tablas()
        self.page.update()
        self.abrir_productos(cliente_id)
#Area Ventas   
    def show_prod_venta(self, form_prod_venta):
        self.update_content(form_prod_venta)
    
    def abrir_prod_venta(self, cliente_id):#Pasamos desde crear_presupuesto cliente_id
        print(f"Cliente ID seleccionado: {cliente_id}")
        form_prod_venta = FormularioPROD_(cliente_id)
        self.show_products(form_prod_venta)
    
    def vender_producto(self,cliente_id):
        self.ocultar_tablas()
        self.dialog.open=False
        self.page.update()
        self.abrir_prod_venta(cliente_id)
       
    def exportar_clientes_a_csv(self):
        """Exporta los datos de la tabla 'clientes' a un archivo CSV llamado 'Lista_clientes.csv'."""
        # Conectar a la base de datos
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()
        # Obtener los datos de la tabla clientes
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()

        if not clientes:
            print("No hay datos en la tabla 'clientes' para exportar.")
            snackbar = ft.SnackBar(content=ft.Text("No hay datos en la tabla 'clientes' para exportar.",weight="bold"),                              
                                bgcolor="Red400")
            snackbar.open = True
            self.page.add(snackbar)
            self.update()
            return None

        # Determinar el directorio de Descargas según el sistema operativo
        sistema = platform.system()
        if sistema == "Linux" or "ANDROID_STORAGE" in os.environ:  # Android o Linux
            directorio = os.path.join(os.getenv('EXTERNAL_STORAGE', '/storage/emulated/0'), "Download")
        elif sistema == "Windows":  # Windows
            directorio = os.path.join(os.getenv('USERPROFILE'), "Downloads")
        elif sistema == "Darwin":  # macOS
            directorio = os.path.join(os.path.expanduser("~"), "Downloads")
        else:
            raise Exception("No se puede determinar el directorio de Descargas.")

        # Crear la carpeta si nso existe
        if not os.path.exists(directorio):
            os.makedirs(directorio)

        # Ruta completa del archivo CSV
        ruta_csv = os.path.join(directorio, "Lista_clientes.csv")

        # Escribir los datos en el archivo CSV
        with open(ruta_csv, mode="w", newline="", encoding="utf-8") as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)

            # Escribir encabezados (ajustar según la estructura de tu tabla clientes)
            encabezados = ["ID", "nombre", "telefono", "email", "cuil","dni","whatsapp"]
            escritor_csv.writerow(encabezados)

            # Escribir los datos de los clientes
            for cliente in clientes:
                escritor_csv.writerow(cliente)

        print(f"Archivo CSV generado exitosamente: {ruta_csv}")
        snackbar = ft.SnackBar(content=ft.Text(f"Archivo CSV generado exitosamente: {ruta_csv}",weight="bold"),                              
                            bgcolor="Green400")
        snackbar.open = True
        self.page.add(snackbar)
        self.update()       
        return    
    
    def importar_tabla_clientes(self):
        """Abre un diálogo para importar datos desde un archivo CSV en la carpeta Descargas."""
        try:
            directorio_descargas = obtener_directorio_descargas()
            ruta_predeterminada = os.path.join(directorio_descargas, "tu_archivo.csv")
            
            # Campo de entrada para la ruta del archivo.
            self.ruta_archivo = ft.TextField(label="Ejemplo: tu_archivo.csv", value=ruta_predeterminada)

            # Crear el diálogo.
            self.dialogo_importar = ft.AlertDialog(
                #adaptive=True,
                title=ft.Text("¿Desea importar la lista de clientes?", size=16),
                content=ft.Column([
                    ft.Text(f"El archivo debe estar en la carpeta local de descargas:\n{directorio_descargas}", size=14),
                    ft.Divider(thickness=1, opacity=0),
                    self.ruta_archivo,
                    ft.Divider(thickness=1, opacity=0),
                    ft.TextButton("Importar CSV", on_click=lambda e: self.importar_datos_csv(self.ruta_archivo.value))
                ]),)
            self.page.dialog = self.dialogo_importar
            self.dialogo_importar.open = True
            self.page.update()

        except Exception as e:
            print(f"Error al abrir el diálogo: {e}")

def obtener_directorio_descargas():
        sistema = platform.system()
        if sistema == "Linux" or "ANDROID_STORAGE" in os.environ:  # Android o Linux
            return os.path.join(os.getenv('EXTERNAL_STORAGE', '/storage/emulated/0'), "Download")
        elif sistema == "Windows":  # Windows
            return os.path.join(os.getenv('USERPROFILE'), "Downloads")
        elif sistema == "Darwin":  # macOS
            return os.path.join(os.path.expanduser("~"), "Downloads")
        else:
            raise Exception("No se puede determinar el directorio de Descargas.")


#Objetivo de hoy, ver presupuesto del cliente
# arreglar metodos de busqueda de las ventas, y los detalles de la venta que vaya a ventas con el cliente_id:

#Colocar dialogo al exportar
