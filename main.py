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
from Modulos.configuration import Configuracion
from Modulos.flightsManager import FlightManager
from Modulos.mysql import Mysql
from Modulos.passengerManager import PassengerManager
from Modulos.utilities import Utilidades
from Objetos.Aerolinea import Aerolinea
from Objetos.Aeropuerto import Aeropuerto
from Objetos.Pasajero import Pasajero
from Objetos.Vuelo import Vuelo
from Utilidades.logtype import LogType


class App:
    author = "Ian García"
    version = None

    def __init__(self, name, debug):
        self.name = name
        self.debug = debug
        self.started = False
        self.modulos = []
        self.mysql = None
        self.airlineManager = None
        self.airportManager = None
        self.passengerManager = None
        self.flightsManager = None
        self.utilities = None
        self.configuracion = None
        self.backupManager = None
        self.dataRefresh = True
        self.printedMenu = False

    def start(self):
        startTime = self.__getTime()
        self.started = True

        self.log(f"{self.name} creado por {self.author}")

        try:
            # UTILITIES
            self.mysql = Mysql(self, "MySQL")
            self.utilities = Utilidades(self, "Utilidades")
            self.configuracion = Configuracion(self, "Configuración")

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
                opcion = str(input("Ingresa una opción: ").strip()).upper()
                if opcion == "VUELOS":
                    print("Los vuelos registrados son: ")
                    for vuelo in self.flightsManager.getAll():
                        print(f"- {vuelo}")
                elif opcion == "AEROLINEAS":
                    print("Las aerolineas registradas son: ")
                    for aerolinea in self.airlineManager.getAll():
                        print(f"- {aerolinea}")
                elif opcion == "AEROPUERTOS":
                    print("Los aeropuertos registrados son: ")
                    for aeropuerto in self.airportManager.getAll():
                        print(f"{aeropuerto.getId()}- {aeropuerto}")
                elif opcion == "PASAJEROS":
                    print("Los pasajeros registrados son: ")
                    for pasajero in self.passengerManager.getAll():
                        print(f"{pasajero.getId()}- {pasajero}")
                elif opcion == "BUSCAR":
                    a = str(input("Qué deseas buscar? (Vuelos/Aerolineas/Pasajeros/Aeropuertos)").strip()).upper()
                    if a == "AEROLINEAS":
                        tipo = str(input("Qué identificador usarás? (ID/CODIGO)").strip()).upper()
                        self.airlineManager.buscar(tipo)
                    elif a == "VUELOS":
                        self.flightsManager.buscar()
                    elif a == "PASAJEROS":
                        tipo = str(input("Que identificador usarás? (ID/NOMBRE)").strip()).upper()
                        self.passengerManager.buscar(tipo)
                    elif a == "AEROPUERTOS":
                        tipo = str(input("Qué identificador usarás? (ID/CODIGO)").strip()).upper()
                        self.airportManager.find(tipo)
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
                        # ORIGEN, DESTINO, CAPACIDAD, DURACION, TIPO, AEROLINEA, PASAJEROS
                        origen = self.airportManager.findCodigo(
                            str(input("Ingresa el codigo del aeropuerto de origen").strip()).upper())
                        destino = self.airportManager.findCodigo(
                            str(input("Ingresa el codigo del aeropuerto de destino").strip()).upper())
                        capacidad = int(input("Ingresa la capacidad que tendrá el vuelo ").strip())
                        duracion = int(input("Ingrea la duración del vuelo en minutos ").strip())
                        tipo = ("INT", "NAC")[origen.getPais() == destino.getPais()]
                        aerolinea = self.airlineManager.findCodigo(
                            str(input("Ingresa el codigo de la aerolinea ").strip()).upper())
                        pasajeros = "0"

                        if not origen or not destino or not capacidad or not duracion or not tipo or not aerolinea or not pasajeros: raise InvalidObject

                        vuelo = Vuelo([])
                        vuelo.setOrigen(origen)
                        vuelo.setDestino(destino)
                        vuelo.setCapacidad(capacidad)
                        vuelo.setDuracion(duracion)
                        vuelo.setTipo(tipo)
                        vuelo.setAerolinea(aerolinea)
                        vuelo.setPasajeros(pasajeros)

                        self.flightsManager.create(vuelo)

                    elif a == "PASAJERO":
                        nombre = str(input("Ingresa el nombre del pasajero")).strip()
                        email = str(input("Ingresa el email del pasajero")).strip()
                        celular = str(input("Ingresa el celular del pasajero")).strip()
                        edad = str(input("Ingresa la edad del pasajero")).strip()
                        pasajero = Pasajero([0, nombre.capitalize(), email.lower(), celular, edad, "0"])
                        self.passengerManager.create(pasajero)
                    elif a == "AEROPUERTO":
                        ciudad = str(input().strip()).capitalize()
                        pais = str(input().strip()).capitalize()
                        codigo = str(input().strip()).upper()
                        airport = Aeropuerto([0, ciudad, pais, codigo])
                        self.airportManager.create(airport)
                    elif a == "CANCELAR":
                        raise CancelledPayload
                    else:
                        raise InvalidOption
                elif opcion == "EDITAR" or opcion == "MODIFICAR":
                    self.log("Para cancelar la petición escribe 'Cancelar'.")
                    a = str(input("Qué deseas buscar? (Vuelos/Aerolineas/Pasajeros/Aeropuertos)").strip()).upper()
                    if a == "AEROLINEAS":
                        id = int(input("Ingresa el ID de la aerolinea a editar"))
                        aerolineaVieja = self.airlineManager.findId(id)
                        if not aerolineaVieja: raise ZeroResults
                        nombre = str(input(
                            f"Ingresa el nuevo nombre de la aerolínea [Actual={aerolineaVieja.getName().upper()}].").strip()).capitalize()
                        codigo = str(input(
                            f"Ingresa el nuevo código de la aerolínea [Actual={aerolineaVieja.getCode().upper()}].").strip()).upper()
                        aerolineaNueva = Aerolinea([0, nombre, codigo])
                        self.airlineManager.edit(aerolineaVieja, aerolineaNueva)
                    elif a == "VUELOS":
                        pass
                    elif a == "PASAJEROS":
                        pass
                    elif a == "AEROPUERTOS":
                        id = int(input("Ingresa el ID del aeropuerto a editar"))
                        oldAirport = self.airportManager.findID(id)
                        if not oldAirport: raise ZeroResults
                        ciudad = str(input(
                            f"Ingresa la nueva ciudad del aeropueto [Actual={oldAirport.getCiudad().upper()}]").strip()).capitalize()
                        pais = str(input(
                            f"Ingresa el nuevo pais del aeropuerto [Actual={oldAirport.getPais().upper()}]").strip()).capitalize()
                        codigo = str(input(
                            f"Ingresa el nuevo código del aeropuerto [Actual={oldAirport.getCode().upper()}]").strip()).upper()
                        newAirport = Aeropuerto([0, ciudad, pais, codigo])
                        self.airportManager.edit(oldAirport, newAirport)
                    elif a == "CANCELAR":
                        raise CancelledPayload
                    else:
                        raise InvalidOption
                elif opcion == "BORRAR" or opcion == "ELIMINAR":
                    self.log("Para cancelar la petición escribe 'Cancelar'.")
                    a = str(input("Qué deseas eliminar? (Vuelos/Aerolineas/Pasajeros/Aeropuertos)")).upper().strip()
                    if a == "AEROLINEAS":
                        id = int(input("Ingresa el ID de la aerolinea a eliminar"))
                        aerolinea = self.airlineManager.findId(id)
                        if not aerolinea: raise ZeroResults
                        self.airlineManager.delete(aerolinea)
                    elif a == "VUELOS":
                        pass
                    elif a == "PASAJEROS":
                        id = int(input("Ingresa el ID del pasajero a eliminar"))
                        pasajero = self.passengerManager.findId(id)
                        if not pasajero: raise ZeroResults
                        self.passengerManager.delete(pasajero)
                    elif a == "AEROPUERTOS":
                        id = int(input("Ingresa el ID del aeropuerto a eliminar"))
                        airport = self.airportManager.findID(id)
                        if not airport: raise ZeroResults
                        self.airportManager.delete(airport)
                    elif a == "CANCELAR":
                        raise CancelledPayload
                    else:
                        raise InvalidOption
                elif opcion == "MENU":
                    self.menu(True)
                elif opcion == "CONFIGURACION" or opcion == "CONFIG":
                    self.log("Configuraciones disponibles:")
                    self.log(f"- DEBUG [CURRENT={str(self.debug)}]")
                    a = int(input("Ingresa la configuración que desees cambiar:"))
                    if a == 1:
                        self.debug = not self.debug
                        print("La configuración ha sido cambiada!")
                    else:
                        raise InvalidOption
                elif opcion == "BACKUP":
                    self.backupManager.airlineBackup()
                elif opcion == "VERSION":
                    self.__getVersion()
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
                print("\n")
                self.log("No se ha podido establecer conexión con la base de datos.", LogType.SEVERE)
                self.log("Cerrando aplicación para evitar futuros errores.", LogType.SEVERE)
                self.stop()
            except ValueError:
                self.log("Valor inválido", LogType.SEVERE)

    def stop(self):
        self.started = False
        for modulo in self.modulos:
            modulo.end()
        print("Aplicación cerrada correctamente.")
        exit()

    def updateData(self):
        if self.dataRefresh:
            if self.debug: self.log("Actualizando datos...")
            for modulo in self.modulos:
                if modulo.isData():
                    modulo.clearData()
                    modulo.loadData()
            if self.debug: self.log("Datos actualizados.")
            self.needUpdate(False)

    def menu(self, forced=False):
        if not self.printedMenu or forced:
            print("-----[ MENU ]-------")
            print("- Aeropuertos")
            print("- Aerolineas")
            print("- Pasajeros")
            print("- Vuelos")
            print("- Buscar")
            print("- Editar")
            print("- Eliminar")
            print("- Backup")
            print("- Configuracion")
            print("- Salir")
            print("--------------------")
            self.printedMenu = True

    def needUpdate(self, bool):
        self.dataRefresh = bool

    def getModulos(self):
        return self.modulos

    def loadModulos(self, modulo):
        self.modulos.append(modulo)

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

    def getConfiguracion(self) -> Configuracion:
        return self.configuracion

    def getBackupManager(self) -> BackupManager:
        return self.backupManager


def main():
    app = App("Sistema de aeropuerto", False)
    app.start()


main()
