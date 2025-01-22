import flet as ft
import sqlite3
import os
import platform
import fpdf

class FormularioVE_(ft.Column): 
    def __init__(self, venta_id): 
        super().__init__()
        self.venta_id = venta_id 
        self.lista_ventas = [] 
        self.detalles_ventas = [] 
        self.main_content_area = None
        self.searchbar = ft.TextField(
            label=f"Buscar ventas, último ID guardado: {self.venta_id}",
            on_change=self.buscar_en_base_de_datos,
            autofocus=False,
            tooltip=f"Último ID {self.venta_id}",
            keyboard_type=ft.KeyboardType.DATETIME
        )
        self.tabla_busqueda = ft.DataTable(
                horizontal_margin=0.4, column_spacing=5, scale=1, visible=True,expand=True,
                border_radius=10,width="adaptative",
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
                ft.DataColumn(label=ft.Text("ID Venta", size=16)),
                ft.DataColumn(label=ft.Text("Fecha", size=16)),
                ft.DataColumn(label=ft.Text("Cliente", size=16)),
                ft.DataColumn(label=ft.Text("Total", size=16)),
            ],
            rows=[],
        )
        self.resultados_selecccionados = ft.DataTable(
            horizontal_margin=0.4, column_spacing=5, scale=1, visible=True,expand=True,
            border_radius=10,width="adaptative",
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
                ft.DataColumn(label=ft.Text("ID Venta", size=16)), 
                ft.DataColumn(label=ft.Text("Producto", size=16)),
                ft.DataColumn(label=ft.Text("Cantidad", size=16)), 
                ft.DataColumn(label=ft.Text("Subtotal", size=16)), 
            ],
            rows=[],
        )
        self.content_Row_button = ft.Row(scroll=ft.ScrollMode.HIDDEN,visible=True,expand=True,controls=[
            ft.TextButton("Exportar",tooltip="Exporte un archivo.cvs\na la carpeta /descargas"),
            ft.TextButton("Importar",tooltip="Importe un archivo.cvs\na la carpeta /descargas"),
            ft.TextButton("fecha",tooltip="Desarollo"),ft.TextButton("cliente",tooltip="Desarollo"),
            ],alignment= ft.MainAxisAlignment.SPACE_AROUND,)
        self.content_Row_detalle_pag = ft.Text("Ventas ",weight="bold",theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.content_Row_tabla = ft.Row(visible=True,expand=True, 
                                        controls=[self.tabla_busqueda],
                                        alignment= ft.MainAxisAlignment.SPACE_AROUND,
                                        on_scroll_interval=3)

    def build(self):

        self.main_content_area = ft.Column()
        self.row_buttons_up = ft.Row(expand=True)
        self.row_buttons_up.controls.append(self.content_Row_button)
        self.main_content_area.controls.append(self.content_Row_detalle_pag)
        self.main_content_area.controls.append(self.searchbar)
        self.main_content_area.controls.append(self.row_buttons_up)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="grey"))
        self.main_content_area.controls.append(ft.Text("Busqueda por fecha, id del cliente o id de la venta\nLista de ventas"))
        self.main_content_area.controls.append(self.content_Row_tabla)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="grey"))
        return ft.Column(controls=[
            self.main_content_area,
        ], expand=True)

    def buscar_en_base_de_datos(self, e):
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()

        query = self.searchbar.value.strip()
        cursor.execute("""SELECT id,  fecha, cliente_id, total 
                       FROM ventas 
                       WHERE id LIKE ? OR fecha LIKE ? OR cliente_id LIKE ?
                       ORDER BY fecha DESC """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        self.lista_ventas = cursor.fetchmany(15)
        conexion.close()
        self.actualizar_tabla_buscar()
    
    
    def actualizar_tabla_buscar(self):
        rows = []

        for venta in self.lista_ventas:
            rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(venta[0]))),
                    ft.DataCell(ft.Text(str(venta[1]))),
                    ft.DataCell(ft.Text(str(venta[2]))),
                    ft.DataCell(ft.Text(f"${venta[3]:.2f}")),
                ],
                on_select_changed=lambda e, id=venta[0]: self.mostrar_detalles_venta(id)
            ))
        self.tabla_busqueda.rows = rows
        self.update()
    
    def mostrar_detalles_venta(self, venta_id):
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()

        try:
            cursor.execute(
                '''SELECT v.id, v.fecha, c.nombre, v.total
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                WHERE v.id = ?''',
                (venta_id,)
            )
            venta = cursor.fetchone()

            if not venta:
                print(f"No se encontró una venta con ID: {venta_id}")
                return

            cursor.execute(
                '''SELECT p.nombre_producto, dv.cantidad, dv.subtotal
                FROM detalles_ventas dv
                INNER JOIN productos p ON dv.producto_id = p.id_producto
                WHERE dv.venta_id = ?
                ''',
                (venta_id,)
            )
            detalles = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error al consultar la base de datos: {e}")
            return
        finally:
            conexion.close()

        contenido = [
            ft.Text("Verifique los datos",size=14),
            ft.Divider(thickness=1,opacity=1,color="black"),
            ft.DataTable(column_spacing=10,  horizontal_margin=10,                                    
                columns=[
                ft.DataColumn(label=ft.Text("Id", size=13)),
                ft.DataColumn(label=ft.Text("Fecha", size=13)),
                ft.DataColumn(label=ft.Text("Nombre", size=13)),
                ],
                rows=[ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(venta[0]),size=13)),
                    ft.DataCell(ft.Text(str(venta[1]),size=13)),
                    ft.DataCell(ft.Text(str(venta[2]),size=13))])])
            ]
        contenido.append(ft.Text("Productos o Servicios",size=10))
        contenido.append(ft.Divider(thickness=1,opacity=1,color="black"))
        contenido.append(ft.Text("P/S  Cantidad  Subtotal",size=15))
        for detalle in detalles:
            
            contenido.append(ft.DataTable(
                horizontal_margin=0.4, column_spacing=10, visible=True,expand=True,
                                 
                columns=[
                ft.DataColumn(label=ft.Text(" ", size=13)),
                ft.DataColumn(label=ft.Text(" ", size=13)),
                ft.DataColumn(label=ft.Text(" ", size=13)),
                ],
                rows=[ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(detalle[0]),size=13)),
                    ft.DataCell(ft.Text(str(detalle[1]),size=13)),
                    ft.DataCell(ft.Text(str(f"{detalle[2]:.2f}"),size=13))])]),
                
            )
        contenido.append(ft.Text(f"Total: ${venta[3]:.2f}"))
        self.dialogo = ft.AlertDialog(adaptive=True,
            title=ft.Text("Detalles de la Venta",size=16),
            content=ft.Column(scroll=ft.ScrollMode.HIDDEN,controls=contenido),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.dismiss_dialog()),
                ft.TextButton("Generar PDF", on_click=lambda e: self.generar_pdf(venta, detalles)),
            ],
        )

        self.page.dialog = self.dialogo
        self.dialogo.open = True
        self.page.update()
    
    def dismiss_dialog(self):
        self.dialogo.open = False
        self.page.update()
    
        
    def dismiss_alert(self):
        self.dialog_alert.open = False
        self.page.update()

    def generar_pdf(self, venta, detalles_venta):
            self.dismiss_dialog()
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
                actions=[
                    ft.TextButton("Aceptar", on_click=lambda e: self.dismiss_alert())
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.page.dialog = self.dialog_alert
            self.dialog_alert.open = True
            self.page.update()


