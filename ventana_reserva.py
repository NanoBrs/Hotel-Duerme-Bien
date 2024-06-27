import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class VentanaReserva:
    def __init__(self, master):
        self.master = master
        self.master.title("Reserva de Habitaciones")
        self.master.geometry("1000x800")
        
        # Crear los widgets de la ventana de reserva
        self.label_id_reserva = tk.Label(master, text="ID de Reserva:")
        self.label_id_reserva.grid(row=0, column=0)
        self.entry_id_reserva = tk.Entry(master)
        self.entry_id_reserva.grid(row=0, column=1)
        
        self.label_id_habitacion = tk.Label(master, text="ID de Habitación:")
        self.label_id_habitacion.grid(row=1, column=0)
        self.entry_id_habitacion = tk.Entry(master)
        self.entry_id_habitacion.grid(row=1, column=1)
        
        self.label_id_usuario = tk.Label(master, text="ID de Usuario:")
        self.label_id_usuario.grid(row=2, column=0)
        self.entry_id_usuario = tk.Entry(master)
        self.entry_id_usuario.grid(row=2, column=1)
        
        self.label_fecha_llegada = tk.Label(master, text="Fecha de Llegada:")
        self.label_fecha_llegada.grid(row=3, column=0)
        self.entry_fecha_llegada = tk.Entry(master)
        self.entry_fecha_llegada.grid(row=3, column=1)
        
        self.label_fecha_salida = tk.Label(master, text="Fecha de Salida:")
        self.label_fecha_salida.grid(row=4, column=0)
        self.entry_fecha_salida = tk.Entry(master)
        self.entry_fecha_salida.grid(row=4, column=1)
        
        self.label_estado_reserva = tk.Label(master, text="Estado de la Reserva:")
        self.label_estado_reserva.grid(row=5, column=0)
        self.entry_estado_reserva = tk.Entry(master)
        self.entry_estado_reserva.grid(row=5, column=1)
        
        self.label_precio_total = tk.Label(master, text="Precio Total:")
        self.label_precio_total.grid(row=6, column=0)
        self.entry_precio_total = tk.Entry(master)
        self.entry_precio_total.grid(row=6, column=1)
        
        # Botones de acciones
        self.button_agregar = tk.Button(master, text="Agregar", command=self.agregar_reserva)
        self.button_agregar.grid(row=7, column=0)
        
        self.button_modificar = tk.Button(master, text="Modificar", command=self.modificar_reserva)
        self.button_modificar.grid(row=7, column=1)
        
        self.button_eliminar = tk.Button(master, text="Eliminar", command=self.eliminar_reserva)
        self.button_eliminar.grid(row=7, column=2)
        
        # Tabla para mostrar las reservas
        self.tree = ttk.Treeview(master, columns=("ID", "ID de Habitacion", "ID de Usuario", "Fecha de Llegada", "Fecha de Salida", "Precio Total", "Estado de la Reserva"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("ID de Habitacion", text="ID de Habitacion")
        self.tree.heading("ID de Usuario", text="ID de Usuario")
        self.tree.heading("Fecha de Llegada", text="Fecha de Llegada")
        self.tree.heading("Fecha de Salida", text="Fecha de Salida")
        self.tree.heading("Precio Total", text="Precio Total")
        self.tree.heading("Estado de la Reserva", text="Estado de la Reserva")
        self.tree.grid(row=8, column=0, columnspan=3)
        
        # Cargar las reservas existentes
        self.cargar_reservas()
    
    def cargar_reservas(self):
        db = Database()
        query = """
        SELECT r.id_reserva, dr.id_habitacion, r.id_usuario, r.fecha_llegada, r.fecha_salida, r.precio_total, r.id_estado_reserva
        FROM reserva r
        JOIN detalle_reserva dr ON r.id_reserva = dr.id_reserva
        """
        rows = db.fetch_all(query)
        for row in rows:
            self.tree.insert("", "end", values=(row['id_reserva'], row['id_habitacion'], row['id_usuario'], row['fecha_llegada'], row['fecha_salida'], row['precio_total'], row['id_estado_reserva']))
    
    def agregar_reserva(self):
        id_reserva = self.entry_id_reserva.get()
        id_habitacion = self.entry_id_habitacion.get()
        id_usuario = self.entry_id_usuario.get()
        fecha_llegada = self.entry_fecha_llegada.get()
        fecha_salida = self.entry_fecha_salida.get()
        precio_total = self.entry_precio_total.get()
        id_estado_reserva = self.entry_estado_reserva.get()
        
        if not all([id_reserva, id_habitacion, id_usuario, fecha_llegada, fecha_salida, precio_total, id_estado_reserva]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        db = Database()
        try:
            db.execute_query("""
            INSERT INTO reserva (id_reserva, id_usuario, fecha_llegada, fecha_salida, precio_total, id_estado_reserva)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_reserva, id_usuario, fecha_llegada, fecha_salida, precio_total, id_estado_reserva))
            
            db.execute_query("""
            INSERT INTO detalle_reserva (id_reserva, id_habitacion)
            VALUES (%s, %s)
            """, (id_reserva, id_habitacion))
            
            messagebox.showinfo("Éxito", "Reserva agregada correctamente")
            self.tree.delete(*self.tree.get_children())  # Limpiar tabla
            self.cargar_reservas()  # Recargar reservas
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def modificar_reserva(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una reserva para modificar")
            return
        
        id_reserva = self.entry_id_reserva.get()
        id_habitacion = self.entry_id_habitacion.get()
        id_usuario = self.entry_id_usuario.get()
        fecha_llegada = self.entry_fecha_llegada.get()
        fecha_salida = self.entry_fecha_salida.get()
        precio_total = self.entry_precio_total.get()
        id_estado_reserva = self.entry_estado_reserva.get()
        
        if not all([id_reserva, id_habitacion, id_usuario, fecha_llegada, fecha_salida, precio_total, id_estado_reserva]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        db = Database()
        try:
            db.execute_query("""
            UPDATE reserva
            SET id_usuario = %s, fecha_llegada = %s, fecha_salida = %s, precio_total = %s, id_estado_reserva = %s
            WHERE id_reserva = %s
            """, (id_usuario, fecha_llegada, fecha_salida, precio_total, id_estado_reserva, id_reserva))
            
            db.execute_query("""
            UPDATE detalle_reserva
            SET id_habitacion = %s
            WHERE id_reserva = %s
            """, (id_habitacion, id_reserva))
            
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
        
        id_reserva = self.tree.item(selected_item)["values"][0]
        
        db = Database()
        try:
            db.execute_query("DELETE FROM detalle_reserva WHERE id_reserva = %s", (id_reserva,))
            db.execute_query("DELETE FROM reserva WHERE id_reserva = %s", (id_reserva,))
            
            messagebox.showinfo("Éxito", "Reserva eliminada correctamente")
            self.tree.delete(*self.tree.get_children())  # Limpiar tabla
            self.cargar_reservas()  # Recargar reservas
        except Exception as e:
            messagebox.showerror("Error", str(e))
