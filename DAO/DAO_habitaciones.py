from DAO.database import Database

class DAO_habitaciones:
    def __init__(self):
        self.db = Database()

    def cargar_estados_habitacion(self):
        query = "SELECT estado FROM estado_habitacion"
        return self.db.fetch_all(query)

    def cargar_tipos_habitacion(self):
        query = "SELECT tipo FROM tipo_habitacion"
        return self.db.fetch_all(query)

    def cargar_orientaciones(self):
        query = "SELECT orientacion FROM orientacion"
        return self.db.fetch_all(query)

    def cargar_habitaciones(self):
        query = """
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
        """
        return self.db.fetch_all(query)

    def agregar_habitacion(self, params):
        query = """
        INSERT INTO habitacion 
        (numero_habitacion, precio_noche, camas, piso, capacidad, id_tipo_habitacion, id_orientacion, id_estado_habitacion) 
        VALUES 
        (%s, %s, %s, %s, %s, 
        (SELECT id_tipo_habitacion FROM tipo_habitacion WHERE tipo = %s), 
        (SELECT id_orientacion FROM orientacion WHERE orientacion = %s), 
        (SELECT id_estado_habitacion FROM estado_habitacion WHERE estado = %s))
        """
        return self.db.execute_query(query, params)

    def modificar_habitacion(self, params):
        query = """
        UPDATE habitacion 
        SET 
            precio_noche = %s, 
            camas = %s, 
            piso = %s, 
            capacidad = %s, 
            id_tipo_habitacion = (SELECT id_tipo_habitacion FROM tipo_habitacion WHERE tipo = %s), 
            id_orientacion = (SELECT id_orientacion FROM orientacion WHERE orientacion = %s), 
            id_estado_habitacion = (SELECT id_estado_habitacion FROM estado_habitacion WHERE estado = %s)
        WHERE numero_habitacion = %s
        """
        return self.db.execute_query(query, params)

    def eliminar_habitacion(self, params):
        query = "DELETE FROM habitacion WHERE numero_habitacion = %s"
        return self.db.execute_query(query, params)
