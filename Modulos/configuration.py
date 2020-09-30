#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
import os

from dotenv import load_dotenv

from Module import Module
from Utilidades.ModuleType import ModuleType


class Configuration(Module):
    """
    Módulo de configuración

    Obtiene información relevante para el programa ubicada en el archivo .env
    """

    def __init__(self, app, name):
        """
        Inicializa el módulo y carga el archivo .env

        :param app: Instancia de la aplicación principal.
        :param name: Nombre del módulo
        """
        super().__init__(app, name, ModuleType.UTILITY)
        load_dotenv()

    def getToken(self) -> str:
        """
        :return: Regresa el valor de TOKEN del archivo .env
        """
        return os.getenv("TOKEN")

    def getUser(self) -> str:
        """
        :return: Regresa el valor de DBUSER del archivo .env
        """
        return os.getenv("DBUSER")

    def getPassword(self) -> str:
        """
        :return: Regresa el valor de DBPASSWORD del archivo .env
        """
        return os.getenv("DBPASSWORD")

    def getHost(self) -> str:
        """
        :return: Regresa el valor de DBHOST del archivo .env
        """
        return os.getenv("DBHOST")

    def getDB(self) -> str:
        """
        :return: Regresa el valor de DBDATABASE del archivo .env
        """
        return os.getenv("DBDATABASE")
