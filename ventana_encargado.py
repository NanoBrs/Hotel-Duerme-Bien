import tkinter as tk
from tkinter import messagebox
from gestion_habitacion import HabitacionCRUD 
from ventana_reserva import VentanaReserva

class VentanaEncargado:
    def __init__(self, master):
        self.master = master
        self.master.title("Ventana del Encargado")
        self.master.geometry("720x480")

        # Crear un canvas para la imagen de fondo y los botones
        self.canvas = tk.Canvas(master, width=720, height=480)
        self.canvas.pack(fill="both", expand=True)

        # Cargar y agregar imagen de fondo
        self.background_image = tk.PhotoImage(file="img/Menu.png")
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Estilo de los botones para hacerlos más grandes y con borde negro
        button_style = {
            "bg": "white", 
            "fg": "black", 
            "relief": "solid", 
            "bd": 2,  # Borde de 2 píxeles
            "width": 25,  # Ancho del botón
            "height": 2,  # Alto del botón
            "font": ("Helvetica", 12)
        }

        # Botón Gestionar Habitaciones
        self.boton_gestionar_habitaciones = tk.Button(master, text="Gestionar Habitaciones", command=self.gestionar_habitaciones, **button_style)
        self.canvas.create_window(360, 150, window=self.boton_gestionar_habitaciones, anchor="center")

        # Botón Gestionar Huéspedes
        self.boton_gestionar_huespedes = tk.Button(master, text="Gestionar Huéspedes", command=self.gestionar_huespedes, **button_style)
        self.canvas.create_window(360, 220, window=self.boton_gestionar_huespedes, anchor="center")

        # Botón Gestionar Reservas
        self.boton_gestionar_reservas = tk.Button(master, text="Gestionar Reservas", command=self.gestionar_reservas, **button_style)
        self.canvas.create_window(360, 290, window=self.boton_gestionar_reservas, anchor="center")

        # Botón Salir
        self.boton_salir = tk.Button(master, text="Salir", command=self.salir, **button_style)
        self.canvas.create_window(360, 360, window=self.boton_salir, anchor="center")

    def gestionar_habitaciones(self):
        # Minimizar la ventana principal
        self.master.iconify()

        # Crear una nueva ventana para gestionar habitaciones
        new_window = tk.Toplevel(self.master)
        new_window.title("Gestión de Habitaciones")
        new_window.geometry("1000x480")

        # Instancia de la clase HabitacionCRUD
        HabitacionCRUD(new_window)

    def gestionar_huespedes(self):
        messagebox.showinfo("Gestionar Huéspedes", "Funcionalidad para gestionar huéspedes.")

    def gestionar_reservas(self):
                # Minimizar la ventana principal
        self.master.iconify()

        # Crear una nueva ventana para gestionar habitaciones
        new_window = tk.Toplevel(self.master)
        new_window.title("Gestión de Reservas")
        new_window.geometry("1000x800")

        # Instancia de la clase HabitacionCRUD
        VentanaReserva(new_window)
    def salir(self):
        self.master.quit()  # Cierra el bucle principal de Tkinter
        print("Saliendo del programa, gracias por preferirnos...")
        self.master.destroy()  # Destruye la ventana principal

