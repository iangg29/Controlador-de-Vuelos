#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 4/9/2020.

import mysql.connector
from mysql.connector import errorcode

from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Objetos.Vuelo import Vuelo
from Utilidades.ModuleType import ModuleType
from Utilidades.logtype import LogType
from modulo import Modulo


class Mysql(Modulo):

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

    def getData(self, configuracion):
        self.log("[SQL] Cargando datos ...", LogType.NORMAL)
        connection = self.initConnection(configuracion.getUser(), configuracion.getPassword(), configuracion.getHost(),
                                         configuracion.getDB())
        if not connection: return
        self.log("[SQL] La conexión con la base de datos fue exitosa.", LogType.NORMAL)
        cursor = connection.cursor()
        query = (
            "SELECT * FROM Vuelos INNER JOIN Aerolineas ON Vuelos.`aerolinea` = Aerolineas.`id` INNER JOIN Aeropuertos AS Aeropuerto1 ON Vuelos.`origen` = Aeropuerto1.`id` INNER JOIN Aeropuertos AS Aeropuerto2 ON  Vuelos.`destino` = Aeropuerto2.`id` INNER JOIN Pasajeros ON Vuelos.`pasajeros`= Pasajeros.`id`")

        cursor.execute(query)

        for x in cursor:
            self.flights.append(x)
        cursor.close()
        cursor = connection.cursor()
        query = ("SELECT * FROM Aerolineas")
        cursor.execute(query)

        for x in cursor:
            self.airlines.append(x)

        self.log("[SQL] Datos cargados correctamente.", LogType.NORMAL)
        cursor.close()
        connection.close()

    def getConn(self):
        return self.connection

    def getFlights(self):
        print("\n")
        print("Los vuelos registrados actualmente son:")
        for vuelo in self.flights:
            self.app.newFlight(Vuelo(vuelo[0], vuelo[12], vuelo[16], vuelo[20], vuelo[9], vuelo))
        '''print(
            f"- Vuelo #{i[0]} [{i[10]}{i[0]}] Origen: {i[12]}({i[14]}), Destino: {i[16]}({i[18]}). Operado por {i[9]}.")
        print("Para más información del vuelo, ingrese el comando \"vuelo #id\".")
        print("\n")'''

    def getAirlines(self):
        print("\n")
        print("Las aerolineas registradas actualmente son:")
        for aerolinea in self.airlines:
            print(f"- {aerolinea[1]} [{aerolinea[2]}].")
        print("\n")
