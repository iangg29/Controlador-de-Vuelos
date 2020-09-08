#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class Aeropuerto:

    def __init__(self, ciudad, codigo):
        self.ciudad = ciudad
        self.codigo = codigo

    def __str__(self) -> str:
        return f"[{self.codigo}] {self.ciudad}"
