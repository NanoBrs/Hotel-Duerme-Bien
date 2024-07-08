import tkinter as tk
from tkinter import ttk, messagebox
from DAO.DAO_habitaciones import DAO_habitaciones
from DAO.DAO_Login import LoginDAO

class Login(tk.Frame):
    def __init__(self, parent, controlador):
        tk.Frame.__init__(self, parent)
        self.controlador = controlador
        self.login_dao = LoginDAO()  # Instancia del DAO

        # Agregar imagen de fondo
        self.background_image = tk.PhotoImage(file="img/loginV2.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
        
        # Configuración de estilos
        style = ttk.Style()
        style.configure("rounded_entry.TEntry", borderwidth=1, relief="flat", background="white", padding=10, font=('Helvetica', 12))
        style.configure("rounded.TButton", borderwidth=2, relief="flat", background="blue", padding=10, font=('Helvetica', 12))
        style.map("rounded.TButton", background=[('active', 'blue')])
        
        style.configure("b.TButton", padding=6, relief="flat", background="black", foreground="Black", font=('Helvetica', 12))
        style.map("b.TButton",
            background=[('active', '#45a049')],
            foreground=[('active', '#45a049')]
        )
        # Barra de menú
        self.menubar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Salir", command=self.quit_app)
        
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Ayuda", command=self.open_help)
        self.help_menu.add_command(label="Solucionar Problemas", command=self.open_troubleshoot)
        self.help_menu.add_command(label="Términos y Condiciones", command=self.open_termin)
        
        self.menubar.add_cascade(label="Archivo", menu=self.file_menu)
        self.menubar.add_cascade(label="Ayuda", menu=self.help_menu)
        
        controlador.config(menu=self.menubar)
        
        # Entradas de usuario y contraseña
        self.entry_user = ttk.Entry(self, style="rounded_entry.TEntry",width=21)
        self.entry_user.place(x=299.2, y=280.6)
        
        self.entry_password = ttk.Entry(self, show='*', style="rounded_entry.TEntry",width=21)
        self.entry_password.place(x=299.2, y=400.5)
        
        # Botón de Login
        self.login_button = ttk.Button(self, text="Ingresar", command=self.on_login, style="b.TButton")
        self.login_button.place(x=301.5, y=460.9)
    
    def on_login(self):
        user = self.entry_user.get()
        password = self.entry_password.get()
        
        if not user or not password:
            messagebox.showwarning("Campos requeridos", "Por favor complete usuario y contraseña.")
            return
        
        user_data = self.login_dao.get_user(user, password)
        
        self.entry_user.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

        if user_data:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            if user_data["id_rol_usuario"] == 1:
                self.controlador.mostrar_frame("GestionEncargados")
            elif user_data["id_rol_usuario"] == 2:
                self.controlador.mostrar_frame("MenuEncargado")
            
            print(f"Usuario {user_data['nombre']} ha iniciado sesión correctamente.")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def open_help(self):
        messagebox.showinfo("Ayuda", "Esta es la ayuda de la aplicación.")
    
    def open_troubleshoot(self):
        messagebox.showinfo("Solucionar Problemas", "Aquí puedes encontrar ayuda para solucionar problemas.")
    
    def open_termin(self):
        # Abrir ventana de términos y condiciones
        terminos_window = tk.Toplevel(self)
        TerminosCondicionesWindow(terminos_window)
    
    def quit_app(self):
        self.controlador.quit()
    
    def destroy_app(self):
        self.controlador.destroy()

class TerminosCondicionesWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Términos y Condiciones")
        self.master.geometry("600x400")
        
        # Frame para el texto
        frame = tk.Frame(master)
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Scrollbar para el texto
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Texto de términos y condiciones
        self.terminos_text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.terminos_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar scrollbar
        scrollbar.config(command=self.terminos_text.yview)
        
        # Cargar términos y condiciones desde el archivo
        self.cargar_terminos_condiciones()
    
    def cargar_terminos_condiciones(self):
        try:
            with open("others/terminos_y_condiciones.txt", "r", encoding="utf-8") as file:
                terminos_condiciones = file.read()
                self.terminos_text.insert(tk.END, terminos_condiciones)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo de términos y condiciones.")
            self.master.destroy()
