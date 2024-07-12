from DAO.database import Database
from datetime import date

class Database_reserva:
    def __init__(self):
        self.db = Database()

class Database_reserva:
    def __init__(self):
        self.db = Database()

    def obtener_id_por_rut(self, rut):
        query = "SELECT id_huesped FROM huespedes WHERE rut = %s"
        resultado = self.db.fetch_all(query, (rut,))
        if resultado:
            return resultado[0]['id_huesped']
        else:
            return None

    def obtener_nombre_apellido_por_rut(self, rut):
        query = "SELECT nombre, apellido1 FROM huespedes WHERE rut = %s"
        resultado = self.db.fetch_all(query, (rut,))
        if resultado:
            return resultado[0]['nombre'], resultado[0]['apellido1']
        else:
            return None

    def cargar_reservas(self):
        query = """
        SELECT r.id_reserva, r.fecha_llegada, r.fecha_salida, h.numero_habitacion, th.tipo AS tipo_habitacion, r.precio_total, eh.estado AS estado_habitacion
        FROM reserva r
        JOIN detalle_reserva dr ON r.id_reserva = dr.id_reserva
        JOIN habitacion h ON dr.id_habitacion = h.id_habitacion
        JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
        JOIN estado_habitacion eh ON h.id_estado_habitacion = eh.id_estado_habitacion
        """
        return self.db.fetch_all(query)

    def cargar_tipos_habitacion(self):
        query = "SELECT id_tipo_habitacion, tipo, cantidad_maxima FROM tipo_habitacion"
        return self.db.fetch_all(query)

    def insert_reserva(self, entrada, salida, id_usuario, precio_total):
        today = date.today()
        if today < entrada:
            estado_reserva = 2  # Reservada
        elif entrada <= today <= salida:
            estado_reserva = 1  # Activa
        else:
            estado_reserva = 3  # Terminada
        id_estado_reserva = estado_reserva

        query_reserva = "INSERT INTO reserva (fecha_llegada, fecha_salida, id_usuario, id_estado_reserva, precio_total) VALUES (%s, %s, %s, %s, %s)"
        self.db.execute_query(query_reserva, (entrada, salida, id_usuario, id_estado_reserva, precio_total))
        id_reserva = self.db.cursor.lastrowid
        return id_reserva
    
    def insert_detalle_reserva(self, id_reserva, id_habitacion, hora):
        query = "INSERT INTO detalle_reserva (id_reserva, id_habitacion, hora) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (id_reserva, id_habitacion, hora))
        id_detalle_reserva = self.db.cursor.lastrowid
        return id_detalle_reserva

    def insert_detalle_huesped(self, id_reserva, id_responsable, id_detalle_reserva):
        query = "INSERT INTO detalle_huespedes (id_reserva, id_responsable, id_detalle_reserva) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (id_reserva, id_responsable, id_detalle_reserva))

    def cargar_habitacion_por_id(self, id_habitacion):
        query = """
        SELECT h.id_habitacion, h.numero_habitacion, h.precio_noche, h.camas, h.piso, th.tipo, o.orientacion, eh.estado 
        FROM habitacion h
        JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
        JOIN orientacion o ON h.id_orientacion = o.id_orientacion
        JOIN estado_habitacion eh ON h.id_estado_habitacion = eh.id_estado_habitacion
        WHERE h.id_habitacion = %s
        """
        return self.db.fetch_all(query, (id_habitacion,))
    
    def cargar_capacidad_habitacion_por_id(self, id_habitacion):
        query = """
        SELECT h.capacidad
        FROM habitacion h
        WHERE h.id_habitacion = %s
        """
        return self.db.fetch_all(query, (id_habitacion,))

    def buscar_habitaciones_disponibles(self, fecha_entrada, fecha_salida, tipo_habitacion):
        query = """
        SELECT h.id_habitacion, h.numero_habitacion, h.precio_noche, h.camas, h.piso, h.capacidad, th.tipo, o.id_orientacion, th.cantidad_maxima, eh.estado
        FROM habitacion h
        JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
        LEFT JOIN orientacion o ON h.id_orientacion = o.id_orientacion
        LEFT JOIN detalle_reserva dr ON h.id_habitacion = dr.id_habitacion
        LEFT JOIN reserva r ON dr.id_reserva = r.id_reserva
        LEFT JOIN estado_habitacion eh ON h.id_estado_habitacion = eh.id_estado_habitacion
        WHERE (r.fecha_salida <= %s OR r.fecha_llegada >= %s OR r.id_reserva IS NULL) 
        AND th.id_tipo_habitacion = %s
        AND eh.estado = 'Disponible'
        """
        return self.db.fetch_all(query, (fecha_salida, fecha_entrada, tipo_habitacion))

    def actualizar_estado_habitacion(self, id_habitacion, nuevo_estado):
        query = "UPDATE habitacion SET id_estado_habitacion = (SELECT id_estado_habitacion FROM estado_habitacion WHERE estado = %s) WHERE id_habitacion = %s"
        self.db.execute_query(query, (nuevo_estado, id_habitacion))


