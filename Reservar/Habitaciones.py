import tkinter as tk
from tkinter import messagebox
from database import Database 

class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Seleccionar habitacion")
        self.root.geometry("1000x580")

        # Conectar a la base de datos
        self.db = Database()
        if not self.db.connect_to_db():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            root.destroy()

        # Variables
        self.indice_habitacion = 0
        self.habitaciones = []
        self.fecha_llegada = "2024-07-10"
        self.fecha_salida = "2024-07-20"

        self.pagina()

    def pagina(self):
        # Mostrar habitaciones
        self.marco_habitacion = tk.Frame(self.root)
        self.marco_habitacion.pack(pady=20)

        self.etiqueta_imagen_habitacion = tk.Label(self.marco_habitacion)
        self.etiqueta_imagen_habitacion.pack()

        self.etiqueta_descripcion_habitacion = tk.Label(self.marco_habitacion, text="")
        self.etiqueta_descripcion_habitacion.pack()

        # Botones de navegacion
        self.boton_anterior = tk.Button(self.root, text="<", command=self.habitacion_anterior)
        self.boton_anterior.pack(side=tk.LEFT, padx=20)

        self.boton_siguiente = tk.Button(self.root, text=">", command=self.habitacion_siguiente)
        self.boton_siguiente.pack(side=tk.RIGHT, padx=20)

        # Botones de accion
        self.boton_descripcion = tk.Button(self.root, text="Descripcion", command=self.mostrar_descripcion)
        self.boton_descripcion.pack(side=tk.LEFT, padx=20)

        self.boton_reservar = tk.Button(self.root, text="Reservar", command=self.reservar_habitacion)
        self.boton_reservar.pack(side=tk.RIGHT, padx=20)

        # Buscar habitaciones
        self.buscar_habitaciones()

    def buscar_habitaciones(self):
        # Consulta para encontrar habitaciones disponibles
        consulta = """
        SELECT h.id_habitacion, h.numero_habitacion, h.precio_noche
        FROM habitacion h
        LEFT JOIN detalle_reserva dr ON h.id_habitacion = dr.id_habitacion
        LEFT JOIN reserva r ON dr.id_reserva = r.id_reserva
        WHERE (r.fecha_salida <= %s OR r.fecha_llegada >= %s) OR r.fecha_llegada IS NULL
        """
        parametros = (self.fecha_llegada, self.fecha_salida)
        habitaciones_disponibles = self.db.fetch_all(consulta, parametros)

        # Actualizar la lista de habitaciones disponibles
        self.habitaciones = [
            {"id": fila["id_habitacion"], "numero": fila["numero_habitacion"], "imagen": "room.png", "descripcion": f"Habitacion {fila['numero_habitacion']} - Precio por noche: {fila['precio_noche']}"}
            for fila in habitaciones_disponibles
        ]

        # Mostrar resultados
        if self.habitaciones:
            self.indice_habitacion = 0
            self.cargar_habitacion()
        else:
            messagebox.showinfo("Sin habitaciones", "No hay habitaciones disponibles para las fechas seleccionadas.")

    def cargar_habitacion(self):
        # Cargar la habitacion actual en la interfaz
        if self.habitaciones:
            habitacion = self.habitaciones[self.indice_habitacion]
            self.etiqueta_imagen_habitacion.config(text=habitacion["imagen"])  # Cambia por la carga de la imagen si es necesario
            self.etiqueta_descripcion_habitacion.config(text=habitacion["numero"])
        else:
            self.etiqueta_imagen_habitacion.config(text="")
            self.etiqueta_descripcion_habitacion.config(text="No hay habitaciones disponibles.")

    def habitacion_anterior(self):
        # Navegar a la habitacion anterior
        if self.habitaciones:
            if self.indice_habitacion > 0:
                self.indice_habitacion -= 1
            else:
                self.indice_habitacion = len(self.habitaciones) - 1
            self.cargar_habitacion()

    def habitacion_siguiente(self):
        # Navegar a la siguiente habitacion
        if self.habitaciones:
            if self.indice_habitacion < len(self.habitaciones) - 1:
                self.indice_habitacion += 1
            else:
                self.indice_habitacion = 0
            self.cargar_habitacion()

    def mostrar_descripcion(self):
        # Mostrar la descripcion de la habitacion actual
        if self.habitaciones:
            habitacion = self.habitaciones[self.indice_habitacion]
            messagebox.showinfo("Descripcion", habitacion["descripcion"])

    def reservar_habitacion(self):
        # Mostrar mensaje de confirmacion de reserva
        if self.habitaciones:
            habitacion = self.habitaciones[self.indice_habitacion]
            messagebox.showinfo("Reserva", f"Reservaste la {habitacion['descripcion']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()
