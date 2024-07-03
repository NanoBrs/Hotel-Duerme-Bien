import tkinter as tk
from tkcalendar import Calendar
from datetime import date

def seleccionar_fecha():
    entrada = cal_entrada.get_date()
    salida = cal_salida.get_date()
    print(f"Fecha de entrada: {entrada}")
    print(f"Fecha de salida: {salida}")

root = tk.Tk()
root.title("Filtrar por Fecha")
root.geometry("1000x480")

lbl_entrada = tk.Label(root, text="Entrada")
lbl_entrada.place(x=250, y=50)

lbl_salida = tk.Label(root, text="Salida")
lbl_salida.place(x=550, y=50)

# Obtener la fecha actual
fecha_actual = date.today()

cal_entrada = Calendar(root, selectmode='day', year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day)
cal_entrada.place(x=200, y=100)

cal_salida = Calendar(root, selectmode='day', year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day)
cal_salida.place(x=500, y=100)

btn_buscar = tk.Button(root, text="Buscar", command=seleccionar_fecha, bg="lightgreen")
btn_buscar.place(x=450, y=350)

root.mainloop()
