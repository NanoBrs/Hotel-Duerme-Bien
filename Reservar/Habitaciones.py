import tkinter as tk

# Definir la ventana principal
ventana = tk.Tk()
ventana.title("Seleccion de habitacion")
ventana.geometry("1500x700")

# Definir las imágenes de las habitaciones
imagen_habitacion1 = tk.PhotoImage(file="img/reserva/habitacion1.png")
imagen_habitacion2 = tk.PhotoImage(file="img/reserva/habitacion2.png")
imagen_habitacion3 = tk.PhotoImage(file="img/reserva/habitacion3.png")
imagen_habitacion4 = tk.PhotoImage(file="img/reserva/habitacion4.png")
imagen_habitacion5 = tk.PhotoImage(file="img/reserva/habitacion5.png")

# Definir las etiquetas de las imágenes
etiqueta_habitacion1 = tk.Label(ventana, image=imagen_habitacion1)
etiqueta_habitacion2 = tk.Label(ventana, image=imagen_habitacion2)
etiqueta_habitacion3 = tk.Label(ventana, image=imagen_habitacion3)
etiqueta_habitacion4 = tk.Label(ventana, image=imagen_habitacion4)
etiqueta_habitacion5 = tk.Label(ventana, image=imagen_habitacion5)

# Definir variables para controlar el índice de la imagen actual
indice_imagen_actual = 1

# Función para cambiar la imagen a la izquierda
def cambiar_imagen_izquierda():
    global indice_imagen_actual
    if indice_imagen_actual == 1:
        indice_imagen_actual = 5
    else:
        indice_imagen_actual -= 1
    actualizar_imagen()

# Función para cambiar la imagen a la derecha
def cambiar_imagen_derecha():
    global indice_imagen_actual
    if indice_imagen_actual == 5:
        indice_imagen_actual = 1
    else:
        indice_imagen_actual += 1
    actualizar_imagen()

# Función para actualizar la imagen en la pantalla
def actualizar_imagen():
    if indice_imagen_actual == 1:
        print("1")
        etiqueta_habitacion1.config(image=imagen_habitacion1)
        etiqueta_habitacion2.config(image=imagen_habitacion2)
        etiqueta_habitacion3.config(image=imagen_habitacion3)
        etiqueta_habitacion4.config(image=imagen_habitacion4)
        etiqueta_habitacion5.config(image=imagen_habitacion5)
    elif indice_imagen_actual == 2:
        print("2")
        etiqueta_habitacion1.config(image=imagen_habitacion2)
        etiqueta_habitacion2.config(image=imagen_habitacion3)
        etiqueta_habitacion3.config(image=imagen_habitacion4)
        etiqueta_habitacion4.config(image=imagen_habitacion5)
        etiqueta_habitacion5.config(image=imagen_habitacion1)
    elif indice_imagen_actual == 3:
        print("3")
        etiqueta_habitacion1.config(image=imagen_habitacion3)
        etiqueta_habitacion2.config(image=imagen_habitacion4)
        etiqueta_habitacion3.config(image=imagen_habitacion5)
        etiqueta_habitacion4.config(image=imagen_habitacion1)
        etiqueta_habitacion5.config(image=imagen_habitacion2)
    elif indice_imagen_actual == 4:
        print("4")
        etiqueta_habitacion1.config(image=imagen_habitacion4)
        etiqueta_habitacion2.config(image=imagen_habitacion5)
        etiqueta_habitacion3.config(image=imagen_habitacion1)
        etiqueta_habitacion4.config(image=imagen_habitacion2)
        etiqueta_habitacion5.config(image=imagen_habitacion3)
    else:
        etiqueta_habitacion1.config(image=imagen_habitacion5)


# Definir las descripciones de las habitaciones
descripcion_habitacion1 = tk.Label(ventana, text="Habitacion 1: Descripcion breve")
descripcion_habitacion2 = tk.Label(ventana, text="Habitacion 2: Descripcion breve")
descripcion_habitacion3 = tk.Label(ventana, text="Habitacion 3: Descripcion breve")
descripcion_habitacion4 = tk.Label(ventana, text="Habitacion 4: Descripcion breve")
descripcion_habitacion5 = tk.Label(ventana, text="Habitacion 5: Descripcion breve")

# Colocar los elementos en la ventana
etiqueta_habitacion1.place(x=75, y=37)
etiqueta_habitacion2.place(x=362, y=37)
etiqueta_habitacion3.place(x=650, y=37)
etiqueta_habitacion4.place(x=937, y=37)
etiqueta_habitacion5.place(x=1215, y=37)

descripcion_habitacion1.place(x=75, y=423)
descripcion_habitacion2.place(x=362, y=423)
descripcion_habitacion3.place(x=650, y=423)
descripcion_habitacion4.place(x=937, y=423)
descripcion_habitacion5.place(x=1215, y=423)

# Definir los botones
boton_reservar1 = tk.Button(ventana, text="Reservar", command=lambda: reservar_habitacion(1))
boton_reservar2 = tk.Button(ventana, text="Reservar", command=lambda: reservar_habitacion(2))
boton_reservar3 = tk.Button(ventana, text="Reservar", command=lambda: reservar_habitacion(3))
boton_reservar4 = tk.Button(ventana, text="Reservar", command=lambda: reservar_habitacion(4))
boton_reservar5 = tk.Button(ventana, text="Reservar", command=lambda: reservar_habitacion(5))

boton_izquierda = tk.Button(ventana, text="<-",command=cambiar_imagen_izquierda)
boton_derecha = tk.Button(ventana, text="->",command=cambiar_imagen_derecha)

boton_informacion1 = tk.Button(ventana, text="Informacion", command=lambda: informacion_habitacion(1))
boton_informacion2 = tk.Button(ventana, text="Informacion", command=lambda: informacion_habitacion(2))
boton_informacion3 = tk.Button(ventana, text="Informacion", command=lambda: informacion_habitacion(3))
boton_informacion4 = tk.Button(ventana, text="Informacion", command=lambda: informacion_habitacion(4))
boton_informacion5 = tk.Button(ventana, text="Informacion", command=lambda: informacion_habitacion(5))


# Colocar los botones en la ventana
boton_reservar1.place(x=75, y=621)
boton_reservar2.place(x=362, y=621)
boton_reservar3.place(x=650, y=621)
boton_reservar4.place(x=937, y=621)
boton_reservar5.place(x=1215, y=621)

boton_izquierda.place(x=19, y=324)
boton_derecha.place(x=1430, y=324)

boton_informacion1.place(x=75, y=565)
boton_informacion2.place(x=362, y=565)
boton_informacion3.place(x=650, y=565)
boton_informacion4.place(x=937, y=565)
boton_informacion5.place(x=1215, y=565)


ventana.mainloop()