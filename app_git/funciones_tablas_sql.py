import sqlite3

def crear_tablas_empresa():
    """Crear las tablas necesarias en la base de datos y establecer relaciones."""
    conexion = sqlite3.connect("database_empresa.db")
    cursor = conexion.cursor()

    # Crear tabla clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT ,
            cuil TEXT ,
            dni TEXT ,
            whatsapp TEXT
        )
    ''')

    # Crear tabla productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_producto TEXT NOT NULL,
            descripcion TEXT,
            categoria TEXT,
            precio_unitario REAL,
            stock INTEGER,
            unidad_medida TEXT,
            fecha_vencimiento TEXT,
            codigo_barras TEXT,
            proveedor TEXT,
            impuesto REAL
        )
    ''')

    # Crear tabla ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            cliente_id INTEGER,
            total REAL NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')

    # Crear tabla detalles_ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalles_ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (venta_id) REFERENCES ventas(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id_producto)
        )
    ''')

    # Crear tabla presupuestos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presupuestos (
            id_presupuesto INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')

    # Crear tabla detalles_presupuestos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalles_presupuestos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            presupuesto_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (presupuesto_id) REFERENCES presupuestos(id_presupuesto),
            FOREIGN KEY (producto_id) REFERENCES productos(id_producto)
        )
    ''')

    conexion.commit()
    conexion.close()
    print("Tablas creadas y relacionadas exitosamente.")

# Llama a la función para crear las tablas
crear_tablas_empresa()
