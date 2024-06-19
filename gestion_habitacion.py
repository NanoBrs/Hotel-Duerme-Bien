import tkinter as tk
from tkinter import ttk, messagebox
from database import Database  # Importa la clase Database desde tu archivo database.py
from PIL import Image, ImageTk

class HabitacionCRUD:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Habitaciones")
        self.root.geometry("1000x480")

        # Instancia de Database
        self.db = Database()
      
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
        form_frame = ttk.Frame(self.root, padding=(20, 10))
        form_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
          # Cargar la imagen de fondo
        self.bg_image = Image.open("img/Habitacion.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Crear un Label para la imagen de fondo
        self.bg_label = tk.Label(form_frame, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Campos de entrada
        # Primera columna
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

        self.cargar_tipos_habitacion()
        self.cargar_orientaciones()
        self.cargar_estados_habitacion()

        # Frame para la tabla de habitaciones

        table_frame = ttk.Frame(self.root)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        table_frame.place(x=5, y=250)
        self.habitaciones_table = ttk.Treeview(
            table_frame, 
            columns=('ID', 'Numero', 'Precio', 'Camas', 'Piso', 'Capacidad', 'Tipo', 'Orientacion', 'Estado'),
            show='headings',  # Para mostrar solo las cabeceras de las columnas
            height=8  # Número de filas visibles, puedes ajustarlo según tus necesidades
        )

        # Tabla de habitaciones
        #self.habitaciones_table = ttk.Treeview(table_frame, columns=('ID', 'Numero', 'Precio', 'Camas', 'Piso', 'Capacidad', 'Tipo', 'Orientacion', 'Estado'))
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

        self.habitaciones_table.pack(fill=tk.BOTH, expand=True)

        self.habitaciones_table.grid(row=0, column=0, padx=20, pady=20)  # Ajustar márgenes a tu preferencia
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.habitaciones_table.yview)
        self.habitaciones_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        # Cargar datos iniciales de la tabla
        self.cargar_habitaciones()

        self.habitaciones_table.bind("<Double-1>", self.cargar_datos_seleccionados) #Evento doble click que carga los datos en la tabla


    
    def cargar_estados_habitacion(self):
        query = "SELECT estado FROM estado_habitacion"
        estados = self.db.fetch_all(query)
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
        query = "SELECT tipo FROM tipo_habitacion"
        tipos = self.db.fetch_all(query)
        if tipos:
            self.tipo_habitacion_combo['values'] = [tipo['tipo'] for tipo in tipos]

    def cargar_orientaciones(self):
        query = "SELECT orientacion FROM orientacion"
        orientaciones = self.db.fetch_all(query)
        if orientaciones:
            self.orientacion_combo['values'] = [orientacion['orientacion'] for orientacion in orientaciones]

    def cargar_habitaciones(self):
        self.habitaciones_table.delete(*self.habitaciones_table.get_children())
        query = """
        SELECT 
            h.id_habitacion, 
            h.numero_habitacion, 
            h.precio_noche, 
            h.camas, 
            h.piso, 
            h.capacidad, 
            th.tipo, 
            o.orientacion, 
            eh.estado 
        FROM habitacion h
        JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
        JOIN orientacion o ON h.id_orientacion = o.id_orientacion
        JOIN estado_habitacion eh ON h.id_estado_habitacion = eh.id_estado_habitacion
        """
        habitaciones = self.db.fetch_all(query)
        if habitaciones:
            for habitacion in habitaciones:
                self.habitaciones_table.insert('', 'end', text='', values=(
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


        
    def cargar_datos_seleccionados(self, event):
        item = self.habitaciones_table.selection()[0]
        habitacion = self.habitaciones_table.item(item, 'values')
        
        self.id_habitacion_var.set(habitacion[0])  # ID de la habitación
        self.numero_habitacion_var.set(habitacion[1])  # Número de habitación
        self.precio_noche_var.set(habitacion[2])  # Precio por noche
        self.camas_var.set(habitacion[3])  # Camas
        self.piso_var.set(habitacion[4])  # Piso
        self.capacidad_var.set(habitacion[5])  # Capacidad
        self.tipo_habitacion_var.set(habitacion[6])  # Tipo de habitación
        self.orientacion_var.set(habitacion[7])  # Orientación
        self.estado_habitacion_var.set(habitacion[8])  # Estado de habitación

    def limpiar_campos(self):
        self.id_habitacion_var.set('')  # ID de la habitación
        self.numero_habitacion_var.set('')
        self.precio_noche_var.set(0.0)
        self.camas_var.set(0)
        self.piso_var.set(0)
        self.capacidad_var.set(0)
        self.tipo_habitacion_var.set('')
        self.orientacion_var.set('')
        self.estado_habitacion_var.set('')

    def agregar_habitacion(self):
        numero_habitacion = self.numero_habitacion_var.get()
        precio_noche = self.precio_noche_var.get()
        camas = self.camas_var.get()
        piso = self.piso_var.get()
        capacidad = self.capacidad_var.get()
        tipo_habitacion = self.tipo_habitacion_combo.get()
        orientacion = self.orientacion_combo.get()
        estado_habitacion = self.estado_habitacion_combo.get()

        if not (numero_habitacion and tipo_habitacion and orientacion and estado_habitacion):
            messagebox.showwarning("Campos requeridos", "Por favor complete los campos obligatorios.")
            return

        query = """
        INSERT INTO habitacion 
        (numero_habitacion, precio_noche, camas, piso, capacidad, id_tipo_habitacion, id_orientacion, id_estado_habitacion) 
        VALUES 
        (%s, %s, %s, %s, %s, 
        (SELECT id_tipo_habitacion FROM tipo_habitacion WHERE tipo = %s), 
        (SELECT id_orientacion FROM orientacion WHERE orientacion = %s), 
        (SELECT id_estado_habitacion FROM estado_habitacion WHERE estado = %s))
        """
        params = (numero_habitacion, precio_noche, camas, piso, capacidad, tipo_habitacion, orientacion, estado_habitacion)

        if self.db.execute_query(query, params):
            messagebox.showinfo("Habitación agregada", "La habitación se agregó correctamente.")
            self.cargar_habitaciones()
            self.limpiar_campos()

    def modificar_habitacion(self):
        numero_habitacion = self.numero_habitacion_var.get()
        precio_noche = self.precio_noche_var.get()
        camas = self.camas_var.get()
        piso = self.piso_var.get()
        capacidad = self.capacidad_var.get()
        tipo_habitacion = self.tipo_habitacion_combo.get()
        orientacion = self.orientacion_combo.get()
        estado_habitacion = self.estado_habitacion_combo.get()

        if not (numero_habitacion and tipo_habitacion and orientacion and estado_habitacion):
            messagebox.showwarning("Campos requeridos", "Por favor complete los campos obligatorios.")
            return

        query = """
        UPDATE habitacion 
        SET 
            precio_noche = %s, 
            camas = %s, 
            piso = %s, 
            capacidad = %s, 
            id_tipo_habitacion = (SELECT id_tipo_habitacion FROM tipo_habitacion WHERE tipo = %s), 
            id_orientacion = (SELECT id_orientacion FROM orientacion WHERE orientacion = %s), 
            id_estado_habitacion = (SELECT id_estado_habitacion FROM estado_habitacion WHERE estado = %s)
        WHERE numero_habitacion = %s
        """
        params = (precio_noche, camas, piso, capacidad, tipo_habitacion, orientacion, estado_habitacion, numero_habitacion)

        if self.db.execute_query(query, params):
            messagebox.showinfo("Habitación modificada", "La habitación se modificó correctamente.")
            self.cargar_habitaciones()
            self.limpiar_campos()

    def eliminar_habitacion(self):
        numero_habitacion = self.numero_habitacion_var.get()

        if not numero_habitacion:
            messagebox.showwarning("Campo requerido", "Por favor ingrese el número de habitación para eliminar.")
            return

        query = "DELETE FROM habitacion WHERE numero_habitacion = %s"
        params = (numero_habitacion,)

        if self.db.execute_query(query, params):
            messagebox.showinfo("Habitación eliminada", "La habitación se eliminó correctamente.")
            self.cargar_habitaciones()
            self.limpiar_campos()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("100x800")  # Ancho de 800 píxeles y alto de 600 píxeles
    app = HabitacionCRUD(root)
    root.mainloop()
