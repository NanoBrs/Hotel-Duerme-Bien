from DAO.database import Database
from datetime import date
from tkinter import messagebox

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
        WITH HabitacionesOrdenadas AS (
            SELECT 
                dr.id_reserva, 
                dr.id_habitacion, 
                ROW_NUMBER() OVER (PARTITION BY dr.id_reserva ORDER BY dr.id_detalle_reserva) AS rn
            FROM 
                detalle_reserva dr
        )
        SELECT 
            r.id_reserva AS "ID reserva", 
            r.fecha_llegada AS "Fecha de Llegada", 
            r.fecha_salida AS "Fecha de Salida",
            th.tipo AS "Tipo de Habitacion", 
            r.precio_total AS "Precio Total", 
            r.id_usuario AS "Usuario", 
            er.estado AS "Estado",
            h1.id_habitacion AS "H.1",
            h2.id_habitacion AS "H.2",
            h3.id_habitacion AS "H.3",
            dh.id_responsable AS "Responsable", 
            hu.rut AS "Rut_Responsable"
        FROM 
            reserva r
        JOIN 
            HabitacionesOrdenadas h1 ON r.id_reserva = h1.id_reserva AND h1.rn = 1
        LEFT JOIN 
            HabitacionesOrdenadas h2 ON r.id_reserva = h2.id_reserva AND h2.rn = 2
        LEFT JOIN 
            HabitacionesOrdenadas h3 ON r.id_reserva = h3.id_reserva AND h3.rn = 3
        JOIN 
            habitacion hab1 ON h1.id_habitacion = hab1.id_habitacion
        LEFT JOIN 
            habitacion hab2 ON h2.id_habitacion = hab2.id_habitacion
        LEFT JOIN 
            habitacion hab3 ON h3.id_habitacion = hab3.id_habitacion
        JOIN 
            tipo_habitacion th ON hab1.id_tipo_habitacion = th.id_tipo_habitacion
        JOIN 
            estado_reserva er ON r.id_estado_reserva = er.id_estado_reserva
        JOIN 
            detalle_huespedes dh ON r.id_reserva = dh.id_reserva
        JOIN 
            huespedes hu ON dh.id_responsable = hu.id_huesped
        GROUP BY 
            r.id_reserva, th.tipo, r.precio_total, r.id_usuario, er.estado, h1.id_habitacion, h2.id_habitacion, h3.id_habitacion, dh.id_responsable, hu.rut;
        """
        reservas = self.db.fetch_all(query)
        reservas_formateadas = []
        for reserva in reservas:
            reservas_formateadas.append({
                'id_reserva': reserva['ID reserva'],
                'fecha_llegada': reserva['Fecha de Llegada'],
                'fecha_salida': reserva['Fecha de Salida'],
                'tipo_habitacion': reserva['Tipo de Habitacion'],
                'precio_total': reserva['Precio Total'],
                'usuario': reserva['Usuario'],
                'estado': reserva['Estado'],
                'habitacion_1': reserva['H.1'],
                'habitacion_2': reserva['H.2'],
                'habitacion_3': reserva['H.3'],
                'responsable': reserva['Responsable'],
                'rut_responsable': reserva['Rut_Responsable']
            })
        return reservas_formateadas

    def cargar_tipos_habitacion(self):
        query = "SELECT id_tipo_habitacion, tipo FROM tipo_habitacion"
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

    def cambiar_estado_disponible(self, id_habitacion, nuevo_estado):
        query = "UPDATE habitacion SET id_estado_habitacion = (SELECT id_estado_habitacion FROM estado_habitacion WHERE estado = %s) WHERE id_habitacion = %s"
        self.db.execute_query(query, (nuevo_estado, id_habitacion))

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

    def obtener_id_habitacion_por_reserva(self, id_reserva):
        query = "SELECT id_habitacion FROM detalle_reserva WHERE id_reserva = %s"
        resultado = self.db.fetch_one(query, (id_reserva,))
        if resultado:
            return resultado['id_habitacion']
        else:
            return None

    def eliminar_reserva_completa(self, id_reserva):
        try:
            id_habitacion = self.obtener_id_habitacion_por_reserva(id_reserva)
            if id_habitacion is None:
                messagebox.showerror("Error", "No se pudo obtener el id de la habitacion.")
                return None
            
            self.eliminar_detalle_huespedes(id_reserva)
            self.eliminar_detalle_reserva(id_reserva)
            result = self.eliminar_reserva(id_reserva)
            
            self.actualizar_estado_habitacion_a_disponible(id_habitacion)

            if result:
                messagebox.showwarning("Eliminado", f"Se elimino la reserva con id: {id_reserva} y la habitación paso a estar Disponible.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar la reserva.")

            return result
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la reserva. Error: {e}")
            return None


    def modificar_reserva(self, id_reserva, nueva_fecha_llegada, nueva_fecha_salida, nuevo_precio_total, id_usuario):
        today = date.today()
        if today < nueva_fecha_llegada:
            estado_reserva = 2  # Reservada
        elif nueva_fecha_llegada <= today <= nueva_fecha_salida:
            estado_reserva = 1  # Activa
        else:
            estado_reserva = 3  # Terminada
        id_estado_reserva = estado_reserva

        query = """
        UPDATE reserva
        SET fecha_llegada = %s, fecha_salida = %s, precio_total = %s, id_usuario = %s, id_estado_reserva = %s
        WHERE id_reserva = %s
        """
        self.db.execute_query(query, (nueva_fecha_llegada, nueva_fecha_salida, nuevo_precio_total, id_usuario, id_estado_reserva, id_reserva))

    def actualizar_detalle_huesped(self, id_reserva, id_huesped):
        query = """
        UPDATE detalle_huespedes
        SET id_responsable = %s
        WHERE id_reserva = %s
        """
        self.db.execute_query(query, (id_huesped, id_reserva))

    def actualizar_detalle_reserva(self,id_habitacion,hora_actual, id_reserva,id_detalle_reserva):
            query = """
            UPDATE detalle_reserva
            SET id_habitacion = %s, hora = %s
            WHERE id_reserva = %s AND id_detalle_reserva = %s
            """
            self.db.execute_query(query, (id_habitacion, hora_actual, id_reserva,id_detalle_reserva))

    def obtener_id_detalle_r(self, id_habitacion):
        query = """
        SELECT id_detalle_reserva
        FROM detalle_reserva
        WHERE id_habitacion = `%s`;
        """
        resultado = self.db.execute_query(query,id_habitacion)
        print(resultado)
    def obtener_detalles_reserva(self, id_reserva):
        query = """
        SELECT id_detalle_reserva
        FROM detalle_reserva
        WHERE id_reserva = %s
        """
        try:
            resultado = self.db.execute_query(query, (id_reserva,))
            return [row['id_detalle_reserva'] for row in resultado]
        except Exception as e:
            print(f"Error al ejecutar la consulta para id_reserva {id_reserva}: {e}")
            return []
