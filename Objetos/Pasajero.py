#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class Pasajeros:

    def __init__(self, nombre, email, celular, edad):
        self.nombre = nombre
        self.email = email
        self.celular = celular
        self.edad = edad
        self.vuelos = []

    def agregarVuelo(self, vuelo):
        self.vuelos.append(vuelo)
