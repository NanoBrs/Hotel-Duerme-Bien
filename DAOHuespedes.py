from database import Database

class DAOHuespedes_Consultas:
    def __init__(self):
        
        #Instancia de database
        self.db = Database()
    
    def agregar_huespedes(self, nombre, apellido1, apellido2, correo, numero, rut):
        query = """
        INSERT INTO huespedes (nombre, apellido1, apellido2, correo, numero, rut)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        parametros = (nombre, apellido1, apellido2, correo, numero, rut)
        return self.db.execute_query(query, parametros)

    def cargar_huespedes(self):
        query = """
        SELECT id_huesped, nombre, apellido1, apellido2, correo, numero, rut 
        FROM huespedes
        """
        return self.db.fetch_all(query)
    
    def eliminar_huespedes(self, id):
        query = """
        DELETE FROM huespedes WHERE id_huesped = %s
        """
        parametros = (id,)
        return self.db.execute_query(query, parametros)
    
    def actualizar_huespedes(self, id, nombre, apellido1, apellido2, correo, numero, rut):
        query = """
        UPDATE huespedes
        SET nombre = %s, apellido1 = %s, apellido2 = %s, correo = %s, numero = %s, rut = %s
        WHERE id_huesped = %s
        """
        parametros = (nombre, apellido1, apellido2, correo, numero, rut, id)
        return self.db.execute_query(query, parametros)
    
    def buscar_huespedes(self, busqueda):
        query = """
        SELECT id_huesped, nombre, apellido1, apellido2, correo, numero, rut
        FROM huespedes
        WHERE nombre LIKE %s OR apellido1 LIKE %s OR apellido2 LIKE %s OR correo LIKE %s
        OR numero LIKE %s OR rut LIKE %s
        """
        
        parametros = ('%' + busqueda + '%') * 6
        return self.db.fetch_all(query, parametros)