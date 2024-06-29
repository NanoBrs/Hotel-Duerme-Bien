import tkinter as tk
import mysql.connector

class VentanaAdministrador:
    def __init__(self, master):
        self.master = master
        self.master.title("Ventana del Administrador")
        self.master.geometry("720x480")

        # Crear una etiqueta de título
        label = tk.Label(master, text="Bienvenido Administrador", font=("Arial",24))
        label.pack(pady=20)

        # Crear un marco para la información del usuario
        self.marco_usuario = tk.Frame(master)
        self.marco_usuario.pack(pady=20)

        # Etiquetas y entradas para la información del encargado
        label_nombre = tk.Label(self.marco_usuario, text="Nombre:")
        label_nombre.pack(pady=5)
        self.entry_nombre = tk.Entry(self.marco_usuario)
        self.entry_nombre.pack(pady=5)

        label_apellido = tk.Label(self.marco_usuario, text="Apellido:")
        label_apellido.pack(pady=5)
        self.entry_apellido = tk.Entry(self.marco_usuario)
        self.entry_apellido.pack(pady=5)

        label_rut = tk.Label(self.marco_usuario, text="RUT:")
        label_rut.pack(pady=5)
        self.entry_rut = tk.Entry(self.marco_usuario)
        self.entry_rut.pack(pady=5)

        # Botón para registrar usuario
        self.boton_registrar = tk.Button(master, text="Registrar encargado", command=self.registrar_usuario)
        self.boton_registrar.pack(pady=10)

    # Función para registrar usuario
    def registrar_usuario(self):
        # Conexión a la base de datos MySQL
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="usuario_mysql",
                password="contrasena_mysql",
                database="nombre_base_datos"
            )
        except mysql.connector.Error as error:
            self.mostrar_mensaje_error(f"Error de conexión: {error}")
            return

        # Obtener los datos del usuario
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        rut = self.entry_rut.get()

        # Validación de datos
        if not nombre or not apellido or not rut:
            self.mostrar_mensaje_error("Todos los campos son obligatorios")
            return

        # Validación de RUT (formato básico)
        if not rut.isdigit():
            self.mostrar_mensaje_error("RUT no válido")
            return

        # Validación de longitud del RUT
        if len(rut) < 7 or len(rut) > 12:
            self.mostrar_mensaje_error("Longitud del RUT no válida")
            return

        # Preparar la consulta SQL para insertar el nuevo usuario
        cursor = db.cursor()
        sql = "INSERT INTO encargados_hotel (nombre, apellido, rut) VALUES (%s, %s, %s)"
        valores = (nombre, apellido, rut)

        # Ejecutar la consulta y guardar los cambios
        try:
            cursor.execute(sql, valores)
            db.commit()
            cursor.close()
            db.close()

            # Mostrar mensaje de confirmación
            self.mostrar_mensaje_exito("Encargado registrado con éxito")

            # Limpiar los campos de entrada
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            self.entry_rut.delete(0, tk.END)
        except mysql.connector.Error as error:
            self.mostrar_mensaje_error(f"Error al registrar: {error}")

    def mostrar_mensaje_error(self, mensaje):
        # Eliminar mensajes anteriores si existen
        for widget in self.master.pack_slaves():
            if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                widget.destroy()
        mensaje_error = tk.Label(self.master, text=mensaje, fg="red")
        mensaje_error.pack()

    def mostrar_mensaje_exito(self, mensaje):
        # Eliminar mensajes anteriores si existen
        for widget in self.master.pack_slaves():
            if isinstance(widget, tk.Label) and widget.cget("fg") == "green":
                widget.destroy()
        mensaje_exito = tk.Label(self.master, text=mensaje, fg="green")
        mensaje_exito.pack()

# Iniciar la interfaz
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaAdministrador(root)
    root.mainloop()
