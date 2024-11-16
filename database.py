import sqlite3

# Función para conectar a la base de datos
def connect_db():
    return sqlite3.connect("mendoza_tours.db")

# Función para crear las tablas necesarias en la base de datos
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Crear tabla de usuarios (si no existe)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Crear tabla de clientes (si no existe)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL,
        telefono TEXT NOT NULL
    )
    """)

    # Crear tabla de proveedores (si no existe)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        contacto TEXT NOT NULL
    )
    """)

    # Crear tabla de productos (si no existe)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos_servicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        precio REAL NOT NULL,
        tipo TEXT NOT NULL
    )
    """)

    # Crear tabla de ventas (si no existe)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_servicio_id INTEGER NOT NULL,
        cliente_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        total REAL NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (producto_servicio_id) REFERENCES productos_servicios (id),
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    )
    """)

    conn.commit()
    conn.close()

# Función para verificar si las credenciales del usuario son correctas
def check_login(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    # Comprobar si existe el usuario y contraseña en la base de datos
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    conn.close()

    # Retorna True si el usuario existe, de lo contrario False
    return user is not None

# Función para agregar un nuevo usuario
def add_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
    
    conn.commit()
    conn.close()

# Función para agregar un cliente
def add_cliente(nombre, email, telefono):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO clientes (nombre, email, telefono) VALUES (?, ?, ?)", (nombre, email, telefono))
    
    conn.commit()
    conn.close()

# Función para agregar un proveedor
def add_proveedor(nombre, contacto):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO proveedores (nombre, contacto) VALUES (?, ?)", (nombre, contacto))
    
    conn.commit()
    conn.close()

# Función para agregar un producto o servicio
def add_producto(nombre, descripcion, precio, tipo):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO productos_servicios (nombre, descripcion, precio, tipo) VALUES (?, ?, ?, ?)", 
                   (nombre, descripcion, precio, tipo))
    
    conn.commit()
    conn.close()

# Función para registrar una venta
def register_venta(producto_servicio_id, cliente_id, cantidad, total):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO ventas (producto_servicio_id, cliente_id, cantidad, total) VALUES (?, ?, ?, ?)",
                   (producto_servicio_id, cliente_id, cantidad, total))
    
    conn.commit()
    conn.close()

# Función para obtener todos los productos/servicios
def get_productos():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos_servicios")
    productos = cursor.fetchall()

    conn.close()
    return productos

# Función para obtener todos los clientes
def get_clientes():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    conn.close()
    return clientes

# Función para obtener todos los proveedores
def get_proveedores():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM proveedores")
    proveedores = cursor.fetchall()

    conn.close()
    return proveedores

# Función para obtener todas las ventas
def get_ventas():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ventas")
    ventas = cursor.fetchall()

    conn.close()
    return ventas
