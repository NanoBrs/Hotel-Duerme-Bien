import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

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
        ttk.Label(form_frame, text="GESTIÓN DE ENCARGADOS", font=("Helvetica", 16)).place(x=5, y=10)

        # Primera columna
        ttk.Label(form_frame, text="Nombre:").place(x=5, y=50)
        self.entry_nombre = ttk.Entry(form_frame)
        self.entry_nombre.place(x=150, y=50)

        ttk.Label(form_frame, text="Apellido:").place(x=5, y=90)
        self.entry_apellido = ttk.Entry(form_frame)
        self.entry_apellido.place(x=150, y=90)

        ttk.Label(form_frame, text="RUT:").place(x=5, y=130)
        self.entry_rut = ttk.Entry(form_frame)
        self.entry_rut.place(x=150, y=130)

        # Botón para registrar usuario
        self.boton_registrar = ttk.Button(form_frame, text="Registrar Encargado", command=self.registrar_usuario)
        self.boton_registrar.place(x=150, y=170)


        # Configuración de estilos
        style = ttk.Style()
        style.configure("rounded.TButton", borderwidth=2, relief="solid", background="white", padding=10, font=('Helvetica', 12))
        style.map("rounded.TButton", background=[('active', 'lightgray')])

        # Botón Gestionar Encargados
        self.boton_gestionar_encargados = ttk.Button(self, text="ENCARGADOS", command=self.mostrar_gestion_encargados, style="rounded.TButton")
        self.boton_gestionar_encargados.place(x=1055, y=266, width=165, height=45)

        # Botón Cerrar Sesión
        self.boton_cerrar_sesion = ttk.Button(self, text="CERRAR SESIÓN", command=self.cerrar_sesion, style="rounded.TButton")
        self.boton_cerrar_sesion.place(x=1055, y=366, width=165, height=45)

    def mostrar_gestion_encargados(self):
        self.controlador.mostrar_frame("GestionEncargados")

    def cerrar_sesion(self):
        print("Sesión cerrada exitosamente.")
        messagebox.showinfo("Cerrar Sesión", "Sesión cerrada exitosamente.")
        self.controlador.mostrar_frame("Login")

    def registrar_usuario(self):

        # Obtener los datos del usuario
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        rut = self.entry_rut.get()

        # Validaciones de los datos ingresados
        if not nombre or not apellido or not rut:
            self.mostrar_mensaje_error("Todos los campos son obligatorios")
            return

        if not self.validar_rut(rut):
            self.mostrar_mensaje_error("RUT no válido")
            return

        # Mostrar mensaje de confirmación
        self.mostrar_mensaje_exito("Encargado registrado con éxito")

        # Limpiar los campos de entrada
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_rut.delete(0, tk.END)

    def mostrar_mensaje_exito(self, mensaje):
        messagebox.showinfo("Éxito", mensaje)

    def mostrar_mensaje_error(self, mensaje):
        messagebox.showerror("Error", mensaje)

    def validar_rut(self, rut):
        # Validación básica del RUT
        if not rut.isdigit():                #isdigit() se aplica a una cadena y devuelve True si todos los caracteres de la cadena son dígitos y hay al menos un carácter en la cadena.
            return False
        if len(rut) < 7 or len(rut) > 12:
            return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestión de Encargados")
    app = GestionEncargados(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
