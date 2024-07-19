import tkinter as tk
from tkinter import ttk, messagebox
from DAO.DAOHuespedes import DAOHuespedes_Consultas  # Importa la clase DAO_huespedes desde tu archivo DAO_huespedes.py
from PIL import Image, ImageTk
import re
import os
import sys
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
class GestionHuespedes(tk.Frame):
    def __init__(self, parent, controlador):
        tk.Frame.__init__(self, parent)
        self.controlador = controlador

        try:
            # Agregar imagen de fondo
            self.background_image = tk.PhotoImage(file=resource_path("MENU2.png"))
            self.background_label = tk.Label(self, image=self.background_image)
            self.background_label.place(relwidth=1, relheight=1)
        except:
            pass
            #print("Fallo huespedes")
        # Instancia de DAO_huespedes
        self.dao = DAOHuespedes_Consultas()

        # Variables para campos de entrada
        self.id_huesped_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.apellido1_var = tk.StringVar()
        self.apellido2_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.numero_var = tk.StringVar()
        self.rut_var = tk.StringVar()
        self.buscar_var = tk.StringVar()

        # Frame para el formulario de ingreso y edición
        form_frame = ttk.Frame(self, padding=(20, 10))
        form_frame.place(x=11.4, y=84.6, width=975.8, height=300)  # Ajustado para la mitad superior del área deseada

        # Campos de entrada
        # Primera columna
        ttk.Label(form_frame, text="GESTIÓN DE HUÉSPEDES").place(x=5, y=10)
        ttk.Label(form_frame, text="ID de Huésped:").place(x=5, y=40)
        ttk.Entry(form_frame, textvariable=self.id_huesped_var, state="readonly").place(x=150, y=40)

        ttk.Label(form_frame, text="Nombre:").place(x=5, y=70)
        ttk.Entry(form_frame, textvariable=self.nombre_var).place(x=150, y=70)

        ttk.Label(form_frame, text="Primer Apellido:").place(x=5, y=100)
        ttk.Entry(form_frame, textvariable=self.apellido1_var).place(x=150, y=100)

        ttk.Label(form_frame, text="Segundo Apellido:").place(x=5, y=130)
        ttk.Entry(form_frame, textvariable=self.apellido2_var).place(x=150, y=130)

        ttk.Label(form_frame, text="Correo:").place(x=5, y=160)
        ttk.Entry(form_frame, textvariable=self.correo_var).place(x=150, y=160)

        # Segunda columna
        ttk.Label(form_frame, text="Número:").place(x=355, y=40)
        ttk.Entry(form_frame, textvariable=self.numero_var).place(x=475, y=40)

        ttk.Label(form_frame, text="RUT:").place(x=355, y=70)
        ttk.Entry(form_frame, textvariable=self.rut_var).place(x=475, y=70)

        # Campo de búsqueda
        ttk.Label(form_frame, text="BUSQUEDA:").place(x=5, y=190)
        ttk.Entry(form_frame, textvariable=self.buscar_var).place(x=5, y=210)

        ttk.Button(form_frame, text="Filtrar", command=self.buscar_huesped).place(x=155, y=210)
        ttk.Button(form_frame, text="Borrar Filtros", command=self.cargar_huespedes).place(x=235, y=210)

        # Botones CRUD
        ttk.Button(form_frame, text="Agregar", command=self.agregar_huesped).place(x=355, y=100)
        ttk.Button(form_frame, text="Modificar", command=self.modificar_huesped).place(x=445, y=100)
        ttk.Button(form_frame, text="Eliminar", command=self.eliminar_huesped).place(x=535, y=100)
        ttk.Button(form_frame, text="Limpiar Datos", command=self.limpiar_datos).place(x=625, y=100)

        # Frame para la tabla de huéspedes
        table_frame = ttk.Frame(self, padding=(10, 5))
        table_frame.place(x=11.4, y=345.7, width=975.8, height=330)

        self.huespedes_table = ttk.Treeview(
            table_frame,
            columns=('ID', 'Nombre', 'Apellido1', 'Apellido2', 'Correo', 'Numero', 'RUT'),
            show='headings',  # Para mostrar solo las cabeceras de las columnas
            height=8  # Número de filas visibles, puedes ajustarlo según tus necesidades
        )

        # Tabla de huéspedes
        self.huespedes_table.heading('ID', text='ID')
        self.huespedes_table.heading('Nombre', text='Nombre')
        self.huespedes_table.heading('Apellido1', text='Primer Apellido')
        self.huespedes_table.heading('Apellido2', text='Segundo Apellido')
        self.huespedes_table.heading('Correo', text='Correo')
        self.huespedes_table.heading('Numero', text='Número')
        self.huespedes_table.heading('RUT', text='RUT')

        self.huespedes_table.column('ID', width=50)
        self.huespedes_table.column('Nombre', width=120)
        self.huespedes_table.column('Apellido1', width=100)
        self.huespedes_table.column('Apellido2', width=100)
        self.huespedes_table.column('Correo', width=150)
        self.huespedes_table.column('Numero', width=100)
        self.huespedes_table.column('RUT', width=100)

        self.huespedes_table.grid(row=0, column=0, padx=20, pady=20)  # Ajustar márgenes a tu preferencia
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.huespedes_table.yview)
        self.huespedes_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Cargar datos iniciales de la tabla
        self.cargar_huespedes()

        self.huespedes_table.bind("<Double-1>", self.cargar_datos_seleccionados)  # Evento doble click que carga los datos en la tabla
#------------------------------------------------------------- MENU ---------------------------------------------------------------------------
        # Configuración de estilos
        style = ttk.Style()
        style.configure("rounded.TButton", borderwidth=2, relief="solid", background="white", padding=10, font=('Helvetica', 12))
        style.map("rounded.TButton", background=[('active', 'lightgray')])

        # Botón Gestionar Habitaciones
        self.boton_gestionar_habitaciones = ttk.Button(self, text="HABITACIONES", command=self.mostrar_gestion_habitaciones, style="rounded.TButton")
        self.boton_gestionar_habitaciones.place(x=1055, y=266, width=165, height=45)

        # Botón Gestionar Huéspedes
        self.boton_gestionar_huespedes = ttk.Button(self, text="HUESPEDES", command=self.mostrar_gestion_huespedes, style="rounded.TButton")
        self.boton_gestionar_huespedes.place(x=1055, y=366, width=165, height=45)

        # Botón Gestionar Reservas
        self.boton_gestionar_reservas = ttk.Button(self, text="RESERVAS", command=self.mostrar_gestion_reservas, style="rounded.TButton")
        self.boton_gestionar_reservas.place(x=1055, y=466, width=165, height=45)

        # Botón Cerrar Sesión
        self.boton_cerrar_sesion = ttk.Button(self, text="CERRAR SESIÓN", command=self.cerrar_sesion, style="rounded.TButton")
        self.boton_cerrar_sesion.place(x=1055, y=566, width=165, height=45)

    def mostrar_gestion_habitaciones(self):
        self.controlador.mostrar_frame("GestionHabitaciones")

    def mostrar_gestion_huespedes(self):
        self.controlador.mostrar_frame("GestionHuespedes")

    def mostrar_gestion_reservas(self):
        self.controlador.mostrar_frame("GestionReservas")

    def cerrar_sesion(self):
        #print("Sesión cerrada exitosamente.")
        messagebox.showinfo("Cerrar Sesion", "Sesión cerrada exitosamente.")
        self.controlador.mostrar_frame("Login")

#------------------------------------------------------------- FIN MENU ---------------------------------------------------------------------------
    def limpiar_datos(self):
        self.id_huesped_var.set("")
        self.nombre_var.set("")
        self.apellido1_var.set("")
        self.apellido2_var.set("")
        self.correo_var.set("")
        self.numero_var.set("")
        self.rut_var.set("")

    def buscar_huesped(self):
        criterio = self.buscar_var.get().lower()
        for item in self.huespedes_table.get_children():
            valores = self.huespedes_table.item(item, 'values')
            if any(criterio in str(valor).lower() for valor in valores):
                self.huespedes_table.selection_set(item)
                self.huespedes_table.see(item)
            else:
                self.huespedes_table.selection_remove(item)

    def cargar_huespedes(self):
        for item in self.huespedes_table.get_children():
            self.huespedes_table.delete(item)
        huespedes = self.dao.cargar_huespedes()
        if huespedes:
            for huesped in huespedes:
                self.huespedes_table.insert('', tk.END, values=(
                    huesped['id_huesped'],
                    huesped['nombre'],
                    huesped['apellido1'],
                    huesped['apellido2'],
                    huesped['correo'],
                    huesped['numero'],
                    huesped['rut']
                ))
                
    def agregar_huesped(self):
        nombre = self.nombre_var.get()
        apellido1 = self.apellido1_var.get()
        apellido2 = self.apellido2_var.get()
        correo = self.correo_var.get()
        numero = self.numero_var.get()
        rut = self.rut_var.get()
        if not nombre or not apellido1 or not correo:
            messagebox.showerror("Error", "Por favor, complete todos los campos obligatorios.")
            return
        # Validación del campo Nombre
        if not nombre.isalpha():
            messagebox.showerror("Error de validación", "El nombre solo debe contener letras.")
            return False

        # Validación del campo Primer Apellido
        if not apellido1.isalpha():
            messagebox.showerror("Error de validación", "El primer apellido solo debe contener letras.")
            return False

        # Validación del campo Segundo Apellido
        if not apellido2.isalpha():
            messagebox.showerror("Error de validación", "El segundo apellido solo debe contener letras.")
            return False

        # Validación del campo Correo
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, correo):
            messagebox.showerror("Error de validación", "El correo electrónico no es válido.")
            return False

        # Validación del campo Número de Teléfono
        phone_regex = r'^\+?\d{10,15}$'
        if not re.match(phone_regex, numero):
            messagebox.showerror("Error de validación", "El número de teléfono no es válido.")
            return False

        # Validación del campo RUT
        rut_regex = r'^\d{1,8}-[\dkK]$'
        if not re.match(rut_regex, rut):
            messagebox.showerror("Error de validación", "El RUT no es válido.")
            return False

            pass
        self.dao.agregar_huesped(nombre, apellido1, apellido2, correo, numero, rut)
        self.cargar_huespedes()
        self.limpiar_datos()
        messagebox.showinfo("Éxito", "Huésped agregado exitosamente.")

    def modificar_huesped(self):
        id_huesped = self.id_huesped_var.get()
        nombre = self.nombre_var.get()
        apellido1 = self.apellido1_var.get()
        apellido2 = self.apellido2_var.get()
        correo = self.correo_var.get()
        numero = self.numero_var.get()
        rut = self.rut_var.get()

        # Validación del campo Nombre
        if not nombre.isalpha():
            messagebox.showerror("Error de validación", "El nombre solo debe contener letras.")
            return False

        # Validación del campo Primer Apellido
        if not apellido1.isalpha():
            messagebox.showerror("Error de validación", "El primer apellido solo debe contener letras.")
            return False

        # Validación del campo Segundo Apellido
        if not apellido2.isalpha():
            messagebox.showerror("Error de validación", "El segundo apellido solo debe contener letras.")
            return False

        # Validación del campo Correo
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, correo):
            messagebox.showerror("Error de validación", "El correo electrónico no es válido.")
            return False

        # Validación del campo Número de Teléfono
        phone_regex = r'^\+?\d{10,15}$'
        if not re.match(phone_regex, numero):
            messagebox.showerror("Error de validación", "El número de teléfono no es válido.")
            return False

        # Validación del campo RUT
        rut_regex = r'^\d{1,8}-[\dkK]$'
        if not re.match(rut_regex, rut):
            messagebox.showerror("Error de validación", "El RUT no es válido.")
            return False

        if not id_huesped or not nombre or not apellido1 or not correo:
            messagebox.showerror("Error", "Por favor, complete todos los campos obligatorios.")
            return
        self.dao.modificar_huesped(id_huesped,nombre, apellido1, apellido2, correo, numero, rut)
        self.cargar_huespedes()
        self.limpiar_datos()
        messagebox.showinfo("Éxito", "Huésped modificado exitosamente.")

    def eliminar_huesped(self):
        id_huesped = self.id_huesped_var.get()
        if not id_huesped:
            messagebox.showerror("Error", "Por favor, seleccione un huésped para eliminar.")
            return
        self.dao.eliminar_huesped(id_huesped)
        self.cargar_huespedes()
        self.limpiar_datos()
        messagebox.showinfo("Éxito", "Huésped eliminado exitosamente.")

    def cargar_datos_seleccionados(self, event):
        item = self.huespedes_table.selection()[0]
        huesped = self.huespedes_table.item(item, 'values')
        self.id_huesped_var.set(huesped[0])
        self.nombre_var.set(huesped[1])
        self.apellido1_var.set(huesped[2])
        self.apellido2_var.set(huesped[3])
        self.correo_var.set(huesped[4])
        self.numero_var.set(huesped[5])
        self.rut_var.set(huesped[6])

    

