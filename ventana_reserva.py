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
        self.label_rut.grid(row=0, column=0)
        self.entry_rut = tk.Entry(master)
        self.entry_rut.grid(row=0, column=1)
        
        self.button_validar_rut = tk.Button(master, text="Validar RUT", command=self.validar_rut)
        self.button_validar_rut.grid(row=0, column=2)
        
        self.label_id_usuario = tk.Label(master, text="ID Usuario:")
        self.label_id_usuario.grid(row=1, column=0)
        self.entry_id_usuario = tk.Entry(master, state='readonly')
        self.entry_id_usuario.grid(row=1, column=1)
        
        self.label_fecha_llegada = tk.Label(master, text="Fecha de Llegada:")
        self.label_fecha_llegada.grid(row=2, column=0)
        self.entry_fecha_llegada = tk.Entry(master)
        self.entry_fecha_llegada.grid(row=2, column=1)
        
        self.label_fecha_salida = tk.Label(master, text="Fecha de Salida:")
        self.label_fecha_salida.grid(row=3, column=0)
        self.entry_fecha_salida = tk.Entry(master)
        self.entry_fecha_salida.grid(row=3, column=1)

        self.label_tipo_habitacion = tk.Label(master, text="Tipo de Habitación:")
        self.label_tipo_habitacion.grid(row=4, column=0)
        self.combo_tipo_habitacion = ttk.Combobox(master)
        self.combo_tipo_habitacion.grid(row=4, column=1)
        self.cargar_tipos_habitacion()
        
        self.label_precio_total = tk.Label(master, text="Precio Total:")
        self.label_precio_total.grid(row=5, column=0)
        self.entry_precio_total = tk.Entry(master, state='readonly')
        self.entry_precio_total.grid(row=5, column=1)

        # Botones de acciones
        self.button_calcular = tk.Button(master, text="Calcular Total", command=self.calcular_total)
        self.button_calcular.grid(row=6, column=0)

        self.button_agregar = tk.Button(master, text="Agregar", command=self.agregar_reserva)
        self.button_agregar.grid(row=6, column=1)
        
        self.button_modificar = tk.Button(master, text="Modificar", command=self.modificar_reserva)
        self.button_modificar.grid(row=6, column=2)
        
        self.button_eliminar = tk.Button(master, text="Eliminar", command=self.eliminar_reserva)
        self.button_eliminar.grid(row=6, column=3)
        
        # Tabla para mostrar las reservas
        self.tree = ttk.Treeview(master, columns=("ID Usuario", "Fecha de Llegada", "Fecha de Salida", "Tipo de Habitación", "Precio Total"), show="headings")
        self.tree.heading("ID Usuario", text="ID Usuario")
        self.tree.heading("Fecha de Llegada", text="Fecha de Llegada")
        self.tree.heading("Fecha de Salida", text="Fecha de Salida")
        self.tree.heading("Tipo de Habitación", text="Tipo de Habitación")
        self.tree.heading("Precio Total", text="Precio Total")
        self.tree.grid(row=7, column=0, columnspan=4)
        
        # Cargar las reservas existentes
        self.cargar_reservas()
    
    def cargar_tipos_habitacion(self):
        db = Database()
        query = "SELECT id_tipo_habitacion, tipo FROM tipo_habitacion"
        rows = db.fetch_all(query)
        tipos = {row['id_tipo_habitacion']: row['tipo'] for row in rows}
        self.tipo_habitacion_dict = tipos
        self.combo_tipo_habitacion['values'] = list(tipos.values())

    def cargar_reservas(self):
        db = Database()
        query = """
        SELECT r.id_usuario, r.fecha_llegada, r.fecha_salida, th.tipo as tipo_habitacion, r.precio_total
        FROM reserva r
        JOIN habitacion h ON r.id_habitacion = h.id_habitacion
        JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
        """
        rows = db.fetch_all(query)
        for row in rows:
            self.tree.insert("", "end", values=(row['id_usuario'], row['fecha_llegada'], row['fecha_salida'], row['tipo_habitacion'], row['precio_total']))

    def validar_rut(self):
        rut = self.entry_rut.get()
        db = Database()
        query = "SELECT id_huesped FROM huespedes WHERE rut = %s"
        result = db.fetch_one(query, (rut,))
        if result:
            self.entry_id_usuario.config(state='normal')
            self.entry_id_usuario.delete(0, tk.END)
            self.entry_id_usuario.insert(0, result['id_huesped'])
            self.entry_id_usuario.config(state='readonly')
            messagebox.showinfo("Éxito", "RUT validado correctamente")
        else:
            messagebox.showerror("Error", "RUT no encontrado. Por favor registre al huésped primero.")

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
            habitacion_query = "SELECT id_habitacion FROM habitacion WHERE id_tipo_habitacion = %s LIMIT 1"
            habitacion = db.fetch_one(habitacion_query, (id_tipo_habitacion,))
            if habitacion:
                id_habitacion = habitacion['id_habitacion']
                db.execute_query("""
                INSERT INTO reserva (id_usuario, fecha_llegada, fecha_salida, id_habitacion, precio_total)
                VALUES (%s, %s, %s, %s, %s)
                """, (id_usuario, fecha_llegada, fecha_salida, id_habitacion, precio_total))

                messagebox.showinfo("Éxito", "Reserva agregada correctamente")
                self.tree.delete(*self.tree.get_children())  # Limpiar tabla
                self.cargar_reservas()  # Recargar reservas
            else:
                messagebox.showerror("Error", "No se encontró una habitación disponible para el tipo seleccionado")
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

        db = Database()
        try:
            habitacion_query = "SELECT id_habitacion FROM habitacion WHERE id_tipo_habitacion = %s LIMIT 1"
            habitacion = db.fetch_one(habitacion_query, (id_tipo_habitacion,))
            if habitacion:
                id_habitacion = habitacion['id_habitacion']
                selected_reserva = self.tree.item(selected_item, "values")
                db.execute_query("""
                UPDATE reserva
                SET id_usuario = %s, fecha_llegada = %s, fecha_salida = %s, id_habitacion = %s, precio_total = %s
                WHERE id_usuario = %s AND fecha_llegada = %s AND fecha_salida = %s
                """, (id_usuario, fecha_llegada, fecha_salida, id_habitacion, precio_total, selected_reserva[0], selected_reserva[1], selected_reserva[2]))

                messagebox.showinfo("Éxito", "Reserva modificada correctamente")
                self.tree.delete(*self.tree.get_children())  # Limpiar tabla
                self.cargar_reservas()  # Recargar reservas
            else:
                messagebox.showerror("Error", "No se encontró una habitación disponible para el tipo seleccionado")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_reserva(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una reserva para eliminar")
            return

        db = Database()
        try:
            selected_reserva = self.tree.item(selected_item, "values")
            db.execute_query("""
            DELETE FROM reserva
            WHERE id_usuario = %s AND fecha_llegada = %s AND fecha_salida = %s
            """, (selected_reserva[0], selected_reserva[1], selected_reserva[2]))

            messagebox.showinfo("Éxito", "Reserva eliminada correctamente")
            self.tree.delete(*self.tree.get_children())  # Limpiar tabla
            self.cargar_reservas()  # Recargar reservas
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaReserva(root)
    root.mainloop()