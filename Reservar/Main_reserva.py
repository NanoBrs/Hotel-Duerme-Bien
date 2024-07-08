import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from database import Database
from habitaciones import HabitacionesApp
from datetime import datetime

USUARIO = 1  # ID del usuario actual que está registrando la reserva

class MainReservaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservas")
        self.root.geometry("1280x720")
        
        self.db = Database()
        if not self.db.connect_to_db():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            self.root.destroy()
            return

        self.fecha_entrada = None
        self.fecha_salida = None
        self.habitaciones_seleccionadas = []
        self.tipo_habitacion_seleccionada = None
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Reservar habitación", font=("Arial", 14)).place(x=500, y=10)

        tk.Label(self.root, text="Entrada").place(x=20, y=50)
        self.cal_entrada = Calendar(self.root, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_entrada.place(x=20, y=80)
        
        tk.Label(self.root, text="Salida").place(x=300, y=50)
        self.cal_salida = Calendar(self.root, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_salida.place(x=300, y=80)
        
        tk.Label(self.root, text="Cantidad de Adultos").place(x=20, y=320)
        self.adultos_spin = tk.Spinbox(self.root, from_=1, to=10)
        self.adultos_spin.place(x=160, y=320)
        
        tk.Label(self.root, text="Cantidad de Niños").place(x=240, y=320)
        self.ninos_spin = tk.Spinbox(self.root, from_=0, to=10)
        self.ninos_spin.place(x=360, y=320)
        
        tk.Label(self.root, text="RUT Huésped responsable").place(x=20, y=380)
        self.rut_huesped_entry = tk.Entry(self.root)
        self.rut_huesped_entry.place(x=160, y=380)
        
        tk.Label(self.root, text="ID Habitación").place(x=20, y=410)
        self.id_habitacion_entry = tk.Entry(self.root, state='readonly')
        self.id_habitacion_entry.place(x=160, y=410)
        
        tk.Button(self.root, text="Seleccionar Habitación", command=self.abrir_ventana_habitaciones).place(x=20, y=440)
        tk.Button(self.root, text="Reservar", command=self.registrar_reserva).place(x=200, y=440)

    def abrir_ventana_habitaciones(self):
        self.fecha_entrada = self.cal_entrada.get_date()
        self.fecha_salida = self.cal_salida.get_date()
        
        if not self.fecha_entrada or not self.fecha_salida:
            messagebox.showerror("Error", "Debe seleccionar fechas de entrada y salida.")
            return
        
        entrada = datetime.strptime(self.fecha_entrada, '%Y-%m-%d').date()
        salida = datetime.strptime(self.fecha_salida, '%Y-%m-%d').date()

        if salida <= entrada:
            messagebox.showerror("Error", "La fecha de salida debe ser posterior a la fecha de entrada.")
            return

        total_personas = int(self.adultos_spin.get()) + int(self.ninos_spin.get())
        habitaciones_app = HabitacionesApp(self, self.fecha_entrada, self.fecha_salida, total_personas)
        self.root.wait_window(habitaciones_app.top)

        if habitaciones_app.habitaciones_seleccionadas:
            self.habitaciones_seleccionadas = habitaciones_app.habitaciones_seleccionadas
            self.tipo_habitacion_seleccionada = habitaciones_app.tipo_habitacion_seleccionada
            habitaciones_texto = ", ".join([f"{hab['id']} - {hab['tipo']}" for hab in self.habitaciones_seleccionadas])
            self.id_habitacion_entry.config(state='normal')
            self.id_habitacion_entry.delete(0, tk.END)
            self.id_habitacion_entry.insert(0, habitaciones_texto)
            self.id_habitacion_entry.config(state='readonly')

    def registrar_reserva(self):
        if not self.fecha_entrada or not self.fecha_salida:
            messagebox.showerror("Error", "Debe seleccionar fechas de entrada y salida.")
            return

        entrada = datetime.strptime(self.fecha_entrada, '%Y-%m-%d').date()
        salida = datetime.strptime(self.fecha_salida, '%Y-%m-%d').date()

        if salida <= entrada:
            messagebox.showerror("Error", "La fecha de salida debe ser despues a la fecha de entrada.")
            return

        rut_huesped = self.rut_huesped_entry.get()

        if not rut_huesped or not self.habitaciones_seleccionadas:
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return

        try:
            id_huesped = self.db.obtener_id_por_rut(rut_huesped)
            if not id_huesped:
                messagebox.showerror("Error", "El RUT ingresado no es válido.")
                return

            noches = (salida - entrada).days
            precio_total = 0

            for hab in self.habitaciones_seleccionadas:
                habitacion = self.db.cargar_habitacion_por_id(hab['id'])
                precio_total += habitacion[0]['precio_noche'] * noches

            id_reserva = self.db.insert_reserva(entrada, salida, USUARIO, precio_total)

            hora_actual = datetime.now().strftime("%H:%M:%S")
            for hab in self.habitaciones_seleccionadas:
                id_detalle_reserva = self.db.insert_detalle_reserva(id_reserva, hab['id'], hora_actual)
                self.db.insert_detalle_huesped(id_reserva, id_huesped, id_detalle_reserva)

            messagebox.showinfo("Éxito", "Reserva registrada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Algo salió mal: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainReservaApp(root)
    root.mainloop()
