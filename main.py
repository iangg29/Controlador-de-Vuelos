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
    """
        La clase principal del programa aquí se almacenan y administran todos los módulos.

        :param author: Nombre del autor del programa
        :param version: Version actual del programa obtenida de GitHub

    """

    author = "Ian García"
    version = None

    def __init__(self, name, debug):
        """
        Inicializa todos los módulos y configura la aplicación.

        :param name: Nombre del programa
        :param debug: Modo debug
        """

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
        """ Es la función principal del programa

            Inicia y añade los módulos, obtiene la información del servidor por primera vez;
            Además maneja toda la lógica de los mensajes del programa, junto con todos los mensajes
            del usuario. Controla las exepciones que pudiera haber al ingresar algún comando
            desconocido o erroneo.


            :raise KeyboardInterrupt: Si en algún momento la aplicación es interrumpida
            :raise InvalidOption:  Si el usuario ingresa alguna opción no contemplada para el programa
            :raise ZeroResults: Si no se encontraron resultados en alguna búsqueda
            :raise InvalidObject: El objeto es inválido al momento de crear uno, ya sea que falte información o tenga algún tipo de dato no admitido
            :raise CancelledPayload: El usuario decidió cancelar la solicitud
            :raise FailedDatabaseConnection: La conexión a la base de datos falló por lo que el programa se detiene
            :raise ValueError: El usuario ingresa algun tipo de valor erroneo
        """

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
                    self.backupManager.globalBackUp()
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
        """
        Detiene la aplicación y finaliza cada uno de los módulos activos.
        """
        self.started = False
        for module in self.modules:
            module.end()
        print("Aplicación cerrada correctamente.")
        exit()

    def updateData(self):
        """
        Obtiene la información del servidor SQL.

        Si la variable del programa dataRefresh de encuentra activa, quiere decir que
        se necesita actualizar la información del programa, ya que alguna de esta, ha
        cambiado. Este proceso lo hace vaciando los arreglos de datos de cada módulo y
        los actualiza haciendo una petición a la base de datos.
        """
        if self.dataRefresh:
            if self.debug: self.log("Actualizando datos...")
            for module in self.modules:
                if module.isData():
                    module.clearData()
                    module.loadData()
            if self.debug: self.log("Datos actualizados.")
            self.needUpdate(False)

    def menu(self, forced=False):
        """ Imprime el menu de opciones que tiene el programa.

        Imprime el menu de las opciones al principio del programa una sola vez,
        o a menos que se lo indique con el parámetro forced.

        :param forced : Estatus para forzar la impresión del menu
        """
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
        """
        Actuliza la variable dataRefresh para actualizar la información.

        :param bool: Estatus para requerir actualización de datos.
        """
        self.dataRefresh = bool

    def getModules(self):
        """
        :return: Lista de todos los módulos cargados.
        """
        return self.modules

    def loadModule(self, module):
        """ Añade un módulo a la lista de módulos.

        :param module: Módulo a añadir
        """
        self.modules.append(module)

    def __getVersion(self):
        """
        Actualiza la versión del programa en base a GitHub.
        """
        response = requests.get("https://api.github.com/repos/iangg29/ITESM-ProyectoPython/releases/latest",
                                {'owner': 'iangg29', 'repo': 'ITESM-ProyectoPython'})
        if response.status_code == 200:
            json = response.json()
            self.version = json['tag_name']
        else:
            self.log(response.status_code, LogType.ERROR)

    def __getTime(self) -> int:
        """
        :return: Regresa el tiempo actual en milisegundos.
        """
        return int(round(time.time() * 1000))

    def log(self, mensaje, tipo=LogType.NORMAL):
        """
        Imprime un mensaje dado con un prefijo de acuerdo a LogType (default es normal).

        :param mensaje: str
        :param tipo: LogType
        """
        print(f"{tipo} {mensaje}")

    def getAirlineManager(self) -> AirlineManager:
        """
        :return: Regresa el controlador de Aerolineas
        """
        return self.airlineManager

    def getPassengerManager(self) -> PassengerManager:
        """
        :return: Regresa el controlador de pasajeros
        """
        return self.passengerManager

    def getFlightManager(self) -> FlightManager:
        """
        :return: Regresa el controlador de vuelos
        """
        return self.flightsManager

    def getMySQLManager(self) -> Mysql:
        return self.mysql

    def getUtilities(self) -> Utilidades:
        """
        :return: Regresa el controlador de Utilidades
        """
        return self.utilities

    def getConfiguracion(self) -> Configuration:
        """
        :return: Regresa el controlador de Configuracion
        """
        return self.configuration

    def getBackupManager(self) -> BackupManager:
        """
        :return: Regresa el controlador de Backup
        """
        return self.backupManager

    def getAirportManager(self) -> AirportManager:
        """
        :return: Regresa el controlador de Aeropuertos
        """
        return self.airportManager


def main():
    """
    Crea una nueva instancia de App y la inicializa.
    """
    app = App("Sistema de aeropuerto", False)
    app.start()


main()
