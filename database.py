import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect_to_db(self):
        try:
            self.conn = mysql.connector.connect(
                host='lucianoberriosdev.cl',
                database='clu100699_hotel_duerme_bien',
                user='clu100699_admin',
                password='contraseña'
            )
            if self.conn.is_connected():
                print("Conexión exitosa")
                self.cursor = self.conn.cursor(dictionary=True)
                return True
        except Error as e:
            messagebox.showerror("Error", f"Error al conectar a MySQL: {e}")
            return False

    def disconnect_from_db(self):
        try:
            if self.conn is not None and self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print("Desconexión exitosa")
        except Error as e:
            messagebox.showerror("Error", f"Error al desconectar de MySQL: {e}")

    def execute_query(self, query, params=None):
        try:
            if not self.connect_to_db():
                return False
            
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Error as e:
            messagebox.showerror("Error", f"Error en la consulta: {e}")
            return False
        finally:
            self.disconnect_from_db()

    def fetch_one(self, query, params=None):
        try:
            if not self.connect_to_db():
                return None
            
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Error as e:
            messagebox.showerror("Error", f"Error al obtener resultado: {e}")
            return None
        finally:
            self.disconnect_from_db()

    def fetch_all(self, query, params=None):
        try:
            if not self.connect_to_db():
                return []
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as e:
            messagebox.showerror("Error", f"Error al obtener resultados: {e}")
            return []
        finally:
            self.disconnect_from_db()
