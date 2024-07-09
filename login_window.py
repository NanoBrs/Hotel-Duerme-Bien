import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from ventana_administrador import VentanaAdministrador
from ventana_encargado import VentanaEncargado

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("720x480")
        
        # Agregar imagen de fondo
        self.background_image = tk.PhotoImage(file="img/login.png")
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
        
        # Configuración de estilos
        style = ttk.Style()
        style.configure("rounded_entry.TEntry", borderwidth=1, relief="flat", background="white", padding=10, font=('Helvetica', 12))
        style.configure("rounded.TButton", borderwidth=2, relief="flat", background="blue", padding=10, font=('Helvetica', 12))
        style.map("rounded.TButton", background=[('active', 'blue')])
        
        # Barra de menú
        self.menubar = tk.Menu(master)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Salir", command=self.quit_app)
        
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Ayuda", command=self.open_help)
        self.help_menu.add_command(label="Solucionar Problemas", command=self.open_troubleshoot)
        self.help_menu.add_command(label="Términos y Condiciones", command=self.open_termin)
        
        self.menubar.add_cascade(label="Archivo", menu=self.file_menu)
        self.menubar.add_cascade(label="Ayuda", menu=self.help_menu)
        
        master.config(menu=self.menubar)
        
        # Entradas de usuario y contraseña
        self.entry_user = ttk.Entry(master, style="rounded_entry.TEntry")
        self.entry_user.place(x=48, y=190.6)
        
        self.entry_password = ttk.Entry(master, show='*', style="rounded_entry.TEntry")
        self.entry_password.place(x=48, y=271)
        
        # Botón de Login
        self.login_button = ttk.Button(master, text="Ingresar", command=self.on_login, style="rounded.TButton")
        self.login_button.place(x=55, y=338.4)
    
    def login(self, user, password):
        db = Database()
        query = "SELECT * FROM usuario WHERE nombre=%s AND contrasena=%s"
        return db.fetch_one(query, (user, password))

    def on_login(self):
        user = self.entry_user.get()
        password = self.entry_password.get()
        
        if not user or not password:
            messagebox.showwarning("Campos requeridos", "Por favor complete usuario y contraseña.")
            return
        
        user_data = self.login(user, password)
        
        if user_data:
            self.master.withdraw()  # Oculta la ventana de login en lugar de destruirla
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            
            if user_data["id_rol_usuario"] == 1:
                admin_window = tk.Toplevel(self.master)
                VentanaAdministrador(admin_window)
            elif user_data["id_rol_usuario"] == 2:
                encargado_window = tk.Toplevel(self.master)
                VentanaEncargado(encargado_window)
            
            print(f"Usuario {user_data['nombre']} ha iniciado sesión correctamente.")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def open_help(self):
        messagebox.showinfo("Ayuda", "Esta es la ayuda de la aplicación.")
    
    def open_troubleshoot(self):
        messagebox.showinfo("Solucionar Problemas", "Aquí puedes encontrar ayuda para solucionar problemas.")
    
    def open_termin(self):
        # Abrir ventana de términos y condiciones
        terminos_window = tk.Toplevel(self.master)
        TerminosCondicionesWindow(terminos_window)
    
    def quit_app(self):
        self.master.quit()
    
    def destroy_app(self):
        self.master.destroy()

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

