#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class Aeropuerto:

    def __init__(self, id, ciudad, pais, codigo):
        self.id = id
        self.ciudad = ciudad
        self.pais = pais
        self.codigo = codigo

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

    def printDetail(self):
        print("----AEROPUERTO----")
        print(f"ID: {self.getId()}")
        print(f"Ciudad: {self.getCiudad()}")
        print(f"Pais: {self.getPais()}")
        print(f"Código: {self.getCode()}")
        print("------------------")
