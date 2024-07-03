import mysql.connector
from mysql.connector import Error

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
            print(f"Error al conectar a MySQL: {e}")
            return False

    def fetch_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def cargar_habitacion_por_id(self, id_habitacion):
        query = f"""
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
        WHERE h.id_habitacion = {id_habitacion}
        """
        return self.fetch_all(query)
