#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
from Objetos.Airline import Airline
from Objetos.Airport import Airport


class Flight:
    """
        Modelo base para Vuelo

        Se define la estructura de datos que seguirá cada vuelo y así poder crear métodos más claros y sencillos para
        que el programa lo pueda leer y utilizar facilmente.
    """

    def __init__(self, id, origen, destino, capacidad, duracion, tipo, aerolinea, pasajeros):
        """
        Inicio del objeto Vuelo

        :param id: ID del vuelo
        :param origen: Aeropuerto de origen del vuelo
        :param destino: Aeropuerto de destino del vuelo
        :param capacidad: Capacidad del vuelo
        :param duracion: Duración del vuelo
        :param tipo: Tipo del vuelo, ya sea nacional o internacional
        :param aerolinea: Aerolínea del vuelo
        :param pasajeros: Lista de pasajeros del vuelo
        """
        self.id = id
        self.origen = origen
        self.destino = destino
        self.capacidad = capacidad
        self.duracion = duracion
        self.tipo = tipo
        self.aerolinea = aerolinea
        self.pasajeros = pasajeros

    def __str__(self) -> str:
        """
        :return: Regresa información resumida del vuelo en caso de imprimir directamente el objeto.
        """
        return f"[{self.getId()}] - Flight {self.getNumber()} de {self.origen} a {self.destino}"

    def getId(self) -> int:
        """
        :return: Regresa el id del vuelo en cuestión.
        """
        return int(self.id)

    def getOrigen(self) -> Airport:
        """
        :return: Regresa el aeropuerto de origen del vuelo en cuestión.
        """
        return self.origen

    def getDestino(self) -> Airport:
        """
        :return: Regresa el aeropuerto de destino del vuelo en cuestión.
        """
        return self.destino

    def getCapacidad(self) -> int:
        """
        :return: Regresa la capacidad del vuelo en cuestión.
        """
        return int(self.capacidad)

    def getDuracion(self) -> int:
        """
        :return: Regresa la duración del vuelo en cuestión.
        """
        return int(self.duracion)

    def getTipo(self) -> str:
        """
        :return: Regresa tipo de vuelo en cuestión.
        """
        return self.tipo

    def getAerolinea(self) -> Airline:
        """
        :return: Regresa la aerolínea del vuelo en cuestión.
        """
        return self.aerolinea

    def getNumber(self) -> str:
        """
        :return: Regresa el número de vuelo en cuestión.
        """
        return f"{self.aerolinea.getCode()}{self.id}"

    def getPasajeros(self):
        """
        :return: Regresa la lista de pasajeros del vuelo en cuestión.
        """
        return self.pasajeros

    def printDetail(self):
        """
        Imprime de forma ordenada la información del vuelo.
        """
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
