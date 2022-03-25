# pylint: disable=line-too-long

"""Modulos tkinter para vistas, modulo re para expresiones regulares, modulo mysql para utilizar motor de base de datos"""
from tkinter import Tk, Label, Entry, Frame, Button, StringVar, END
from tkinter.ttk import Treeview
from tkinter.messagebox import showerror, showinfo, askyesno
import re
import tkcalendar as tk_calendar
import mysql.connector


#################################################################################################
# FUNCIONES PARA TRABAJAR CON BASE DE DATOS MYSQL
#################################################################################################


def crear_base_de_datos():
    """Crea la base de datos en caso de que no exista"""
    mibase = mysql.connector.connect(host="localhost", user="root", passwd="")
    micursor = mibase.cursor()
    micursor.execute("CREATE DATABASE IF NOT EXISTS mi_empresa")


# ------------------------------------------------------------------------------------------------#


def crear_tabla():
    """Crea la tabla personal en la base de datos en caso de que no exista"""
    mibase = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="mi_empresa"
    )
    micursor = mibase.cursor()
    micursor.execute(
        "CREATE TABLE IF NOT EXISTS personal(dni VARCHAR(8) NOT NULL PRIMARY KEY, nombre VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, apellido VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, empresa VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, telefono VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, email VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, direccion VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, nacimiento VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL)"
    )


# ------------------------------------------------------------------------------------------------#


def insertar_registro():
    """Inserta nuevos registros en la base de datos"""
    mibase = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="mi_empresa"
    )
    if (
        var_dni.get() == ""
        or var_nombre.get() == ""
        or var_apellido.get() == ""
        or var_empresa.get() == ""
        or var_telefono.get() == ""
        or var_email.get() == ""
        or var_direccion.get() == ""
        or var_nacimiento.get() == ""
    ):
        mensaje_error("Debe completar todos los datos")
    else:
        try:
            micursor = mibase.cursor()
            sql = "INSERT INTO personal (dni, nombre, apellido, empresa, telefono, email, direccion, nacimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            datos = (
                var_dni.get(),
                var_nombre.get(),
                var_apellido.get(),
                var_empresa.get(),
                var_telefono.get(),
                var_email.get(),
                var_direccion.get(),
                var_nacimiento.get(),
            )
            micursor.execute(sql, datos)
            mibase.commit()
            mensaje_ok("La informacion fue agregada")
            vaciar_entry()
        except:
            mensaje_error("El DNI ingresado ya se encuentra registrado")


# ------------------------------------------------------------------------------------------------#


def borrar_registro():
    """Elimina registros de la base de datos"""
    flag = False
    mibase = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="mi_empresa"
    )
    if askyesno("Borrar", "Esta seguro que desea borrar la informacion?"):
        micursor = mibase.cursor()
        sql = "DELETE FROM personal WHERE dni = %s"
        dato = (var_dni.get(),)
        sql_validar = "SELECT dni FROM personal"
        micursor.execute(sql_validar)
        resultado_validar = micursor.fetchall()
        for contador in resultado_validar:
            if dato == contador:
                micursor.execute(sql, dato)
                mibase.commit()
                mensaje_ok("La informacion fue borrada")
                flag = True
                vaciar_entry()
        if not flag:
            mensaje_error(
                "No se pudo realizar la eliminacion de datos. Intente nuevamente"
            )


# ------------------------------------------------------------------------------------------------#


def buscar_registro():
    """Busca registros de la base de datos para poder actualizarlos o trabajarlos"""
    mibase = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="mi_empresa"
    )
    micursor = mibase.cursor()
    sql = "SELECT * FROM personal WHERE dni = %s"
    dato = (var_dni.get(),)
    try:
        micursor.execute(sql, dato)
        resultado = micursor.fetchall()
        for fila in resultado:
            tv_tabla.insert(
                "",
                "end",
                text="",
                values=(
                    fila[0],
                    fila[1],
                    fila[2],
                    fila[3],
                    fila[4],
                    fila[5],
                    fila[6],
                    fila[7],
                ),
            )
        vaciar_entry()
        insertar_elemento(fila)
    except:
        mensaje_error("El DNI ingresado no existe")
        vaciar_entry()


# ------------------------------------------------------------------------------------------------#


def actualizar_registro():
    """Actualizar los registros de la DB"""
    flag = False
    mibase = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="mi_empresa"
    )
    if (
        var_dni.get() == ""
        or var_nombre.get() == ""
        or var_apellido.get() == ""
        or var_empresa.get() == ""
        or var_telefono.get() == ""
        or var_email.get() == ""
        or var_direccion.get() == ""
        or var_nacimiento.get() == ""
    ):
        mensaje_error("Debe completar todos los datos")
    else:
        if askyesno("Modificar", "Esta seguro que desea modificar la informacion?"):
            micursor = mibase.cursor()
            sql = "UPDATE personal SET nombre = %s, apellido = %s, empresa = %s, telefono = %s, email = %s, direccion = %s, nacimiento = %s WHERE dni = %s"
            dato = (
                var_nombre.get(),
                var_apellido.get(),
                var_empresa.get(),
                var_telefono.get(),
                var_email.get(),
                var_direccion.get(),
                var_nacimiento.get(),
                var_dni.get(),
            )
            sql_validar = "SELECT dni FROM personal"
            dato_validar = (var_dni.get(),)
            micursor.execute(sql_validar)
            resultado_validar = micursor.fetchall()
            for contador in resultado_validar:
                if dato_validar == contador:
                    micursor.execute(sql, dato)
                    mibase.commit()
                    mensaje_ok("La informacion fue modificada")
                    flag = True
                    vaciar_entry()
            if not flag:
                mensaje_error(
                    "No se pudo realizar la modificacion de datos. Intente nuevamente"
                )


#################################################################################################
# NOTIFICACIONES MEDIANTE CAJAS DE DIALOGO
#################################################################################################


def mensaje_error(desc_error):
    """Muestra mensaje de error"""
    showerror("Error", desc_error)


# ------------------------------------------------------------------------------------------------#


def mensaje_ok(desc_mensaje):
    """Muestra mensaje de informacion"""
    showinfo("Mensaje", desc_mensaje)


#################################################################################################
# FUNCIONES REGEX
#################################################################################################


def validar_email(evento):
    """Validacion mediante expresiones regulares de los campos"""
    cadena_mail = var_email.get()
    patron_mail = "^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
    if not re.match(patron_mail, cadena_mail):
        mensaje_error("E-mail invalido")
    ent_nombre.focus()


# ------------------------------------------------------------------------------------------------#


def validar_nacimiento(evento):
    """Validacion mediante expresiones regulares de los campos"""
    cadena_nacimiento = var_nacimiento.get()
    patron_nacimiento = "^^(((0[1-9]|[12][0-9]|30)[-/]?(0[13-9]|1[012])|31[-/]?(0[13578]|1[02])|(0[1-9]|1[0-9]|2[0-8])[-/]?02)[-/]?[0-9]{4}|29[-/]?02[-/]?([0-9]{2}(([2468][048]|[02468][48])|[13579][26])|([13579][26]|[02468][048]|0[0-9]|1[0-6])00))$"
    if not re.match(patron_nacimiento, cadena_nacimiento):
        mensaje_error("Fecha invalida")
    ent_nombre.focus()


# ------------------------------------------------------------------------------------------------#


def validar_dni(evento):
    """Validacion mediante expresiones regulares de los campos"""
    cadena_dni = var_dni.get()
    patron_dni = "^[0-9]{7,8}$"
    if not re.match(patron_dni, cadena_dni):
        mensaje_error("DNI invalido")
    ent_nombre.focus()


# ------------------------------------------------------------------------------------------------#


def validar_telefono(evento):
    """Validacion mediante expresiones regulares de los campos"""
    cadena_telefono = var_telefono.get()
    patron_telefono = "^[0-9]{10,20}$"
    if not re.match(patron_telefono, cadena_telefono):
        mensaje_error("Fecha invalida")
    ent_nombre.focus()


#################################################################################################
# FUNCIONES VARIAS
#################################################################################################


def vaciar_entry():
    """Deja todos los entry de la vista vacios para poder utilizarlos nuevamente"""
    ent_dni.delete(0, END)
    ent_nombre.delete(0, END)
    ent_apellido.delete(0, END)
    ent_empresa.delete(0, END)
    ent_telefono.delete(0, END)
    ent_email.delete(0, END)
    ent_direccion.delete(0, END)
    ent_nacimiento.delete(0, END)


# ------------------------------------------------------------------------------------------------#


def insertar_elemento(val_elem):
    """Llena con los datos especificados los entry de la vista para poder utilizarlos"""
    ent_dni.insert(0, val_elem[0])
    ent_nombre.insert(0, val_elem[1])
    ent_apellido.insert(0, val_elem[2])
    ent_empresa.insert(0, val_elem[3])
    ent_telefono.insert(0, val_elem[4])
    ent_email.insert(0, val_elem[5])
    ent_direccion.insert(0, val_elem[6])
    ent_nacimiento.insert(0, val_elem[7])


# ------------------------------------------------------------------------------------------------#


def seleccionar_elemento(evento):
    """Selecciona el elemento del TreeView y los coloca en los entry de la vista (previo a borrar los valores de los entry en caso de que no esten vacios)"""
    item_seleccionado = tv_tabla.focus()
    valores = tv_tabla.item(item_seleccionado, "values")
    vaciar_entry()
    insertar_elemento(valores)


# ------------------------------------------------------------------------------------------------#


def registros_inicio_app():
    """Funcion para desarrollo. Rellena la base de datos con 4 registros por defecto"""
    mibase = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="mi_empresa"
    )
    datos = [
        (
            "11111111",
            "Juan",
            "Perez",
            "UTNar",
            "1111112222",
            "juan.perez@gmail.com",
            "Moreno 1111",
            "01/01/1989",
        ),
        (
            "22222222",
            "Jose",
            "Lopez",
            "UTNar",
            "1122223333",
            "jose.lopez@gmail.com",
            "Sarratea 2222",
            "02/02/1989",
        ),
        (
            "33333333",
            "Marcos",
            "Gutierrez",
            "UTNar",
            "1133334444",
            "marcos.gutierrez@gmail.com",
            "Malabia 3333",
            "03/03/1989",
        ),
        (
            "44444444",
            "Matias",
            "Gonzalez",
            "UTNar",
            "1144445555",
            "matias.gonzalez@gmail.com",
            "Pedriel 4444",
            "02/02/1989",
        ),
    ]
    micursor = mibase.cursor()
    sql = "INSERT IGNORE INTO personal (dni, nombre, apellido, empresa, telefono, email, direccion, nacimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    for contador in datos:
        micursor.execute(sql, contador)
        mibase.commit()


#################################################################################################
# MAIN.PY
#################################################################################################

crear_base_de_datos()
crear_tabla()
registros_inicio_app()

root = Tk()

#################################################################################################
# CENTRAR LA POSICION DE LA VENTANA(APLICACION) CON RESPECTO A LA PANTALLA
#################################################################################################

ANCHO_VENTANA = 820
ALTO_VENTANA = 600
x_ventana = root.winfo_screenwidth() // 2 - ANCHO_VENTANA // 2
y_ventana = root.winfo_screenheight() // 2 - ALTO_VENTANA // 2
POSICION = (
    str(ANCHO_VENTANA)
    + "x"
    + str(ALTO_VENTANA)
    + "+"
    + str(x_ventana)
    + "+"
    + str(y_ventana)
)

#################################################################################################
# CONFIGURACIONES DE ROOT
#################################################################################################

root.title("TP FINAL - DIPLOMATURA INICIAL - DATOS DE PERSONAL")
root.geometry(POSICION)
root.resizable(False, False)

#################################################################################################
# INFORMACION SOLICITADA AL USUARIO
#################################################################################################

var_dni = StringVar()
var_nombre = StringVar()
var_apellido = StringVar()
var_empresa = StringVar()
var_telefono = StringVar()
var_email = StringVar()
var_direccion = StringVar()
var_nacimiento = StringVar()

#################################################################################################
# DIVIDO ROOT EN 4 FRAMES
#################################################################################################

fra_encabezado = Frame(root)
fra_encabezado.grid(row=0, column=0)
fra_principal = Frame(root)
fra_principal.grid(row=1, column=0)
fra_botonera = Frame(root)
fra_botonera.grid(row=2, column=0)
fra_vista = Frame(root)
fra_vista.grid(row=3, column=0)

#################################################################################################
# FRAME ENCABEZADO
#################################################################################################

label_titulo = Label(fra_encabezado, text="---------- PERSONAL ----------")
label_titulo.grid(row=0, column=0, pady=10)

#################################################################################################
# FRAME PRINCIPAL
#################################################################################################

lbl_dni = Label(fra_principal, text="DNI:")
lbl_dni.grid(row=0, column=0, padx=5, pady=10)
ent_dni = Entry(fra_principal, textvariable=var_dni, width=40)
ent_dni.bind("<FocusOut>", validar_dni)
ent_dni.grid(row=0, column=1, padx=10, pady=10)

lbl_nombre = Label(fra_principal, text="Nombre:")
lbl_nombre.grid(row=1, column=0, padx=5, pady=10)
ent_nombre = Entry(fra_principal, textvariable=var_nombre, width=40)
ent_nombre.grid(row=1, column=1, padx=10, pady=10)

lbl_apellido = Label(fra_principal, text="Apellido:")
lbl_apellido.grid(row=2, column=0, padx=5, pady=10)
ent_apellido = Entry(fra_principal, textvariable=var_apellido, width=40)
ent_apellido.grid(row=2, column=1, padx=10, pady=10)

lbl_empresa = Label(fra_principal, text="Empresa:")
lbl_empresa.grid(row=3, column=0, padx=5, pady=10)
ent_empresa = Entry(fra_principal, textvariable=var_empresa, width=40)
ent_empresa.grid(row=3, column=1, padx=10, pady=10)

lbl_telefono = Label(fra_principal, text="Telefono:")
lbl_telefono.grid(row=4, column=0, padx=5, pady=10)
ent_telefono = Entry(fra_principal, textvariable=var_telefono, width=40)
ent_telefono.bind("<FocusOut>", validar_telefono)
ent_telefono.grid(row=4, column=1, padx=10, pady=10)

lbl_email = Label(fra_principal, text="E-mail:")
lbl_email.grid(row=5, column=0, padx=5, pady=10)
ent_email = Entry(fra_principal, textvariable=var_email, width=40)
ent_email.bind("<FocusOut>", validar_email)
ent_email.grid(row=5, column=1, padx=10, pady=10)

lbl_direccion = Label(fra_principal, text="Direccion:")
lbl_direccion.grid(row=6, column=0, padx=5, pady=10)
ent_direccion = Entry(fra_principal, textvariable=var_direccion, width=40)
ent_direccion.grid(row=6, column=1, padx=10, pady=10)

lbl_nacimiento = Label(fra_principal, text="F. Nacimiento:")
lbl_nacimiento.grid(row=7, column=0, padx=5, pady=10)
ent_nacimiento = Entry(fra_principal, textvariable=var_nacimiento, width=40)
ent_nacimiento.bind("<FocusOut>", validar_nacimiento)
ent_nacimiento.grid(row=7, column=1, padx=10, pady=10)

calendario = tk_calendar.Calendar(fra_principal, selectmode="day", year=2021, month=12)
calendario.grid(row=0, column=3, rowspan=4)

lbl_info = Label(
    fra_principal,
    text="DNI / TELEFONO: solo numeros sin \nseparadores ni espacios\nNOMBRE / APELLIDO: Solo letras y espacios\nEMAIL: formato email@email.com\nFECHA: formato dd/mm/aaaa",
)
lbl_info.grid(row=4, column=3, rowspan=4)

#################################################################################################
# FRAME BOTONERA
#################################################################################################

btn_agregar = Button(fra_botonera, text="Agregar", command=insertar_registro)
btn_agregar.grid(row=0, column=0, padx=20, pady=10)

btn_borrar = Button(fra_botonera, text="Borrar", command=borrar_registro)
btn_borrar.grid(row=0, column=1, padx=20, pady=10)

btn_modificar = Button(fra_botonera, text="Modificar", command=actualizar_registro)
btn_modificar.grid(row=0, column=2, padx=20, pady=10)

btn_buscar = Button(fra_botonera, text="Buscar", command=buscar_registro)
btn_buscar.grid(row=0, column=3, padx=20, pady=10)

btn_vaciar_campos = Button(fra_botonera, text="Vaciar Campos", command=vaciar_entry)
btn_vaciar_campos.grid(row=0, column=4, padx=20, pady=10)

#################################################################################################
# FRAME TREEVIEW
#################################################################################################

tv_tabla = Treeview(
    root, columns=("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8"), height=5
)
tv_tabla["show"] = "headings"
tv_tabla.grid(row=3, column=0, columnspan=4, padx=10, pady=10)
tv_tabla.heading("#1", text="DNI")
tv_tabla.column("#1", width=100)
tv_tabla.heading("#2", text="Nombre")
tv_tabla.column("#2", width=100)
tv_tabla.heading("#3", text="Apellido")
tv_tabla.column("#3", width=100)
tv_tabla.heading("#4", text="Empresa")
tv_tabla.column("#4", width=100)
tv_tabla.heading("#5", text="Telefono")
tv_tabla.column("#5", width=100)
tv_tabla.heading("#6", text="E-mail")
tv_tabla.column("#6", width=100)
tv_tabla.heading("#7", text="Direccion")
tv_tabla.column("#7", width=100)
tv_tabla.heading("#8", text="Nacimiento")
tv_tabla.column("#8", width=100)
tv_tabla.bind("<ButtonRelease-1>", seleccionar_elemento)

root.mainloop()
