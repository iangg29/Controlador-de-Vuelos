#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.


class Vuelo:

    def __init__(self, object):
        self.id = object[0]
        self.origen = f"{object[12]}, {object[13]} [{object[14]}]"
        self.destino = f"{object[16]}, {object[17]} [{object[18]}]"
        self.capacidad = object[3]
        self.duracion = object[4]
        self.tipo = object[5]
        self.aerolinea = f"{object[9]} [{object[10]}]"
        self.pasajeros = object[7]
        self.object = object

    def __str__(self) -> str:
        return f"Vuelo [#{self.id}] de {self.origen} a {self.destino}"

    def getId(self) -> int:
        return int(self.id)

    def getOrigen(self) -> str:
        return self.origen

    def setOrigen(self, origen):
        self.origen = origen

    def getDestino(self) -> str:
        return self.destino

    def setDestino(self, destino):
        self.destino = destino

    def getCapacidad(self) -> int:
        return int(self.capacidad)

    def setCapacidad(self, capacidad):
        self.capacidad = capacidad

    def getDuracion(self) -> int:
        return int(self.duracion)

    def setDuracion(self, duracion):
        self.duracion = duracion

    def getTipo(self) -> str:
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getAerolinea(self) -> str:
        return self.aerolinea

    def setAerolinea(self, aerolinea):
        self.aerolinea = aerolinea

    def getNumer(self) -> str:
        return f"{self.object[10]}{self.id}"

    def getPasajeros(self):
        return self.pasajeros

    def setPasajeros(self, pasajeros):
        self.pasajeros = pasajeros
