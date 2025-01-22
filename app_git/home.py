import sqlite3
import flet as ft


class Home_(ft.Column):
    def __init__(self):
        super().__init__()
        self.lista_clientes = []
        self.lista_productos = []
        self.lista_empleados = []
        self.lista_ventas = []
        self.lista_presupuestos = []
        self.detalles_presupuestos = []
        self.detalles_ventas = []
        #Falta detalle_servicio
        # tabla servicio
        # tabla de estado de venta:

        self.main_content_area = None
        self.main_content_button = None
        self.row_buttons = ft.Row(expand=True, controls=[
            ft.ElevatedButton("Ingresar a Base de Datos",
                               on_click=self.buscar_en_base_de_datos)
        ])
        self.searchbar = ft.TextField(expand=True,
            label="Buscador",
            on_change=self.buscar_en_base_de_datos,
            autofocus=False
        )
        self.tabla_busqueda = ft.DataTable(
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
            data_row_color={"hovered": "0x30FF0000"},
            #show_checkbox_column=True,
            divider_thickness=0,
            columns=[
                ft.DataColumn(label=ft.Text("ID",size=16)),
                ft.DataColumn(label=ft.Text("Nombre",size=16)),
                ft.DataColumn(label=ft.Text("Detalles",size=16)),
            ],
            rows=[],
        )

    def build(self):
        self.main_content_button = ft.Column(expand=True)
        self.main_content_area = ft.Column(expand=True)
        self.main_content_button.controls.append(self.row_buttons)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="grey"))
        self.main_content_area.controls.append(self.tabla_busqueda)
        self.main_content_area.controls.append(ft.Divider(thickness=1,opacity=1,color="grey"))
        return ft.Column(
            controls=[
                self.searchbar,
                self.main_content_button,
                self.main_content_area,
            ])

    def buscar_en_base_de_datos(self, e):
        """Buscar en todas las tablas de la base de datos."""
        conexion = sqlite3.connect("database_empresa.db")
        cursor = conexion.cursor()
        query = self.searchbar.value.strip()
        # Buscar en clientes
        cursor.execute("SELECT id, nombre, telefono FROM clientes WHERE nombre LIKE ?", (f"%{query}%",))
        self.lista_clientes = cursor.fetchall()
        # Buscar en productos
        cursor.execute("SELECT id_producto, nombre_producto, descripcion FROM productos WHERE nombre_producto LIKE ?", (f"%{query}%",))
        self.lista_productos = cursor.fetchall()
        # Buscar en ventas
        cursor.execute("SELECT id, fecha, total FROM ventas WHERE fecha LIKE ?", (f"%{query}%",))
        self.lista_ventas = cursor.fetchall()
        # Buscar en presupuestos
        cursor.execute("SELECT id_presupuesto, cliente_id, fecha FROM presupuestos WHERE cliente_id LIKE ?", (f"%{query}%",))
        self.lista_presupuestos = cursor.fetchall()
        conexion.close()
        self.actualizar_tabla_buscar()

    def actualizar_tabla_buscar(self):
        """Actualizar la tabla_busqueda con resultados."""
        rows = []
        for cliente in self.lista_clientes:
            rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cliente[0]))),
                    ft.DataCell(ft.Text(cliente[1])),
                    ft.DataCell(ft.Text(cliente[2])),
                ]
            ))
        for producto in self.lista_productos:
            rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(producto[0]))),
                    ft.DataCell(ft.Text(producto[1])),
                    ft.DataCell(ft.Text(producto[2])),
                ]
            ))
        for venta in self.lista_ventas:
            rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(venta[0]))),
                    ft.DataCell(ft.Text(venta[1])),
                    ft.DataCell(ft.Text(str(venta[2]))),
                ]
            ))
        for presupuesto in self.lista_presupuestos:
            rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(presupuesto[0]))),
                    ft.DataCell(ft.Text(str(presupuesto[1]))),
                    ft.DataCell(ft.Text(str(presupuesto[2]))),
                ]
            ))

        self.tabla_busqueda.rows = rows
        self.update()

    def tabla_clientes(self, e):
        """Actualizar self.tabla_busqueda con la información de clientes."""
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cliente[0]))),
                    ft.DataCell(ft.Text(cliente[1])),
                    ft.DataCell(ft.Text(cliente[2])),
                ]
            )
            for cliente in self.lista_clientes
        ]
        self.tabla_busqueda.rows = rows
        self.update()

    def tabla_ventas(self, e):
        """Actualizar self.tabla_busqueda con la información de ventas."""
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(venta[0]))),
                    ft.DataCell(ft.Text(venta[1])),
                    ft.DataCell(ft.Text(str(venta[2]))),
                ]
            )
            for venta in self.lista_ventas
        ]
        self.tabla_busqueda.rows = rows
        self.update()

    def tabla_productos(self, e):
        """Actualizar self.tabla_busqueda con la información de productos."""
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(producto[0]))),
                    ft.DataCell(ft.Text(producto[1])),
                    ft.DataCell(ft.Text(producto[2])),
                ]
            )
            for producto in self.lista_productos
        ]
        self.tabla_busqueda.rows = rows
        self.update()

    def tabla_presupuestos(self, e):
        """Actualizar self.tabla_busqueda con la información de presupuestos."""
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(presupuesto[0]))),
                    ft.DataCell(ft.Text(str(presupuesto[1]))),
                    ft.DataCell(ft.Text(str(presupuesto[2])))]
            )
            for presupuesto in self.lista_presupuestos
        ]
        self.tabla_busqueda.rows = rows
        self.update()
