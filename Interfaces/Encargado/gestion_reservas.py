import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from DAO.DAO_reserva import Database_reserva

class GestionReservas(tk.Frame):
    def __init__(self, parent, controlador):
        tk.Frame.__init__(self, parent)
        self.controlador = controlador
        self.root = parent
        self.db = Database_reserva()
        
        self.fecha_entrada = None
        self.fecha_salida = None
        self.habitaciones_seleccionadas = []
        self.tipo_habitacion_seleccionada = None

        # Agregar imagen de fondo
        self.background_image = tk.PhotoImage(file="img/MENU2.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Frame para el formulario de ingreso y edición
        form_frame = ttk.Frame(self, padding=(20, 10))
        form_frame.place(x=11.4, y=84.6, width=975.8, height=600)

        # Llamar al create para ver la ventana
        self.generar_ventana(form_frame)

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

    def generar_ventana(self, parent):
        ttk.Label(parent, text="GESTIÓN DE RESERVAS").place(x=5, y=10)
        
        tk.Label(parent, text="RUT Huésped responsable").place(x=5, y=50)
        self.rut_huesped_entry = tk.Entry(parent)
        self.rut_huesped_entry.place(x=185, y=50, width=150)
        self.button_verificar = tk.Button(parent, text="Verificar RUT", command=self.verificar_rut)
        self.button_verificar.place(x=345, y=47, width=100)

        tk.Label(parent, text="Entrada").place(x=5, y=90)
        self.cal_entrada = Calendar(parent, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_entrada.place(x=5, y=120, width=300, height=200)
        
        tk.Label(parent, text="Salida").place(x=315, y=90)
        self.cal_salida = Calendar(parent, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_salida.place(x=315, y=120, width=300, height=200)
        
        tk.Label(parent, text="Cantidad de Adultos").place(x=5, y=330)
        self.adultos_spin = tk.Spinbox(parent, from_=1, to=10)
        self.adultos_spin.place(x=145, y=330, width=100)
        
        tk.Label(parent, text="Cantidad de Niños").place(x=255, y=330)
        self.ninos_spin = tk.Spinbox(parent, from_=0, to=10)
        self.ninos_spin.place(x=345, y=330, width=100)

        tk.Label(parent, text="ID Habitación").place(x=5, y=370)
        self.id_habitacion_entry = tk.Entry(parent, state='readonly')
        self.id_habitacion_entry.place(x=145, y=370, width=150)

        self.label_tipo_habitacion = tk.Label(parent, text="Tipo de Habitación:")
        self.label_tipo_habitacion.place(x=5, y=410)
        self.combo_tipo_habitacion = ttk.Combobox(parent)
        self.combo_tipo_habitacion.place(x=145, y=410, width=150)
        self.cargar_tipos_habitacion()

        tk.Button(parent, text="Reservar", command=self.registrar_reserva).place(x=200, y=450, width=100)

        # Botón Buscar Habitaciones
        tk.Button(parent, text="Buscar Habitaciones", command=self.buscar_habitaciones).place(x=315, y=450, width=150)

        # Tabla para mostrar las reservas
        self.tree = ttk.Treeview(parent, columns=("ID Usuario", "Fecha de Llegada", "Fecha de Salida", "Tipo de Habitación", "Precio Total"), show="headings")
        self.tree.heading("ID Usuario", text="ID Usuario")
        self.tree.heading("Fecha de Llegada", text="Fecha de Llegada")
        self.tree.heading("Fecha de Salida", text="Fecha de Salida")
        self.tree.heading("Tipo de Habitación", text="Tipo de Habitación")
        self.tree.heading("Precio Total", text="Precio Total")
        self.tree.place(x=5, y=500, width=950, height=90)

        # Cargar las reservas existentes
        self.cargar_reservas()

        # Tabla para mostrar las habitaciones
        self.habitaciones_table = ttk.Treeview(
            parent,
            columns=('ID', 'Numero', 'Precio', 'Camas', 'Piso', 'Capacidad', 'Tipo', 'Orientacion', 'Estado'),
            show='headings',  # Para mostrar solo las cabeceras de las columnas
            height=8  # Número de filas visibles, puedes ajustarlo según tus necesidades
        )
        self.habitaciones_table.heading('ID', text='ID')
        self.habitaciones_table.heading('Numero', text='Número de Habitación')
        self.habitaciones_table.heading('Precio', text='Precio por Noche')
        self.habitaciones_table.heading('Camas', text='Camas')
        self.habitaciones_table.heading('Piso', text='Piso')
        self.habitaciones_table.heading('Capacidad', text='Capacidad')
        self.habitaciones_table.heading('Tipo', text='Tipo de Habitación')
        self.habitaciones_table.heading('Orientacion', text='Orientación')
        self.habitaciones_table.heading('Estado', text='Estado')

        self.habitaciones_table.place(x=625, y=120, width=350, height=200)  # Ajustar la posición y tamaño de la tabla

        # Scrollbar para la tabla de habitaciones
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.habitaciones_table.yview)
        self.habitaciones_table.configure(yscroll=scrollbar.set)
        scrollbar.place(x=975, y=120, height=200)  # Ajustar la posición del scrollbar

    def cargar_reservas(self):
        rows = self.db.cargar_reservas()
        for row in rows:
            self.tree.insert("", "end", values=(row['id_reserva'], row['fecha_llegada'], row['fecha_salida'], row['tipo_habitacion'], row['precio_total'], row['estado_habitacion']))

    def cargar_tipos_habitacion(self):
        rows = self.db.cargar_tipos_habitacion()
        tipos = {row['id_tipo_habitacion']: f"{row['tipo']} - Máximo {row['cantidad_maxima']} personas" for row in rows}
        self.tipo_habitacion_dict = tipos
        self.combo_tipo_habitacion['values'] = list(tipos.values())

    def verificar_rut(self):
        rut_huesped = self.rut_huesped_entry.get()
        if not rut_huesped:
            messagebox.showerror("Error", "Por favor, ingrese un RUT.")
            return
        
        try:
            huesped_info = self.db.obtener_nombre_apellido_por_rut(rut_huesped)
            if huesped_info:
                nombre, apellido = huesped_info
                messagebox.showinfo("Éxito", f"El RUT ingresado es valido.\nNombre: {nombre} \nApellido: {apellido}")
            else:
                messagebox.showerror("Error", "El RUT ingresado no es valido.")
        except Exception as e:
            messagebox.showerror("Error", f"Algo salió mal: {e}")

    def registrar_reserva(self):
        try:
            rut_huesped = self.rut_huesped_entry.get()
            fecha_entrada = self.cal_entrada.get_date()
            fecha_salida = self.cal_salida.get_date()
            cant_adultos = self.adultos_spin.get()
            cant_ninos = self.ninos_spin.get()
            tipo_habitacion = self.combo_tipo_habitacion.get()
            tipo_habitacion_id = [k for k, v in self.tipo_habitacion_dict.items() if v == tipo_habitacion][0]
            
            reserva_exitosa = self.db.registrar_reserva(rut_huesped, fecha_entrada, fecha_salida, cant_adultos, cant_ninos, tipo_habitacion_id)
            
            if reserva_exitosa:
                messagebox.showinfo("Reserva Registrada", "La reserva ha sido registrada exitosamente.")
            else:
                messagebox.showerror("Error", "No se pudo registrar la reserva.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

    def buscar_habitaciones(self):
        try:
            fecha_entrada = self.cal_entrada.get_date()
            fecha_salida = self.cal_salida.get_date()
            tipo_habitacion = self.combo_tipo_habitacion.get()

            # Obtener el ID del tipo de habitación
            tipo_habitacion_id = [k for k, v in self.tipo_habitacion_dict.items() if v == tipo_habitacion][0]

            # Limpiar tabla antes de buscar
            for row in self.habitaciones_table.get_children():
                self.habitaciones_table.delete(row)

            # Buscar habitaciones disponibles
            habitaciones = self.db.buscar_habitaciones_disponibles(fecha_entrada, fecha_salida, tipo_habitacion_id)

            # Imprimir las habitaciones para depuración
            print("Habitaciones devueltas por la base de datos:", habitaciones)

            if habitaciones:
                for habitacion in habitaciones:
                    self.habitaciones_table.insert("", "end", values=(
                        habitacion['id_habitacion'], 
                        habitacion['numero_habitacion'], 
                        habitacion['precio_noche'], 
                        habitacion['camas'], 
                        habitacion['piso'], 
                        habitacion['capacidad'], 
                        habitacion['tipo'], 
                        habitacion['id_orientacion'], 
                        habitacion['estado']
                    ))
            else:
                messagebox.showinfo("Habitaciones no encontradas", "No hay habitaciones disponibles para las fechas seleccionadas y el tipo de habitación.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")


