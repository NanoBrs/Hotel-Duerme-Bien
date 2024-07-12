import tkinter as tk
from tkinter import ttk, messagebox
from DAO.DAO_encargados import DAO_usuarios

class GestionEncargados(tk.Frame):
    def __init__(self, parent, controlador):
        tk.Frame.__init__(self, parent)
        self.controlador = controlador

        # Agregar imagen de fondo
        self.background_image = tk.PhotoImage(file="img/MENU2.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Instancia de DAO_usuarios
        self.dao = DAO_usuarios()

        # Variables para campos de entrada
        self.id_usuario_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.buscar_var = tk.StringVar()

        # Frame para el formulario de ingreso y edición
        form_frame = ttk.Frame(self, padding=(20, 10))
        form_frame.place(x=11.4, y=84.6, width=975.8, height=300)  # Ajustado para la mitad superior del área deseada

        # Campos de entrada
        # Primera columna
        ttk.Label(form_frame, text="GESTION DE USUARIOS ENCARGADOS").place(x=5, y=10)
        ttk.Label(form_frame, text="ID de Usuario:").place(x=5, y=40)
        ttk.Entry(form_frame, textvariable=self.id_usuario_var, state="readonly").place(x=150, y=40)

        ttk.Label(form_frame, text="Nombre:").place(x=5, y=70)
        ttk.Entry(form_frame, textvariable=self.nombre_var).place(x=150, y=70)

        ttk.Label(form_frame, text="Apellido:").place(x=5, y=100)
        ttk.Entry(form_frame, textvariable=self.apellido_var).place(x=150, y=100)

        ttk.Label(form_frame, text="Correo:").place(x=5, y=130)
        ttk.Entry(form_frame, textvariable=self.correo_var).place(x=150, y=130)

        ttk.Label(form_frame, text="Contraseña:").place(x=5, y=160)
        ttk.Entry(form_frame, textvariable=self.contrasena_var).place(x=150, y=160)

        # Campo de búsqueda
        ttk.Label(form_frame, text="BUSQUEDA:").place(x=5, y=190)
        ttk.Entry(form_frame, textvariable=self.buscar_var).place(x=5, y=210)

        ttk.Button(form_frame, text="Filtrar", command=self.buscar_usuario).place(x=155, y=210)
        ttk.Button(form_frame, text="Borrar Filtros", command=self.cargar_usuarios).place(x=235, y=210)

        # Botones CRUD
        ttk.Button(form_frame, text="Agregar", command=self.agregar_usuario).place(x=355, y=160)
        ttk.Button(form_frame, text="Modificar", command=self.modificar_usuario).place(x=445, y=160)
        ttk.Button(form_frame, text="Eliminar", command=self.eliminar_usuario).place(x=535, y=160)
        ttk.Button(form_frame, text="Limpiar Datos", command=self.limpiar_datos).place(x=625, y=160)

        # Frame para la tabla de usuarios
        table_frame = ttk.Frame(self, padding=(10, 5))
        table_frame.place(x=11.4, y=345.7, width=975.8, height=330)

        self.usuarios_table = ttk.Treeview(
            table_frame,
            columns=('ID', 'Nombre', 'Apellido', 'Correo', 'Contraseña'),
            show='headings',  # Para mostrar solo las cabeceras de las columnas
            height=8  # Número de filas visibles, puedes ajustarlo según tus necesidades
        )

        # Tabla de usuarios
        self.usuarios_table.heading('ID', text='ID')
        self.usuarios_table.heading('Nombre', text='Nombre')
        self.usuarios_table.heading('Apellido', text='Apellido')
        self.usuarios_table.heading('Correo', text='Correo')
        self.usuarios_table.heading('Contraseña', text='Contraseña')

        self.usuarios_table.column('ID', width=50)
        self.usuarios_table.column('Nombre', width=120)
        self.usuarios_table.column('Apellido', width=120)
        self.usuarios_table.column('Correo', width=150)
        self.usuarios_table.column('Contraseña', width=150)

        self.usuarios_table.grid(row=0, column=0, padx=20, pady=20)  # Ajustar márgenes a tu preferencia
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.usuarios_table.yview)
        self.usuarios_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Cargar datos iniciales de la tabla
        self.cargar_usuarios()

        self.usuarios_table.bind("<Double-1>", self.cargar_datos_seleccionados)  # Evento doble click que carga los datos en la tabla

        
#--------------------------------------------------------- MENU -----------------------------------------------------------------
        # Configuración de estilos
        style = ttk.Style()
        style.configure("rounded.TButton", borderwidth=2, relief="solid", background="white", padding=10, font=('Helvetica', 12))
        style.map("rounded.TButton", background=[('active', 'lightgray')])

        # Botón Cerrar Sesion
        self.boton_gestionar_habitaciones = ttk.Button(self, text="CERRAR SESIÓN", command=self.cerrar_sesion, style="rounded.TButton")
        self.boton_gestionar_habitaciones.place(x=1055, y=266, width=165, height=45)


    def cerrar_sesion(self):
        print("Sesión cerrada exitosamente.")
        messagebox.showinfo("Cerrar Sesion", "Sesión cerrada exitosamente.")
        self.controlador.mostrar_frame("Login")

#--------------------------------------------------------- FIN MENU -----------------------------------------------------------------

    def validar_entradas(self):
        if not self.nombre_var.get():
            messagebox.showerror("Error", "El campo Nombre es obligatorio")
            return False
        if not self.apellido_var.get():
            messagebox.showerror("Error", "El campo Apellido es obligatorio")
            return False
        if not self.correo_var.get():
            messagebox.showerror("Error", "El campo Correo es obligatorio")
            return False
        if not self.contrasena_var.get():
            messagebox.showerror("Error", "El campo Contraseña es obligatorio")
            return False
        return True

    def limpiar_datos(self):
        self.id_usuario_var.set("")
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.correo_var.set("")
        self.contrasena_var.set("")
        self.buscar_var.set("")

    def cargar_usuarios(self):
        for item in self.usuarios_table.get_children():
            self.usuarios_table.delete(item)
        usuarios = self.dao.cargar_usuarios_encargados()
        if usuarios:
            for usuario in usuarios:
                self.usuarios_table.insert('', tk.END, values=(
                    usuario['id_usuario'],
                    usuario['nombre'],
                    usuario['apellido'],
                    usuario['correo'],
                    usuario['contrasena']
                ))
                
    def agregar_usuario(self):
        if not self.validar_entradas():
            return
        params = (self.nombre_var.get(), self.apellido_var.get(), self.correo_var.get(), self.contrasena_var.get())
        self.dao.agregar_usuario(params)
        self.limpiar_datos()
        self.cargar_usuarios()
        
                

    def modificar_usuario(self):
        if not self.validar_entradas() or not self.id_usuario_var.get():
            messagebox.showerror("Error", "Debe seleccionar un usuario para modificar")
            return

        params = (self.nombre_var.get(), self.apellido_var.get(), self.correo_var.get(), self.contrasena_var.get(), self.id_usuario_var.get())
        self.dao.modificar_usuario(params)
        self.limpiar_datos()
        self.cargar_usuarios()


    def modificar_usuario(self):
        if not self.validar_entradas() or not self.id_usuario_var.get():
            messagebox.showerror("Error", "Debe seleccionar un usuario para modificar")
            return

        params = (self.nombre_var.get(), self.apellido_var.get(), self.correo_var.get(), self.contrasena_var.get(), self.id_usuario_var.get())
        self.dao.modificar_usuario(params)
        self.limpiar_datos()
        self.cargar_usuarios()

    def eliminar_usuario(self):
        id_usuario = self.id_usuario_var.get()
        if not id_usuario:
            messagebox.showerror("Error", "Debe seleccionar un usuario para eliminar")
            return
        self.dao.eliminar_usuario(id_usuario)
        self.limpiar_datos()
        self.cargar_usuarios()
        
        
    def cargar_datos_seleccionados(self, event):
        seleccion = self.usuarios_table.selection()
        if seleccion:
            item = self.usuarios_table.item(seleccion[0])
            valores = item['values']
            self.id_usuario_var.set(valores[0])
            self.nombre_var.set(valores[1])
            self.apellido_var.set(valores[2])
            self.correo_var.set(valores[3])
            self.contrasena_var.set(valores[4])

            
    def buscar_usuario(self):
        termino_busqueda = self.buscar_var.get()
        resultados = self.dao.buscar_usuario(termino_busqueda)
        self.usuarios_table.delete(*self.usuarios_table.get_children())
        for usuario in resultados:
            self.usuarios_table.insert('', 'end', values=(usuario['id_usuario'], usuario['nombre'], usuario['apellido'], usuario['correo'], usuario['contrasena']))


# Código para iniciar la aplicación Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Usuarios Encargados")
    root.geometry("1000x700")
    app = GestionUsuarios(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
