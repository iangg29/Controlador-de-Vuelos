#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class Aerolinea:

    def __init__(self, objeto):
        self.id = objeto[0]
        self.name = objeto[1]
        self.clave = objeto[2]

    def __str__(self):
        return f"{self.id} {self.name} [{self.clave}]"

    def getId(self) -> int:
        return int(self.id)

    def getName(self) -> str:
        return self.name

    def getCode(self) -> str:
        return self.clave
