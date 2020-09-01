#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
import time

from Exceptions.ModuleFailedLoading import ModuleFailedLoading
from Módulos.api import Api
from Módulos.configuration import Configuracion
from Módulos.utilities import Utilidades
from Utilidades.logtype import LogType


class App:

    def __init__(self, name, debug):
        self.name = name
        self.author = "Ian García"
        self.version = "1.0"
        self.debug = debug
        self.started = False
        self.modulos = []

    def start(self):
        startTime = self.getTime()
        self.started = True

        self.log(f"{self.name} creado por {self.author}", LogType.NORMAL)
        self.log(f"Version: {self.version}", LogType.NORMAL)

        try:
            utilidades = Utilidades(self, "Utilidades")
            configuracion = Configuracion(self, "Configuración")
            api = Api(self, "APIManager")
        except ModuleFailedLoading:
            exit()

        token = configuracion.getToken()

        finishTime = self.getTime()
        self.log(f"Aplicación iniciada en [{finishTime - startTime}ms].", LogType.NORMAL)
        while self.started:
            try:
                opcion = str(input("Ingresa una opción:  ".strip())).upper()
                if opcion == "FLIGHTS":
                    pass
                elif opcion == "SALIR":
                    self.stop()
                else:
                    self.log("Opción inválida", LogType.ERROR)
            except KeyboardInterrupt:
                print("\n")
                self.log("Aplicación interrumpida", LogType.SEVERE)
                self.stop()

    def stop(self):
        self.started = False
        # TODO: End all modules.
        for modulo in self.modulos:
            modulo.end()
        print("Aplicación cerrada correctamente.")
        exit()

    def getModulos(self):
        return self.modulos

    def loadModulos(self, modulo):
        self.modulos.append(modulo)

    def getTime(self) -> int:
        return int(round(time.time() * 1000))

    def log(self, mensaje, tipo):
        print(f"{tipo} {mensaje}")


def main():
    app = App("Hotel System", True)
    app.start()


main()
