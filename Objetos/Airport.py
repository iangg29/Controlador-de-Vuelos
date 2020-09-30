#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class Airport:
    """
    Modelo base para Aeropuerto

    Se define la estructura de datos que seguirá cada aeropuerto y así poder crear métodos más claros y sencillos para
    que el programa lo pueda leer y utilizar facilmente.
    """

    def __init__(self, id, ciudad, pais, codigo):
        """
        Inicio del objeto Aeropuerto

        :param id: ID del aeropuerto
        :param ciudad: Ciudad del aeropuerto
        :param pais: País donde se encuentra la ciudad
        :param codigo: Código clave del aeropuerto (único)
        """
        self.id = id
        self.ciudad = ciudad
        self.pais = pais
        self.codigo = codigo

    def __str__(self) -> str:
        """
        :return: Regresa información resumida del aeropuerto en caso de imprimir directamente el objeto.
        """
        return f"{self.ciudad}, {self.pais} [{self.codigo}]"

    def getId(self) -> int:
        """
        :return: Regresa el id del aeropuerto en cuestión.
        """
        return int(self.id)

    def getPais(self) -> str:
        """
        :return: Regresa el país del aeropuerto en cuestión.
        """
        return self.pais

    def getCiudad(self) -> str:
        """
        :return: Regresa la ciudad del aeropuerto en cuestión.
        """
        return self.ciudad

    def getCode(self) -> str:
        """
        :return: Regresa el código del aeropuerto en cuestión.
        """
        return self.codigo

    def printDetail(self):
        """
        Imprime de forma ordenada la información del aeropuerto.
        """
        print("----AEROPUERTO----")
        print(f"ID: {self.getId()}")
        print(f"Ciudad: {self.getCiudad()}")
        print(f"Pais: {self.getPais()}")
        print(f"Código: {self.getCode()}")
        print("------------------")
