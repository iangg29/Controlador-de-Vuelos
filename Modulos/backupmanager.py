#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.
from Module import Module
from Utilidades.ModuleType import ModuleType


class BackupManager(Module):
    """
    Módulo controlador de Backups.

    Gestiona y administra todos los backups que realiza el sistema

    :param fileName: Nombre del archivo base.
    """

    fileName = "airline_backup.txt"

    def __init__(self, app, name):
        """
        Inicializa el módulo.

        :param app: Instancia de la aplicación principal
        :param name: Nombre del módulo
        """
        super().__init__(app, name, ModuleType.UTILITY)
        self.mysql = app.getMySQLManager()

    def airlineBackup(self):
        """
        Inicia el backup de las aerolineas generando un archivo de texto con todos los datos.
        """
        self.log("Iniciando backup de aerolineas...")
        file = open(self.fileName, "wt")
        aerolineas = self.app.getAirlineManager().getAll()
        self._header(self.app.getAirlineManager(), file)
        file.write("Las aerolineas registradas a la fecha son:\n")
        for aerolinea in aerolineas:
            file.write(f"{aerolinea}\n")
        file.close()
        self.log("Backup de aerolineas completado.")

    def _header(self, modulo, file):
        """
        Imprime el encabezado de cada archivo de backup.

        :param modulo: Nombre del módulo a hacer backup
        :param file: Nombre del archivo para escribir en el
        """
        file.write("--------------------")
        file.write("\n")
        file.write("FILE: " + self.fileName)
        file.write("\n")
        file.write(f"MODULE: {modulo.getName()}")
        file.write("\n")
        file.write(f"DATE: {self.app.getUtilities().getCurrentDate()}")
        file.write("\n")
        file.write(f"HORA: {self.app.getUtilities().getCurrentTime()}")
        file.write("\n")
        file.write("--------------------")
        file.write("\n")
