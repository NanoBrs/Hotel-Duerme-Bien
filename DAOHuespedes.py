from database import Database

class DAOHuespedes_Consultas:
    def __init__(self):
        
        #Instancia de database
        self.db = Database()
        
    def cargar_huespedes(self):
        query = """
        SELECT id_huesped, nombre, apellido1, apellido2, correo, numero, rut 
        FROM huespedes
        """
        return self.db.fetch_all(query)