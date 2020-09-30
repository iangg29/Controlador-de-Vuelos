#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 4/9/2020.

import mysql.connector
from mysql.connector import errorcode

from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Objetos.Flight import Flight
from Utilidades.ModuleType import ModuleType
from Utilidades.logtype import LogType
from Module import Module


class Mysql(Module):

    def __init__(self, app, name):
        super().__init__(app, name, ModuleType.UTILITY)

    def initConnection(self, dbuser, dbpassword, dbhost, dbdatabase):
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
        return self.connection
