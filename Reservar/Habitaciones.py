import tkinter as tk
from tkinter import messagebox
from database import Database

class HabitacionesApp:
    def __init__(self, parent, fecha_entrada, fecha_salida, total_personas):
        self.parent = parent
        self.top = tk.Toplevel(parent.root)
        self.top.title("Seleccionar habitación")
        self.top.geometry("1000x580")

        self.db = Database()
        if not self.db.connect_to_db():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            self.top.destroy()
            return

        self.indice_habitacion = 0
        self.habitaciones = []
        self.habitaciones_seleccionadas = []
        self.total_personas = total_personas
        self.personas_asignadas = 0
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.tipo_habitacion_seleccionada = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.top, text="Seleccionar habitación", font=("Arial", 14)).pack(pady=10)

        self.marco_habitacion = tk.Frame(self.top)
        self.marco_habitacion.pack(pady=20)

        self.etiqueta_imagen_habitacion = tk.Label(self.marco_habitacion)
        self.etiqueta_imagen_habitacion.pack()

        self.etiqueta_descripcion_habitacion = tk.Label(self.marco_habitacion, text="")
        self.etiqueta_descripcion_habitacion.pack()

        # Botones de navegación
        self.boton_anterior = tk.Button(self.top, text="<", command=self.habitacion_anterior)
        self.boton_anterior.pack(side=tk.LEFT, padx=20)

        self.boton_siguiente = tk.Button(self.top, text=">", command=self.habitacion_siguiente)
        self.boton_siguiente.pack(side=tk.RIGHT, padx=20)

        # Botones de acción
        self.boton_descripcion = tk.Button(self.top, text="Descripción", command=self.mostrar_descripcion)
        self.boton_descripcion.pack(side=tk.LEFT, padx=20)

        self.boton_reservar = tk.Button(self.top, text="Reservar", command=self.confirmar_habitacion)
        self.boton_reservar.pack(side=tk.RIGHT, padx=20)

        # Buscar habitaciones
        self.buscar_habitaciones()

    def buscar_habitaciones(self):
        habitaciones_disponibles = self.db.buscar_habitaciones_disponibles(self.fecha_entrada, self.fecha_salida)

        self.habitaciones = [
            {
                "id": fila["id_habitacion"], 
                "numero": fila["numero_habitacion"], 
                "tipo": fila["tipo"], 
                "cantidad_maxima": fila["cantidad_maxima"], 
                "imagen": "room.png", 
                "descripcion": f"Habitación {fila['numero_habitacion']} - {fila['tipo']} - Precio por noche: {fila['precio_noche']}"
            }
            for fila in habitaciones_disponibles
        ]

        if self.habitaciones:
            self.indice_habitacion = 0
            self.cargar_habitacion()
        else:
            messagebox.showinfo("Sin habitaciones", "No hay habitaciones disponibles para las fechas seleccionadas.")


    def cargar_habitacion(self):
        if self.habitaciones:
            habitacion = self.habitaciones[self.indice_habitacion]
            self.etiqueta_imagen_habitacion.config(text=habitacion["imagen"])  # Cambia por la carga de la imagen si es necesario
            self.etiqueta_descripcion_habitacion.config(text=habitacion["descripcion"])
        else:
            self.etiqueta_imagen_habitacion.config(text="")
            self.etiqueta_descripcion_habitacion.config(text="")

    def habitacion_anterior(self):
        if self.habitaciones:
            if self.indice_habitacion > 0:
                self.indice_habitacion -= 1
            else:
                self.indice_habitacion = len(self.habitaciones) - 1
            self.cargar_habitacion()

    def habitacion_siguiente(self):
        if self.habitaciones:
            if self.indice_habitacion < len(self.habitaciones) - 1:
                self.indice_habitacion += 1
            else:
                self.indice_habitacion = 0
            self.cargar_habitacion()

    def mostrar_descripcion(self):
        if self.habitaciones:
            habitacion = self.habitaciones[self.indice_habitacion]
            messagebox.showinfo("Descripción", habitacion["descripcion"])

    def confirmar_habitacion(self):
        if self.habitaciones:
            habitacion = self.habitaciones[self.indice_habitacion]
            self.habitaciones_seleccionadas.append(habitacion)
            self.personas_asignadas += habitacion["cantidad_maxima"]
            self.tipo_habitacion_seleccionada = habitacion["tipo"]
            
            if self.personas_asignadas >= self.total_personas:
                self.top.destroy()
            else:
                messagebox.showinfo("Seleccione otra habitación", "La cantidad de personas excede la capacidad de esta habitación, seleccione otra habitación.")
