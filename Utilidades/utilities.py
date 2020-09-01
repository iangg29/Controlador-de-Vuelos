#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

import time

from modules import Modulo


class Utilidades(Modulo):

    def __init__(self, app, nombre):
        super().__init__(app, nombre)

    def log(self, mensaje, tipo):
        print(f"{tipo} {mensaje}")
