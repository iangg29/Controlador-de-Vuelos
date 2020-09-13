#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.
from Utilidades.ModuleType import ModuleType
from modulo import Modulo


class BackupManager(Modulo):
    fileName = "airline_backup.txt"

    def __init__(self, app, name):
        super().__init__(app, name, ModuleType.UTILITY)
        self.mysql = app.getMySQLManager()

    def airlineBackup(self):
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
