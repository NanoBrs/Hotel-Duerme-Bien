from DAO.database import Database
from tkinter import ttk, messagebox

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
        mensaje = f"Se ha agregado correctamente la habitación"
        messagebox.showinfo("Información", mensaje)
        return self.db.execute_query(query, params)

    def modificar_habitacion(self, params):
        id_habitacion = params[-1]  # Último parámetro es el ID de la habitación
        if not self.validar_existencia_habitacion(id_habitacion):
            messagebox.showerror("Error", f"No existe una habitación con ID: {id_habitacion}")
            return False
        
        query = """
        UPDATE habitacion 
        SET 
            precio_noche = %s, 
            camas = %s, 
            piso = %s, 
            capacidad = %s, 
            id_tipo_habitacion = (SELECT id_tipo_habitacion FROM tipo_habitacion WHERE tipo = %s), 
            id_orientacion = (SELECT id_orientacion FROM orientacion WHERE orientacion = %s), 
            id_estado_habitacion = (SELECT id_estado_habitacion FROM estado_habitacion WHERE estado = %s),
            numero_habitacion = %s
        WHERE id_habitacion = %s
        """
        mensaje = f"Se ha modificado la habitación de ID: {id_habitacion}"
        messagebox.showinfo("Información", mensaje)
        return self.db.execute_query(query, params)


    def eliminar_habitacion(self, id):
        query = "DELETE FROM habitacion WHERE id_habitacion = %s"
        
        try:
            mensaje = f"Se eliminó la habitación de id: {id}"
            messagebox.showinfo("Eliminado", mensaje)
        except:
            messagebox.showerror("Error", "No se pudo eliminar la habitación")
        return self.db.execute_query(query, id)
    
    def validar_existencia_habitacion(self, id_habitacion):
        query = "SELECT COUNT(*) as count FROM habitacion WHERE id_habitacion = %s"
        result = self.db.fetch_one(query, (id_habitacion,))
        
        if result is not None and 'count' in result and result['count'] > 0:
            return True
        else:
            return False

