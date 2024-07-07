import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from database import Database
from datetime import datetime
from datetime import date
import mysql.connector  # Asegúrate de importar mysql.connector

usuario_actual = 1  # ID del usuario actual (ejemplo)

class ReservaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reservar Habitación")
        self.root.geometry("1280x720")
        self.db = Database()
        if not self.db.connect_to_db():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            self.root.destroy()
            return

        # Crear widgets de la interfaz
        self.create_widgets()
    
    def create_widgets(self):
        frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)
        frame.place(x=40, y=40, width=1200, height=640)

        tk.Label(frame, text="Reservar habitación", font=("Arial", 14)).place(x=500, y=10)

        tk.Label(frame, text="Entrada").place(x=20, y=50)
        self.cal_entrada = Calendar(frame, selectmode='day')
        self.cal_entrada.place(x=20, y=80)
        
        tk.Label(frame, text="Salida").place(x=240, y=50)
        self.cal_salida = Calendar(frame, selectmode='day')
        self.cal_salida.place(x=240, y=80)
        
        tk.Label(frame, text="Cantidad de Adultos").place(x=20, y=300)
        self.adultos_spin = tk.Spinbox(frame, from_=1, to=10)
        self.adultos_spin.place(x=160, y=300)
        
        tk.Label(frame, text="Cantidad de Niños").place(x=240, y=300)
        self.ninos_spin = tk.Spinbox(frame, from_=0, to=10)
        self.ninos_spin.place(x=360, y=300)
        
        self.agregar_cama_var = tk.IntVar()
        tk.Checkbutton(frame, text="Agregar cama?", variable=self.agregar_cama_var).place(x=20, y=330)
        
        tk.Label(frame, text="ID Huésped responsable").place(x=20, y=360)
        self.id_huesped_entry = tk.Entry(frame)
        self.id_huesped_entry.place(x=160, y=360)
        
        tk.Label(frame, text="ID Habitación").place(x=20, y=390)
        self.id_habitacion_entry = tk.Entry(frame)
        self.id_habitacion_entry.place(x=160, y=390)
        
        tk.Button(frame, text="Registrar", command=self.registrar_reserva).place(x=20, y=420)
        tk.Button(frame, text="Siguiente", command=self.siguiente_habitacion).place(x=100, y=420)

    def registrar_reserva(self):
        # Obtener los datos del formulario
        entrada = self.cal_entrada.get_date()
        salida = self.cal_salida.get_date()
        cantidad_adultos = self.adultos_spin.get()
        cantidad_ninos = self.ninos_spin.get()
        agregar_cama = self.agregar_cama_var.get()
        id_huesped = self.id_huesped_entry.get()
        id_habitacion = self.id_habitacion_entry.get()
        
        # Aquí se pueden agregar validaciones adicionales
        if not id_huesped or not id_habitacion:
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return

        try:
            # Convertir fechas
            entrada_date = datetime.strptime(entrada, '%d/%m/%y').date()
            salida_date = datetime.strptime(salida, '%d/%m/%y').date()
            
            # Insertar la reserva y obtener el ID de la reserva
            id_reserva = self.db.insert_reserva(entrada_date, salida_date, usuario_actual)
            
            # Insertar en detalle_reserva
            self.db.insert_detalle_reserva(id_reserva, id_habitacion)
            
            # Insertar en detalle_huesped
            self.db.insert_detalle_huesped(id_reserva, id_huesped, True)

            messagebox.showinfo("Éxito", "Reserva registrada con éxito")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al registrar la reserva: {e}")

    def siguiente_habitacion(self):
        # Lógica para registrar otra habitación si se desea
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ReservaApp(root)
    root.mainloop()
