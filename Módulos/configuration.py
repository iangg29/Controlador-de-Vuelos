#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
import os

from dotenv import load_dotenv

from Module import Module


class Configuracion(Module):

    def __init__(self, app, nombre):
        super().__init__(app, nombre)
        load_dotenv()

    def getToken(self) -> str:
        return os.getenv("TOKEN")
