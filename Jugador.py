from datetime import datetime

class Jugador:
    __nombre: str
    __fecha: datetime
    __hora: datetime
    __puntaje: int
    def __init__(self, nombre, fecha =datetime.now().strftime('%d/%m/%Y'), hora=datetime.now().strftime('%H:%M') ,puntaje=0):
        self.__nombre = nombre
        self.__fecha = fecha
        self.__hora =  hora
        self.__puntaje = puntaje
        

    def get__nombre(self):
        return self.__nombre
    def get__fecha(self):
        return self.__fecha
    def get__hora(self):
        return self.__hora
    def get__puntaje(self):
        return self.__puntaje
    def set__puntaje(self, puntos):
        self.__puntaje = puntos

    def __gt__(self, otro):
        return   otro.get__puntaje() > self.get__puntaje()
    
    def toJSON(self):
        d = dict(
            __class__ = self.__class__.__name__,
            __atributtes__ = dict(
                nombre = self.__nombre,
                fecha = self.__fecha,
                hora = self.__hora,
                puntaje = self.__puntaje
            )
        )
        return d

    def __str__(self) -> str:
        return f"{self.__nombre} Puntaje {self.__puntaje}"