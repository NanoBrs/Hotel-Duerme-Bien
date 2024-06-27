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
        
        self.label_id_cliente = tk.Label(master, text="ID de Cliente:")
        self.label_id_cliente.grid(row=2, column=0)
        self.entry_id_cliente = tk.Entry(master)
        self.entry_id_cliente.grid(row=2, column=1)
        
        self.label_fecha_entrada = tk.Label(master, text="Fecha de Entrada:")
        self.label_fecha_entrada.grid(row=3, column=0)
        self.entry_fecha_entrada = tk.Entry(master)
        self.entry_fecha_entrada.grid(row=3, column=1)
        
        self.label_fecha_salida = tk.Label(master, text="Fecha de Salida:")
        self.label_fecha_salida.grid(row=4, column=0)
        self.entry_fecha_salida = tk.Entry(master)
        self.entry_fecha_salida.grid(row=4, column=1)
        
        self.label_estado = tk.Label(master, text="Estado:")
        self.label_estado.grid(row=5, column=0)
        self.entry_estado = tk.Entry(master)
        self.entry_estado.grid(row=5, column=1)
        
        # Botones de acciones
        self.button_agregar = tk.Button(master, text="Agregar", command=self.agregar_reserva)
        self.button_agregar.grid(row=6, column=0)
        
        self.button_modificar = tk.Button(master, text="Modificar", command=self.modificar_reserva)
        self.button_modificar.grid(row=6, column=1)
        
        self.button_eliminar = tk.Button(master, text="Eliminar", command=self.eliminar_reserva)
        self.button_eliminar.grid(row=6, column=2)
        
        # Tabla para mostrar las reservas
        self.tree = ttk.Treeview(master, columns=("ID", "ID de Habitacion", "ID de Cliente", "Fecha de Entrada", "Fecha de Salida", "Estado"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("ID de Habitacion", text="ID de Habitacion")
        self.tree.heading("ID de Cliente", text="ID de Cliente")
        self.tree.heading("Fecha de Entrada", text="Fecha de Entrada")
        self.tree.heading("Fecha de Salida", text="Fecha de Salida")
        self.tree.heading("Estado", text="Estado")
        self.tree.grid(row=7, column=0, columnspan=3)
        
        # Cargar las reservas existentes
        self.cargar_reservas()
    
    def cargar_reservas(self):
        db = Database()
        query = """
        SELECT r.id_reserva, dr.id_habitacion, r.id_cliente, r.fecha_entrada, r.fecha_salida, r.estado
        FROM reserva r
        JOIN detalle_reserva dr ON r.id_reserva = dr.id_reserva
        """
        rows = db.fetch_all(query)
        for row in rows:
            self.tree.insert("", "end", values=(row['id_reserva'], row['id_habitacion'], row['id_cliente'], row['fecha_entrada'], row['fecha_salida'], row['estado']))
            
    def agregar_reserva(self):
        id_reserva = self.entry_id_reserva.get()
        id_habitacion = self.entry_id_habitacion.get()
        id_cliente = self.entry_id_cliente.get()
        fecha_entrada = self.entry_fecha_entrada.get()
        fecha_salida = self.entry_fecha_salida.get()
        estado = self.entry_estado.get()
        
        if not all([id_reserva, id_habitacion, id_cliente, fecha_entrada, fecha_salida, estado]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        db = Database()
        try:
            db.execute_query("""
            INSERT INTO reserva (id_reserva, id_cliente, fecha_entrada, fecha_salida, estado)
            VALUES (%s, %s, %s, %s, %s)
            """, (id_reserva, id_cliente, fecha_entrada, fecha_salida, estado))
            
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
        id_cliente = self.entry_id_cliente.get()
        fecha_entrada = self.entry_fecha_entrada.get()
        fecha_salida = self.entry_fecha_salida.get()
        estado = self.entry_estado.get()
        
        if not all([id_reserva, id_habitacion, id_cliente, fecha_entrada, fecha_salida, estado]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        db = Database()
        try:
            db.execute_query("""
            UPDATE reserva
            SET id_cliente = %s, fecha_entrada = %s, fecha_salida = %s, estado = %s
            WHERE id_reserva = %s
            """, (id_cliente, fecha_entrada, fecha_salida, estado, id_reserva))
            
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
            
            
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("100x800")  # Ancho de 800 píxeles y alto de 600 píxeles
    app = VentanaReserva(root)
    root.mainloop()