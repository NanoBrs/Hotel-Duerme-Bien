import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from database import Database

# Clase principal de la aplicacion
class HabitacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Habitacion")  # Titulo de la ventana
        self.root.geometry("1280x720")  # Tamano de la ventana
        
        self.db = Database()  # Instancia de la base de datos
        self.db.connect_to_db()  # Conexion a la base de datos
        
        self.id_habitacion_buscar = None  # Variable para buscar por ID de habitacion
        self.current_image_index = 0  # Indice de la imagen actual
        self.images = ["habitacion1.png", "habitacion2.png", "habitacion3.png"]  # Lista de imagenes
        
        self.habitaciones = []  # Lista para almacenar datos de las habitaciones
        self.current_habitacion = 0  # Indice de la habitacion actual
        
        self.setup_ui()  # Metodo para configurar la interfaz de usuario
        self.cargar_datos_habitacion()  # Metodo para cargar datos de la habitacion
    
    def setup_ui(self):
        # Configurar el lienzo para mostrar las imagenes
        self.canvas = tk.Canvas(self.root, width=400, height=300)
        self.canvas.place(x=50, y=50)
        
        # Cargar y redimensionar la imagen inicial
        self.img = Image.open(self.images[self.current_image_index])
        self.img = self.img.resize((400, 300), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Boton para mostrar la imagen anterior
        self.prev_button = ttk.Button(self.root, text="<", command=self.prev_image)
        self.prev_button.place(x=50, y=370)
        
        # Boton para mostrar la imagen siguiente
        self.next_button = ttk.Button(self.root, text=">", command=self.next_image)
        self.next_button.place(x=350, y=370)
        
        # Etiqueta para mostrar la informacion de la habitacion
        self.info_label = ttk.Label(self.root, text="")
        self.info_label.place(x=500, y=50)

        # Boton para realizar la reserva
        self.reservar_button = ttk.Button(self.root, text="Realizar Reserva", command=self.realizar_reserva)
        self.reservar_button.place(x=500, y=400)
    
    def cargar_datos_habitacion(self):
        # Cargar datos de la habitacion segun el ID
        if self.id_habitacion_buscar is not None:
            self.habitaciones = self.db.cargar_habitacion_por_id(self.id_habitacion_buscar)
        else:
            self.habitaciones = self.db.cargar_habitacion_por_id(1) 

        # Si se encuentran datos de la habitacion, mostrarlos
        if self.habitaciones:
            habitacion = self.habitaciones[0]
            info = (
                f"Tipo de habitacion: {habitacion['tipo']}\n"
                f"Camas: {habitacion['camas']}\n"
                f"Piso: {habitacion['piso']}\n"
                f"Numero: {habitacion['numero_habitacion']}\n"
                f"Precio noche: {habitacion['precio_noche']}\n"
                f"Orientacion: {habitacion['orientacion']}\n"
                f"Cantidad maxima de personas: {habitacion['capacidad']}"
            )
            self.info_label.config(text=info)
        else:
            self.info_label.config(text="No se encontro la habitacion")
    
    # Metodo para mostrar la imagen anterior
    def prev_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.images)
        self.update_image()
    
    # Metodo para mostrar la imagen siguiente
    def next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.update_image()
    
    # Metodo para actualizar la imagen mostrada
    def update_image(self):
        self.img = Image.open(self.images[self.current_image_index])
        self.img = self.img.resize((400, 300), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
    
    # Metodo para realizar la reserva (solo imprime un mensaje en consola)
    def realizar_reserva(self):
        print("Reserva realizada")

# Funcion principal para ejecutar la aplicacion
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitacionApp(root)
    root.mainloop()
