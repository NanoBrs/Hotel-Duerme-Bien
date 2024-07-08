import mysql.connector
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
        except mysql.connector.Error as err:
            print(f"Error al conectar a MySQL: {err}")
            return False

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def obtener_id_por_rut(self, rut):
        query = "SELECT id_huesped FROM huespedes WHERE rut = %s"
        resultado = self.fetch_all(query, (rut,))
        if resultado:
            return resultado[0]['id_huesped']
        else:
            return None

    def insert_reserva(self, entrada, salida, id_usuario, precio_total):
        today = date.today()
        if entrada == today:
            estado_reserva = "Activa"
        elif entrada > today:
            estado_reserva = "Reservada"
        else:
            estado_reserva = "Terminada"

        query_estado_reserva = """
        INSERT INTO estado_reserva (estado)
        VALUES (%s)
        """
        self.cursor.execute(query_estado_reserva, (estado_reserva,))
        id_estado_reserva = self.cursor.lastrowid

        query_reserva = """
        INSERT INTO reserva (fecha_llegada, fecha_salida, id_usuario, id_estado_reserva, precio_total)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query_reserva, (entrada, salida, id_usuario, id_estado_reserva, precio_total))
        id_reserva = self.cursor.lastrowid

        self.conn.commit()
        return id_reserva
    
    def insert_detalle_reserva(self, id_reserva, id_habitacion, hora):
        query = """
        INSERT INTO detalle_reserva (id_reserva, id_habitacion, hora)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (id_reserva, id_habitacion, hora))
        id_detalle_reserva = self.cursor.lastrowid
        self.conn.commit()
        return id_detalle_reserva

    def insert_detalle_huesped(self, id_reserva, id_responsable, id_detalle_reserva):
        query = """
        INSERT INTO detalle_huespedes (id_reserva, id_responsable, id_detalle_reserva)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (id_reserva, id_responsable, id_detalle_reserva))
        self.conn.commit()

    def cargar_habitacion_por_id(self, id_habitacion):
        query = """
        SELECT 
            h.id_habitacion, 
            h.numero_habitacion, 
            h.precio_noche, 
            h.camas, 
            h.piso, 
            th.tipo, 
            o.orientacion, 
            eh.estado 
        FROM habitacion h
        JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
        JOIN orientacion o ON h.id_orientacion = o.id_orientacion
        JOIN estado_habitacion eh ON h.id_estado_habitacion = eh.id_estado_habitacion
        WHERE h.id_habitacion = %s
        """
        return self.fetch_all(query, (id_habitacion,))
    
    def buscar_habitaciones_disponibles(self, fecha_entrada, fecha_salida):
        query = """
        SELECT h.id_habitacion, h.numero_habitacion, th.tipo, th.cantidad_maxima, h.precio_noche
        FROM habitacion h
        JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
        LEFT JOIN detalle_reserva dr ON h.id_habitacion = dr.id_habitacion
        LEFT JOIN reserva r ON dr.id_reserva = r.id_reserva
        WHERE (r.fecha_salida <= %s OR r.fecha_llegada >= %s) OR r.fecha_llegada IS NULL
        """
        return self.fetch_all(query, (fecha_entrada, fecha_salida))
