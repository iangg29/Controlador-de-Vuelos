#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class Pasajero:

    def __init__(self, id, nombre, email, celular, edad, vuelos):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.celular = celular
        self.edad = edad
        self.vuelos = vuelos

    def __str__(self):
        return self.nombre

    def getId(self) -> int:
        return int(self.id)

    def getName(self) -> str:
        return self.nombre

    def getEmail(self) -> str:
        return self.email

    def getCelular(self) -> str:
        return self.celular

    def getEdad(self) -> int:
        return int(self.edad)

    def getVuelos(self) -> str:
        return self.vuelos

    def printDetail(self):
        print("---- PASAJERO ----")
        print(f"ID: {self.getId()}")
        print(f"Nombre: {self.getName()}")
        print(f"Email: {self.getEmail()}")
        print(f"Celular: {self.getCelular()}")
        print(f"Edad: {self.getEdad()}")
        print(f"Vuelos: {self.getVuelos()}")
        print("------------------")
