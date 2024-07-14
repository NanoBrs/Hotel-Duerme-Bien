import tkinter as tk
from login_window import Login
from menu_encargado import MenuEncargado
from gestion_habitacion import GestionHabitaciones
from gestion_huespedes import GestionHuespedes
from gestion_reservas import GestionReservas
from ventana_administrador import GestionEncargados
from tkinter import PhotoImage
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AppPrincipal(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Aplicación de Gestión")
        self.geometry("1280x720")
        self.resizable(False, False)

        # Establece el ícono de la ventana y la barra de tareas usando un archivo .ico
        try:
            self.icon_image = PhotoImage(file=resource_path("icono.png"))
            self.iconphoto(True, self.icon_image)
        except: 
            print("Error al cargar el icono")

        contenedor = tk.Frame(self)
        contenedor.pack(side="top", fill="both", expand=True)

        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, GestionHabitaciones,GestionEncargados,MenuEncargado,GestionReservas,GestionHuespedes):
            nombre_pagina = F.__name__
            frame = F(parent=contenedor, controlador=self)
            self.frames[nombre_pagina] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame("Login")
        #self.mostrar_frame("GestionHuespedes")

    def mostrar_frame(self, nombre_pagina):
        frame = self.frames[nombre_pagina]
        frame.tkraise()

if __name__ == "__main__":
    try:
        app = AppPrincipal()
        app.mainloop()
        input("Presiona Enter para salir...")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        input("Presiona Enter para salir...")
