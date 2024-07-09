import tkinter as tk
from tkinter import ttk, messagebox
from DAO.DAO_habitaciones import DAO_habitaciones  # Importa la clase DAO_habitaciones desde tu archivo DAO_habitaciones.py
from PIL import Image, ImageTk

class GestionHabitaciones(tk.Frame):
    def __init__(self, parent, controlador):
        tk.Frame.__init__(self, parent)
        self.controlador = controlador

        # Agregar imagen de fondo
        self.background_image = tk.PhotoImage(file="img/MENU2.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Instancia de DAO_habitaciones
        self.dao = DAO_habitaciones()

        # Variables para campos de entrada
        self.id_habitacion_var = tk.StringVar()
        self.numero_habitacion_var = tk.StringVar()
        self.precio_noche_var = tk.DoubleVar()
        self.camas_var = tk.IntVar()
        self.piso_var = tk.IntVar()
        self.capacidad_var = tk.IntVar()
        self.tipo_habitacion_var = tk.StringVar()
        self.orientacion_var = tk.StringVar()
        self.estado_habitacion_var = tk.StringVar()
        self.buscar_var = tk.StringVar()

        # Frame para el formulario de ingreso y edición
        form_frame = ttk.Frame(self, padding=(20, 10))
        form_frame.place(x=11.4, y=84.6, width=975.8, height=300)  # Ajustado para la mitad superior del área deseada

        # Campos de entrada
        # Primera columna
        ttk.Label(form_frame, text="GESTION DE HABITACIONES").place(x=5, y=10)
        ttk.Label(form_frame, text="ID de Habitación:").place(x=5, y=40)
        ttk.Entry(form_frame, textvariable=self.id_habitacion_var, state="readonly").place(x=150, y=40)

        ttk.Label(form_frame, text="Número de Habitación:").place(x=5, y=70)
        ttk.Entry(form_frame, textvariable=self.numero_habitacion_var).place(x=150, y=70)

        ttk.Label(form_frame, text="Precio por Noche:").place(x=5, y=100)
        ttk.Entry(form_frame, textvariable=self.precio_noche_var).place(x=150, y=100)

        ttk.Label(form_frame, text="Camas:").place(x=5, y=130)
        ttk.Entry(form_frame, textvariable=self.camas_var).place(x=150, y=130)

        ttk.Label(form_frame, text="Piso:").place(x=5, y=160)
        ttk.Entry(form_frame, textvariable=self.piso_var).place(x=150, y=160)

        # Segunda columna
        ttk.Label(form_frame, text="Capacidad:").place(x=355, y=40)
        ttk.Entry(form_frame, textvariable=self.capacidad_var).place(x=475, y=40)

        ttk.Label(form_frame, text="Tipo de Habitación:").place(x=355, y=70)
        self.tipo_habitacion_combo = ttk.Combobox(form_frame, textvariable=self.tipo_habitacion_var, state="readonly")
        self.tipo_habitacion_combo.place(x=475, y=70)

        ttk.Label(form_frame, text="Orientación:").place(x=355, y=100)
        self.orientacion_combo = ttk.Combobox(form_frame, textvariable=self.orientacion_var, state="readonly")
        self.orientacion_combo.place(x=475, y=100)

        ttk.Label(form_frame, text="Estado de Habitación:").place(x=355, y=130)
        self.estado_habitacion_combo = ttk.Combobox(form_frame, textvariable=self.estado_habitacion_var, state="readonly")
        self.estado_habitacion_combo.place(x=475, y=130)

        # Campo de búsqueda
        ttk.Label(form_frame, text="BUSQUEDA:").place(x=5, y=190)
        ttk.Entry(form_frame, textvariable=self.buscar_var).place(x=5, y=210)

        ttk.Button(form_frame, text="Filtrar", command=self.buscar_habitacion).place(x=155, y=210)
        ttk.Button(form_frame, text="Borrar Filtros", command=self.cargar_habitaciones).place(x=235, y=210)

        # Botones CRUD
        ttk.Button(form_frame, text="Agregar", command=self.agregar_habitacion).place(x=355, y=160)
        ttk.Button(form_frame, text="Modificar", command=self.modificar_habitacion).place(x=445, y=160)
        ttk.Button(form_frame, text="Eliminar", command=self.eliminar_habitacion).place(x=535, y=160)
        ttk.Button(form_frame, text="Limpiar Datos", command=self.limpiar_datos).place(x=625, y=160)
        # Frame para la tabla de habitaciones
        # Frame para la tabla de habitaciones
        table_frame = ttk.Frame(self, padding=(10, 5))
        table_frame.place(x=11.4, y=345.7, width=975.8, height=330)

        self.habitaciones_table = ttk.Treeview(
            table_frame,
            columns=('ID', 'Numero', 'Precio', 'Camas', 'Piso', 'Capacidad', 'Tipo', 'Orientacion', 'Estado'),
            show='headings',  # Para mostrar solo las cabeceras de las columnas
            height=8  # Número de filas visibles, puedes ajustarlo según tus necesidades
        )

        # Tabla de habitaciones
        self.habitaciones_table.heading('#0', text='')  # Dejamos el encabezado de la columna #0 vacío
        self.habitaciones_table.heading('ID', text='ID')
        self.habitaciones_table.heading('Numero', text='Número de Habitación')
        self.habitaciones_table.heading('Precio', text='Precio por Noche')
        self.habitaciones_table.heading('Camas', text='Camas')
        self.habitaciones_table.heading('Piso', text='Piso')
        self.habitaciones_table.heading('Capacidad', text='Capacidad')
        self.habitaciones_table.heading('Tipo', text='Tipo de Habitación')
        self.habitaciones_table.heading('Orientacion', text='Orientación')
        self.habitaciones_table.heading('Estado', text='Estado')

        self.habitaciones_table.column('#0', width=0, stretch=tk.NO)  # Configuramos la columna #0 para que no se muestre
        self.habitaciones_table.column('ID', width=50)
        self.habitaciones_table.column('Numero', width=120)
        self.habitaciones_table.column('Precio', width=100)
        self.habitaciones_table.column('Camas', width=50)
        self.habitaciones_table.column('Piso', width=50)
        self.habitaciones_table.column('Capacidad', width=70)
        self.habitaciones_table.column('Tipo', width=150)
        self.habitaciones_table.column('Orientacion', width=150)
        self.habitaciones_table.column('Estado', width=150)

        self.habitaciones_table.grid(row=0, column=0, padx=20, pady=20)  # Ajustar márgenes a tu preferencia
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.habitaciones_table.yview)
        self.habitaciones_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Cargar datos iniciales de la tabla
        self.cargar_habitaciones()
        
        self.cargar_tipos_habitacion()
        self.cargar_orientaciones()
        self.cargar_estados_habitacion()

        self.habitaciones_table.bind("<Double-1>", self.cargar_datos_seleccionados)  # Evento doble click que carga los datos en la tabla

#--------------------------------------------------------- MENU -----------------------------------------------------------------
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
        print("Sesión cerrada exitosamente.")
        messagebox.showinfo("Cerrar Sesion", "Sesión cerrada exitosamente.")
        self.controlador.mostrar_frame("Login")

    def volver_menu_encargado(self):
        self.controlador.mostrar_frame("VentanaEncargado")
#--------------------------------------------------------- FIN MENU -----------------------------------------------------------------
    def limpiar_datos(self):
            self.id_habitacion_var.set("")
            self.numero_habitacion_var.set("")
            self.precio_noche_var.set(0)
            self.camas_var.set(0)
            self.piso_var.set(0)
            self.capacidad_var.set(0)
            self.tipo_habitacion_var.set("")
            self.orientacion_var.set("")
            self.estado_habitacion_var.set("")


    def cargar_estados_habitacion(self):
        estados = self.dao.cargar_estados_habitacion()
        if estados:
            self.estado_habitacion_combo['values'] = [estado['estado'] for estado in estados]

    def buscar_habitacion(self):
        criterio = self.buscar_var.get().lower()
        for item in self.habitaciones_table.get_children():
            valores = self.habitaciones_table.item(item, 'values')
            if any(criterio in str(valor).lower() for valor in valores):
                self.habitaciones_table.see(item)
                self.habitaciones_table.selection_set(item)
            else:
                self.habitaciones_table.detach(item)

    def cargar_tipos_habitacion(self):
        tipos = self.dao.cargar_tipos_habitacion()
        if tipos:
            self.tipo_habitacion_combo['values'] = [tipo['tipo'] for tipo in tipos]

    def cargar_orientaciones(self):
        orientaciones = self.dao.cargar_orientaciones()
        if orientaciones:
            self.orientacion_combo['values'] = [orientacion['orientacion'] for orientacion in orientaciones]

    def cargar_habitaciones(self):
        for item in self.habitaciones_table.get_children():
            self.habitaciones_table.delete(item)
        habitaciones = self.dao.cargar_habitaciones()
        if habitaciones:
            for habitacion in habitaciones:
                self.habitaciones_table.insert('', tk.END, values=(
                    habitacion['id_habitacion'],
                    habitacion['numero_habitacion'],
                    habitacion['precio_noche'],
                    habitacion['camas'],
                    habitacion['piso'],
                    habitacion['capacidad'],
                    habitacion['tipo'],
                    habitacion['orientacion'],
                    habitacion['estado']
                ))

    def agregar_habitacion(self):
        if not self.id_habitacion_var.get():
            params = (
                self.numero_habitacion_var.get(),
                self.precio_noche_var.get(),
                self.camas_var.get(),
                self.piso_var.get(),
                self.capacidad_var.get(),
                self.tipo_habitacion_var.get(),
                self.orientacion_var.get(),
                self.estado_habitacion_var.get()
            )
            if not self.dao.validar_existencia_habitacion(self.id_habitacion_var.get()):
                self.dao.agregar_habitacion(params)
                self.cargar_habitaciones()
                self.limpiar_datos()
            else:
                messagebox.showerror("Error", "La habitación ya existe.")
        else:
            messagebox.showerror("Error", "El ID de la habitación no debe estar especificado para agregar.")
            self.id_habitacion_var.set("")

    def modificar_habitacion(self):
        params = (
            self.precio_noche_var.get(),
            self.camas_var.get(),
            self.piso_var.get(),
            self.capacidad_var.get(),
            self.tipo_habitacion_var.get(),
            self.orientacion_var.get(),
            self.estado_habitacion_var.get(),
            self.numero_habitacion_var.get(),
            self.id_habitacion_var.get()
        )
        
        self.dao.modificar_habitacion(params)
        self.cargar_habitaciones()
        self.limpiar_datos()

    def eliminar_habitacion(self):
        params = (self.id_habitacion_var.get(),)
        self.dao.eliminar_habitacion(params)
        self.cargar_habitaciones()

    def cargar_datos_seleccionados(self, event):
        selected_item = self.habitaciones_table.focus()
        if selected_item:
            item_data = self.habitaciones_table.item(selected_item)
            values = item_data['values']
            self.id_habitacion_var.set(values[0])
            self.numero_habitacion_var.set(values[1])
            self.precio_noche_var.set(values[2])
            self.camas_var.set(values[3])
            self.piso_var.set(values[4])
            self.capacidad_var.set(values[5])
            self.tipo_habitacion_var.set(values[6])
            self.orientacion_var.set(values[7])
            self.estado_habitacion_var.set(values[8])
