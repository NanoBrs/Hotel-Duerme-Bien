import tkinter as tk
from tkinter import ttk

class GestionClientes(tk.Frame):
    def __init__(self, parent, controlador):
        tk.Frame.__init__(self, parent)
        self.controlador = controlador
        self.pack(fill="both", expand=True)

 

        # Variables
        self.id_cliente_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.dni_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.buscar_var = tk.StringVar()

        # Frame del formulario
        form_frame = ttk.Frame(self, padding=(20, 10))
        form_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Campos de entrada
        ttk.Label(form_frame, text="ID de Cliente:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.id_cliente_var, state="readonly").grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.nombre_var).grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Apellido:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.apellido_var).grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="DNI:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.dni_var).grid(row=3, column=1, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.email_var).grid(row=4, column=1, pady=5)

        ttk.Label(form_frame, text="Teléfono:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.telefono_var).grid(row=5, column=1, pady=5)

        # Campo de búsqueda
        ttk.Label(form_frame, text="Buscar:").grid(row=6, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.buscar_var).grid(row=6, column=1, pady=5)
        ttk.Button(form_frame, text="Filtrar", command=self.buscar_cliente).grid(row=6, column=2, pady=5)
        ttk.Button(form_frame, text="Borrar Filtros", command=self.cargar_clientes).grid(row=6, column=3, pady=5)

        # Botones CRUD
        ttk.Button(form_frame, text="Agregar", command=self.agregar_cliente).grid(row=7, column=0, pady=10)
        ttk.Button(form_frame, text="Modificar", command=self.modificar_cliente).grid(row=7, column=1, pady=10)
        ttk.Button(form_frame, text="Eliminar", command=self.eliminar_cliente).grid(row=7, column=2, pady=10)

        # Frame de la tabla
        table_frame = ttk.Frame(self)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.clientes_table = ttk.Treeview(table_frame, columns=('ID', 'Nombre', 'Apellido', 'DNI', 'Email', 'Telefono'), show='headings', height=8)
        self.clientes_table.heading('ID', text='ID')
        self.clientes_table.heading('Nombre', text='Nombre')
        self.clientes_table.heading('Apellido', text='Apellido')
        self.clientes_table.heading('DNI', text='DNI')
        self.clientes_table.heading('Email', text='Email')
        self.clientes_table.heading('Telefono', text='Teléfono')

        for col in self.clientes_table['columns']:
            self.clientes_table.column(col, width=100)

        self.clientes_table.pack(fill=tk.BOTH, expand=True)

        self.clientes_table.bind("<Double-1>", self.cargar_datos_seleccionados)

        self.cargar_clientes()

    def buscar_cliente(self):
        pass

    def cargar_clientes(self):
        pass

    def agregar_cliente(self):
        pass

    def modificar_cliente(self):
        pass

    def eliminar_cliente(self):
        pass

    def cargar_datos_seleccionados(self, event):
        pass
