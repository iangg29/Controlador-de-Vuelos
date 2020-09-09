#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
import time

from Exceptions.CancelledPayload import CancelledPayload
from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Exceptions.InvalidObject import InvalidObject
from Exceptions.InvalidOption import InvalidOption
from Exceptions.ModuleFailedLoading import ModuleFailedLoading
from Exceptions.ZeroResults import ZeroResults
from Modulos.airlineManager import AirlineManager
from Modulos.backupmanager import BackupManager
from Modulos.configuration import Configuracion
from Modulos.mysql import Mysql
from Modulos.utilities import Utilidades
from Objetos.Aerolinea import Aerolinea
from Utilidades.logtype import LogType


class App:
    author = "Ian García"
    version = "1.1"

    def __init__(self, name, debug):
        self.name = name
        self.debug = debug
        self.started = False
        self.modulos = []
        self.mysql = None
        self.airlineManager = None
        self.utilities = None

    def start(self):
        startTime = self._getTime()
        self.started = True

        self.log(f"{self.name} creado por {self.author}")
        self.log(f"Version: {self.version}")

        try:
            # UTILITIES

            self.mysql = Mysql(self, "MySQL")
            self.utilities = Utilidades(self, "Utilidades")
            configuracion = Configuracion(self, "Configuración")

            # DATA MANAGERS
            self.airlineManager = AirlineManager(self, "AirlineManager", self.mysql, configuracion)
            backupManager = BackupManager(self, "BackupManager", self.mysql)
        except ModuleFailedLoading:
            self.log("Error al inicializar un módulo.", LogType.SEVERE)
            exit()

        finishTime = self._getTime()
        self.log(f"Aplicación iniciada en [{finishTime - startTime}ms].")
        while self.started:
            try:
                opcion = str(input("Ingresa una opción:  ".strip())).upper().strip()
                if opcion == "VUELOS":
                    pass
                elif opcion == "AEROLINEAS":
                    print("Las aerolineas registradas son: ")
                    for aerolinea in self.airlineManager.getAll():
                        print(f"- {aerolinea}")
                elif opcion == "AEROPUERTOS":
                    pass
                elif opcion == "PASAJEROS":
                    pass
                elif opcion == "BUSCAR":
                    a = str(input("Qué deseas buscar? (Vuelos/Aerolineas/Pasajeros/Aeropuertos)")).upper().strip()
                    if a == "AEROLINEAS":
                        tipo = str(input("Qué identificador usarás? (ID/CODIGO)")).upper().strip()
                        self.airlineManager.buscar(tipo)
                    elif a == "VUELOS":
                        pass
                    elif a == "PASAJEROS":
                        pass
                    elif a == "AEROPUERTOS":
                        pass
                    else:
                        raise InvalidOption
                elif opcion == "CREAR" or opcion == "NUEVO":
                    self.log("Para cancelar la petición escribe 'Cancelar'.")
                    a = str(input("Qué deseas crear? (Vuelo/Aerolinea/Pasajero/Aeropuerto)")).upper().strip()
                    if a == "AEROLINEA":
                        nombre = str(input("Ingresa el nombre de la aerolínea")).strip()
                        codigo = str(input("Ingresa el código de la aerolínea")).strip()
                        aerolinea = Aerolinea([0, nombre.capitalize(), codigo.upper()])
                        self.airlineManager.create(aerolinea)
                    elif a == "VUELO":
                        pass
                    elif a == "PASAJERO":
                        pass
                    elif a == "AEROPUERTO":
                        pass
                    elif a == "CANCELAR":
                        raise CancelledPayload
                    else:
                        raise InvalidOption
                elif opcion == "EDITAR":
                    self.log("Para cancelar la petición escribe 'Cancelar'.")
                    a = str(input("Qué deseas buscar? (Vuelos/Aerolineas/Pasajeros/Aeropuertos)")).upper().strip()
                    if a == "AEROLINEAS":
                        id = int(input("Ingresa el ID de la aerolinea a editar"))
                        aerolineaVieja = self.airlineManager.findId(id)
                        nombre = str(input(
                            f"Ingresa el nuevo nombre de la aerolínea [Actual={aerolineaVieja.getName().upper()}].")).strip()
                        codigo = str(input(
                            f"Ingresa el nuevo código de la aerolínea [Actual={aerolineaVieja.getCode().upper()}].")).strip()
                        aerolineaNueva = Aerolinea([0, nombre, codigo])
                        self.airlineManager.edit(aerolineaVieja, aerolineaNueva)
                    elif a == "VUELOS":
                        pass
                    elif a == "PASAJEROS":
                        pass
                    elif a == "AEROPUERTOS":
                        pass
                    elif a == "CANCELAR":
                        raise CancelledPayload
                    else:
                        raise InvalidOption
                elif opcion == "CONFIGURACION":
                    self.log("Configuraciones disponibles:")
                    self.log(f"- DEBUG [CURRENT={str(self.debug)}]")
                    a = int(input("Ingresa la configuración que desees cambiar:"))
                    if a == 1:
                        self.debug = not self.debug
                        print("La configuración ha sido cambiada!")
                elif opcion == "BACKUP":
                    backupManager.airlineBackup()
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
            except InvalidObject:
                self.log("Hubo un error al crear un nuevo registro.", LogType.SEVERE)
            except CancelledPayload:
                self.log("Se ha cancelado la petición.", LogType.SEVERE)
            except FailedDatabaseConnection:
                self.log("No se ha podido establecer conexión con la base de datos.", LogType.SEVERE)
                self.log("Cerrando aplicación para evitar futuros errores.", LogType.SEVERE)
                self.stop()

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

    def log(self, mensaje, tipo=LogType.NORMAL):
        print(f"{tipo} {mensaje}")

    def getFlights(self):
        return self.flights

    def newFlight(self, flight):
        self.flights.append(flight)

    def getAirlineManager(self) -> AirlineManager:
        return self.airlineManager

    def getMySQLManager(self) -> Mysql:
        return self.mysql

    def getUtilities(self) -> Utilidades:
        return self.utilities


def main():
    app = App("Sistema de aeropuerto", True)
    app.start()


main()
