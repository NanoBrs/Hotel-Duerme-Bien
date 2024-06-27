import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class VentanaReserva:
    def __init__(self, master):
        self.master = master
        self.master.title("Reserva de Habitaciones")
        self.master.geometry("1000x600")
        
        self.db = Database()
        
        #Variables para entradas 
        self.id_reserva_var = tk.StringVar()
        self.id_habitacion_var = tk.StringVar()
        self.id_cliente_var = tk.StringVar()
        self.fecha_entrada_var = tk.StringVar()
        self.fecha_salida_var = tk.StringVar()
        self.estado_var = tk.StringVar()
        self.buscar_var = tk.StringVar()

        #formulario de ingre y edicion (frame)
        form_frame = ttk.Frame(self.master, padding=(20, 10))
        form_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        #campos para la variable de entradas
        ttk.Label(form_frame, text="ID de Reserva:").place(x=5, y=40)
        ttk.Entry(form_frame, textvariable=self.id_reserva_var, state="readonly").place(x=150, y=40)

        ttk.Label(form_frame, text="ID de Habitación:").place(x=5, y=70)
        ttk.Entry(form_frame, textvariable=self.id_habitacion_var).place(x=150, y=70)

        ttk.Label(form_frame, text="ID de Cliente:").place(x=5, y=100)
        ttk.Entry(form_frame, textvariable=self.id_cliente_var).place(x=150, y=100)

        ttk.Label(form_frame, text="Fecha de Entrada:").place(x=5, y=130)
        ttk.Entry(form_frame, textvariable=self.fecha_entrada_var).place(x=150, y=130)

        ttk.Label(form_frame, text="Fecha de Salida:").place(x=5, y=160)
        ttk.Entry(form_frame, textvariable=self.fecha_salida_var).place(x=150, y=160)

        ttk.Label(form_frame, text="Estado:").place(x=5, y=190)
        self.estado_combo = ttk.Combobox(form_frame, textvariable=self.estado_var, state="readonly")
        self.estado_combo.place(x=150, y=190)

        ttk.Label(form_frame, text="BUSQUEDA:").place(x=5, y=220)
        ttk.Entry(form_frame, textvariable=self.buscar_var).place(x=5, y=240)

        ttk.Button(form_frame, text="Filtrar", command=self.buscar_reserva).place(x=155, y=240)
        ttk.Button(form_frame, text="Borrar Filtros", command=self.cargar_reservas).place(x=235, y=240)

        ttk.Button(form_frame, text="Agregar", command=self.agregar_reserva).place(x=355, y=160)
        ttk.Button(form_frame, text="Modificar", command=self.modificar_reserva).place(x=445, y=160)
        ttk.Button(form_frame, text="Eliminar", command=self.eliminar_reserva).place(x=535, y=160)

        self.cargar_estados_reserva()
        
        #cuadro para la tabla de reservas
        table_frame = ttk.Frame(self.master)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.reservas_table = ttk.Treeview(
            table_frame, 
            columns=('ID', 'ID Habitación', 'ID Cliente', 'Fecha Entrada', 'Fecha Salida', 'Estado'),
            show='headings',
            height=8
        )
        
        
        self.reservas_table.heading('ID', text='ID')
        self.reservas_table.heading('ID Habitación', text='ID de Habitación')
        self.reservas_table.heading('ID Cliente', text='ID de Cliente')
        self.reservas_table.heading('Fecha Entrada', text='Fecha de Entrada')
        self.reservas_table.heading('Fecha Salida', text='Fecha de Salida')
        self.reservas_table.heading('Estado', text='Estado')

        self.reservas_table.column('ID', width=50)
        self.reservas_table.column('ID Habitación', width=120)
        self.reservas_table.column('ID Cliente', width=100)
        self.reservas_table.column('Fecha Entrada', width=100)
        self.reservas_table.column('Fecha Salida', width=100)
        self.reservas_table.column('Estado', width=100)

        self.reservas_table.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.reservas_table.yview)
        self.reservas_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.cargar_reservas()
        self.reservas_table.bind("<Double-1>", self.cargar_datos_seleccionados)
        
        
        
                
        pass