import tkinter as tk
from tkinter import ttk, messagebox
from DAO.DAO_habitaciones import DAO_habitaciones  # Importa la clase DAO_habitaciones desde tu archivo DAO_habitaciones.py
from PIL import Image, ImageTk
import tkinter as tk

class GestionEncargados(tk.Frame):
    def __init__(self, parent, controlador):
        tk.Frame.__init__(self, parent)
        self.controlador = controlador

        # Agregar imagen de fondo
        self.background_image = tk.PhotoImage(file="img/MENU2.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

       
        # Frame para el formulario de ingreso y edición
        form_frame = ttk.Frame(self, padding=(20, 10))
        form_frame.place(x=11.4, y=84.6, width=975.8, height=300)  # Ajustado para la mitad superior del área deseada

        # Campos de entrada
        # Primera columna
        ttk.Label(form_frame, text="GESTION DE ENCARGADOS").place(x=5, y=10)

        #--------------------------------------------------------- MENU -----------------------------------------------------------------
        # Configuración de estilos
        style = ttk.Style()
        style.configure("rounded.TButton", borderwidth=2, relief="solid", background="white", padding=10, font=('Helvetica', 12))
        style.map("rounded.TButton", background=[('active', 'lightgray')])

        # Botón Gestionar Habitaciones
        self.boton_gestionar_habitaciones = ttk.Button(self, text="ENCARGADOS", command=self.mostrar_gestion_encargados, style="rounded.TButton")
        self.boton_gestionar_habitaciones.place(x=1055, y=266, width=165, height=45)

        # Botón Cerrar Sesión
        self.boton_cerrar_sesion = ttk.Button(self, text="CERRAR SESIÓN", command=self.cerrar_sesion, style="rounded.TButton")
        self.boton_cerrar_sesion.place(x=1055, y=366, width=165, height=45)


    def mostrar_gestion_encargados(self):
        self.controlador.mostrar_frame("GestionEncargados")


    def cerrar_sesion(self):
        print("Sesión cerrada exitosamente.")
        messagebox.showinfo("Cerrar Sesion", "Sesión cerrada exitosamente.")
        self.controlador.mostrar_frame("Login")

    def volver_menu_encargado(self):
        self.controlador.mostrar_frame("VentanaEncargado")
#--------------------------------------------------------- FIN MENU -----------------------------------------------------------------