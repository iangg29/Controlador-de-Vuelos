#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 30/9/2020.

import mysql.connector
from mysql.connector import errorcode

from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Module import Module
from Utilidades.ModuleType import ModuleType
from Utilidades.logtype import LogType


class Mysql(Module):
    """
    Módulo de MySQL

    Controla la conexión con la base de datos.
    """

    def __init__(self, app, name):
        """
        Inicializa el módulo.

        :param app: Instancia de la aplicación general
        :param name: Nombre del módulo
        """
        super().__init__(app, name, ModuleType.UTILITY)

    def initConnection(self, dbuser, dbpassword, dbhost, dbdatabase):
        """
        Inicializa la conexión con el servidor SQL.

        :param dbuser: Usuario de la base de datos
        :param dbpassword: Contraseña de la base de datos
        :param dbhost: Host de la base de datos
        :param dbdatabase: Nombre de la base de datos

        :return: Conexión a la base de datos
        """
        try:
            return mysql.connector.connect(user=dbuser, password=dbpassword, host=dbhost,
                                           database=dbdatabase)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise FailedDatabaseConnection
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.log("[SQL] Error en la base de datos, no existe.", LogType.SEVERE)
                exit()
            else:
                self.log(err, LogType.SEVERE)
                exit()

    def getConn(self):
        """
        :return: Regresa la conexión a la base de datos
        """
        return self.connection
