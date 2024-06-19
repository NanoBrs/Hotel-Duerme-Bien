import tkinter as tk

class VentanaAdministrador:
    def __init__(self, master):
        self.master = master
        self.master.title("Ventana del Administrador")
        self.master.geometry("720x480")

        # Aqui falta desarrollar la ventana de administrador bien
        label = tk.Label(master, text="Bienvenido Administrador")
        label.pack()
