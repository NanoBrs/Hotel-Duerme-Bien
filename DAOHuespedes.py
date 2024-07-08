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