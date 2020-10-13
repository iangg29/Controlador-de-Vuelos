#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class Passenger:
    """
    Modelo base para Pasajero

    Se define la estructura de datos que seguirá cada pasajero y así poder crear métodos más claros y sencillos para
    que el programa lo pueda leer y utilizar facilmente.
    """

    def __init__(self, id, nombre, email, celular, edad, vuelos):
        """
        Inicio del objeto Pasajero

        :param id: ID del pasajero
        :param nombre: Nombre del pasajero
        :param email: Email del pasajero
        :param celular: Celular del pasajero
        :param edad: Edad del pasajero
        :param vuelos: Lista de vuelos en los que ha ido el pasajero
        """
        self.id = id
        self.nombre = nombre
        self.email = email
        self.celular = celular
        self.edad = edad
        self.vuelos = vuelos

    def __str__(self):
        """
        :return: Regresa el nombre del pasajero en caso de imprimir directamente el objeto.
        """
        return self.nombre

    def getId(self) -> int:
        """
        :return: Regresa el id del pasajero en cuestión.
        """
        return int(self.id)

    def getName(self) -> str:
        """
        :return: Regresa el nombre del pasajero en cuestión.
        """
        return self.nombre

    def getEmail(self) -> str:
        """
        :return: Regresa el email del pasajero en cuestión.
        """
        return self.email

    def getCelular(self) -> str:
        """
        :return: Regresa el celular del pasajero en cuestión.
        """
        return self.celular

    def getEdad(self) -> int:
        """
        :return: Regresa la edad del pasajero en cuestión.
        """
        return int(self.edad)

    def getVuelos(self) -> str:
        """
        :return: Regresa los vuelos del pasajero en cuestión.
        """
        return self.vuelos

    def printDetail(self):
        """
        Imprime de forma ordenada la información del pasajero.
        """
        print("---- PASAJERO ----")
        print(f"ID: {self.getId()}")
        print(f"Nombre: {self.getName()}")
        print(f"Email: {self.getEmail()}")
        print(f"Celular: {self.getCelular()}")
        print(f"Edad: {self.getEdad()}")
        print(f"Vuelos: {(len(self.getVuelos().split('-')), 0)[self.getVuelos() == '-1']}")
        print("------------------")
