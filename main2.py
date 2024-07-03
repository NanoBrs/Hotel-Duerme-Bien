import tkinter as tk
from login_window import Login
from ventana_encargado import VentanaEncargado  
from gestion_habitacion import GestionHabitaciones

class AppPrincipal(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Aplicación de Gestión")
        self.geometry("1000x580")

        contenedor = tk.Frame(self)
        contenedor.pack(side="top", fill="both", expand=True)

        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, VentanaEncargado, GestionHabitaciones):
            nombre_pagina = F.__name__
            frame = F(parent=contenedor, controlador=self)
            self.frames[nombre_pagina] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame("Login")

    def mostrar_frame(self, nombre_pagina):
        frame = self.frames[nombre_pagina]
        frame.tkraise()

if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()
