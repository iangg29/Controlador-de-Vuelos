#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class Pasajero:

    def __init__(self, objeto):
        self.id = objeto[0]
        self.nombre = objeto[1]
        self.email = objeto[2]
        self.celular = objeto[3]
        self.edad = objeto[4]
        self.vuelos = objeto[5]

    def __str__(self):
        return self.nombre

    def getId(self) -> int:
        return int(self.id)

    def getName(self) -> str:
        return self.nombre

    def getEmail(self) -> str:
        return self.email

    def getCelular(self) -> str:
        return self.celular

    def getEdad(self) -> int:
        return int(self.edad)

    def getVuelos(self) -> str:
        return self.vuelos
