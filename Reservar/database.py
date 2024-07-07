import mysql.connector
from mysql.connector import Error
from datetime import date

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

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def insert_reserva(self, entrada, salida, id_usuario):
        # Determinar el estado de la reserva
        today = date.today()
        if entrada == today:
            estado_reserva = "Activa"
        elif entrada > today:
            estado_reserva = "Reservada"
        else:
            estado_reserva = "Terminada"

        # Insertar en la tabla estado_reserva
        query_estado_reserva = """
        INSERT INTO estado_reserva (estado)
        VALUES (%s)
        """
        self.cursor.execute(query_estado_reserva, (estado_reserva,))
        id_estado_reserva = self.cursor.lastrowid

        # Insertar en la tabla reserva
        query_reserva = """
        INSERT INTO reserva (fecha_llegada, fecha_salida, id_usuario, id_estado_reserva)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query_reserva, (entrada, salida, id_usuario, id_estado_reserva))
        id_reserva = self.cursor.lastrowid

        self.conn.commit()
        return id_reserva

    def insert_detalle_reserva(self, id_reserva, id_habitacion):
        query = """
        INSERT INTO detalle_reserva (id_reserva, id_habitacion)
        VALUES (%s, %s)
        """
        self.cursor.execute(query, (id_reserva, id_habitacion))
        self.conn.commit()

    def insert_detalle_huesped(self, id_reserva, id_huespedes_h, id_responsable):
        query = """
        INSERT INTO detalle_huespedes (id_reserva, id_huespedes_h, id_responsable)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (id_reserva, id_huespedes_h, id_responsable))
        self.conn.commit()

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
