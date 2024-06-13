from Jugador import Jugador
import json
from pathlib import Path
from configs import ARCHIVO_PUNTAJES



class GestorPuntaje:
    __lista : list
    def __init__(self) -> None:
        self.__lista = []
    def agregarJugador(self, unJugador):

        leidos = oe.leerArchivoJSON(ARCHIVO_PUNTAJES)
        self.__lista = self.__lista + oe.decodificarDiccionario(leidos)
        self.__lista.append(unJugador)

        d = self.toJSON() 

        oe.guardarArchivoJSON(d , ARCHIVO_PUNTAJES)

    def appendDesdeEncoder(self, unJugador):
        
        self.__lista.append(unJugador)

    def toJSON(self): #Transformar clase jugador a JSON
        d = dict(
            __class__ = self.__class__.__name__,
            lista = [jugador.toJSON() for jugador in self.__lista]
        )
        return d
    def get__lista(self):
        return self.__lista

    def get__puntajesOrdenados(self):
        leidos = oe.leerArchivoJSON(ARCHIVO_PUNTAJES)
        lista = oe.decodificarDiccionario(leidos)
        return sorted(lista)
    
class ObjectEnconder(object):
    def decodificarDiccionario(self, d): #Permite leer el JSON y transformalo en lista python
        if '__class__' not in d:
            print("NO SE ENCONTRO __class__")
            return d
        else:
            clase_nombre = d['__class__'] #Si el diccionario tiene una clave '__class__', entonces se obtiene el valor de esa clave.
            clase = eval(clase_nombre) 
            if clase_nombre == "GestorPuntaje":
                lista = d['lista'] 
                if(len(lista)):
                    dJugador = lista[0]
                    gestor = clase()
                    for i in range(len(lista)):
                        dJugador = lista[i]
                        clase_nombre = dJugador.pop('__class__')
                        clase = eval(clase_nombre)
                        atributos = dJugador['__atributtes__']
                        unJugador = clase(**atributos)
                        gestor.appendDesdeEncoder(unJugador)
                    return gestor.get__lista()
                else:
                    return []

    def guardarArchivoJSON(self, diccionario, archivo):
        with Path(archivo).open("w", encoding="UTF-8") as destino:
            json.dump(diccionario,destino, indent=4)
            destino.close()
    
    def leerArchivoJSON(self, archivo):
        try:
            with Path(archivo).open(encoding="UTF-8") as fuente:
                diccionario = json.load(fuente)
                fuente.close()
                return diccionario
        except StopIteration:
            print("sin puntajes")
            d = {
                "__class__": "GestorPuntaje",
                "lista": [] 
                }
            return d
        else:
            d = {
                "__class__": "GestorPuntaje",
                "lista": [] 
                }
            return d
        
oe = ObjectEnconder()