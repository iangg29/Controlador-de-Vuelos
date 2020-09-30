#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class Airline:

    def __init__(self, id, name, clave):
        self.id = id
        self.name = name
        self.clave = clave

    def __str__(self):
        return f"{self.id} {self.name} [{self.clave}]"

    def getId(self) -> int:
        return int(self.id)

    def getName(self) -> str:
        return self.name

    def getCode(self) -> str:
        return self.clave

    def printDetail(self):
        print("----AEROLINEA----")
        print(f"ID: {self.getId()}")
        print(f"Nombre: {self.getName()}")
        print(f"Código: {self.getCode()}")
        print("-----------------")
