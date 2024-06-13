from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from random import choice, sample
from sys import exit as quitgame
from Jugador import Jugador
from gestorPuntaje import GestorPuntaje
from configs import dificultadesBotones,estiloBoton,botones,estiloGrid,color

gp= GestorPuntaje()

class SimonGame():
    __ventana: object
    __bVerde: object
    __bRojo: object
    __bAmarillo: object
    __bAzul: object
    __textopuntaje: Label
    __labelJugador: Label
    __nombreJugadorStr:str
    __botonPresionado: StringVar
    __puntos: IntVar
    __dialogo: Toplevel
    __galeria: Toplevel
    __elecciones: list
    __juego: bool
    selecDificultad: ttk.Combobox
    __difActual = StringVar
    __labelTiempo: Label
    __tiempoRestante = IntVar
    __jugador : Jugador

    def __init__(self):
        self.__elecciones = []
        self.__juego = False
        self.__ventana= Tk()
        self.__ventana.resizable(False, False)
        self.__ventana.geometry('620x480+500+100')
        self.__ventana.configure(pady=10, padx=10)
        self.__ventana.title('Simon Game')
        self.__puntos = IntVar()
        self.__difActual =  StringVar()
        self.__puntos.set(0)
        cadenaPuntaje= f"Puntaje: {self.__puntos.get()}"
        self.__textopuntaje = Label(self.__ventana, text=cadenaPuntaje, height=1)  
        self.__tiempoRestante = IntVar()
        self.__tiempoRestante.set(10)
        #TEMPORIZADOR
        self.__labelTiempo = Label(self.__ventana)
        self.__labelTiempo.grid(row=4,column=1, sticky=E)

        #Menu de opciones
        barraMenu= Menu(self.__ventana)
        menuPuntajes= Menu(barraMenu, tearoff=0)
        menuPuntajes.add_command(label="Ver Puntajes", command= self.modalPuntajes)
        menuPuntajes.add_command(label="Salir",command=self.__ventana.destroy)
        barraMenu.add_cascade(label="Archivo", menu=menuPuntajes)
        self.__ventana.config(menu=barraMenu)

        #Label de nombre del jugador
        self.__nombreJugadorStr = "Anónimo"
        self.modalJugador() #Ventana de ingresar nombre del Jugador
        self.__jugador = Jugador(self.__nombreJugadorStr)
        cadenaNombreJugador = f"Jugador: {self.__nombreJugadorStr}"
        self.__labelJugador = Label(self.__ventana, text= cadenaNombreJugador, height=1)
        self.__labelJugador.grid(row=0, column=0, sticky="N",pady=10)
        self.__textopuntaje.grid(row=0, column=1, sticky="N", pady=10)
        
        #Selector de dificultad
        labelSelect = Label(self.__ventana, text="Elegir dificultad")
        labelSelect.grid(row=1,column=0)
        self.selecDificultad = ttk.Combobox(self.__ventana, values=["Normal", "Experto", "Super Experto"])
        self.selecDificultad.grid(row=1, column=1)
        self.selecDificultad.bind("<<ComboboxSelected>>", self.handleDificultad)
    
        #Estilo y funcionalidades de los botones
        self.__bRojo=Button(self.__ventana,bg=color["rojo"], **estiloBoton, command=self.presionarRojo)
        self.__bVerde=Button(self.__ventana,bg=color["verde"], **estiloBoton, command=self.presionarVerde)
        self.__bAmarillo = Button(self.__ventana,bg=color["amarillo"], **estiloBoton, command=self.presionarAmarillo)
        self.__bAzul= Button(self.__ventana,bg=color["azul"], **estiloBoton, command=self.presionarAzul)
        

        #Posiciones de los boton
        self.__bRojo.grid(row=2,column=0,**estiloGrid,sticky="W")
        self.__bVerde.grid(row=2,column=1,**estiloGrid, sticky="E")
        self.__bAmarillo.grid(row=3,column=0,**estiloGrid ,sticky="SW")
        self.__bAzul.grid(row=3,column=1,**estiloGrid, sticky="SE")
        
    
        self.__botonPresionado = StringVar()# Boton que presiono el Jugador
        self.__ventana.update()
        self.__ventana.wait_variable(self.__difActual)
        self.iniciarJuego()
        self.__ventana.mainloop()
    

    def iniciarJuego(self):
        #¿INICIA JUEGO CON TEMPORIZADOR?
        if self.__difActual.get() == "Experto" or self.__difActual.get() == "Super Experto":
            self.actualizar_temporizador()
            self.__labelTiempo.config(text=f"Tiempo: {self.__tiempoRestante.get()}")
        else:
             self.__labelTiempo.config(text="")
        if  self.__difActual.get() != "Super Experto":
            self.SeleccionNormal()
        else:
             self.SeleccionSuperExperto()

        
    #Metodos de los botones al ser clickeados
    def presionarRojo(self):
        self.__botonPresionado.set("rojo")
    def presionarVerde(self):
        self.__botonPresionado.set("verde")
    def presionarAmarillo(self):
        self.__botonPresionado.set("amarillo")
    def presionarAzul(self):
        self.__botonPresionado.set("azul")
    #metodos CHOICE
    def SeleccionNormal(self):
        while self.__juego: #Inicio del juego NORMAL O EXPERTO
            botonRamdom = choice(botones)
            self.__elecciones.append(botonRamdom)
            for i in range(len(self.__elecciones)):
                if self.__elecciones[i] == "verde":
                    self.__bVerde.config(bg= color["verde-on"])
                    self.__ventana.after(dificultadesBotones[self.__difActual.get()][0], self.__ventana.update())
                    self.__bVerde.config(bg= color["verde"])
                    self.__ventana.after(dificultadesBotones[self.__difActual.get()][1], self.__ventana.update())
                elif self.__elecciones[i] == "rojo":
                    self.__bRojo.config(bg= color["rojo-on"])
                    self.__ventana.after(dificultadesBotones[self.__difActual.get()][0], self.__ventana.update())
                    self.__bRojo.config(bg= color["rojo"])
                    self.__ventana.after(dificultadesBotones[self.__difActual.get()][1], self.__ventana.update())
                elif self.__elecciones[i] == "amarillo":
                    self.__bAmarillo.config(bg=color["amarillo-on"])
                    self.__ventana.after(dificultadesBotones[self.__difActual.get()][0], self.__ventana.update())
                    self.__bAmarillo.config(bg= color["amarillo"])
                    self.__ventana.after(dificultadesBotones[self.__difActual.get()][1], self.__ventana.update())
                elif self.__elecciones[i] == "azul":
                    self.__bAzul.config(bg= color["azul-on"])
                    self.__ventana.after(dificultadesBotones[self.__difActual.get()][0], self.__ventana.update())
                    self.__bAzul.config(bg= color["azul"])
                    self.__ventana.after(dificultadesBotones[self.__difActual.get()][1], self.__ventana.update())
                
            for i in range(len(self.__elecciones)):
                self.__ventana.wait_variable(self.__botonPresionado) #Espera a que el jugador haga click en un boton
                if self.__tiempoRestante.get() > 0 and self.__elecciones[i] == self.__botonPresionado.get():      
                                incrementador = int(self.__puntos.get()) + 1
                                self.__puntos.set(incrementador)
                                cadenaPuntaje = f"Puntaje: {self.__puntos.get()}"
                                self.__textopuntaje.config(text=cadenaPuntaje)
                                self.__ventana.update()
                                self.__tiempoRestante.set(10)
                else:#Si el boton clickeado no es igual al esperado = GAMEOVER
                    self.gameOver(gp)
    def SeleccionSuperExperto(self):
        bandera = False
        while self.__juego: #Inicio en SUPER EXPERTO
            duplaRandom = sample(botones,2)
            self.__elecciones.append(duplaRandom)
            self.__juego = False
            
            for dupla in self.__elecciones:
                
                if "verde" in dupla:
                    self.__bVerde.config(bg=color["verde-on"])
                if "rojo" in dupla:
                    self.__bRojo.config(bg=color["rojo-on"])
                if "amarillo" in dupla:
                    self.__bAmarillo.config(bg=color["amarillo-on"])
                if "azul" in dupla:
                    self.__bAzul.config(bg=color["azul-on"])

                self.__ventana.update()
                self.__ventana.after(dificultadesBotones[self.__difActual.get()][0])

                if "verde" in dupla:
                    self.__bVerde.config(bg=color["verde"])
                if "rojo" in dupla:
                    self.__bRojo.config(bg=color["rojo"])
                if "amarillo" in dupla:
                    self.__bAmarillo.config(bg=color["amarillo"])
                if "azul" in dupla:
                    self.__bAzul.config(bg=color["azul"])

                self.__ventana.update()
                self.__ventana.after(dificultadesBotones[self.__difActual.get()][1])

            self.__juego = True
            if bandera:
                self.actualizar_temporizador()

            
            
            for dupla in self.__elecciones:
                
                botones_presionados= []
                self.__ventana.wait_variable(self.__botonPresionado)#Espera a que el jugador haga click en el primer boton
                botones_presionados.append(self.__botonPresionado.get())
                self.__ventana.wait_variable(self.__botonPresionado)#Espera a que el jugador haga click en el segundo boton
                botones_presionados.append(self.__botonPresionado.get())

                if self.__tiempoRestante.get() > 0 and set(botones_presionados) == set(dupla):      
                                incrementador = int(self.__puntos.get()) + 1
                                self.__puntos.set(incrementador)
                                cadenaPuntaje = f"Puntaje: {self.__puntos.get()}"
                                self.__textopuntaje.config(text=cadenaPuntaje)
                                self.__ventana.update()
                                self.__tiempoRestante.set(10)
                                self.__juego = True
                else:#Si el boton clickeado no es igual al esperado = GAMEOVER
                    self.gameOver(gp)
            bandera = True
    #metodos temporizador
    def actualizar_temporizador(self):
        if self.__tiempoRestante.get() > 0:
            decremento = self.__tiempoRestante.get() -1
            self.__tiempoRestante.set(decremento)
            self.__labelTiempo.config(text=f"Tiempo: {self.__tiempoRestante.get()}")
            if self.__juego:
                self.__labelTiempo.after(1000, self.actualizar_temporizador)
        else:
            self.__labelTiempo.config(text="¡Tiempo agotado!")
    #Metodos Modal Nombre
    def buttonModalJugador(self):
        if self.inputEntry.get():
            self.__nombreJugadorStr = self.inputEntry.get()
        self.__dialogo.destroy()     
    def modalJugador(self):
        self.__dialogo = Toplevel()
        self.__dialogo.geometry('200x100+700+250')
        self.__dialogo.resizable(False,False)
        self.__dialogo.title("Simon Game")
        self.inputLabel = Label(self.__dialogo, text="Ingrese Nombre: ")
        self.inputEntry = Entry(self.__dialogo,width=20, textvariable=self.__nombreJugadorStr)
        self.inputLabel.pack(side=TOP)   
        self.inputEntry.pack(side=TOP, fill= BOTH, padx=20,pady=10)
        boton = Button(self.__dialogo, text='Empezar!',command=self.buttonModalJugador)
        boton.pack(side=BOTTOM, padx=20 , pady=10)

        self.__dialogo.transient(master=self.__ventana)
        self.__dialogo.grab_set()
        self.__ventana.wait_window(self.__dialogo)        
    def modalPuntajes(self):
        #TODO: ARREGLAR BOTON DE CERRAR MODAL
        self.__galeria = Toplevel()
        self.__galeria.geometry('500x300+500+100')
        self.__galeria.resizable(False,False)
        contenedorTabla = LabelFrame(self.__galeria, bg="#dfdfdf", width=490,text="Galeria de Puntajes")
        contenedorTabla.pack(side=TOP, fill=Y, expand=True)
        encabezado = Label(contenedorTabla,height=1,text="JUGADOR            FECHA                HORA             PUNTAJE" , bg="#dfdfdf",font=("Arial", 10, "bold"))
        encabezado.pack(side=TOP)
        tablaPuntajes = Label(contenedorTabla, width=480, height=250,bg="#ffffff", bd=1)
        tablaPuntajes.pack(side=TOP, padx=25,pady=10, fill=Y,expand=True)
        listapuntajes = gp.get__puntajesOrdenados()
        i=0
        total_columns = 4
        for jugador in listapuntajes[:10]:
            for j in range(total_columns):
                    e = Entry(tablaPuntajes,font=("Courier",10), width=13,bd=0, justify=CENTER)
                    e.grid(row=i, column=j)
                    if j == 0:
                        dato = jugador.get__nombre()
                        e.insert(END, dato)
                    elif j == 1:
                        dato = jugador.get__fecha()
                        e.insert(END, dato)
                    elif j == 2:
                        dato = jugador.get__hora()
                        e.insert(END, dato)
                    elif j == 3:
                        dato = jugador.get__puntaje()
                        e.insert(END, dato)
                    e.config(state=DISABLED, disabledbackground="#ffffff", disabledforeground="black" ) 
            i+=1
         
        self.__galeria.update()
        
        botonCerrar = Button(self.__galeria, text='Cerrar',command=self.__galeria.destroy)
        botonCerrar.pack(side=BOTTOM, padx=20 , pady=10)  
    def handleDificultad(self,evento):
        seleccion = self.selecDificultad.get()
        self.__difActual.set(seleccion)
        if self.__juego == False:
            self.__juego= True
            self.iniciarJuego()
    def gameOver(self, gp):
        self.__juego =False
        confirm = messagebox.askquestion('GAME OVER!',f'Tu puntaje: {self.__puntos.get()}, Desea seguir jugando?')
        p = int(self.__puntos.get())
        self.__jugador.set__puntaje(p)
        
        #SE GUARDA EL SCORE DEL JUGADOR EN EL JSON
        gp.agregarJugador(self.__jugador)
        gp.get__puntajesOrdenados()

        if confirm == 'yes':

                self.__nombreJugadorStr = "Anónimo"
                self.modalJugador() #Ventana de ingresar nombre del Jugador
                self.__jugador = Jugador(self.__nombreJugadorStr)
                cadenaNombreJugador = f"Jugador: {self.__nombreJugadorStr}"
                self.__labelJugador.config(text= cadenaNombreJugador) 
                self.__elecciones = []
                self.__puntos.set(0)
                cadenaPuntaje = f"Puntaje: {self.__puntos.get()}"
                self.__textopuntaje.config(text=cadenaPuntaje)
                self.__difActual.set('')
                self.selecDificultad.set('')
                self.__labelTiempo.config(text="")
                self.__tiempoRestante.set(10)
                self.__juego =False
                self.__ventana.update() 
            
            
        else:
            self.__juego = False
            quitgame()       
def testAPP():
    mi_app = SimonGame()
if __name__ == '__main__':
    testAPP()