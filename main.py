import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
import os
import sqlite3
import database
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def connect_db():
    # Obtiene la ruta absoluta del archivo .py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "mendoza_tour.db")
    return sqlite3.connect(db_path)


database.create_tables()  
database.add_user("admin", "admin")  
database.add_user("cliente", "cliente") 

# Estilo 
def apply_styles(widget):
    widget.config(bg="#f1f1f1", fg="#333", font=("Arial", 12), padx=10, pady=5)

# Ventana de Login y de Vendedor/Cliente
def login_window():
    # Obtener la ruta absoluta del directorio donde se encuentra el archivo .py
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio donde está el script
    
    # Construir la ruta al archivo de icono
    icon_path = os.path.join(script_dir, "images", "logo.ico")

    login_win = tk.Tk()
    login_win.title("Login")
    login_win.geometry("300x250")
    login_win.config(bg="#e5e5e5")
    #login_win.iconbitmap("images/logo.ico")
    #login_win.overrideredirect(True)
    try:
        login_win.iconbitmap(icon_path)
    except Exception as e:
        print(f"Error al cargar el icono: {e}")

        # Construir la ruta al archivo de la imagen de fondo
    fondo_path = os.path.join(script_dir, "images", "parque_san_martin.jpg")

    fondo_imagen = Image.open(fondo_path)  # Ruta de la imagen de fondo
    fondo_imagen = fondo_imagen.resize((300, 250))  # Ajustar el tamaño de la imagen
    fondo_photo = ImageTk.PhotoImage(fondo_imagen)
    fondo_label = tk.Label(login_win, image=fondo_photo)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)  # Establecer la posición y el tamaño del fondo
    fondo_label.image = fondo_photo
    
    tk.Label(login_win, text="Usuario", font=("Arial", 14), bg="#e5e5e5").pack(pady=5)
    username_entry = tk.Entry(login_win, font=("Arial", 12))
    username_entry.pack(pady=5)

    tk.Label(login_win, text="Contraseña", font=("Arial", 14), bg="#e5e5e5").pack(pady=5)
    password_entry = tk.Entry(login_win, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)

    def check_credentials():
        username = username_entry.get()
        password = password_entry.get()
        if database.check_login(username, password):
            login_win.destroy()
            if username == "admin":
                main_seller_window(username)  # Ventana para admin/vendedor
            else:
                main_client_window(username)  # Ventana para cliente
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    apply_styles(tk.Button(login_win, text="Entrar", command=check_credentials))
    tk.Button(login_win, text="Entrar", command=check_credentials).pack(pady=10)

    login_win.mainloop()

# Función para la ventana principal del vendedor
def main_seller_window(username):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "images", "logo.ico")

    main_win = tk.Tk()
    main_win.title("Sistema de Ventas - Mendoza Tours (Vendedor)")
    main_win.geometry("600x500")
    main_win.config(bg="#f1f1f1")
    #main_win.iconbitmap("images/logo.ico")
    #main_win.overrideredirect(True)
    # Imagen de fondo
    fondo_path = os.path.join(script_dir, "images", "bodega_mendoza.jpg")

    img_path = fondo_path
    if not os.path.exists(img_path):
        messagebox.showerror("Error", f"No se encontró la imagen en la ruta: {img_path}")
        return
    
    img = Image.open(img_path)
    img = img.resize((600,500))
    img = ImageTk.PhotoImage(img)

    main_win.img = img

# Usamos un Canvas para colocar los elementos
    canvas = tk.Canvas(main_win, width=600, height=500)
    canvas.pack()

    # Colocamos la imagen de fondo en el Canvas
    canvas.create_image(0, 0, anchor="nw", image=main_win.img)

    # Crear fuente elegante para el texto
    elegancia_fuente = font.Font(family="Times New Roman", size=30, weight="bold")

    # Colocar el texto sobre la imagen de fondo
    canvas.create_text(300, 100, text="MENDOZA TIERRA DEL SOL Y BUEN VINO \n \n Modo Ventas", font=elegancia_fuente, fill="#333", anchor="center", justify="center", width=500)

    menu = tk.Menu(main_win, bg="#6e7f8f", fg="#fff", font=("Arial", 12))
    main_win.config(menu=menu)

    stock_menu = tk.Menu(menu, tearoff=0, bg="#d6e1e5", fg="#333")
    menu.add_cascade(label="Stock", menu=stock_menu)
    stock_menu.add_command(label="Ver productos", command=ver_productos)
    stock_menu.add_command(label="Agregar producto", command=agregar_producto)

    ventas_menu = tk.Menu(menu, tearoff=0, bg="#d6e1e5", fg="#333")
    menu.add_cascade(label="Ventas", menu=ventas_menu)
    ventas_menu.add_command(label="Realizar venta", command=realizar_venta)
    ventas_menu.add_command(label="Ver ventas", command=ver_ventas)
    ventas_menu.add_command(label="Ver Carrito", command=ver_carrito)

    clientes_menu = tk.Menu(menu, tearoff=0, bg="#d6e1e5", fg="#333")
    menu.add_cascade(label="Clientes", menu=clientes_menu)
    clientes_menu.add_command(label="Ver clientes", command=ver_clientes)
    clientes_menu.add_command(label="Agregar cliente", command=agregar_cliente)

    proveedores_menu = tk.Menu(menu, tearoff=0, bg="#d6e1e5", fg="#333")
    menu.add_cascade(label="Proveedores", menu=proveedores_menu)
    proveedores_menu.add_command(label="Ver proveedores", command=ver_proveedores)
    proveedores_menu.add_command(label="Agregar proveedor", command=agregar_proveedor)

    main_win.mainloop()

# Función para la ventana del cliente
def main_client_window(username):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "images", "logo.ico")

    main_win = tk.Tk()
    main_win.title("Sistema de Ventas - Mendoza Tours (Cliente)")
    main_win.geometry("600x500")
    main_win.config(bg="#f1f1f1")
    #main_win.iconbitmap("images/logo.ico")

    fondo_path = os.path.join(script_dir, "images", "bodega_mendoza.jpg")
    img_path = fondo_path
    if not os.path.exists(img_path):
        messagebox.showerror("Error", f"No se encontró la imagen en la ruta: {img_path}")
        return
    
    try:
        img = Image.open(img_path)
        img = img.resize((600,500))
        img = ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
        return

    main_win.img = img
    # Usamos un Canvas para colocar los elementos
    canvas = tk.Canvas(main_win, width=600, height=500)
    canvas.pack()

    # Colocamos la imagen de fondo en el Canvas
    canvas.create_image(0, 0, anchor="nw", image=main_win.img)

    # Crear fuente elegante para el texto
    elegancia_fuente = font.Font(family="Times New Roman", size=30, weight="bold")

    # Colocar el texto sobre la imagen de fondo
    canvas.create_text(300, 100, text="MENDOZA TIERRA DEL SOL Y BUEN VINO", font=elegancia_fuente, fill="#333", anchor="center", justify="center", width=500)

    menu = tk.Menu(main_win, bg="#6e7f8f", fg="#fff", font=("Arial", 12))
    main_win.config(menu=menu)


    menu = tk.Menu(main_win, bg="#6e7f8f", fg="#fff", font=("Arial", 12))
    main_win.config(menu=menu)

    productos_menu = tk.Menu(menu, tearoff=0, bg="#d6e1e5", fg="#333")
    menu.add_cascade(label="Productos", menu=productos_menu)
    productos_menu.add_command(label="Ver productos", command=ver_productos)
    productos_menu.add_command(label="Realizar pedido", command=realizar_venta)

    main_win.mainloop()

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mendoza_tour.db")


# Función para agregar un producto
def agregar_producto():
    agregar_producto_win = tk.Toplevel()
    agregar_producto_win.title("Agregar Producto")
    agregar_producto_win.geometry("400x300")
    agregar_producto_win.config(bg="#e5e5e5")

    tk.Label(agregar_producto_win, text="Nombre del Producto", font=("Arial", 14)).pack(pady=5)
    nombre_entry = tk.Entry(agregar_producto_win, font=("Arial", 12))
    nombre_entry.pack(pady=5)

    tk.Label(agregar_producto_win, text="Precio", font=("Arial", 14)).pack(pady=5)
    precio_entry = tk.Entry(agregar_producto_win, font=("Arial", 12))
    precio_entry.pack(pady=5)

    tk.Label(agregar_producto_win, text="Descripción", font=("Arial", 14)).pack(pady=5)
    cantidad_entry = tk.Entry(agregar_producto_win, font=("Arial", 12))
    cantidad_entry.pack(pady=5)

    def guardar_producto():
        nombre = nombre_entry.get()
        precio = precio_entry.get()
        descripción = cantidad_entry.get()

        # Validar que los campos no estén vacíos y que el precio y cantidad sean numéricos
        if nombre and precio and descripción:
            try:
                precio = float(precio)  # Convertir el precio a float
                descripción = str(descripción)  # Descripción como texto

                # Conectar a la base de datos
                conn = database.connect_db()
                cursor = conn.cursor()
                
                # Insertar el nuevo producto en la base de datos
                cursor.execute("INSERT INTO productos (nombre, precio, descripción) VALUES (?, ?, ?)",
                               (nombre, precio, descripción))
                conn.commit()
                conn.close()

                messagebox.showinfo("Éxito", "Producto agregado correctamente")
                agregar_producto_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa valores válidos para el precio y la cantidad.")
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos")

    # Botones para guardar o cancelar
    apply_styles(tk.Button(agregar_producto_win, text="Guardar Producto", command=guardar_producto))
    apply_styles(tk.Button(agregar_producto_win, text="Cancelar", command=agregar_producto_win.destroy))
    tk.Button(agregar_producto_win, text="Guardar Producto", command=guardar_producto).pack(pady=10)
    tk.Button(agregar_producto_win, text="Cancelar", command=agregar_producto_win.destroy).pack(pady=5)

# Funciones para ver productos y realizar compras
def ver_productos():
    ver_productos_win = tk.Toplevel()
    ver_productos_win.title("Ver Productos")
    ver_productos_win.geometry("600x400")
    ver_productos_win.config(bg="#f1f1f1")

    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()

    tree = ttk.Treeview(ver_productos_win, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Precio", text="Precio")
    tree.heading("Stock", text="Stock")

    tree.pack(fill=tk.BOTH, expand=True)

    for producto in productos:
        tree.insert("", "end", values=producto)

    apply_styles(tk.Button(ver_productos_win, text="Cerrar", command=ver_productos_win.destroy))
    tk.Button(ver_productos_win, text="Cerrar", command=ver_productos_win.destroy).pack(pady=10)

# Función para generar el ticket de la venta
def generar_ticket_venta(cliente_id, producto_id, cantidad, total):
    # Obtener los datos del cliente y producto desde la base de datos
    conn = database.connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT nombre, email FROM clientes WHERE id=?", (cliente_id,))
    cliente = cursor.fetchone()

    cursor.execute("SELECT nombre, precio FROM productos WHERE id=?", (producto_id,))
    producto = cursor.fetchone()

    conn.close()

    if cliente and producto:
        cliente_nombre = cliente[0]
        cliente_email = cliente[1]
        producto_nombre = producto[0]
        producto_precio = producto[1]

        # Crear ventana emergente para el ticket
        ticket_win = tk.Toplevel()
        ticket_win.title("Ticket de Venta")
        ticket_win.geometry("500x600")
        ticket_win.config(bg="#ffffff")

        canvas = tk.Canvas(ticket_win, width=400, height=500, bg="#ffffff")
        canvas.pack()

        y_position = 20  # Posición inicial en el eje Y

        # Título del ticket
        canvas.create_text(200, y_position, text="TICKET DE VENTA", font=("Helvetica", 16, "bold"), fill="black")
        y_position += 30

        # Detalles del cliente
        canvas.create_text(200, y_position, text=f"Cliente: {cliente_nombre}", font=("Helvetica", 12), fill="black")
        y_position += 20
        canvas.create_text(200, y_position, text=f"Email: {cliente_email}", font=("Helvetica", 12), fill="black")
        y_position += 30

        # Detalles del producto
        canvas.create_text(200, y_position, text=f"Producto: {producto_nombre}", font=("Helvetica", 12), fill="black")
        y_position += 20
        canvas.create_text(200, y_position, text=f"Precio: ${producto_precio:.2f}", font=("Helvetica", 12), fill="black")
        y_position += 20
        canvas.create_text(200, y_position, text=f"Cantidad: {cantidad}", font=("Helvetica", 12), fill="black")
        y_position += 20

        # Total de la venta
        canvas.create_text(200, y_position, text=f"Total: ${total:.2f}", font=("Helvetica", 14, "bold"), fill="black")
        y_position += 30

        # Mensaje de agradecimiento
        canvas.create_text(200, y_position, text="¡Gracias por su compra!", font=("Helvetica", 12), fill="black")

        # Botón para cerrar el ticket
        close_button = tk.Button(ticket_win, text="Cerrar", command=ticket_win.destroy)
        close_button.pack(pady=10)
        
def ver_ventas():
    ver_ventas_win = tk.Toplevel()
    ver_ventas_win.title("Ver Ventas")
    ver_ventas_win.geometry("600x400")
    ver_ventas_win.config(bg="#f1f1f1")

    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ventas.id, clientes.nombre, productos.nombre, ventas.cantidad, ventas.total 
        FROM ventas
        JOIN clientes ON ventas.id_cliente = clientes.id
        JOIN productos ON ventas.id_servicio = productos.id
    """)
    ventas = cursor.fetchall()
    conn.close()

    tree = ttk.Treeview(ver_ventas_win, columns=("ID", "Cliente", "Producto", "Cantidad", "Total"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Cliente", text="Cliente")
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Total", text="Total")

    tree.pack(fill=tk.BOTH, expand=True)

    for venta in ventas:
        tree.insert("", "end", values=venta)

    apply_styles(tk.Button(ver_ventas_win, text="Cerrar", command=ver_ventas_win.destroy))
    tk.Button(ver_ventas_win, text="Cerrar", command=ver_ventas_win.destroy).pack(pady=10)

carrito = []

def realizar_venta():
    realizar_venta_win = tk.Toplevel()
    realizar_venta_win.title("Realizar Venta")
    realizar_venta_win.geometry("400x300")
    realizar_venta_win.config(bg="#e5e5e5")

    tk.Label(realizar_venta_win, text="ID del Producto", font=("Arial", 14)).pack(pady=5)
    producto_id_entry = tk.Entry(realizar_venta_win, font=("Arial", 12))
    producto_id_entry.pack(pady=5)

    tk.Label(realizar_venta_win, text="ID del Cliente", font=("Arial", 14)).pack(pady=5)
    cliente_id_entry = tk.Entry(realizar_venta_win, font=("Arial", 12))
    cliente_id_entry.pack(pady=5)
    
    tk.Label(realizar_venta_win, text="Cantidad", font=("Arial", 14)).pack(pady=5)
    cantidad_entry = tk.Entry(realizar_venta_win, font=("Arial", 12))
    cantidad_entry.pack(pady=5)



def ver_carrito():
    carrito_win = tk.Toplevel()
    carrito_win.title("Carrito de Compras")
    carrito_win.geometry("600x400")
    carrito_win.config(bg="#f1f1f1")

    # Crear un Treeview para mostrar los productos en el carrito
    tree = ttk.Treeview(carrito_win, columns=("Nombre", "Precio", "Cantidad", "Total"), show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Precio", text="Precio")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Total", text="Total")


    for item in carrito:
        tree.insert("", "end", values=(item["producto_nombre"], f"${item['precio']:.2f}", item["cantidad"],f"${item['total']:.2f}"))

    tree.pack(fill=tk.BOTH, expand=True)

    # Función para realizar la venta y generar el ticket
    def realizar_venta_carrito():
        total_venta = sum(item["total"] for item in carrito)

# Crear el ticket de venta para todos los productos
        ticket_win = tk.Toplevel()
        ticket_win.title("Ticket de Venta")
        ticket_win.geometry("500x600")
        ticket_win.config(bg="#ffffff")

        canvas = tk.Canvas(ticket_win, width=400, height=500, bg="#ffffff")
        canvas.pack()

        y_position = 20  # Posición inicial en el eje Y

        # Título del ticket
        canvas.create_text(200, y_position, text="TICKET DE VENTA", font=("Helvetica", 16, "bold"), fill="black")
        y_position += 30

        # Mostrar los detalles de cada producto en el carrito
        for producto in carrito:
            canvas.create_text(200, y_position, text=f"Producto: {producto['producto_nombre']}", font=("Helvetica", 12), fill="black")
            y_position += 20
            canvas.create_text(200, y_position, text=f"Precio: ${producto['precio']:.2f}", font=("Helvetica", 12), fill="black")
            y_position += 20
            canvas.create_text(200, y_position, text=f"Cantidad: {producto['cantidad']}", font=("Helvetica", 12), fill="black")
            y_position += 20
            canvas.create_text(200, y_position, text=f"Total: ${producto['total']:.2f}", font=("Helvetica", 12), fill="black")
            y_position += 30

        # Total de la venta
        canvas.create_text(200, y_position, text=f"TOTAL: ${total_venta:.2f}", font=("Helvetica", 14, "bold"), fill="black")
        y_position += 30

        # Mensaje de agradecimiento
        canvas.create_text(200, y_position, text="¡Gracias por su compra!", font=("Helvetica", 12), fill="black")

        # Botón para cerrar el ticket
        close_button = tk.Button(ticket_win, text="Cerrar", command=ticket_win.destroy)
        close_button.pack(pady=10)

        # Limpiar el carrito después de realizar la venta
        carrito.clear()
        carrito_win.destroy()

    # Botón para realizar la venta y generar el ticket
    realizar_venta_btn = tk.Button(carrito_win, text="Realizar Venta", command=realizar_venta_carrito)
    apply_styles(realizar_venta_btn)
    realizar_venta_btn.pack(pady=10)

    # Botón para cerrar el carrito
    cerrar_btn = tk.Button(carrito_win, text="Cerrar", command=carrito_win.destroy)
    apply_styles(cerrar_btn)
    cerrar_btn.pack(pady=5)

# Función para cambiar el botón "Realizar Venta" a "Agregar al Carrito"
def realizar_venta():
    realizar_venta_win = tk.Toplevel()
    realizar_venta_win.title("Realizar Venta")
    realizar_venta_win.geometry("400x300")
    realizar_venta_win.config(bg="#e5e5e5")

    tk.Label(realizar_venta_win, text="ID del Producto", font=("Arial", 14)).pack(pady=5)
    producto_id_entry = tk.Entry(realizar_venta_win, font=("Arial", 12))
    producto_id_entry.pack(pady=5)

    tk.Label(realizar_venta_win, text="ID del Cliente", font=("Arial", 14)).pack(pady=5)
    cliente_id_entry = tk.Entry(realizar_venta_win, font=("Arial", 12))
    cliente_id_entry.pack(pady=5)

    tk.Label(realizar_venta_win, text="Cantidad", font=("Arial", 14)).pack(pady=5)
    cantidad_entry = tk.Entry(realizar_venta_win, font=("Arial", 12))
    cantidad_entry.pack(pady=5)

    # Función para procesar la venta y generar el ticket
    def añadir_al_carrito():
        cliente_id = cliente_id_entry.get()
        producto_id = producto_id_entry.get()
        cantidad = cantidad_entry.get()

        if producto_id and cantidad and cliente_id:
            try:
                conn = database.connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM productos WHERE id=?", (producto_id,))
                producto = cursor.fetchone()

                if producto:
                    precio = producto[2]  # Asumiendo que el precio es el 3er campo
                    total = precio * int(cantidad)

                    # Añadir al carrito
                    carrito.append({
                        "producto_nombre": producto[1],
                        "precio": precio,
                        "cantidad": int(cantidad),
                        "total": total
                    })

                    #messagebox.showinfo("Carrito", "Producto añadido al carrito")
                    realizar_venta_win.destroy()
                    ver_carrito()
                else:
                    messagebox.showerror("Error", "Producto no encontrado")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa valores válidos")
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos")


    # Botón para agregar al carrito
    carrito_btn = tk.Button(realizar_venta_win, text="Agregar al Carrito", command=añadir_al_carrito)
    apply_styles(carrito_btn)
    carrito_btn.pack(pady=10)

    # Botón para cancelar
    cancelar_btn = tk.Button(realizar_venta_win, text="Cancelar", command=realizar_venta_win.destroy)
    apply_styles(cancelar_btn)
    cancelar_btn.pack(pady=5)



# Funciones para manejar clientes y proveedores
def agregar_cliente():
    agregar_cliente_win = tk.Toplevel()
    agregar_cliente_win.title("Agregar Cliente")
    agregar_cliente_win.geometry("400x300")
    agregar_cliente_win.config(bg="#e5e5e5")

    tk.Label(agregar_cliente_win, text="Nombre del Cliente", font=("Arial", 14)).pack(pady=5)
    nombre_entry = tk.Entry(agregar_cliente_win, font=("Arial", 12))
    nombre_entry.pack(pady=5)

    tk.Label(agregar_cliente_win, text="Email", font=("Arial", 14)).pack(pady=5)
    email_entry = tk.Entry(agregar_cliente_win, font=("Arial", 12))
    email_entry.pack(pady=5)

    tk.Label(agregar_cliente_win, text="Teléfono", font=("Arial", 14)).pack(pady=5)
    telefono_entry = tk.Entry(agregar_cliente_win, font=("Arial", 12))
    telefono_entry.pack(pady=5)

    def guardar_cliente():
        nombre = nombre_entry.get()
        email = email_entry.get()
        telefono = telefono_entry.get()

        if nombre and email and telefono:
            conn = database.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (nombre, email, telefono) VALUES (?, ?, ?)", 
                           (nombre, email, telefono))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente")
            agregar_cliente_win.destroy()
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos")

    apply_styles(tk.Button(agregar_cliente_win, text="Guardar Cliente", command=guardar_cliente))
    apply_styles(tk.Button(agregar_cliente_win, text="Cancelar", command=agregar_cliente_win.destroy))
    tk.Button(agregar_cliente_win, text="Guardar Cliente", command=guardar_cliente).pack(pady=10)
    tk.Button(agregar_cliente_win, text="Cancelar", command=agregar_cliente_win.destroy).pack(pady=5)

def ver_clientes():
    ver_clientes_win = tk.Toplevel()
    ver_clientes_win.title("Ver Clientes")
    ver_clientes_win.geometry("600x400")
    ver_clientes_win.config(bg="#f1f1f1")

    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()

    tree = ttk.Treeview(ver_clientes_win, columns=("ID", "Nombre", "Email", "Teléfono"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Email", text="Email")
    tree.heading("Teléfono", text="Teléfono")

    tree.pack(fill=tk.BOTH, expand=True)

    for cliente in clientes:
        tree.insert("", "end", values=cliente)

    apply_styles(tk.Button(ver_clientes_win, text="Cerrar", command=ver_clientes_win.destroy))
    tk.Button(ver_clientes_win, text="Cerrar", command=ver_clientes_win.destroy).pack(pady=10)

def agregar_proveedor():
    agregar_proveedor_win = tk.Toplevel()
    agregar_proveedor_win.title("Agregar Proveedor")
    agregar_proveedor_win.geometry("400x300")
    agregar_proveedor_win.config(bg="#e5e5e5")

    tk.Label(agregar_proveedor_win, text="Nombre del Proveedor", font=("Arial", 14)).pack(pady=5)
    nombre_entry = tk.Entry(agregar_proveedor_win, font=("Arial", 12))
    nombre_entry.pack(pady=5)

    tk.Label(agregar_proveedor_win, text="Contacto", font=("Arial", 14)).pack(pady=5)
    contacto_entry = tk.Entry(agregar_proveedor_win, font=("Arial", 12))
    contacto_entry.pack(pady=5)

    def guardar_proveedor():
        nombre = nombre_entry.get()
        contacto = contacto_entry.get()

        if nombre and contacto:
            conn = database.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO proveedores (nombre, contacto) VALUES (?, ?)", 
                           (nombre, contacto))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente")
            agregar_proveedor_win.destroy()
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos")

    apply_styles(tk.Button(agregar_proveedor_win, text="Guardar Proveedor", command=guardar_proveedor))
    apply_styles(tk.Button(agregar_proveedor_win, text="Cancelar", command=agregar_proveedor_win.destroy))
    tk.Button(agregar_proveedor_win, text="Guardar Proveedor", command=guardar_proveedor).pack(pady=10)
    tk.Button(agregar_proveedor_win, text="Cancelar", command=agregar_proveedor_win.destroy).pack(pady=5)

def ver_proveedores():
    ver_proveedores_win = tk.Toplevel()
    ver_proveedores_win.title("Ver Proveedores")
    ver_proveedores_win.geometry("600x400")
    ver_proveedores_win.config(bg="#f1f1f1")

    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proveedores")
    proveedores = cursor.fetchall()
    conn.close()

    tree = ttk.Treeview(ver_proveedores_win, columns=("ID", "Nombre", "Contacto"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Contacto", text="Contacto")

    tree.pack(fill=tk.BOTH, expand=True)

    for proveedor in proveedores:
        tree.insert("", "end", values=proveedor)

    apply_styles(tk.Button(ver_proveedores_win, text="Cerrar", command=ver_proveedores_win.destroy))
    tk.Button(ver_proveedores_win, text="Cerrar", command=ver_proveedores_win.destroy).pack(pady=10)

# Ejecutar la ventana de login al inicio
login_window()
