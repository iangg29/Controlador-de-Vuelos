#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
import time

import requests

from Exceptions.CancelledPayload import CancelledPayload
from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Exceptions.InvalidObject import InvalidObject
from Exceptions.InvalidOption import InvalidOption
from Exceptions.ModuleFailedLoading import ModuleFailedLoading
from Exceptions.ZeroResults import ZeroResults
from Modulos.airlineManager import AirlineManager
from Modulos.airportManager import AirportManager
from Modulos.backupmanager import BackupManager
from Modulos.configuration import Configuration
from Modulos.flightsManager import FlightManager
from Modulos.mysql import Mysql
from Modulos.passengerManager import PassengerManager
from Modulos.utilities import Utilidades
from Utilidades.logtype import LogType


class App:
    author = "Ian García"
    version = None

    def __init__(self, name, debug):
        self.name = name
        self.debug = debug
        self.started = False
        self.modules = []
        self.mysql = None
        self.airlineManager = None
        self.airportManager = None
        self.passengerManager = None
        self.flightsManager = None
        self.utilities = None
        self.configuration = None
        self.backupManager = None
        self.dataRefresh = True
        self.printedMenu = False

    def start(self):
        startTime = self.__getTime()
        self.started = True

        self.log(f"{self.name} creado por {self.author}.")

        try:
            # UTILITIES
            self.mysql = Mysql(self, "MySQL")
            self.utilities = Utilidades(self, "Utilidades")
            self.configuration = Configuration(self, "Configuración")

            # DATA MANAGERS
            self.airlineManager = AirlineManager(self, "AirlineManager")
            self.airportManager = AirportManager(self, "AirportManager")
            self.passengerManager = PassengerManager(self, "PassengerManager")
            self.flightsManager = FlightManager(self, "FlightsManager")
            self.backupManager = BackupManager(self, "BackupManager")
        except ModuleFailedLoading:
            self.log("Error al inicializar un módulo.", LogType.SEVERE)
            exit()

        self.updateData()
        self.__getVersion()

        self.log(f"Version: {str(self.version)}")
        finishTime = self.__getTime()
        self.log(f"Aplicación iniciada en [{finishTime - startTime}ms].")
        while self.started:
            try:
                self.menu()
                option = str(input("Ingresa una opción: ").strip()).upper()
                if option in "VUELOS":
                    self.log("Las opciones para vuelos son:")
                    self.flightsManager.menu()
                    self.flightsManager.handleRequest(
                        self.utilities.handleRequest(str(input("¿Qué deseas hacer? ").strip())))
                elif option in "AEROLINEAS":
                    self.log("Las opciones para aerolineas son:")
                    self.airlineManager.menu()
                    self.airlineManager.handleRequest(
                        self.utilities.handleRequest(str(input("¿Qué desdeas hacer? ").strip())))
                elif option in "AEROPUERTOS":
                    self.log("Las opciones para aeropuertos son:")
                    self.airportManager.menu()
                    self.airportManager.handleRequest(
                        self.utilities.handleRequest(str(input("¿Qué deseas hacer? ").strip())))
                elif option in "PASAJEROS":
                    self.log("Las opciones para pasajeros son:")
                    self.passengerManager.menu()
                    self.passengerManager.handleRequest(
                        self.utilities.handleRequest(str(input("¿Qué deseas hacer? ").strip())))
                elif option == "MENU":
                    self.menu(True)
                elif option == "CONFIGURACION" or option == "CONFIG":
                    self.log("Configuraciones disponibles:")
                    self.log(f"- DEBUG [ACTUAL={str(self.debug)}]")
                    a = int(input("Ingresa la configuración que desees cambiar:"))
                    if a == 1:
                        self.debug = not self.debug
                        print("La configuración ha sido cambiada!")
                    else:
                        raise InvalidOption
                elif option == "BACKUP":
                    self.backupManager.airlineBackup()
                elif option == "SALIR":
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
            except InvalidObject:
                self.log("Hubo un error al crear un nuevo registro.", LogType.SEVERE)
            except CancelledPayload:
                self.log("Se ha cancelado la petición.", LogType.SEVERE)
            except FailedDatabaseConnection:
                print("\n")
                self.log("No se ha podido establecer conexión con la base de datos.", LogType.SEVERE)
                self.log("Cerrando aplicación para evitar futuros errores.", LogType.SEVERE)
                self.stop()
            except ValueError:
                self.log("Valor inválido", LogType.SEVERE)

    def stop(self):
        self.started = False
        for module in self.modules:
            module.end()
        print("Aplicación cerrada correctamente.")
        exit()

    def updateData(self):
        if self.dataRefresh:
            if self.debug: self.log("Actualizando datos...")
            for module in self.modules:
                if module.isData():
                    module.clearData()
                    module.loadData()
            if self.debug: self.log("Datos actualizados.")
            self.needUpdate(False)

    def menu(self, forced=False):
        if not self.printedMenu or forced:
            print("-----[ MENU ]-------")
            print("- Aeropuerto")
            print("- Aerolínea")
            print("- Pasajero")
            print("- Vuelo")
            print("- Backup")
            print("- Configuracion")
            print("- Salir")
            print("- Menu")
            print("--------------------")
            self.printedMenu = True

    def needUpdate(self, bool):
        self.dataRefresh = bool

    def getModules(self):
        return self.modules

    def loadModules(self, module):
        self.modules.append(module)

    def __getVersion(self):
        response = requests.get("https://api.github.com/repos/iangg29/ITESM-ProyectoPython/releases/latest",
                                {'owner': 'iangg29', 'repo': 'ITESM-ProyectoPython'})
        if response.status_code == 200:
            json = response.json()
            self.version = json['tag_name']
        else:
            self.log(response.status_code, LogType.ERROR)

    def __getTime(self) -> int:
        return int(round(time.time() * 1000))

    def log(self, mensaje, tipo=LogType.NORMAL):
        print(f"{tipo} {mensaje}")

    def getAirlineManager(self) -> AirlineManager:
        return self.airlineManager

    def getMySQLManager(self) -> Mysql:
        return self.mysql

    def getUtilities(self) -> Utilidades:
        return self.utilities

    def getConfiguracion(self) -> Configuration:
        return self.configuration

    def getBackupManager(self) -> BackupManager:
        return self.backupManager

    def getAirportManager(self) -> AirportManager:
        return self.airportManager


def main():
    app = App("Sistema de aeropuerto", False)
    app.start()


main()
