from DAO.database import Database
from tkinter import messagebox

class DAO_usuarios:
    def __init__(self):
        self.db = Database()

    def cargar_usuarios_encargados(self):
        query = """
        SELECT u.id_usuario, u.nombre, u.apellido, u.correo, u.contrasena
        FROM usuario u
        JOIN rol_usuario r ON u.id_rol_usuario = r.id_rol_usuario
        WHERE r.id_rol_usuario = 2
        """
        return self.db.fetch_all(query)

    def agregar_usuario(self, params):
        query = """
        INSERT INTO usuario (nombre, apellido, correo, contrasena, id_rol_usuario)
        VALUES (%s, %s, %s, %s, 2)
        """
        return self.db.execute_query(query, params)

    def modificar_usuario(self, params):
        id_usuario = params[-1]  # Último parámetro es el ID del usuario
        if not self.validar_existencia_usuario(id_usuario):
            messagebox.showerror("Error", f"No existe un usuario con ID: {id_usuario}")
            return False

        query = """
        UPDATE usuario
        SET nombre = %s, apellido = %s, correo = %s, contrasena = %s
        WHERE id_usuario = %s AND id_rol_usuario = 2
        """
        mensaje = f"Se ha modificado el usuario con ID: {id_usuario}"
        messagebox.showinfo("Información", mensaje)
        return self.db.execute_query(query, params)

    def eliminar_usuario(self, id):
        query = "DELETE FROM usuario WHERE id_usuario = %s AND id_rol_usuario = 2"
        try:
            self.db.execute_query(query, (id,))
            messagebox.showwarning("Eliminado", f"Se eliminó el usuario con ID: {id}")
        except:
            messagebox.showerror("Error", "No se pudo eliminar el usuario")
        return self.db.execute_query(query, (id,))
    
    def validar_existencia_usuario(self, id_usuario):
        query = "SELECT COUNT(*) as count FROM usuario WHERE id_usuario = %s"
        result = self.db.fetch_one(query, (id_usuario,))
        
        if result is not None and 'count' in result and result['count'] > 0:
            return True
        else:
            return False
    
    def buscar_usuario(self, termino_busqueda):
        query = """
        SELECT u.id_usuario, u.nombre, u.apellido, u.correo, u.contrasena
        FROM usuario u
        JOIN rol_usuario r ON u.id_rol_usuario = r.id_rol_usuario
        WHERE r.id_rol_usuario = 2
        AND (u.nombre LIKE %s OR u.apellido LIKE %s OR u.correo LIKE %s)
        """
        params = (f'%{termino_busqueda}%', f'%{termino_busqueda}%', f'%{termino_busqueda}%')
        return self.db.fetch_all(query, params)
