#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
import os

from dotenv import load_dotenv

from Utilidades.ModuleType import ModuleType
from Module import Modulo


class Configuration(Modulo):

    def __init__(self, app, name):
        super().__init__(app, name, ModuleType.UTILITY)
        load_dotenv()

    def getToken(self) -> str:
        return os.getenv("TOKEN")

    def getUser(self) -> str:
        return os.getenv("DBUSER")

    def getPassword(self) -> str:
        return os.getenv("DBPASSWORD")

    def getHost(self) -> str:
        return os.getenv("DBHOST")

    def getDB(self) -> str:
        return os.getenv("DBDATABASE")
