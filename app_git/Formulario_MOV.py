import flet as ft
import sqlite3
import os
import platform
import fpdf

class FormularioMOV_(ft.Column):
    def __init__(self, presupuesto_id):
        super().__init__()
        self.presupuesto_id = presupuesto_id
        self.lista_presupuesto = []
        self.detalles_presupuestos = []
        self.main_content_area = None

        self.searchbar = ft.TextField(label=f"Buscar Pre.., ultimo id guardado; {self.presupuesto_id}",
            on_change=self.buscar_en_base_de_datos,
            autofocus=False,
            keyboard_type=ft.KeyboardType.DATETIME,
            tooltip=f"Ultimo id {self.presupuesto_id}")#From presupuestos
        self.tabla_busqueda = ft.DataTable(#From presupuestos
            horizontal_margin=0.4, column_spacing=40, scale=1, visible=True,expand=True,
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
                ft.DataColumn(label=ft.Text("ID Presupuesto", size=16)),
                ft.DataColumn(label=ft.Text("Cliente", size=16)),
                ft.DataColumn(label=ft.Text("Fecha", size=16)),
            ],
            rows=[],
        )
        self.resultados_selecccionados = ft.DataTable(
            horizontal_margin=0.4, column_spacing=10, scale=1, visible=True,expand=True,
            border_radius=10,width="adaptative",
            bgcolor="lightgrey",
            border=ft.border.all(4, "lightblue"),
            
            vertical_lines=ft.border.BorderSide(3, "lightblue"),
            horizontal_lines=ft.border.BorderSide(3, "lightblue"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.LIGHT_BLUE,
            heading_row_height=50,
            data_row_color={"hovered": "0x30FFF600"},
            #show_checkbox_column=True,
            divider_thickness=0,
            columns=[
                ft.DataColumn(label=ft.Text("ID", size=16)),
                ft.DataColumn(label=ft.Text("Nombre", size=16)),
                ft.DataColumn(label=ft.Text("Precio", size=16)),
                ft.DataColumn(label=ft.Text("Cantidad", size=16)),
                ft.DataColumn(label=ft.Text("Subtotal", size=16)),
                ft.DataColumn(label=ft.Text("Eliminar", size=16)),
            ],
            rows=[],
        )
        self.content_Row_button = ft.Row(visible=True, controls=[
            ft.TextButton("Exportar",tooltip="Desarollo"),ft.TextButton("Importar",tooltip="Desarollo"),
            ft.TextButton("Filtrar",tooltip="Desarollo"),ft.TextButton("Opciones",tooltip="Desarollo"),
            ],alignment= ft.MainAxisAlignment.SPACE_AROUND,)
        self.content_Row_detalle_pag = ft.Text("Presupuestos ",weight="bold",theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.content_tabla = ft.Row(expand=True)
    def build(self):
        self.row_buttons_up = ft.Row(expand=True)
        self.content_tabla.controls.append(self.tabla_busqueda)
        
        self.main_content_area = ft.Column(expand=True)
        self.row_buttons_up.controls.append(self.content_Row_button)
        self.main_content_area.controls.append(self.content_Row_detalle_pag)
        self.main_content_area.controls.append(self.searchbar)
        self.main_content_area.controls.append(self.row_buttons_up)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="grey"))
        self.main_content_area.controls.append(ft.Text("Busqueda por fecha, id del cliente o id del prespuesto\nLista de presupuestos",theme_style="bold"))
        self.main_content_area.controls.append(self.content_tabla)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="grey"))

        return ft.Column(controls=[
            self.main_content_area,

            ],
            expand=True)

    def buscar_en_base_de_datos(self,e):
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()

        query = self.searchbar.value.strip()
        cursor.execute("""
            SELECT id_presupuesto, cliente_id, fecha total 
            FROM presupuestos 
            WHERE id_presupuesto LIKE ? OR cliente_id LIKE ? OR fecha LIKE ?
            ORDER BY fecha DESC """, (f"%{query}%",f"%{query}%",f"%{query}%",))
        self.lista_presupuestos = cursor.fetchall()

        conexion.close()

        self.actualizar_tabla_buscar()     
    
    def actualizar_tabla_buscar(self):
        rows = []

        for presupuesto in self.lista_presupuestos:
            rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(presupuesto[0]))),
                    ft.DataCell(ft.Text(str(presupuesto[1]))),
                    ft.DataCell(ft.Text(str(str(presupuesto[2])))),
                ],on_select_changed=lambda e, id=presupuesto[0]:self.mostrar_detalles_presupuesto(id)
            ))
        self.tabla_busqueda.rows = rows
        self.update()
   
    def mostrar_detalles_presupuesto(self, presupuesto_id):
        """Muestra un diálogo con los detalles de un presupuesto."""
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()

        try:
            # Obtener los datos principales del presupuesto y el cliente asociado
            cursor.execute(
                '''SELECT p.id_presupuesto, p.fecha, c.nombre, p.total
                FROM presupuestos p
                LEFT JOIN clientes c ON p.cliente_id = c.id
                WHERE p.id_presupuesto = ?''',
                (presupuesto_id,)
            )
            presupuesto = cursor.fetchone()

            if not presupuesto:
                print(f"No se encontró un presupuesto con ID: {presupuesto_id}")
                return

            # Obtener los detalles del presupuesto
            cursor.execute(
                '''SELECT pr.nombre_producto, dp.cantidad, dp.subtotal
                FROM detalles_presupuestos dp
                INNER JOIN productos pr ON dp.producto_id = pr.id_producto
                WHERE dp.presupuesto_id = ?''',
                (presupuesto_id,)
            )
            detalles = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error al consultar la base de datos: {e}")
            return
        finally:
            conexion.close()

        # Crear contenido del diálogo
        contenido = [
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

        # Mostrar diálogo de presupuestos
        self.dialogo = ft.AlertDialog(
            title=ft.Text("Detalles del Presupuesto"),
            content=ft.Column(controls=contenido),
                    actions=[
            ft.TextButton("Cerrar", on_click=lambda e: self.dismiss_dialog()),
            ft.TextButton("Generar PDF", on_click=lambda e: self.generar_pdf(presupuesto, detalles)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = self.dialogo
        self.dialogo.open = True
        self.page.update()
    
    def dismiss_dialog(self):
        self.dialogo.open = False
        self.page.update()
    
    def generar_pdf(self, presupuesto, detalles_presupuesto):
        self.dismiss_dialog()
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
    
    def dismiss_alert(self):
        self.dialog_alert.open = False
        self.page.update()

            
