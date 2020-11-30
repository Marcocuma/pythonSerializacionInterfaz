import pickle
import tkinter as tk
import tkinter.messagebox


from models.contacto import Contacto


class Application(tk.Frame):
    def __init__(self):
        super().__init__(root)
        self.title = "Gestion Contactos"
        self.grid()
        self.arrayContactos = list()
        self.leer()
        self.create_widgets()
        self.recargarLista()


    def create_widgets(self):
        self.listbox = tk.Listbox(root)
        self.listbox.bind("<Double-1>", self.seleccionarContacto)
        self.listbox.grid(row=0, column=0)
        labelTelf = tk.Label(root, text='Telefono')
        labelTelf.grid(row=1, column=0)
        self.textFieldTelefono = tk.Entry(root)
        self.textFieldTelefono.grid(row=2, column=0)
        labelNomb= tk.Label(root, text='Nombre')
        labelNomb.grid(row=3, column=0)
        self.textFieldNombre = tk.Entry(root)
        self.textFieldNombre.grid(row=4, column=0)
        labelApellido = tk.Label(root, text='Apellido')
        labelApellido.grid(row=5, column=0)
        self.textFieldApellido = tk.Entry(root)
        self.textFieldApellido.grid(row=6, column=0)
        self.frame = tk.Frame(root)
        self.frame.grid(row=7,column=0)
        self.botonAniadir = tk.Button(self.frame)
        self.botonAniadir["text"] = "Añadir"
        self.botonAniadir["command"] = self.anadirContacto
        self.botonAniadir.grid(row=8, column=0)
        self.botonDel = tk.Button(self.frame)
        self.botonDel["text"] = "Eliminar"
        self.botonDel["command"] = self.eliminarContacto
        self.botonDel.grid(row=8, column=1)
        self.botonUpd = tk.Button(self.frame)
        self.botonUpd["text"] = "Actualizar"
        self.botonUpd["command"] = self.modificarContacto
        self.botonUpd.grid(row=8, column=2)

    def seleccionarContacto(self,event):
        selection = event.widget.curselection()
        seleccionado = self.arrayContactos.__getitem__(self.listbox.index(selection))
        self.textFieldTelefono.delete("0",tk.END)
        self.textFieldTelefono.insert(tk.END,seleccionado.telefono)
        self.textFieldNombre.delete("0",tk.END)
        self.textFieldNombre.insert(tk.END, seleccionado.nombre)
        self.textFieldApellido.delete("0",tk.END)
        self.textFieldApellido.insert(tk.END, seleccionado.apellidos)

    def recargarLista(self):
        self.listbox.delete(0, tk.END)
        for contacto in self.arrayContactos:
            self.listbox.insert(tk.END, contacto.nombre+" "+contacto.apellidos)

    def anadirContacto(self):
        try:
            telefono = int(self.textFieldTelefono.get())
            nombre = self.textFieldNombre.get()
            apellidos = self.textFieldApellido.get()
            if(not self.comprobarExiste(telefono)):
                self.arrayContactos.append(Contacto(telefono,nombre,apellidos))
                self.guardar()
                self.recargarLista()
            else:
                tkinter.messagebox.showerror(title="Numero duplicado", message="Ese numero ya esta guardado")
        except ValueError:
            tkinter.messagebox.showerror(title="Telefono incorrecto", message="Debe ser un numero")

    def eliminarContacto(self):
        try:
            telefono = int(self.textFieldTelefono.get())
            if (self.comprobarExiste(telefono)):
                for con in self.arrayContactos:
                    if int(con.telefono) == telefono:
                        self.arrayContactos.remove(con)
                        self.guardar()
                self.recargarLista()
            else:
                tkinter.messagebox.showerror(title="No se encuentra", message="El telefono insertado no existe")
        except ValueError:
            tkinter.messagebox.showerror(title="Telefono incorrecto", message="Debe ser un numero")

    def comprobarExiste(self,telefono):
        for con in self.arrayContactos:
            if(int(con.telefono) == telefono):
                return True
        return False

    def modificarContacto(self):
        try:
            telefono = int(self.textFieldTelefono.get())
            if(self.comprobarExiste(telefono)):
                nombre = str(self.textFieldNombre.get()).strip()
                apellidos = str(self.textFieldApellido.get()).strip()
                if not nombre or not apellidos:
                    tkinter.messagebox.showerror(title="Campos incorrectos", message="Rellena todos los campos")
                else:
                    for con in self.arrayContactos:
                        if int(con.telefono) == telefono:
                            con.nombre = self.textFieldNombre.get()
                            con.apellidos = self.textFieldApellido.get()
                            self.guardar()
                    self.recargarLista()
            else:
                tkinter.messagebox.showerror(title="No se encuentra", message="El telefono insertado no existe")
        except ValueError:
            tkinter.messagebox.showerror(title="Telefono incorrecto", message="Debe ser un numero")

    def guardar(self):
        ficheroLista = open("ficheroLista", "wb")
        pickle.dump(self.arrayContactos, ficheroLista)
        ficheroLista.close()
        del (ficheroLista)

    def leer(self):
        try:
            fichero_lista_contacto = open("ficheroLista", "rb")
            self.arrayContactos = pickle.load(fichero_lista_contacto)
            fichero_lista_contacto.close()
            del (fichero_lista_contacto)
        except FileNotFoundError:
            print("No existe el fichero, no se mostrara nada")

root = tk.Tk()
app = Application()
app.mainloop()