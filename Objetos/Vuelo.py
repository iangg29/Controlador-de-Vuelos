#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class Vuelo:

    def __init__(self, id, origen, destino, capacidad, aerolinea, object):
        self.id = id
        self.origen = origen
        self.destino = destino
        self.capacidad = capacidad
        self.aerolinea = aerolinea
        self.object = object

    def __str__(self) -> str:
        return f"Vuelo [#{self.id}] de {self.origen} a {self.destino}"

    def getOrigen(self) -> str:
        return self.origen

    def getNumer(self) -> str:
        return f"{self.object[10]}{self.id}"
