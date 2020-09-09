#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

from datetime import datetime

from modulo import Modulo


class Utilidades(Modulo):

    def __init__(self, app, nombre):
        super().__init__(app, nombre)

    def log(self, mensaje, tipo):
        print(f"{tipo} {mensaje}")

    def getCurrentDate(self) -> str:
        dateTime = datetime.now()
        return f"{dateTime.day}/{dateTime.month}/{dateTime.year}"

    def getCurrentTime(self) -> str:
        dateTime = datetime.now()
        return f"{dateTime.hour}:{dateTime.minute}:{dateTime.second}"