#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
import requests

from Module import Module


class Utilidades(Module):

    def __init__(self, app, nombre):
        super().__init__(app, nombre)

    def log(self, mensaje, tipo):
        print(f"{tipo} {mensaje}")

    def getVersion(self):
        response = requests.get("https://api.github.com/repos/iangg29/ITESM-ProyectoPython/releases/latest")
        if response.status_code == 200:
            print(response.json())