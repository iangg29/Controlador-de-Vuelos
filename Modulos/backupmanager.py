#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.

from Module import Module
from Utilidades.ModuleType import ModuleType
from Utilidades.logtype import LogType


class BackupManager(Module):
    """
    Módulo controlador de Backups.

    Gestiona y administra todos los backups que realiza el sistema

    :param fileName: Nombre del archivo base.
    """

    def __init__(self, app, name):
        """
        Inicializa el módulo.

        :param app: Instancia de la aplicación principal
        :param name: Nombre del módulo
        """
        super().__init__(app, name, ModuleType.UTILITY)

    def globalBackUp(self):
        """
        Realiza el backup de toda la base de datos en diferentes archivos
        """
        self.log("Iniciando backup...", LogType.NORMAL)
        self.airlineBackup("aerolineas.txt")
        self.airportBackup("aeropuertos.txt")
        self.pasajerosBackup("pasajeros.txt")
        self.vuelosBackup("vuelos.txt")
        self.log("Backup finalizado", LogType.NORMAL)

    def airlineBackup(self, archivo):
        """
        Inicia el backup de las aerolineas generando un archivo de texto con todos los datos.
        """
        file = open(archivo, "wt")
        aerolineas = self.app.getAirlineManager().getAll()
        self._header(self.app.getAirlineManager(), file)
        file.write("* Los registros son:\n")
        for aerolinea in aerolineas:
            file.write(f"{aerolinea}\n")
        file.close()

    def airportBackup(self, archivo):
        """
        Inicia el backup de las aerolineas generando un archivo de texto con todos los datos.
        """
        file = open(archivo, "wt")
        aeropuertos = self.app.getAirportManager().getAll()
        self._header(self.app.getAirportManager(), file)
        file.write("* Los registros son:\n")
        for aeropuerto in aeropuertos:
            file.write(f"{aeropuerto}\n")
        file.close()

    def pasajerosBackup(self, archivo):
        """
        Inicia el backup de las aerolineas generando un archivo de texto con todos los datos.
        """
        file = open(archivo, "wt")
        pasajeros = self.app.getPassengerManager().getAll()
        self._header(self.app.getPassengerManager(), file)
        file.write("* Los registros son:\n")
        for pasajero in pasajeros:
            file.write(f"{pasajero}\n")
        file.close()

    def vuelosBackup(self, archivo):
        """
        Inicia el backup de las aerolineas generando un archivo de texto con todos los datos.
        """
        file = open(archivo, "wt")
        vuelos = self.app.getFlightManager().getAll()
        self._header(self.app.getFlightManager(), file)
        file.write("* Los registros son:\n")
        for vuelo in vuelos:
            file.write(f"{vuelo}\n")
        file.close()

    def _header(self, modulo, file):
        """
        Imprime el encabezado de cada archivo de backup.

        :param modulo: Nombre del módulo a hacer backup
        :param file: Nombre del archivo para escribir en el
        """
        file.write("*--------------------\n")
        file.write("*\n")
        file.write("* FILE: " + str(file.name) + "\n")
        file.write("*\n")
        file.write(f"* MODULE: {modulo.getName()}\n")
        file.write("*\n")
        file.write(f"* DATE: {self.app.getUtilities().getCurrentDate()}\n")
        file.write("*\n")
        file.write(f"* HORA: {self.app.getUtilities().getCurrentTime()}\n")
        file.write("*\n")
        file.write("* --------------------\n")
