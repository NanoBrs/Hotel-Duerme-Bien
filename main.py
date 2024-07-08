import tkinter as tk
from Interfaces.login_window import Login
from Interfaces.Encargado.menu_encargado import MenuEncargado
from Interfaces.Encargado.gestion_habitacion import GestionHabitaciones
from Interfaces.Encargado.gestion_huespedes import GestionHuespedes
from Interfaces.Encargado.gestion_reservas import GestionReservas
from Interfaces.Administrador.ventana_administrador import GestionEncargados
from tkinter import PhotoImage


class AppPrincipal(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Aplicación de Gestión")
        self.geometry("1280x720")
        self.resizable(False, False)

        # Establece el ícono de la ventana y la barra de tareas usando un archivo .ico
        self.icon_image = PhotoImage(file="img/icono.png")
        self.iconphoto(True, self.icon_image)

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
        #self.mostrar_frame("Habitacion")

    def mostrar_frame(self, nombre_pagina):
        frame = self.frames[nombre_pagina]
        frame.tkraise()

if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()
