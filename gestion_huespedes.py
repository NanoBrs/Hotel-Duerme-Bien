import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
from DAOHuespedes import DAOHuespedes_Consultas

class GestionHuespedes(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestion de Huéspedes")
        self.geometry("1280x720")
        
        #Instancia de DAOHuespedes
        self.db = DAOHuespedes_Consultas() 
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self, padding = "10 10 10 10")
        main_frame.pack(fill = tk.BOTH, expand = True)
        
        #Inputs
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.campos = ["Nombre", "Apellido_1", "Apellido_2", "Telefono", "Correo Electronico", "RUT"]
        self.inputs = {}
        
        for i, campo in enumerate(self.campos):
            ttk.Label(input_frame, text=f"{campo}:").grid(row=i//2, column=i%2*2, sticky="e", padx=5, pady=5)
            self.inputs[campo] = ttk.Entry(input_frame)
            self.inputs[campo].grid(row=i//2, column=i%2*2+1, sticky="ew", padx=5, pady=5)
        
        # Botones
        boton_frame = ttk.Frame(input_frame)
        boton_frame.grid(row = 3, column = 0, columnspan = 4, sticky = "e", padx = 5, pady = 5)
        
        ttk.Button(boton_frame, text = "Agregar Huésped", command = self.agregar_huesped).pack(side = tk.LEFT, padx = (0, 5))
        ttk.Button(boton_frame, text = "Eliminar Huésped", command = self.eliminar_huesped).pack(side = tk.LEFT, padx = (0, 5))
        ttk.Button(boton_frame, text = "Limpiar Datos", command = self.limpiar_campos).pack(side = tk.LEFT, padx = 2)
        
        # Barra de busqueda
        buscar_frame = ttk.Frame(main_frame)
        buscar_frame.pack(fill = tk.X, pady = (0, 10))
        ttk.Label(buscar_frame, text = "Buscar: ").pack(side = tk.LEFT, padx = 5)
        self.buscar = ttk.Entry(buscar_frame, width = 40)
        self.buscar.pack(side = tk.LEFT, padx = 5)
        ttk.Button(buscar_frame, text = "Buscar", command = self.buscar_huesped).pack(side = tk.LEFT, padx = 5)
        
        # Lista de huéspedes
        self.tree = ttk.Treeview(main_frame, columns = ["ID"] + self.campos, show = 'headings')
        self.tree.heading("ID", text = "ID")
        self.tree.column("ID", width = 50)
        for col in self.campos:
            self.tree.heading(col, text = col)
            self.tree.column(col, width = 100)
        self.tree.pack(fill = tk.BOTH, expand = True)
        
        self.cargar_datos()
        
    def cargar_datos(self):
        huespedes = self.db.cargar_huespedes()
        for huesped in huespedes:
            self.tree.insert('', tk.END, values =  (huesped['id_huesped'], huesped['nombre'], huesped['apellido1'], 
                                                    huesped['apellido2'], huesped['correo'], 
                                                    huesped['numero'], huesped['rut']))
    
    def buscar_huesped(self):
        buscar = self.buscar.get().lower()
        for item in self.tree.get_children():
            valores = self.tree.item(item)['values']
            if any(buscar in str(valor).lower() for valor in valores):
                self.tree.selection_add(item)
            else:
                self.tree.selection_remove(item)
    
    def agregar_huesped(self):
        nuevo_huesped = []
        for campo in self.campos:
            nuevo_huesped.append(self.inputs[campo].get())
            
        self.tree.insert('', tk.END, values = nuevo_huesped)
        
        self.limpiar_campos()

    def eliminar_huesped(self):
        eliminar = self.tree.selection()
        if not eliminar:
            messagebox.showwarning("Eliminar Huésped", "Por favor, seleccione un huésped para eliminar")
            return
        if messagebox.askyesno("Eliminar Huésped", "¿Esta seguro de eliminar este huésped?"):
            for item in eliminar:
                self.tree.delete(item)

    def limpiar_campos(self):
        for entrada in self.inputs.values():
            entrada.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = GestionHuespedes(root)
    root.mainloop()