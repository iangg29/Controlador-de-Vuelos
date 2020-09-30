#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

from datetime import datetime

from Utilidades.ModuleType import ModuleType
from Utilidades.RequestType import RequestType
from Module import Module


class Utilidades(Module):

    def __init__(self, app, nombre):
        super().__init__(app, nombre, ModuleType.UTILITY)

    def log(self, mensaje, tipo):
        print(f"{tipo} {mensaje}")

    def getCurrentDate(self) -> str:
        dateTime = datetime.now()
        return f"{dateTime.day}/{dateTime.month}/{dateTime.year}"

    def getCurrentTime(self) -> str:
        dateTime = datetime.now()
        return f"{dateTime.hour}:{dateTime.minute}:{dateTime.second}"

    def confirm(self) -> bool:
        seguro = str(input("¿Estás seguro de realizar esta acción? (S/N): ").strip()).upper()
        return seguro == "S"

    def handleRequest(self, type) -> RequestType:
        request = type.upper()
        if request == "TODOS":
            return RequestType.TODOS
        elif request == "CREAR":
            return RequestType.CREAR
        elif request == "BUSCAR":
            return RequestType.BUSCAR
        elif request == "EDITAR":
            return RequestType.EDITAR
        elif request == "ELIMINAR":
            return RequestType.ELIMINAR
        else:
            return RequestType.INVALIDA
