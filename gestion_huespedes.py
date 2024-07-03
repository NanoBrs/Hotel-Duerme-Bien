import tkinter as tk
from tkinter import simpledialog, messagebox

class GestionHuespedes(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestion de Huéspedes")
        self.geometry("1580x600")
        
        # Frame principal
        main_frame = tk.Frame(self, padx = 10, pady = 10)
        main_frame.pack(fill = tk.BOTH, expand = True)
        
        # Barra de busqueda
        buscar_frame = tk.Frame(main_frame)
        buscar_frame.pack(fill = tk.X, pady = (0, 10))
        tk.Label(buscar_frame, text = "Buscar: ").pack(side = tk.LEFT)
        self.buscar = tk.Entry(buscar_frame, width = 40)
        self.buscar.pack(side = tk.LEFT, padx = (5, 10))
        tk.Button(buscar_frame, text = "Buscar", command = self.buscar_huesped).pack(side = tk.LEFT)

        # Filtro
        #filtro_frame = tk.Frame(main_frame)
        #filtro_frame.pack(fill = tk.X, pady = (0, 10)) 
        #tk.Label(filtro_frame, text = "Filtrar por:").pack(side = tk.LEFT) 
        #self.barra_filtro = tk.StringVar()
        #filtro_opcion = ...
        
        # Lista de huéspedes
        lista_frame = tk.Frame(main_frame)
        lista_frame.pack(fill=tk.BOTH, expand = True)
        
        self.lista = tk.Listbox(lista_frame, height = 15)
        self.lista.pack(fill = tk.BOTH, expand = True)
        encabezado = ["Nombre", "Apellido_1", "Apellido_2", "Telefono", "Correo Electronico", "RUT"]
        self.lista.insert(tk.END, " | ".join(encabezado))
        self.lista.insert(tk.END, "-" *91)
        
        #Inputs
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.campos = ["Nombre", "Apellido_1", "Apellido_2", "Telefono", "Correo Electronico", "RUT"]
        self.inputs = {}
        
        for i, campo in enumerate(self.campos):
            tk.Label(input_frame, text=campo).grid(row=i//3*2, column=i%3, sticky="w", padx=5, pady=2)
            self.inputs[campo] = tk.Entry(input_frame, width=20)
            self.inputs[campo].grid(row=i//3*2+1, column=i%3, sticky="ew", padx=5, pady=2)
        input_frame.grid_columnconfigure((0,1,2), weight=1)
        # Botones
        boton_frame = tk.Frame(main_frame)
        boton_frame.pack(fill = tk.X, pady = (10, 0))
        
        tk.Button(boton_frame, text = "Agregar Huésped", command = self.agregar_huesped).pack(side = tk.LEFT, padx = (0, 5))
        tk.Button(boton_frame, text = "Eliminar Huésped", command = self.eliminar_huesped).pack(side = tk.LEFT, padx = (0, 5))
        
        #self.cargar_datos()
        
    def buscar_huesped(self):
        busqueda = self.buscar.get().lower()
        for i in range(2, self.lista.size()):
            item = self.lista.get(i)
            if busqueda in item.lower():
                self.lista.selection_clear(0, tk.END)
                self.lista.selection_set(i)
                self.lista.see(i)
                return
    
    def agregar_huesped(self):
        nuevo_huesped = []
        for campo in self.campos:
            nuevo_huesped.append(self.inputs[campo].get())
            
        self.lista.insert(tk.END, " | ".join(nuevo_huesped))
        for entrada in self.inputs.values():
            entrada.delete(0, tk.END)

    def eliminar_huesped(self):
        eliminar = self.lista.curselection()
        if not eliminar:
            messagebox.showwarning("Eliminar Huésped", "AAAA")
            return
        indice = eliminar[0]
        if indice < 2:
            return
        if messagebox.askyesno("Eliminar Huésped", "¿Esta seguro de eliminar?"):
            self.lista.delete(indice)
    
    #def cargar_datos(self):
        #datos = [("Oscar", "Acevedo", "Sanchez", "89435058", "oscaracevedosanchez@gmail.com", "20921224-2")]
        #for dato in datos:
            #self.lista.insert(tk.END, " | ".join(dato))

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = GestionHuespedes(root)
    root.mainloop()