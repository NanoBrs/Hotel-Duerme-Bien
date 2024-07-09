import re
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
        self.huesped_seleccionado = None
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self, padding = "10 10 10 10")
        main_frame.pack(fill = tk.BOTH, expand = True)
        
        #Inputs
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.campos = ["Nombre", "Apellido_1", "Apellido_2", "Correo Electronico", "Telefono", "RUT"]
        self.inputs = {}
        
        for i, campo in enumerate(self.campos):
            ttk.Label(input_frame, text=f"{campo}:").grid(row=i//2, column=i%2*2, sticky="e", padx=5, pady=5)
            self.inputs[campo] = ttk.Entry(input_frame)
            self.inputs[campo].grid(row=i//2, column=i%2*2+1, sticky="ew", padx=5, pady=5)
        
        # Botones
        boton_frame = ttk.Frame(input_frame)
        boton_frame.grid(row = 3, column = 0, columnspan = 4, sticky = "e", padx = 5, pady = 5)
        
        ttk.Button(boton_frame, text = "Agregar Huésped", command = self.agregar_huesped).pack(side = tk.LEFT, padx = (0, 5))
        ttk.Button(boton_frame, text = "Modificar Datos", command = self.modificar_huesped).pack(side = tk.LEFT, padx = (0, 5))
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
        
        self.tree.bind("<Double-1>", self.huesped_select)
        
        self.cargar_datos()
        
    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        huespedes = self.db.cargar_huespedes()
        for huesped in huespedes:
            self.tree.insert('', tk.END, values =  (huesped['id_huesped'], huesped['nombre'], huesped['apellido1'], 
                                                    huesped['apellido2'], huesped['correo'], 
                                                    huesped['numero'], huesped['rut']))
    #Validaciones
    def validar_inputs(self):
        try:
            for campo, entrada in self.inputs.items():
                valor = entrada.get().strip()
                if not valor:
                    raise ValueError(f"El campo {campo} es obligatorio")
                if campo in ['Nombre', 'Apellido_1', 'Apellido_2']:
                    self.validar_nombre(campo, valor)
                elif campo == 'Correo Electronico':
                    self.validar_correo(valor)
                elif campo == 'Telefono':
                    self.validar_telefono(valor)
                elif campo == 'RUT':
                    self.validar_rut(valor)
            return True
        except Exception as e:
            messagebox.showerror("Error de validación", str(e))
            return False

    def validar_nombre(self, campo, valor):
        if len(valor) > 40:
            raise ValueError(f"{campo} debe tener máximo 40 caracteres")
        if not valor.replace(" ", "").isalpha():
            raise ValueError(f"{campo} solo debe contener letras y espacios")

    def validar_correo(self, valor):
        if len(valor) > 70:
            raise ValueError("Correo debe tener máximo 70 caracteres")
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", valor):
            raise ValueError("Correo inválido. Debe tener un formato válido (ejemplo@dominio.com)")

    def validar_telefono(self, valor):
        if len(valor) > 15:
            raise ValueError("Teléfono debe tener máximo 15 caracteres")
        if not valor.isdigit():
            raise ValueError("Teléfono debe contener solo dígitos")

    def validar_rut(self, valor):
        if len(valor) > 20:
            raise ValueError("RUT debe tener máximo 20 caracteres")
        if not re.match(r"^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$", valor):
            raise ValueError("RUT inválido. Formato esperado: 12.345.678-9")

    def buscar_huesped(self):
        buscar = self.buscar.get()
        resultado = self.db.buscar_huespedes(buscar)
        
        #Limpia la vista actual
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        #Muestra los resultados
        for huesped in resultado:
            self.tree.insert('', tk.END, values =  (huesped['id'], huesped['nombre'], huesped['apellido1'], 
                                                    huesped['apellido2'], huesped['correo'], 
                                                    huesped['numero'], huesped['rut']))
    
    def agregar_huesped(self):
        if self.validar_inputs():
            nuevo_huesped = [self.inputs[campo].get() for campo in self.campos]
            if self.db.agregar_huespedes(*nuevo_huesped):
                self.cargar_datos()
                self.limpiar_campos()
                messagebox.showinfo("Exito", "Huésped agregado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo agregar al huesped")

    def eliminar_huesped(self):
        eliminar = self.tree.selection()
        if not eliminar:
            messagebox.showwarning("Eliminar Huésped", "Por favor, seleccione un huésped para eliminar")
            return
        if messagebox.askyesno("Eliminar Huésped", "¿Esta seguro de eliminar este huésped?"):
            for item in eliminar:
                valores = self.tree.item(item)['values']
                id = valores[0]
                if self.db.eliminar_huespedes(id):
                    self.tree.delete(item)
                else:
                    messagebox.showerror(f"No se pudo eliminar el huesped con ID {id}")

    def huesped_select(self, evento):
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.huesped_seleccionado = valores[0]
        for i, campo in enumerate(self.campos):
            self.inputs[campo].delete(0, tk.END)
            self.inputs[campo].insert(0, valores[i+1])
    
    def modificar_huesped(self):
        if not self.huesped_seleccionado:
            messagebox.showwarning("Modificar Huésped", "Por favor, seleccione un huésped para modificar")
            return
        
        if not self.validar_inputs():
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        nuevos_datos = [self.inputs[campo].get() for campo in self.campos]
        if self.db.actualizar_huespedes(self.huesped_seleccionado, *nuevos_datos):
            messagebox.showinfo("Exito", "Huésped actualizado correctamente")
            self.cargar_datos()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el huésped")
        
    def limpiar_campos(self):
        for entrada in self.inputs.values():
            entrada.delete(0, tk.END)
        self.huesped_seleccionado = None

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = GestionHuespedes(root)
    root.mainloop()