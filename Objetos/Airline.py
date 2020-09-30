#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class Airline:
    """
        Modelo base para Aeropuerto

        Se define la estructura de datos que seguirá cada aeropuerto y así poder crear métodos más claros y sencillos para
        que el programa lo pueda leer y utilizar facilmente.
    """

    def __init__(self, id, name, clave):
        """
        Inicio del objeto Aeropuerto

        :param id: ID de la aerolínea
        :param name: Nombre de la aerolínea
        :param clave: Clave de la aerolínea
        """
        self.id = id
        self.name = name
        self.clave = clave

    def __str__(self):
        """
        :return: Regresa información resumida de la aerolínea en caso de imprimir directamente el objeto.
        """
        return f"{self.id} {self.name} [{self.clave}]"

    def getId(self) -> int:
        """
        :return: Regresa el id de la aerolínea en cuestión.
        """
        return int(self.id)

    def getName(self) -> str:
        """
        :return: Regresa el nombre de la aerolínea en cuestión.
        """
        return self.name

    def getCode(self) -> str:
        """
        :return: Regresa el código de la aerolínea en cuestión.
        """
        return self.clave

    def printDetail(self):
        """
        Imprime de forma ordenada la información de la aerolínea.
        """
        print("----AEROLINEA----")
        print(f"ID: {self.getId()}")
        print(f"Nombre: {self.getName()}")
        print(f"Código: {self.getCode()}")
        print("-----------------")
