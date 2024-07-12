from DAO.database import Database
from datetime import date
from tkinter import ttk, messagebox

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
        SELECT r.id_reserva, r.fecha_llegada, r.fecha_salida, h.numero_habitacion,
        th.tipo AS tipo_habitacion, r.precio_total,r.id_usuario, er.estado AS estado_reserva,
        dr.id_habitacion,dh.id_responsable,hu.rut
        FROM reserva r
        JOIN detalle_reserva dr ON r.id_reserva = dr.id_reserva
        JOIN habitacion h ON dr.id_habitacion = h.id_habitacion
        JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
        JOIN estado_reserva er ON r.id_estado_reserva = er.id_estado_reserva
        Join detalle_huespedes dh ON dr.id_detalle_reserva = dh.id_detalle_reserva
        JOIN huespedes hu ON dh.id_responsable = hu.id_huesped
        """
        return self.db.fetch_all(query)

    def cargar_tipos_habitacion(self):
        query = "SELECT id_tipo_habitacion, tipo, cantidad_maxima FROM tipo_habitacion"
        return self.db.fetch_all(query)

    def insert_reserva(self, entrada, salida, id_usuario, precio_total):
        today = date.today()
        estado_reserva = "Activa" if entrada == today else "Reservada" if entrada > today else "Terminada"

        query_estado_reserva = "INSERT INTO estado_reserva (estado) VALUES (%s)"
        self.db.execute_query(query_estado_reserva, (estado_reserva,))
        id_estado_reserva = self.db.cursor.lastrowid

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

    def modificar_reserva(self, id_reserva, nuevo_rut, nueva_fecha_llegada, nueva_fecha_salida, nueva_tipo_habitacion, nueva_id_habitacion, nuevo_precio_total):
        query = """
        UPDATE reservas
        SET fecha_llegada = %s, fecha_salida = %s, tipo_habitacion = %s, id_habitacion = %s, precio_total = %s
        WHERE id_reserva = %s
        """
        self.db.execute_query(query, (nueva_fecha_llegada, nueva_fecha_salida, nueva_tipo_habitacion, nueva_id_habitacion, nuevo_precio_total, id_reserva))

        # También debes actualizar los detalles del huésped si el RUT cambia
        id_huesped = self.obtener_id_por_rut(nuevo_rut)
        if id_huesped:
            query_detalle = """
            UPDATE detalle_reserva
            SET id_huesped = %s
            WHERE id_reserva = %s
            """
            self.db.execute_query(query_detalle, (id_huesped, id_reserva))
        
        
    def obtener_id_habitacion_por_reserva(self, id_reserva):
        query = "SELECT id_habitacion FROM detalle_reserva WHERE id_reserva = %s"
        resultado = self.db.fetch_one(query, (id_reserva,))
        if resultado:
            return resultado['id_habitacion']
        else:
            return None

    def eliminar_detalle_huespedes(self, id_reserva):
        query = "DELETE FROM detalle_huespedes WHERE id_reserva = %s"
        return self.db.execute_query(query, (id_reserva,))

    def eliminar_detalle_reserva(self, id_reserva):
        query = "DELETE FROM detalle_reserva WHERE id_reserva = %s"
        return self.db.execute_query(query, (id_reserva,))

    def eliminar_reserva(self, id_reserva):
        query = "DELETE FROM reserva WHERE id_reserva = %s"
        return self.db.execute_query(query, (id_reserva,))

    def actualizar_estado_habitacion_a_disponible(self, id_habitacion):
        query = "UPDATE habitacion SET id_estado_habitacion = 1 WHERE id_habitacion = %s"
        return self.db.execute_query(query, (id_habitacion,))

    def eliminar_reserva_completa(self, id_reserva):
        try:
            id_habitacion = self.obtener_id_habitacion_por_reserva(id_reserva)
            if id_habitacion is None:
                messagebox.showerror("Error", "No se pudo obtener el id de la habitación.")
                return None
            
            self.eliminar_detalle_huespedes(id_reserva)
            self.eliminar_detalle_reserva(id_reserva)
            result = self.eliminar_reserva(id_reserva)
            
            self.actualizar_estado_habitacion_a_disponible(id_habitacion)

            if result:
                messagebox.showwarning("Eliminado", f"Se eliminó la reserva con id: {id_reserva} y la habitación pasó a estar Disponible.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar la reserva.")

            return result
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la reserva. Error: {e}")
            return None



