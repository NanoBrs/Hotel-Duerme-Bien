import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, date
from DAO.DAO_reserva import Database_reserva

USUARIO = 1
Selecionar_habitacion_numero = 0
capacidad_restante = 0
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
        self.total_personas = 0 

        # Agregar imagen de fondo
        self.background_image = tk.PhotoImage(file="img/MENU2.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Frame para el formulario de ingreso y edicion
        form_frame = ttk.Frame(self, padding=(20, 10))
        form_frame.place(x=11.4, y=84.6, width=975.8, height=600)

        # Llamar al create para ver la ventana
        self.generar_ventana(form_frame)

        #--------------------------------------------------------- MENU -----------------------------------------------------------------
        # Configuracion de estilos
        style = ttk.Style()
        style.configure("rounded.TButton", borderwidth=2, relief="solid", background="white", padding=10, font=('Helvetica', 12))
        style.map("rounded.TButton", background=[('active', 'lightgray')])

        # Boton Gestionar Habitaciones
        self.boton_gestionar_habitaciones = ttk.Button(self, text="HABITACIONES", command=self.mostrar_gestion_habitaciones, style="rounded.TButton")
        self.boton_gestionar_habitaciones.place(x=1055, y=266, width=165, height=45)

        # Boton Gestionar Huespedes
        self.boton_gestionar_huespedes = ttk.Button(self, text="HUESPEDES", command=self.mostrar_gestion_huespedes, style="rounded.TButton")
        self.boton_gestionar_huespedes.place(x=1055, y=366, width=165, height=45)

        # Boton Gestionar Reservas
        self.boton_gestionar_reservas = ttk.Button(self, text="RESERVAS", command=self.mostrar_gestion_reservas, style="rounded.TButton")
        self.boton_gestionar_reservas.place(x=1055, y=466, width=165, height=45)

        # Boton Cerrar Sesion
        self.boton_cerrar_sesion = ttk.Button(self, text="CERRAR SESION", command=self.cerrar_sesion, style="rounded.TButton")
        self.boton_cerrar_sesion.place(x=1055, y=566, width=165, height=45)

    def mostrar_gestion_habitaciones(self):
        self.controlador.mostrar_frame("GestionHabitaciones")

    def mostrar_gestion_huespedes(self):
        self.controlador.mostrar_frame("GestionHuespedes")

    def mostrar_gestion_reservas(self):
        self.controlador.mostrar_frame("GestionReservas")

    def cerrar_sesion(self):
        print("Sesion cerrada exitosamente.")
        messagebox.showinfo("Cerrar Sesion", "Sesion cerrada exitosamente.")
        self.controlador.mostrar_frame("Login")

    def volver_menu_encargado(self):
        self.controlador.mostrar_frame("VentanaEncargado")
        #--------------------------------------------------------- FIN MENU -----------------------------------------------------------------

    def generar_ventana(self, parent):
        ttk.Label(parent, text="GESTION DE RESERVAS").place(x=5, y=10)
        
        tk.Label(parent, text="RUT Huesped responsable").place(x=5, y=50)
        self.rut_huesped_entry = tk.Entry(parent)
        self.rut_huesped_entry.place(x=185, y=50, width=150)
        self.button_verificar = tk.Button(parent, text="Verificar RUT", command=self.verificar_rut)
        self.button_verificar.place(x=345, y=47, width=100)

        tk.Label(parent, text="Entrada").place(x=5, y=90)
        self.cal_entrada = Calendar(parent, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_entrada.place(x=5, y=120, width=260, height=160)
        
        tk.Label(parent, text="Salida").place(x=315, y=90)
        self.cal_salida = Calendar(parent, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_salida.place(x=315, y=120, width=260, height=160)
        
        tk.Label(parent, text="Cantidad de Adultos").place(x=5, y=330)
        self.adultos_spin = tk.Spinbox(parent, from_=1, to=10)
        self.adultos_spin.place(x=145, y=330, width=50)
        
        tk.Label(parent, text="Cantidad de Niños").place(x=255, y=330)
        self.ninos_spin = tk.Spinbox(parent, from_=0, to=10)
        self.ninos_spin.place(x=355, y=330, width=50)

        habitacion_1 = tk.Label(parent, text="Habitacion 1 seleccionada")
        self.id_habitacion_entry_1 = tk.Entry(parent, state='readonly')

        habitacion_2 = tk.Label(parent, text="Habitacion 2 seleccionada")
        self.id_habitacion_entry_2 = tk.Entry(parent, state='readonly')


        def ocultar_habitacion_1():
            habitacion_1.place_forget()
            self.id_habitacion_entry_1.place_forget()

        def ocultar_habitacion_1():
            habitacion_1.place_forget()
            self.id_habitacion_entry_1.place_forget()

        def mostrar_habitacion_1():
            global Selecionar_habitacion_numero
            Selecionar_habitacion_numero = 1
            print(f"1:{Selecionar_habitacion_numero}")
            ocultar_habitacion_2()
            habitacion_1.place(x=20, y=370)
            self.id_habitacion_entry_1.place(x=165, y=370, width=150)
            btn_2.place(x=5, y=370)
            btn_1.place_forget()

        def ocultar_habitacion_2():
            habitacion_2.place_forget()
            self.id_habitacion_entry_2.place_forget()

        def mostrar_habitacion_2():
            global Selecionar_habitacion_numero
            Selecionar_habitacion_numero = 2
            print(f"2:{Selecionar_habitacion_numero}")
            ocultar_habitacion_1()
            habitacion_2.place(x=20, y=370)
            self.id_habitacion_entry_2.place(x=165, y=370, width=150)
            btn_1.place(x=5, y=370)
            btn_2.place_forget()
            habitacion_seleccionada = self.id_habitacion_entry_1.get()
            if habitacion_seleccionada:
                habitacion_id = habitacion_seleccionada.split(",")[0].split(":")[1].strip()
                habitacion = self.db.cargar_capacidad_habitacion_por_id(habitacion_id)[0]
                capacidad_restante = total_personas - habitacion['capacidad']
                if capacidad_restante < 0:
                    capacidad_restante = 0
            else:
                capacidad_restante = total_personas
            self.buscar_habitaciones()

        btn_1 = tk.Button(parent, text="1", command=mostrar_habitacion_1)
        btn_2 = tk.Button(parent, text="2", command=mostrar_habitacion_2)
        mostrar_habitacion_1()

        self.label_tipo_habitacion = tk.Label(parent, text="Tipo de Habitacion:")
        self.label_tipo_habitacion.place(x=5, y=400)
        self.combo_tipo_habitacion = ttk.Combobox(parent)
        self.combo_tipo_habitacion.place(x=145, y=400, width=150)
        self.cargar_tipos_habitacion()

        tk.Button(parent, text="Reservar", command=self.registrar_reserva).place(x=320, y=365, width=100)

        # Boton Buscar Habitaciones
        tk.Button(parent, text="Buscar Habitaciones", command=self.buscar_habitaciones).place(x=435, y=365, width=150)

        # Tabla para mostrar las reservas
        self.tree = ttk.Treeview(parent, columns=("ID reserva", "Fecha de Llegada", "Fecha de Salida", "Tipo de Habitacion", "Precio Total"),height=10, show="headings")
        self.tree.heading("ID reserva", text="ID reserva")
        self.tree.heading("Fecha de Llegada", text="Fecha de Llegada")
        self.tree.heading("Fecha de Salida", text="Fecha de Salida")
        self.tree.heading("Tipo de Habitacion", text="Tipo de Habitacion")
        self.tree.heading("Precio Total", text="Precio Total")
        
        #columnas
        self.tree.column('ID reserva', width=30)
        self.tree.column('Fecha de Llegada', width=60)
        self.tree.column('Fecha de Salida', width=60)
        self.tree.column('Tipo de Habitacion', width=80)
        self.tree.column('Precio Total', width=50)
        self.tree.place(x=5, y=430, width=500, height=150)  # Ajustar la posicion y tamaño de la tabla
        # Cargar las reservas existentes
        self.cargar_reservas()

        # Tabla para mostrar las habitaciones
        self.habitaciones_table = ttk.Treeview(
            parent,
            columns=('ID', 'Numero', 'Precio', 'Camas', 'Piso', 'Capacidad', 'Tipo', 'Orientacion', 'Estado'),
            show='headings',  # Para mostrar solo las cabeceras de las columnas
            height=20  # Numero de filas visibles, puedes ajustarlo segun tus necesidades
        )
        self.habitaciones_table.heading('ID', text='ID')
        self.habitaciones_table.heading('Numero', text='Numero de Habitacion')
        self.habitaciones_table.heading('Precio', text='Precio por Noche')
        self.habitaciones_table.heading('Camas', text='Camas')
        self.habitaciones_table.heading('Piso', text='Piso')
        self.habitaciones_table.heading('Capacidad', text='Capacidad')
        self.habitaciones_table.heading('Tipo', text='Tipo de Habitacion')
        self.habitaciones_table.heading('Orientacion', text='Orientacion')
        self.habitaciones_table.heading('Estado', text='Estado')
        #columnas
        self.habitaciones_table.column('ID', width=30)
        self.habitaciones_table.column('Numero', width=135)
        self.habitaciones_table.column('Precio', width=100)
        self.habitaciones_table.column('Camas', width=50)
        self.habitaciones_table.column('Piso', width=50)
        self.habitaciones_table.column('Capacidad', width=80)
        self.habitaciones_table.column('Tipo', width=105)
        self.habitaciones_table.column('Orientacion', width=72)
        self.habitaciones_table.column('Estado', width=80)

        self.habitaciones_table.place(x=625, y=120, width=300, height=200)  # Ajustar la posicion y tamaño de la tabla

        scrollbar_horizontal = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.habitaciones_table.xview)
        self.habitaciones_table.configure(xscroll=scrollbar_horizontal.set)
        scrollbar_horizontal.place(x=625, y=305, width=300)

        # Vincular el evento de doble clic
        self.habitaciones_table.bind("<Double-1>", self.cargar_datos_seleccionados)


    def cargar_reservas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.db.cargar_reservas()
        for row in rows:
            self.tree.insert("", "end", values=(row['id_reserva'], row['fecha_llegada'], row['fecha_salida'], row['tipo_habitacion'], row['precio_total'], row['estado_habitacion']))

    def cargar_tipos_habitacion(self):
        rows = self.db.cargar_tipos_habitacion()
        tipos = {row['id_tipo_habitacion']: f"{row['tipo']} - Maximo {row['cantidad_maxima']} personas" for row in rows}
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
                messagebox.showinfo("Exito", f"El RUT ingresado es valido.\nNombre: {nombre} \nApellido: {apellido}")
            else:
                messagebox.showerror("Error", "El RUT ingresado no es valido.")
        except Exception as e:
            messagebox.showerror("Error", f"Algo salio mal: {e}")

    def registrar_reserva(self):
        try:
            id_usuario = USUARIO
            rut_huesped = self.rut_huesped_entry.get()
            fecha_entrada = self.cal_entrada.get_date()
            fecha_salida = self.cal_salida.get_date()
            habitacion_seleccionada = self.id_habitacion_entry_1.get()
            habitacion_seleccionada_2 = self.id_habitacion_entry_2.get()
            print(f"1:{habitacion_seleccionada}")
            print(f"2:{habitacion_seleccionada_2}")
            adultos = int(self.adultos_spin.get())
            ninos = int(self.ninos_spin.get())
            total_personas = adultos + ninos
            print(total_personas)

            if not rut_huesped or not fecha_entrada or not fecha_salida or not habitacion_seleccionada:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            id_huesped = self.db.obtener_id_por_rut(rut_huesped)
            if not id_huesped:
                messagebox.showerror("Error", "El RUT ingresado es valido.")
                return

            # Convertir fechas de string a objetos date
            fecha_entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d').date()
            fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d').date()

            if fecha_salida <= fecha_entrada:
                messagebox.showerror("Error", "La fecha de salida debe ser despues de la fecha de entrada.")
                return
            noches = (fecha_salida - fecha_entrada).days
            precio_total = 0

            # Verificar la capacidad de la habitacion seleccionada
            if habitacion_seleccionada_2 == "":
                habitacion_id = habitacion_seleccionada.split(",")[0].split(":")[1].strip()
                habitacion = self.db.cargar_capacidad_habitacion_por_id(habitacion_id)[0]

                if total_personas > habitacion['capacidad']:
                    messagebox.showerror("Error", f"La cantidad de personas ({total_personas}) supera la capacidad de la habitacion ({habitacion['capacidad']})\nSelecciona otra habitacion mas.")
                    return

            habitaciones_id = []
            capacidades = []

            if habitacion_seleccionada:
                habitacion_id = habitacion_seleccionada.split(",")[0].split(":")[1].strip()
                habitaciones_id.append(habitacion_id)
                habitacion = self.db.cargar_capacidad_habitacion_por_id(habitacion_id)[0]
                capacidades.append(habitacion['capacidad'])

            if habitacion_seleccionada_2:
                habitacion_id_2 = habitacion_seleccionada_2.split(",")[0].split(":")[1].strip()
                habitaciones_id.append(habitacion_id_2)
                habitacion_2 = self.db.cargar_capacidad_habitacion_por_id(habitacion_id_2)[0]
                capacidades.append(habitacion_2['capacidad'])

            capacidad_total = sum(capacidades)

            if total_personas > capacidad_total:
                messagebox.showerror("Error", f"La cantidad de personas ({total_personas}) supera la capacidad combinada de las habitaciones ({capacidad_total}).")
                return

            # Calcular el precio total de la reserva
            for hab in self.habitaciones_seleccionadas:
                habitacion_1 = self.db.cargar_habitacion_por_id(hab['id'])[0]
                precio_total += habitacion_1['precio_noche'] * noches
            print(precio_total)

            # Insertar la reserva
            id_reserva = self.db.insert_reserva(fecha_entrada, fecha_salida, id_usuario, precio_total)

            # Insertar detalle de la reserva
            hora_actual = datetime.now().time().strftime('%H:%M:%S')
            id_detalle_reserva = self.db.insert_detalle_reserva(id_reserva, habitacion_id, hora_actual)
            if habitacion_seleccionada_2 != "":
                habitacion_id_2 = habitacion_seleccionada_2.split(",")[0].split(":")[1].strip()
                id_detalle_reserva = self.db.insert_detalle_reserva(id_reserva, habitacion_id_2, hora_actual)

            # Insertar detalle del huesped
            self.db.insert_detalle_huesped(id_reserva, id_huesped, id_detalle_reserva)

            # Actualizar el estado de la habitacion
            self.db.actualizar_estado_habitacion(habitacion_id, 'Ocupada')
            if habitacion_seleccionada_2 != "":
                self.db.actualizar_estado_habitacion(habitacion_id_2, 'Ocupada')
            self.cargar_reservas()
            self.limpiar_inputs()
            messagebox.showinfo("Reserva Registrada", "La reserva ha sido registrada exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

    def buscar_habitaciones(self):
        try:
            fecha_entrada = self.cal_entrada.get_date()
            fecha_salida = self.cal_salida.get_date()
            if fecha_salida <= fecha_entrada:
                messagebox.showerror("Error", "La fecha de salida debe ser despues a la fecha de entrada.")
                return
            tipo_habitacion = self.combo_tipo_habitacion.get()
            if not tipo_habitacion:
                messagebox.showerror("Error", "Por favor, seleccione un tipo de habitacion.")
                return
            # Obtener el ID del tipo de habitacionf
            tipo_habitacion_id = [k for k, v in self.tipo_habitacion_dict.items() if v == tipo_habitacion][0]

            # Limpiar tabla antes de buscar
            for row in self.habitaciones_table.get_children():
                self.habitaciones_table.delete(row)

            # Buscar habitaciones disponibles
            habitaciones = self.db.buscar_habitaciones_disponibles(fecha_entrada, fecha_salida, tipo_habitacion_id)

            if Selecionar_habitacion_numero == 2 and capacidad_restante > 0:
                habitaciones = [hab for hab in habitaciones if hab['capacidad'] >= capacidad_restante]
            # Imprimir las habitaciones para depuracion
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
                messagebox.showinfo("Habitaciones no encontradas", "No hay habitaciones disponibles para las fechas seleccionadas y el tipo de habitacion.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

    def cargar_datos_seleccionados(self, event):
        selected_item = self.habitaciones_table.selection()[0]
        habitacion_id = self.habitaciones_table.item(selected_item, 'values')[0]
        numero_habitacion = self.habitaciones_table.item(selected_item, 'values')[1]
        self.habitaciones_seleccionadas.append({'id': habitacion_id, 'numero': numero_habitacion})
        if Selecionar_habitacion_numero == 1:
            self.id_habitacion_entry_1.config(state='normal')
            self.id_habitacion_entry_1.delete(0, tk.END)
            self.id_habitacion_entry_1.insert(0, f"ID: {habitacion_id}  Numero: {numero_habitacion}")
            self.id_habitacion_entry_1.config(state='readonly')
        elif Selecionar_habitacion_numero == 2:
            self.id_habitacion_entry_2.config(state='normal')
            self.id_habitacion_entry_2.delete(0, tk.END)
            self.id_habitacion_entry_2.insert(0, f"ID: {habitacion_id}  Numero: {numero_habitacion}")
            self.id_habitacion_entry_2.config(state='readonly')

    def limpiar_inputs(self):
        self.rut_huesped_entry.delete(0, tk.END)
        self.adultos_spin.delete(0, tk.END)
        self.adultos_spin.insert(0, 1)
        self.ninos_spin.delete(0, tk.END)
        self.ninos_spin.insert(0, 0)
        self.id_habitacion_entry_1.config(state='normal')
        self.id_habitacion_entry_1.delete(0, tk.END)
        self.id_habitacion_entry_1.config(state='readonly')
        self.id_habitacion_entry_2.config(state='normal')
        self.id_habitacion_entry_2.delete(0, tk.END)
        self.id_habitacion_entry_2.config(state='readonly')
        self.combo_tipo_habitacion.set('')
        for item in self.habitaciones_table.get_children():
            self.habitaciones_table.delete(item)

