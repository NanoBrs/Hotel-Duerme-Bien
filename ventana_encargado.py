import tkinter as tk
from tkinter import ttk

class VentanaEncargado(tk.Frame):
    def __init__(self, parent, controlador):
        tk.Frame.__init__(self, parent)
        self.controlador = controlador

        # Agregar imagen de fondo
        self.background_image = tk.PhotoImage(file="img/Menu.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Configuración de estilos
        style = ttk.Style()
        style.configure("rounded.TButton", borderwidth=2, relief="solid", background="white", padding=10, font=('Helvetica', 12))
        style.map("rounded.TButton", background=[('active', 'lightgray')])

        # Botón Gestionar Habitaciones
        self.boton_gestionar_habitaciones = ttk.Button(self, text="Gestionar Habitaciones", command=self.mostrar_gestion_habitaciones, style="rounded.TButton")
        self.boton_gestionar_habitaciones.place(x=300, y=150, width=360, height=40)

        # Botón Gestionar Huéspedes
        self.boton_gestionar_huespedes = ttk.Button(self, text="Gestionar Huéspedes", command=self.mostrar_gestion_huespedes, style="rounded.TButton")
        self.boton_gestionar_huespedes.place(x=300, y=210, width=360, height=40)

        # Botón Gestionar Reservas
        self.boton_gestionar_reservas = ttk.Button(self, text="Gestionar Reservas", command=self.mostrar_gestion_reservas, style="rounded.TButton")
        self.boton_gestionar_reservas.place(x=300, y=270, width=360, height=40)

        # Botón Cerrar Sesión
        self.boton_cerrar_sesion = ttk.Button(self, text="Cerrar Sesión", command=self.cerrar_sesion, style="rounded.TButton")
        self.boton_cerrar_sesion.place(x=300, y=330, width=360, height=40)

    def mostrar_gestion_habitaciones(self):
        self.controlador.mostrar_frame("GestionHabitaciones")

    def mostrar_gestion_huespedes(self):
        self.controlador.mostrar_frame("GestionClientes")

    def mostrar_gestion_reservas(self):
        self.controlador.mostrar_frame("GestionReservas")

    def cerrar_sesion(self):
        # Aquí deberías implementar la lógica para cerrar la sesión actual
        # Puedes mostrar un mensaje, limpiar datos de sesión, etc.
        print("Sesión cerrada exitosamente.")
        # Luego, probablemente quieras volver a la ventana de inicio de sesión o cerrar la aplicación
        # Por ejemplo:
        self.controlador.mostrar_frame("Login")  # Cambiar a la ventana de inicio de sesión
        # O si deseas cerrar la aplicación:
        # self.controlador.quit()  # Cierra el bucle principal de Tkinter
        # self.controlador.destroy()  # Destruye la ventana principal
