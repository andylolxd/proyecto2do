import sqlite3

def crear_base_de_datos():
    # Conecta o crea la base de datos mendoza_tours.db
    conn = sqlite3.connect("mendoza_tours.db")
    cursor = conn.cursor()

    # Crear la tabla de clientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL,
        telefono TEXT NOT NULL
    );
    ''')

    # Crear la tabla de proveedores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        contacto TEXT NOT NULL
    );
    ''')

    # Crear la tabla de servicios (productos/tours)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS servicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        precio REAL NOT NULL,
        imagen TEXT NOT NULL  -- Aquí se guarda la ruta o nombre de la imagen del servicio
    );
    ''')

    # Crear la tabla de ventas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        id_servicio INTEGER,
        cantidad INTEGER NOT NULL,
        total REAL NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY(id_cliente) REFERENCES clientes(id),
        FOREIGN KEY(id_servicio) REFERENCES servicios(id)
    );
    ''')

    # Confirmar que los cambios fueron aplicados
    conn.commit()
    
    print("Base de datos y tablas creadas correctamente.")

    # Cerrar la conexión
    conn.close()

# Llamamos a la función para crear la base de datos
crear_base_de_datos()
