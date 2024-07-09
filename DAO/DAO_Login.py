from DAO.database import Database

class LoginDAO:
    def __init__(self):
        self.db = Database()
    
    def get_user(self, user, password):
        query = "SELECT * FROM usuario WHERE nombre=%s AND contrasena=%s"
        return self.db.fetch_one(query, (user, password))
