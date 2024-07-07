import calendar
import datetime
import tkinter as tk

# Crear la ventana principal
root = tk.Tk()
root.title("Calendario")
parent = root
citas = []
root.resizable(False, False)
# Funcion para obtener todos los dias entre dos fechas
def obtener_dias_entre_fechas(fecha_inicio, fecha_fin):
    dias = []
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        dias.append((fecha_actual.day, fecha_actual.month, fecha_actual.year))
        fecha_actual += datetime.timedelta(days=1)
    return dias

# Funcion para obtener todos los dias rojos a partir de multiples rangos
def obtener_dias_rojos(rangos):
    dias_rojos = []
    for rango in rangos:
        fecha_inicio, fecha_fin = rango
        dias_rojos.extend(obtener_dias_entre_fechas(fecha_inicio, fecha_fin))
    return dias_rojos

# Clase para la vista del calendario
class VistaCalendario:
    def __init__(self, parent):
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)  # Crear el calendario
        self.anio, self.mes = datetime.date.today().year, datetime.date.today().month  # Obtener anio y mes actuales
        self.wid = []  # Lista para guardar los widgets
        self.dia_seleccionado = None
        self.mes_seleccionado = None
        self.anio_seleccionado = None
        self.nombre_dia = None
        self.COLOR_FLECHAS_CALENDARIO = "#33CCFF"
        self.COLOR_ETIQUETA_CALENDARIO = "#33CCFF"
        self.COLOR_BOTONES_DIA = "#FFFFFF"
        self.COLOR_BOTONES_DIA_CITAS = "#FF9999"
        self.COLOR_BOTONES_DIA_ROJO = "#FF0000"  # Color para dias rojos
        self.configurar(self.anio, self.mes)  # Configurar el calendario

    # Metodo para limpiar los widgets
    def limpiar(self):
        for w in self.wid:
            w.grid_forget()
            w.destroy()
        self.wid = []

    # Metodo para ir al mes anterior
    def ir_anterior(self):
        self.limpiar()
        if self.mes == 1:
            self.anio -= 1
            self.mes = 12
        else:
            self.mes -= 1
        self.configurar(self.anio, self.mes, dias_rojos)

    # Metodo para ir al mes siguiente
    def ir_siguiente(self):
        self.limpiar()
        if self.mes == 12:
            self.anio += 1
            self.mes = 1
        else:
            self.mes += 1
        self.configurar(self.anio, self.mes, dias_rojos)

    # Metodo para seleccionar un dia
    def seleccion(self, dia, nombre):
        self.dia_seleccionado = dia
        self.mes_seleccionado = self.mes
        self.anio_seleccionado = self.anio
        self.nombre_dia = nombre

    # Metodo para configurar el calendario
    def configurar(self, a, m, dias_rojos=[]):
        self.limpiar()
        contador_dias = 1

        # Crear y mostrar la etiqueta con el mes y anio
        etiqueta = tk.Label(self.parent, text=f"{calendar.month_name[m]} {a}", bg=self.COLOR_ETIQUETA_CALENDARIO, font=("Arial", 12, "bold"))
        etiqueta.grid(row=0, columnspan=5, sticky="w")
        self.wid.append(etiqueta)

        # Boton para ir al mes anterior
        boton_anterior = tk.Button(self.parent, text="<", bg=self.COLOR_FLECHAS_CALENDARIO, command=self.ir_anterior)
        boton_anterior.grid(row=1, column=0, sticky="w")
        self.wid.append(boton_anterior)

        # Boton para ir al mes siguiente
        boton_siguiente = tk.Button(self.parent, text=">", bg=self.COLOR_FLECHAS_CALENDARIO, command=self.ir_siguiente)
        boton_siguiente.grid(row=1, column=4, sticky="e")
        self.wid.append(boton_siguiente)

        # Mostrar los nombres de los dias de la semana
        for i in range(7):
            etiqueta_dia = tk.Label(self.parent, text=calendar.day_abbr[i], bg=self.COLOR_ETIQUETA_CALENDARIO)
            etiqueta_dia.grid(row=2, column=i, sticky="w")
            self.wid.append(etiqueta_dia)

        # Mostrar los dias del mes
        for w, semana in enumerate(self.cal.monthdayscalendar(a, m), 3):
            for d, dia in enumerate(semana):
                if dia != 0:
                    # Seleccionar el color del boton segun si es dia rojo o tiene cita
                    color = self.COLOR_BOTONES_DIA_CITAS if (dia, m, a) in citas else (self.COLOR_BOTONES_DIA_ROJO if (dia, m, a) in dias_rojos else self.COLOR_BOTONES_DIA)
                    btn = tk.Button(self.parent, text=dia, width=2, height=2, bg=color, command=lambda dia=dia: self.seleccion(dia, calendar.day_name[d]))
                    btn.grid(row=w, column=d)
                    self.wid.append(btn)

# Definir multiples rangos de dias rojos
rangos_dias_rojos = [
    (datetime.date(2024, 6, 1), datetime.date(2024, 6, 5)),
    (datetime.date(2024, 6, 7), datetime.date(2024, 6, 9)),
    (datetime.date(2024, 6, 22), datetime.date(2024, 6, 29))
]

# Obtener todos los dias rojos a partir de los rangos definidos
dias_rojos = obtener_dias_rojos(rangos_dias_rojos)

# Crear la vista del calendario y configurarla
vista_calendario = VistaCalendario(parent)
vista_calendario.configurar(2024, 6, dias_rojos)

# Funcion para actualizar y refrescar el calendario
def actualizar_y_refrescar():
    dias_rojos = [...] 
    vista_calendario.configurar(vista_calendario.anio, vista_calendario.mes, dias_rojos)

# Iniciar el bucle principal de la interfaz grafica
root.mainloop()
