import tkinter as tk
from tkinter import ttk

class GestionReservas(tk.Frame):
    def __init__(self, parent, controlador):
        tk.Frame.__init__(self, parent)
        self.controlador = controlador
        self.pack(fill="both", expand=True)

        # Variables
        self.id_reserva_var = tk.StringVar()
        self.id_cliente_var = tk.StringVar()
        self.id_habitacion_var = tk.StringVar()
        self.fecha_entrada_var = tk.StringVar()
        self.fecha_salida_var = tk.StringVar()
        self.buscar_var = tk.StringVar()

        # Frame del formulario
        form_frame = ttk.Frame(self, padding=(20, 10))
        form_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Campos de entrada
        ttk.Label(form_frame, text="ID de Reserva:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.id_reserva_var, state="readonly").grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="ID de Cliente:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.id_cliente_var).grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="ID de Habitación:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.id_habitacion_var).grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Fecha de Entrada:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.fecha_entrada_var).grid(row=3, column=1, pady=5)

        ttk.Label(form_frame, text="Fecha de Salida:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.fecha_salida_var).grid(row=4, column=1, pady=5)

        # Campo de búsqueda
        ttk.Label(form_frame, text="Buscar:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.buscar_var).grid(row=5, column=1, pady=5)
        ttk.Button(form_frame, text="Filtrar", command=self.buscar_reserva).grid(row=5, column=2, pady=5)
        ttk.Button(form_frame, text="Borrar Filtros", command=self.cargar_reservas).grid(row=5, column=3, pady=5)

        # Botones CRUD
        ttk.Button(form_frame, text="Agregar", command=self.agregar_reserva).grid(row=6, column=0, pady=10)
        ttk.Button(form_frame, text="Modificar", command=self.modificar_reserva).grid(row=6, column=1, pady=10)
        ttk.Button(form_frame, text="Eliminar", command=self.eliminar_reserva).grid(row=6, column=2, pady=10)

        # Frame de la tabla
        table_frame = ttk.Frame(self)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.reservas_table = ttk.Treeview(table_frame, columns=('ID', 'Cliente', 'Habitacion', 'Entrada', 'Salida'), show='headings', height=8)
        self.reservas_table.heading('ID', text='ID')
        self.reservas_table.heading('Cliente', text='ID Cliente')
        self.reservas_table.heading('Habitacion', text='ID Habitación')
        self.reservas_table.heading('Entrada', text='Fecha de Entrada')
        self.reservas_table.heading('Salida', text='Fecha de Salida')

        for col in self.reservas_table['columns']:
            self.reservas_table.column(col, width=100)

        self.reservas_table.pack(fill=tk.BOTH, expand=True)

        self.reservas_table.bind("<Double-1>", self.cargar_datos_seleccionados)

        self.cargar_reservas()

    def buscar_reserva(self):
        pass

    def cargar_reservas(self):
        pass

    def agregar_reserva(self):
        pass

    def modificar_reserva(self):
        pass

    def eliminar_reserva(self):
        pass

    def cargar_datos_seleccionados(self, event):
        pass
