#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 30/9/2020.
from datetime import datetime

import requests

from Module import Module
from Utilidades.ModuleType import ModuleType
from Utilidades.RequestType import RequestType


class Utilidades(Module):
    """
        Utilidades de la aplicación

        Clase con funciones que son repetitivas a lo largo de la aplicación.
    """

    def __init__(self, app, nombre):
        """
        Inicio de la instancia de utilidades

        :param app: Instancia de la aplicación principal
        :param nombre: Nombre del módulo
        """
        super().__init__(app, nombre, ModuleType.UTILITY)

    def log(self, mensaje, tipo):
        """
        Imprime un mensaje dado con un prefijo de acuerdo a LogType (default es normal).

        :param mensaje: Mensaje a imprimir
        :param tipo: Clasificación del mensaje
        """
        print(f"{tipo} {mensaje}")

    def getVersion(self):
        """
        Imprime la versión del programa en base a GitHub.
        """
        response = requests.get("https://api.github.com/repos/iangg29/ITESM-ProyectoPython/releases/latest")
        if response.status_code == 200:
            print(response.json())

    def getCurrentDate(self) -> str:
        """
        :return: Regresa la fecha actual con formato dd/mm/yyyy.
        """
        dateTime = datetime.now()
        return f"{dateTime.day}/{dateTime.month}/{dateTime.year}"

    def getCurrentTime(self) -> str:
        """
        :return: Regresa la hora actual con formato mm:hhh:ss.
        """
        dateTime = datetime.now()
        return f"{dateTime.hour}:{dateTime.minute}:{dateTime.second}"

    def confirm(self) -> bool:
        """
        Método para confirmar una acción

        :return: Regresa la respuesta del usuario
        """
        seguro = str(input("¿Estás seguro de realizar esta acción? (S/N): ").strip()).upper()
        return seguro == "S"

    def handleRequest(self, type) -> RequestType:
        """
        Maneja el tipo de solicitud ingresada por el usuario

        :param type: Input del usuario
        :return: RequestType
        """
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
        elif request == "PASAJEROS":
            return RequestType.PASAJEROS
        elif request == "VUELOS":
            return RequestType.VUELOS
        else:
            return RequestType.INVALIDA
