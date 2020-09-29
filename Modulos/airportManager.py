#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.
from Exceptions.CancelledPayload import CancelledPayload
from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Exceptions.InvalidObject import InvalidObject
from Exceptions.InvalidOption import InvalidOption
from Exceptions.ZeroResults import ZeroResults
from Objetos.Aeropuerto import Aeropuerto
from Utilidades.ModuleType import ModuleType
from modulo import Modulo


class AirportManager(Modulo):

    def __init__(self, app, name):
        super().__init__(app, name, ModuleType.DATA)
        self.app = app
        self.airports = []
        self.mysqlModule = app.getMySQLManager()
        self.configurationModule = app.getConfiguracion()

    def loadData(self):
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection
        cursor = connection.cursor()
        query = ("SELECT * FROM Aeropuertos")

        cursor.execute(query)

        for x in cursor:
            self.airports.append(Aeropuerto(x[0], x[1], x[2], x[3]))
        cursor.close()
        connection.close()

    def findID(self, id) -> list:
        self.app.updateData()
        return list(filter(lambda airport: airport.getId() == id, self.airports))

    def findCodigo(self, code) -> list:
        self.app.updateData()
        return list(filter(lambda airport: airport.getCode().upper() == code.upper(), self.airports))

    def create(self, airport):
        if not airport: raise InvalidObject
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection
        cursor = connection.cursor()
        query = ("INSERT INTO Aeropuertos (ciudad, pais, codigo) VALUES (%s, %s, %s)")
        valores = (airport.getCiudad(), airport.getPais(), airport.getCode())
        cursor.execute(query, valores)
        connection.commit()
        self.log("Nuevo registro creado.")
        self.app.needUpdate(True)

    def edit(self, oldAirport, newAirport):
        if not oldAirport and not newAirport: raise InvalidObject
        connection = self.initConnection()
        if not connection: FailedDatabaseConnection

        cursor = connection.cursor()
        query = ("UPDATE Aeropuertos SET ciudad = %s, pais = %s, codigo = %s WHERE id = %s")
        valores = (newAirport.getCiudad(), newAirport.getPais(), newAirport.getCode(), oldAirport.getId())
        cursor.execute(query, valores)
        connection.commit()
        self.log(f"{cursor.rowcount} registro(s) afectados.")
        self.app.needUpdate(True)

    def find(self, type):
        if type.upper() == "ID":
            airports = self.findID(int(input("Por favor inresa el ID: ").strip()))
            if len(airports) > 0:
                for airport in airports:
                    airport.printDetail()
            else:
                raise ZeroResults
        elif type.upper() == "CODIGO":
            airports = self.findCodigo(str(input("Por favor ingresa el código: ").strip()).upper())
            if len(airports) > 0:
                for airport in airports:
                    airport.printDetail()
            else:
                raise ZeroResults
        else:
            raise InvalidOption

    def delete(self, airport):
        if not airport: raise InvalidObject
        sure = str(input(f"¿Estas seguro que deseas eliminar el aeropuerto [{airport}]? (S/N) ").strip()).upper()
        if sure == "S":
            connection = self.initConnection()
            if not connection: raise FailedDatabaseConnection
            cursor = connection.cursor()
            query = f"DELETE FROM Aeropuertos WHERE id='{airport.getId()}'"
            cursor.execute(query)
            connection.commit()
            self.log(f"{cursor.rowcount} registro(s) afectados.")
            self.app.needUpdate(True)
        else:
            raise CancelledPayload

    def getAll(self):
        self.app.updateData()
        return self.airports

    def clearData(self):
        self.airports.clear()

    def end(self):
        super().end()
        self.clearData()
