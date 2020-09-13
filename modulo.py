#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
from Exceptions.ModuleFailedLoading import ModuleFailedLoading
from Utilidades.ModuleType import ModuleType
from Utilidades.logtype import LogType


class Modulo:

    def __init__(self, app, name, type):
        if not app and not name: raise ModuleFailedLoading
        self.app = app
        self.name = name
        self.type = type
        if app.debug: self.log(f"Iniciando módulo [{name.upper()}].", LogType.NORMAL)
        app.loadModulos(self)

    def end(self):
        if self.app.debug: self.log(f"Cerrando módulo [{self.name.lower()}].", LogType.NORMAL)

    def getApp(self):
        return self.app

    def log(self, mensaje, tipo=LogType.NORMAL):
        print(f"{tipo} {mensaje}")

    def getName(self) -> str:
        return self.name

    def getType(self) -> ModuleType:
        return self.type

    def isData(self) -> bool:
        return self.type == ModuleType.DATA
