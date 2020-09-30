#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
from Objetos.Airline import Airline
from Objetos.Airport import Airport


class Flight:

    def __init__(self, id, origen, destino, capacidad, duracion, tipo, aerolinea, pasajeros):
        self.id = id
        self.origen = origen
        self.destino = destino
        self.capacidad = capacidad
        self.duracion = duracion
        self.tipo = tipo
        self.aerolinea = aerolinea
        self.pasajeros = pasajeros

    def __str__(self) -> str:
        return f"[{self.getId()}] - Flight {self.getNumber()} de {self.origen} a {self.destino}"

    def getId(self) -> int:
        return int(self.id)

    def getOrigen(self) -> Airport:
        return self.origen

    def getDestino(self) -> Airport:
        return self.destino

    def getCapacidad(self) -> int:
        return int(self.capacidad)

    def getDuracion(self) -> int:
        return int(self.duracion)

    def getTipo(self) -> str:
        return self.tipo

    def getAerolinea(self) -> Airline:
        return self.aerolinea

    def getNumber(self) -> str:
        return f"{self.aerolinea.getCode()}{self.id}"

    def getPasajeros(self):
        return self.pasajeros

    def printDetail(self):
        print("---- VUELO ----")
        print(f"ID: {self.getId()}")
        print(f"Origen: {self.getOrigen().getCiudad()}, {self.getOrigen().getPais()}")
        print(f"Destino: {self.getDestino().getCiudad()}, {self.getDestino().getPais()}")
        print(f"Capacidad: {self.getCapacidad()}")
        print(f"Duración: {self.getDuracion()}")
        print(f"Tipo: {('NACIONAL', 'INTERNACIONAL')[self.getTipo() == 'INT']}")
        print(f"Airline: {self.getAerolinea().getName()} [{self.getAerolinea().getCode()}]")
        print(f"Pasajeros: {self.getPasajeros()}")
        print("------------------")