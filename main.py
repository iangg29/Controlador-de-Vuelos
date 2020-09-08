#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
import time

from Exceptions.InvalidOption import InvalidOption
from Exceptions.ModuleFailedLoading import ModuleFailedLoading
from Exceptions.ZeroResults import ZeroResults
from Módulos.airlineManager import AirlineManager
from Módulos.configuration import Configuracion
from Módulos.mysql import Mysql
from Módulos.utilities import Utilidades
from Utilidades.logtype import LogType


class App:
    author = "Ian García"
    version = "1.0"

    def __init__(self, name, debug):
        self.name = name
        self.debug = debug
        self.started = False
        self.modulos = []
        self.flights = []

    def start(self):
        startTime = self._getTime()
        self.started = True

        self.log(f"{self.name} creado por {self.author}", LogType.NORMAL)
        self.log(f"Version: {self.version}", LogType.NORMAL)

        try:
            # UTILITIES

            mysql = Mysql(self, "MySQL")
            utilidades = Utilidades(self, "Utilidades")
            configuracion = Configuracion(self, "Configuración")

            # DATA MANAGERS
            airlineManager = AirlineManager(self, "AirlineManager", mysql, configuracion)
        except ModuleFailedLoading:
            self.log("Error al inicializar un módulo.", LogType.SEVERE)
            exit()

        finishTime = self._getTime()
        self.log(f"Aplicación iniciada en [{finishTime - startTime}ms].", LogType.NORMAL)
        while self.started:
            try:
                opcion = str(input("Ingresa una opción:  ".strip())).upper().strip()
                if opcion == "VUELOS":
                    pass
                elif opcion == "AEROLINEAS":
                    print("Las aerolineas registradas son: ")
                    for aerolinea in airlineManager.getAll():
                        print(f"- {aerolinea}")
                elif opcion == "AEROPUERTOS":
                    pass
                elif opcion == "PASAJEROS":
                    pass
                elif opcion == "BUSCAR":
                    a = str(input("Qué deseas buscar? (Vuelos/Aerolineas/Pasajeros/Aeropuertos)")).upper().strip()
                    if a == "AEROLINEAS":
                        tipo = str(input("Qué identificador usarás? (ID/CODIGO)")).upper().strip()
                        airlineManager.buscar(tipo)
                    elif a == "VUELOS":
                        pass
                    elif a == "PASAJEROS":
                        pass
                    elif a == "AEROPUERTOS":
                        pass
                    else:
                        raise InvalidOption
                elif opcion == "CONFIGURACION":
                    self.log("Configuraciones disponibles:", LogType.NORMAL)
                    self.log(f"- DEBUG [CURRENT={str(self.debug)}]", LogType.NORMAL)
                    a = int(input("Ingresa la configuración que desees cambiar:"))
                    if a == 1:
                        self.debug = not self.debug
                        print("La configuración ha sido cambiada!")
                elif opcion == "BACKUP":
                    print("El backup no esta disponible en esta versión.")
                elif opcion == "SALIR":
                    self.stop()
                else:
                    raise InvalidOption
            except KeyboardInterrupt:
                print("\n")
                self.log("Aplicación interrumpida", LogType.SEVERE)
                self.stop()
            except InvalidOption:
                self.log("Opción inválida", LogType.SEVERE)
            except ZeroResults:
                self.log("No se encontraron resultados", LogType.SEVERE)

    def stop(self):
        self.started = False
        for modulo in self.modulos:
            modulo.end()
        print("Aplicación cerrada correctamente.")
        exit()

    def getModulos(self):
        return self.modulos

    def loadModulos(self, modulo):
        self.modulos.append(modulo)

    def _getTime(self) -> int:
        return int(round(time.time() * 1000))

    def log(self, mensaje, tipo):
        print(f"{tipo} {mensaje}")

    def getFlights(self):
        return self.flights

    def newFlight(self, flight):
        self.flights.append(flight)


def main():
    app = App("Sistema de aeropuerto", True)
    app.start()


main()
