import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from datetime import datetime

class VentanaReserva:
    def __init__(self, master):
        self.master = master
        self.master.title("Reserva de Habitaciones")
        self.master.geometry("1000x800")
        
        # Crear los widgets de la ventana de reserva
        self.label_rut = tk.Label(master, text="RUT:")
        self.label_rut.grid(row=0, column=0, padx=10, pady=5)
        self.entry_rut = tk.Entry(master)
        self.entry_rut.grid(row=0, column=1, padx=10, pady=5)
        
        self.button_verificar = tk.Button(master, text="Verificar RUT", command=self.verificar_rut)
        self.button_verificar.grid(row=0, column=2, padx=10, pady=5)
        
        self.label_id_usuario = tk.Label(master, text="ID Usuario:")
        self.label_id_usuario.grid(row=1, column=0, padx=10, pady=5)
        self.entry_id_usuario = tk.Entry(master)
        self.entry_id_usuario.grid(row=1, column=1, padx=10, pady=5)
        self.entry_id_usuario.config(state='disabled')
        
        self.label_fecha_llegada = tk.Label(master, text="Fecha de Llegada:")
        self.label_fecha_llegada.grid(row=2, column=0, padx=10, pady=5)
        self.entry_fecha_llegada = tk.Entry(master)
        self.entry_fecha_llegada.grid(row=2, column=1, padx=10, pady=5)
        
        self.label_fecha_salida = tk.Label(master, text="Fecha de Salida:")
        self.label_fecha_salida.grid(row=3, column=0, padx=10, pady=5)
        self.entry_fecha_salida = tk.Entry(master)
        self.entry_fecha_salida.grid(row=3, column=1, padx=10, pady=5)

        self.label_tipo_habitacion = tk.Label(master, text="Tipo de Habitación:")
        self.label_tipo_habitacion.grid(row=4, column=0, padx=10, pady=5)
        self.combo_tipo_habitacion = ttk.Combobox(master)
        self.combo_tipo_habitacion.grid(row=4, column=1, padx=10, pady=5)
        self.cargar_tipos_habitacion()
        
        self.label_precio_total = tk.Label(master, text="Precio Total:")
        self.label_precio_total.grid(row=5, column=0, padx=10, pady=5)
        self.entry_precio_total = tk.Entry(master, state='readonly')
        self.entry_precio_total.grid(row=5, column=1, padx=10, pady=5)

        # Botones de acciones
        self.button_calcular = tk.Button(master, text="Calcular Total", command=self.calcular_total)
        self.button_calcular.grid(row=6, column=0, padx=10, pady=5)

        self.button_agregar = tk.Button(master, text="Agregar", command=self.agregar_reserva)
        self.button_agregar.grid(row=6, column=1, padx=10, pady=5)
        
        self.button_modificar = tk.Button(master, text="Modificar", command=self.modificar_reserva)
        self.button_modificar.grid(row=6, column=2, padx=10, pady=5)
        
        self.button_eliminar = tk.Button(master, text="Eliminar", command=self.eliminar_reserva)
        self.button_eliminar.grid(row=6, column=3, padx=10, pady=5)
        
        # Tabla para mostrar las reservas
        self.tree = ttk.Treeview(master, columns=("ID Usuario", "Fecha de Llegada", "Fecha de Salida", "Tipo de Habitación", "Precio Total"), show="headings")
        self.tree.heading("ID Usuario", text="ID Usuario")
        self.tree.heading("Fecha de Llegada", text="Fecha de Llegada")
        self.tree.heading("Fecha de Salida", text="Fecha de Salida")
        self.tree.heading("Tipo de Habitación", text="Tipo de Habitación")
        self.tree.heading("Precio Total", text="Precio Total")
        self.tree.grid(row=7, column=0, columnspan=4, padx=10, pady=5)
        
        # Cargar las reservas existentes
        self.cargar_reservas()

    
    def cargar_tipos_habitacion(self):
        db = Database()
        query = """
        SELECT id_tipo_habitacion, tipo, cantidad_maxima 
        FROM tipo_habitacion
        """
        rows = db.fetch_all(query)
        tipos = {row['id_tipo_habitacion']: f"{row['tipo']} - Máximo {row['cantidad_maxima']} personas" for row in rows}
        self.tipo_habitacion_dict = tipos
        self.combo_tipo_habitacion['values'] = list(tipos.values())
  


    def cargar_reservas(self):
        db = Database()
        query = """
        SELECT r.id_reserva, r.fecha_llegada, r.fecha_salida, h.numero_habitacion, th.tipo AS tipo_habitacion, r.precio_total, eh.estado AS estado_habitacion
        FROM reserva r
        JOIN detalle_reserva dr ON r.id_reserva = dr.id_reserva
        JOIN habitacion h ON dr.id_habitacion = h.id_habitacion
        JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
        JOIN estado_habitacion eh ON h.id_estado_habitacion = eh.id_estado_habitacion
        """
        rows = db.fetch_all(query)
        for row in rows:
            self.tree.insert("", "end", values=(row['id_reserva'], row['fecha_llegada'], row['fecha_salida'], row['tipo_habitacion'], row['precio_total'], row['estado_habitacion']))

    def verificar_rut(self):
        rut = self.entry_rut.get()
        if not rut:
            messagebox.showerror("Error", "Debe ingresar un RUT")
            return

        db = Database()
        query = "SELECT id_huesped, nombre, apellido1 FROM huespedes WHERE rut = %s"
        row = db.fetch_one(query, (rut,))

        if row:
            self.entry_id_usuario.config(state='normal')
            self.entry_id_usuario.delete(0, tk.END)
            self.entry_id_usuario.insert(0, row['id_huesped'])
            self.entry_id_usuario.config(state='readonly')
            messagebox.showinfo("Éxito", f"Huésped encontrado: {row['nombre']} {row['apellido1']}")
        else:
            messagebox.showerror("Error", "Huésped no encontrado")

    def calcular_total(self):
        fecha_llegada = self.entry_fecha_llegada.get()
        fecha_salida = self.entry_fecha_salida.get()
        tipo_habitacion = self.combo_tipo_habitacion.get()
        
        if not fecha_llegada or not fecha_salida or not tipo_habitacion:
            messagebox.showerror("Error", "Todos los campos son obligatorios para calcular el total")
            return
        
        try:
            fecha_llegada = datetime.strptime(fecha_llegada, "%Y-%m-%d")
            fecha_salida = datetime.strptime(fecha_salida, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use AAAA-MM-DD")
            return
        
        if fecha_llegada >= fecha_salida:
            messagebox.showerror("Error", "La fecha de salida debe ser posterior a la fecha de llegada")
            return
        
        dias_estadia = (fecha_salida - fecha_llegada).days
        id_tipo_habitacion = list(self.tipo_habitacion_dict.keys())[list(self.tipo_habitacion_dict.values()).index(tipo_habitacion)]
        
        db = Database()
        query = "SELECT precio_noche FROM habitacion WHERE id_tipo_habitacion = %s"
        row = db.fetch_one(query, (id_tipo_habitacion,))
        
        if row:
            precio_total = dias_estadia * row['precio_noche']
            self.entry_precio_total.config(state='normal')
            self.entry_precio_total.delete(0, tk.END)
            self.entry_precio_total.insert(0, precio_total)
            self.entry_precio_total.config(state='readonly')
        else:
            messagebox.showerror("Error", "No se encontró el tipo de habitación seleccionado")

    def agregar_reserva(self):
        id_usuario = self.entry_id_usuario.get()
        fecha_llegada = self.entry_fecha_llegada.get()
        fecha_salida = self.entry_fecha_salida.get()
        tipo_habitacion = self.combo_tipo_habitacion.get()
        precio_total = self.entry_precio_total.get()

        if not all([id_usuario, fecha_llegada, fecha_salida, tipo_habitacion, precio_total]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        id_tipo_habitacion = list(self.tipo_habitacion_dict.keys())[list(self.tipo_habitacion_dict.values()).index(tipo_habitacion)]

        db = Database()
        try:
            # Insertar en la tabla reserva
            db.execute_query("""
            INSERT INTO reserva (id_usuario, fecha_llegada, fecha_salida, precio_total, id_estado_reserva)
            VALUES (%s, %s, %s, %s, %s)
            """, (id_usuario, fecha_llegada, fecha_salida, precio_total, 1))  # Asumimos que el estado inicial es '1' (pendiente)

            # Obtener el ID de la reserva recién insertada
            id_reserva = db.fetch_one("SELECT LAST_INSERT_ID() as id_reserva")['id_reserva']

            # Insertar en la tabla detalle_reserva para cada habitación seleccionada
            query_habitaciones = """
            SELECT id_habitacion FROM habitacion 
            WHERE id_tipo_habitacion = %s AND id_estado_habitacion = 1  -- Habitaciones disponibles
            """
            habitaciones_disponibles = db.fetch_all(query_habitaciones, (id_tipo_habitacion,))

            if habitaciones_disponibles:
                id_habitacion = habitaciones_disponibles[0]['id_habitacion']
                db.execute_query("""
                INSERT INTO detalle_reserva (id_reserva, id_habitacion, hora)
                VALUES (%s, %s, %s)
                """, (id_reserva, id_habitacion, datetime.now().strftime("%H:%M:%S")))

                # Actualizar el estado de la habitación a ocupada
                db.execute_query("UPDATE habitacion SET id_estado_habitacion = 3 WHERE id_habitacion = %s", (id_habitacion,))
                
                messagebox.showinfo("Éxito", "Reserva agregada correctamente")
                self.tree.delete(*self.tree.get_children())  # Limpiar tabla
                self.cargar_reservas()  # Recargar reservas
            else:
                messagebox.showerror("Error", "No hay habitaciones disponibles para el tipo seleccionado")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def modificar_reserva(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una reserva para modificar")
            return
        
        id_usuario = self.entry_id_usuario.get()
        fecha_llegada = self.entry_fecha_llegada.get()
        fecha_salida = self.entry_fecha_salida.get()
        tipo_habitacion = self.combo_tipo_habitacion.get()
        precio_total = self.entry_precio_total.get()
        
        if not all([id_usuario, fecha_llegada, fecha_salida, tipo_habitacion, precio_total]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        id_tipo_habitacion = list(self.tipo_habitacion_dict.keys())[list(self.tipo_habitacion_dict.values()).index(tipo_habitacion)]
        item = self.tree.item(selected_item)
        id_reserva = item['values'][0]

        db = Database()
        try:
            db.execute_query("""
            UPDATE reserva
            SET id_usuario = %s, fecha_llegada = %s, fecha_salida = %s, id_tipo_habitacion = %s, precio_total = %s
            WHERE id_reserva = %s
            """, (id_usuario, fecha_llegada, fecha_salida, id_tipo_habitacion, precio_total, id_reserva))

            messagebox.showinfo("Éxito", "Reserva modificada correctamente")
            self.tree.delete(*self.tree.get_children())  # Limpiar tabla
            self.cargar_reservas()  # Recargar reservas
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_reserva(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una reserva para eliminar")
            return

        item = self.tree.item(selected_item)
        id_reserva = item['values'][0]

        db = Database()
        try:
            db.execute_query("DELETE FROM reserva WHERE id_reserva = %s", (id_reserva,))
            messagebox.showinfo("Éxito", "Reserva eliminada correctamente")
            self.tree.delete(*self.tree.get_children())  # Limpiar tabla
            self.cargar_reservas()  # Recargar reservas
        except Exception as e:
            messagebox.showerror("Error", str(e))
