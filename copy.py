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

# Función para realizar venta
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

    def procesar_venta():
        cliente_id = cliente_id_entry.get()
        producto_id = producto_id_entry.get()
        cantidad = cantidad_entry.get()
        
        if producto_id and cantidad and cliente_id:
            conn = database.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE id=?", (producto_id,))
            producto = cursor.fetchone()
            
            if producto:
                precio = producto[2]  # Asumiendo que el precio es el 3er campo
                total = precio * int(cantidad)
                
                cursor.execute("INSERT INTO ventas (id_cliente, id_servicio, cantidad, total) VALUES (?, ?, ?, ?)", 
                               (cliente_id, producto_id, cantidad, total))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Venta realizada correctamente")
                realizar_venta_win.destroy()
            else:
                messagebox.showerror("Error", "Producto no encontrado")
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos")

    apply_styles(tk.Button(realizar_venta_win, text="Procesar Venta", command=procesar_venta))
    apply_styles(tk.Button(realizar_venta_win, text="Cancelar", command=realizar_venta_win.destroy))
    tk.Button(realizar_venta_win, text="Procesar Venta", command=procesar_venta).pack(pady=10)
    tk.Button(realizar_venta_win, text="Cancelar", command=realizar_venta_win.destroy).pack(pady=5)
