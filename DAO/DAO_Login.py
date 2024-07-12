from DAO.database import Database

class LoginDAO:
    def __init__(self):
        self.db = Database()
    
    def get_user_by_email(self, email, password):
        query = "SELECT * FROM usuario WHERE correo=%s AND contrasena=%s"
        return self.db.fetch_one(query, (email, password))
