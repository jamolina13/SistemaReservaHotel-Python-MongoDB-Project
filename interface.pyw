from tkinter import *
from pymongo import MongoClient
from conexion import *
from datetime import datetime
from bson.objectid import ObjectId

import tkinter

#//////////////creacion de la ventana
raiz = Tk()

raiz.title("Venta Principal")  # Titulo a la ventana

raiz.resizable(0, 0)# recibe valores true o false
raiz.iconbitmap('empre.ico') #cambiar el icono de la ventana
raiz.geometry("1300x1500")

# ///////////////////////////////////////FRAME//////////////////////////////////////////////////
framePrincipal = Frame(raiz)
framePrincipal.pack()
framePrincipal.config(width="1300", height="75")
framePrincipal.config(bg='green')


frameTabla = Frame(raiz)
frameTabla.pack()
frameTabla.config(width="1300", height="525")

frame2 = Frame(raiz)
frame2.pack()
frame2.config(width="1300", height="525")
frame2.config()

#/////////////////////////////////////////////////////////////////////////////////

titulo = Label(framePrincipal,
               text="Sistema de Registro de Clientes - Hotel Empresaurios 2.0", font=('Times Roman', 20, 'bold'), background='green')
titulo.place(x=300, y=10)

ID_USUARIO = ""

#///////////////////////////////////////////METODOS//////////////////////////////////////////////////////////////////////////
def mostrarDatos(cedula=""):
    objetoBuscar={}
    if len(cedula)!=0:
        objetoBuscar["cedula"]=cedula
    try:
        registros = tabla.get_children()
        for registro in registros:
            tabla.delete(registro)
        for documento in coleccion.find(objetoBuscar):
            tabla.insert('', 0, text=documento["_id"], values=(documento["foto"], documento["nombre"],
                                                               documento["apellido"], documento["cedula"], documento["telefono"], documento["correo"], documento["direccion"], documento["tipoHabitacion"], documento['fechaI'], documento['fechaF'], str(documento['tarifa'])))
        cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo exedido "+errorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a mongodb "+errorConexion)

#/////////////VALIDACIONES
def crearRegistro():
    if len(foto.get()) != 0 and len(nombre.get()) != 0 and len(apellido.get()) != 0 and len(cedula.get()) != 0 and len(telefono.get()) != 0 and len(correo.get()) != 0 and len(direccion.get()) != 0 and len(tipoA.get()) != 0 and len(fechaI.get()) != 0 and len(fechaF.get()) != 0 and len(tarifa.get()) != 0:
        if nombre.get().isalpha():
            if apellido.get().isalpha():
                if tipoA.get().isalpha():
                    if cedula.get().isdigit():
                        if len(cedula.get())==10:
                            if telefono.get().isdigit():
                                if  len(telefono.get())==10: 
                                    if "@" in correo.get() :
                                        if tipoA.get().isalpha:
                                            try:
                                                (datetime.strptime(fechaI.get(), '%Y-%m-%d') and  datetime.strptime(fechaF.get(), '%Y-%m-%d')) 
                                                if fechaI.get() != fechaF.get():
                                                
                                                    try:
                                                        documento = {"foto": foto.get(), "nombre": nombre.get(), "apellido": apellido.get(), "cedula": cedula.get(), "telefono": telefono.get(), "correo": correo.get(
                                                        ), "direccion": direccion.get(), "tipoHabitacion": tipoA.get(), "fechaI": fechaI.get(), "fechaF": fechaF.get(), "tarifa": tarifa.get()}
                                                        coleccion.insert(documento)
                                                        foto.delete(0, END)
                                                        apellido.delete(0, END)
                                                        nombre.delete(0, END)
                                                        cedula.delete(0, END)
                                                        telefono.delete(0, END)
                                                        correo.delete(0, END)
                                                        direccion.delete(0, END)
                                                        tipoA.delete(0, END)
                                                        fechaI.delete(0, END)
                                                        fechaF.delete(0, END)
                                                        tarifa.delete(0, END)
                                                        messagebox.showinfo("CORRECTO","Usuario creado exitosamente")
                                                    except pymongo.errors.ConnectionFailure as error:
                                                        print(error)
                                                else:
                                                    messagebox.showerror("ERROR","Las fechas de ingreso y salida no deben ser las mismas")
                                            except ValueError:
                                                messagebox.showerror("ERROR","El formato de la fecha es incorrecto, example: Y-m-d")      
                                        else:
                                            messagebox.showerror("ERROR","Solo se admiten letras en el tipo de habitación")
                                    else:
                                        messagebox.showerror("ERROR","Debe contener un @: example@.com")
                                else:
                                    messagebox.showerror("ERROR","Solo se admiten 10 numeros en el telefono")
                            else:
                                messagebox.showerror("ERROR","Solo se admiten numeros en el telefono")
                        else:
                             messagebox.showerror("ERROR","Solo se admiten 10 numeros en el cedula")
                    else:
                        messagebox.showerror("ERROR","Solo se admiten numeros la cédula")
                else:
                    messagebox.showerror("ERROR","Solo se admiten letras en el tipo de habitación")
            else:
                messagebox.showerror("ERROR","Solo se admiten letras en el apellido")
        else:
            messagebox.showerror("ERROR","Solo se admiten letras en el nombre")
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrarDatos()


def dobleClickTabla(event):
    global ID_USUARIO
    ID_USUARIO = str(tabla.item(tabla.selection())["text"])
    print(ID_USUARIO)
    documento = coleccion.find({"_id": ObjectId(ID_USUARIO)})[0]
    print(documento)
    foto.delete(0, END)
    foto.insert(0, documento["foto"])
    nombre.delete(0, END)
    nombre.insert(0, documento["nombre"])
    apellido.delete(0, END)
    apellido.insert(0, documento["apellido"])
    cedula.delete(0, END)
    cedula.insert(0, documento["cedula"])
    telefono.delete(0, END)
    telefono.insert(0, documento["cedula"])
    correo.delete(0, END)
    correo.insert(0, documento["correo"])
    direccion.delete(0, END)
    direccion.insert(0, documento["direccion"])
    tipoA.delete(0, END)
    tipoA.insert(0, documento["tipoHabitacion"])
    fechaI.delete(0, END)
    fechaI.insert(0, documento["fechaI"])
    fechaF.delete(0, END)
    fechaF.insert(0, documento["fechaF"])
    tarifa.delete(0, END)
    tarifa.insert(0, documento["tarifa"])
    crear["state"] = "disabled"
    editar["state"] = "normal"
    borrar["state"] = "normal"


def editarRegistro():
    global ID_USUARIO
    if len(foto.get()) != 0 and len(nombre.get()) != 0 and len(apellido.get()) != 0 and len(cedula.get()) != 0 and len(telefono.get()) != 0 and len(correo.get()) != 0 and len(direccion.get()) != 0 and len(tipoA.get()) != 0 and len(fechaI.get()) != 0 and len(fechaF.get()) != 0 and len(tarifa.get()) != 0:
        if nombre.get().isalpha():
            if apellido.get().isalpha():
                if tipoA.get().isalpha():
                    if cedula.get().isdigit():
                        if len(cedula.get())==10:
                            if telefono.get().isdigit():
                                if  len(telefono.get())==10: 
                                    if "@" in correo.get() :
                                        if tipoA.get().isalpha:
                                            try:
                                                (datetime.strptime(fechaI.get(), '%Y-%m-%d') and  datetime.strptime(fechaF.get(), '%Y-%m-%d')) 
                                                if fechaI.get() != fechaF.get():
                                                
                                                    try:
                                                            idBuscar = {"_id": ObjectId(ID_USUARIO)}
                                                            nuevosValores = {"foto": foto.get(), "nombre": nombre.get(), "apellido": apellido.get(), "cedula": cedula.get(), "telefono": telefono.get(
                                                            ), "correo": correo.get(), "direccion": direccion.get(), "tipoHabitacion": tipoA.get(), "fechaI": fechaI.get(), "fechaF": fechaF.get(), "tarifa": tarifa.get()}
                                                            coleccion.update(idBuscar, nuevosValores)
                                                            foto.delete(0, END)
                                                            nombre.delete(0, END)
                                                            apellido.delete(0, END)
                                                            cedula.delete(0, END)
                                                            telefono.delete(0, END)
                                                            correo.delete(0, END)
                                                            direccion.delete(0, END)
                                                            tipoA.delete(0, END)
                                                            fechaI.delete(0, END)
                                                            fechaF.delete(0, END)
                                                            tarifa.delete(0, END)
                                                    except pymongo.errors.ConnectionFailure as error:
                                                            print(error)
                                                else:
                                                    messagebox.showerror("ERROR","Las fechas de ingreso y salida no deben ser las mismas")
                                                    dobleClickTabla()
                                            except ValueError:
                                                messagebox.showerror("ERROR","El formato de la fecha es incorrecto, example: Y-m-d") 
                                                dobleClickTabla()     
                                        else:
                                            messagebox.showerror("ERROR","Solo se admiten letras en el tipo de habitación")
                                            dobleClickTabla()
                                    else:
                                        messagebox.showerror("ERROR","Debe contener un @: example@.com")
                                        dobleClickTabla()
                                else:
                                    messagebox.showerror("ERROR","Solo se admiten 10 numeros en el telefono")
                                    dobleClickTabla()
                            else:
                                messagebox.showerror("ERROR","Solo se admiten numeros en el telefono")
                                dobleClickTabla()
                        else:
                             messagebox.showerror("ERROR","Solo se admiten 10 numeros en el cedula")
                             dobleClickTabla()
                    else:
                        messagebox.showerror("ERROR","Solo se admiten numeros la cédula")
                        dobleClickTabla()
                else:
                    messagebox.showerror("ERROR","Solo se admiten letras en el tipo de habitación")
                    dobleClickTabla()
            else:
                messagebox.showerror("ERROR","Solo se admiten letras en el apellido")
                dobleClickTabla()
        else:
            messagebox.showerror("ERROR","Solo se admiten letras en el nombre")
            dobleClickTabla()
    else:
        messagebox.showerror("ERROR","Los campos no pueden estar vacios")
    mostrarDatos()
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"]="disabled"


def borrarRegistro():
    global ID_USUARIO
    try:
        idBuscar = {"_id": ObjectId(ID_USUARIO)}
        coleccion.delete_one(idBuscar)
        foto.delete(0, END)
        nombre.delete(0, END)
        apellido.delete(0, END)
        cedula.delete(0, END)
        telefono.delete(0, END)
        correo.delete(0, END)
        direccion.delete(0, END)
        tipoA.delete(0, END)
        fechaI.delete(0, END)
        fechaF.delete(0, END)
        tarifa.delete(0, END)
    except pymongo.errors.ConnectionFailure as error:
        print(error)
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
    mostrarDatos()

def buscarRegistro():
    if len(buscarCedula.get())!=0:
        if buscarCedula.get().isdigit():
            if len(buscarCedula.get())<=10:
                mostrarDatos(buscarCedula.get())
            else:
                messagebox.showerror("ERROR","No debe ingresar más de 10 dígitos")   
        else:
            messagebox.showerror("ERROR","Los campos deben ser numericos")
    else:
        mostrarDatos()

#///////////////////////////// SE CREA LA TABLA
tabla = ttk.Treeview(frameTabla, height=15,  columns=(
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'))
tabla.grid(row=1, column=0, columnspan=1)
tabla.column("#0", width=60)
tabla.column("a", width=80, anchor=CENTER)
tabla.column("b", width=80, anchor=CENTER)
tabla.column("c", width=80, anchor=CENTER)
tabla.column("d", width=80, anchor=CENTER)
tabla.column("e", width=80, anchor=CENTER)
tabla.column("f", width=200, anchor=CENTER)
tabla.column("g", width=200, anchor=CENTER)
tabla.column("h", width=110, anchor=CENTER)
tabla.column("i", width=110, anchor=CENTER)
tabla.column("j", width=110, anchor=CENTER)
tabla.column("k", width=80, anchor=CENTER)
tabla.column("l", width=80, anchor=CENTER)

tabla.heading("#0", text="ID")
tabla.heading("#1", text="FOTO")
tabla.heading("#2", text="NOMBRE")
tabla.heading("#3", text="APELLIDO")
tabla.heading("#4", text="CEDULA")
tabla.heading("#5", text="TELEFONO")
tabla.heading("#6", text="CORREO")
tabla.heading("#7", text="DIRECCION")
tabla.heading("#8", text="TIPO HABITACIÓN")
tabla.heading("#9", text="FECHA INGRESO")
tabla.heading("#10", text="FECHA SALIDA")
tabla.heading("#11", text="TARIFA")


tabla.bind("<Double-Button-1>", dobleClickTabla)

#///////////////COMPONENTES

Label(frame2, text="Configuración de los usuarios",
      font=('Times Roman', 15, 'bold')).grid(row=0, column=1)
Label(frame2).grid(row=1, column=0)
Label(frame2, text="FOTO", font=('Times Roman', 10, 'bold')).grid(row=2, column=0)
foto = Entry(frame2, width=40)
foto.grid(row=2, column=1)

Label(frame2, text="NOMBRE", font=('Times Roman', 10, 'bold')).grid(row=3, column=0)
nombre = Entry(frame2, width=40)
nombre.grid(row=3, column=1)

Label(frame2, text="APELLIDO", font=('Times Roman', 10, 'bold')).grid(row=4, column=0)
apellido = Entry(frame2, width=40)
apellido.grid(row=4, column=1)

Label(frame2, text="CEDULA", font=('Times Roman', 10, 'bold')).grid(row=5, column=0)
cedula = Entry(frame2, width=40)
cedula.grid(row=5, column=1)

Label(frame2, text="TELEFONO", font=('Times Roman', 10, 'bold')).grid(row=6, column=0)
telefono = Entry(frame2, width=40)
telefono.grid(row=6, column=1)

Label(frame2, text="CORREO", font=('Times Roman', 10, 'bold')).grid(row=7, column=0)
correo = Entry(frame2, width=40)
correo.grid(row=7, column=1)

Label(frame2, text="DIRECCION", font=('Times Roman', 10, 'bold')).grid(row=8, column=0)
direccion = Entry(frame2, width=40)
direccion.grid(row=8, column=1)


Label(frame2, text="TIPO HABITACIÓN", font=('Times Roman', 10, 'bold')).grid(row=9, column=0)
tipoA = Entry(frame2, width=40)
tipoA.grid(row=9, column=1)


Label(frame2, text="FECHA INGRESO", font=('Times Roman', 10, 'bold')).grid(row=10, column=0)
fechaI = Entry(frame2, width=40)
fechaI.grid(row=10, column=1)


Label(frame2, text="FECHA SALIDA", font=('Times Roman', 10, 'bold')).grid(row=11, column=0)
fechaF = Entry(frame2, width=40)
fechaF.grid(row=11, column=1)


Label(frame2, text="TARIFA", font=('Times Roman', 10, 'bold')).grid(row=12, column=0)
tarifa = Entry(frame2, width=40)
tarifa.grid(row=12, column=1)

Label(frame2).grid(row=13, column=0)

Label(frame2).grid(row=16, column=0)
Label(frame2,text="Buscar por cedula", font=('Times Roman', 10, 'bold')).grid(row=17,column=0)

#/////BOTONES
# Boton crear
crear = Button(frame2, text="Crear usuario", width=30, font=(
    'Times Roman', 10, 'bold'), command=crearRegistro, bg="green", fg="black")
crear.grid(row=15, column=0)
# Boton editar
editar = Button(frame2, text="Editar usuario", width=30, font=(
    'Times Roman', 10, 'bold'), command=editarRegistro, bg="blue", fg="black")
editar.grid(row=15, column=1)
editar["state"] = "disabled"
#BOTON BORRAR
borrar = Button(frame2, text="Borrar usuario",width=30, font=(
    'Times Roman', 10, 'bold'), command=borrarRegistro, bg="red", fg="black")
borrar.grid(row=15, column=2)
borrar["state"] = "disabled"

buscarCedula=Entry(frame2, width=40)
buscarCedula.grid(row=17,column=1)
Label(frame2).grid(row=18, column=0)
#BOTON BUSCAR
buscar=Button(frame2,text="Buscar usuario ",command=buscarRegistro,bg="blue",fg="black",width=30, font=(
    'Times Roman', 10, 'bold'))
buscar.grid(row=19,columnspan=3)

mostrarDatos()

raiz.mainloop()  # siempre debe estar al final este método
