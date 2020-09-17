#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class Aeropuerto:

    def __init__(self, objeto):
        self.id = objeto[0]
        self.ciudad = objeto[1]
        self.pais = objeto[2]
        self.codigo = objeto[3]

    def __str__(self) -> str:
        return f"{self.ciudad}, {self.pais} [{self.codigo}]"

    def getId(self) -> int:
        return int(self.id)

    def getPais(self) -> str:
        return self.pais

    def getCiudad(self) -> str:
        return self.ciudad

    def getCode(self) -> str:
        return self.codigo
