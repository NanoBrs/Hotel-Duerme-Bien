import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class VentanaAdministrador(tk.Frame):
    def __init__(self, parent, controlador):
        tk.Frame.__init__(self, parent)
        self.controlador = controlador

        # Agregar imagen de fondo

        # Frame para el formulario de ingreso y edición
        form_frame = ttk.Frame(self, padding=(20, 10))
        form_frame.place(x=11.4, y=84.6, width=975.8, height=300)  # Ajustado para la mitad superior del área deseada

        # Campos de entrada
        ttk.Label(form_frame, text="GESTION DE ENCARGADOS").place(x=5, y=10)

        ttk.Label(form_frame, text="Nombre:").place(x=10, y=50)
        self.entry_nombre = ttk.Entry(form_frame)
        self.entry_nombre.place(x=100, y=50)

        ttk.Label(form_frame, text="Apellido:").place(x=10, y=100)
        self.entry_apellido = ttk.Entry(form_frame)
        self.entry_apellido.place(x=100, y=100)

        ttk.Label(form_frame, text="RUT:").place(x=10, y=150)
        self.entry_rut = ttk.Entry(form_frame)
        self.entry_rut.place(x=100, y=150)

        # Botón para registrar usuario
        self.boton_registrar = ttk.Button(form_frame, text="Registrar encargado", command=self.registrar_usuario)
        self.boton_registrar.place(x=100, y=200)

        # Botón Cerrar Sesión
        self.boton_cerrar_sesion = ttk.Button(self, text="CERRAR SESIÓN", command=self.cerrar_sesion, style="rounded.TButton")
        self.boton_cerrar_sesion.place(x=1055, y=366, width=165, height=45)

    def registrar_usuario(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        rut = self.entry_rut.get()

        if not nombre or not apellido or not rut:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Validación de RUT (formato básico)
        if not rut.isdigit():
            messagebox.showerror("Error", "RUT no válido")
            return

        # Validación de longitud del RUT
        if len(rut) < 7 or len(rut) > 12:
            messagebox.showerror("Error", "Longitud del RUT no válida")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="clu100699",
                password="20973380-3",
                database="clu100699_hotel_duerme_bien"
            )
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO administrador (Nombre, Apellido, Rut) VALUES (%s, %s, %s)",
                (nombre, apellido, rut)
            )
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Éxito", "Encargado registrado con éxito")
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            self.entry_rut.delete(0, tk.END)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el encargado: {e}")

    def cerrar_sesion(self):
        print("Sesión cerrada exitosamente.")
        messagebox.showinfo("Cerrar Sesion", "Sesión cerrada exitosamente.")
        self.controlador.mostrar_frame("Login")

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaAdministrador(root, None)
    app.pack(expand=True, fill="both")
    root.mainloop()

