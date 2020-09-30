#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
from Exceptions.ModuleFailedLoading import ModuleFailedLoading
from Utilidades.ModuleType import ModuleType
from Utilidades.logtype import LogType


class Module:
    """
    Clase base para todos los módulos del programa.

    Se controla el inicio y el fin de cada módulo, también provee de funciones escenciales a cada módulo de la aplicación.
    """

    def __init__(self, app, name, type):
        """
        Inicializa el módulo y los añade a la aplicación principal.
        Imprime mensajes de debug si está habilitado.

        :param app: Instancia de la aplicación principal
        :param name: Nombre del módulo
        :param type: Tipo del módulo
        """
        if not app and not name: raise ModuleFailedLoading
        self.app = app
        self.name = name
        self.type = type
        self.mysqlManager = app.getMySQLManager()
        self.configManager = app.getConfiguracion()
        if app.debug: self.log(f"Iniciando módulo [{name.upper()}].", LogType.NORMAL )
        app.loadModule(self)

    def end(self):
        """
        Cierre del módulo
        """
        if self.app.debug: self.log(f"Cerrando módulo [{self.name.lower()}].", LogType.NORMAL)

    def menu(self):
        """
        Imprime las opciones disponibles para cada módulo
        """
        print("- Todos")
        print("- Crear")
        print("- Buscar")
        print("- Editar")
        print("- Eliminar")

    def handleRequest(self):
        """
        Función base para controlar las peticiones que se hacen a los módulos.
        """
        self.log("Para cancelar la petición escribe 'Cancelar'.")

    def getApp(self):
        """
        :return: Regresa la instancia de la aplicación principal.
        """
        return self.app

    def log(self, mensaje, tipo=LogType.NORMAL):
        """
        Imprime un mensaje con un prefijo dependiendo del tipo.

        :param mensaje: Mensaje a imprimir
        :param tipo: Tipo de mensaje
        """
        print(f"{tipo} {mensaje}")

    def getName(self) -> str:
        """
        :return: Regresa el nombre del módulo
        """
        return self.name

    def getType(self) -> ModuleType:
        """
        :return: Regresa el tipo del módulo
        """
        return self.type

    def isData(self) -> bool:
        """
        :return: Regresa si el tipo de módulo es igual a DATA.
        """
        return self.type == ModuleType.DATA

    def initConnection(self):
        """
        Inicializa la conexión con la base de datos con datos provenientes de la configuración.

        :return: Regresa la conexión a la base de datos.
        """
        return self.mysqlManager.initConnection(self.configManager.getUser(),
                                                self.configManager.getPassword(),
                                                self.configManager.getHost(),
                                                self.configManager.getDB())
