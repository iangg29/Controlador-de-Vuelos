#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.
from Exceptions.CancelledPayload import CancelledPayload
from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Exceptions.InvalidObject import InvalidObject
from Exceptions.InvalidOption import InvalidOption
from Exceptions.ZeroResults import ZeroResults
from Objetos.Aerolinea import Aerolinea
from Utilidades.ModuleType import ModuleType
from modulo import Modulo


class AirlineManager(Modulo):

    def __init__(self, app, name):
        super().__init__(app, name, ModuleType.DATA)
        self.app = app
        self.airlines = []
        self.mysqlModule = app.getMySQLManager()
        self.configurationModule = app.getConfiguracion()

    def loadData(self):
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection
        cursor = connection.cursor()
        query = ("SELECT * FROM Aerolineas")

        cursor.execute(query)

        for x in cursor:
            self.airlines.append(Aerolinea(x[0], x[1], x[2]))
        cursor.close()
        connection.close()

    def findId(self, id) -> list:
        self.app.updateData()
        return list(filter(lambda aerolinea: aerolinea.getId() == id, self.airlines))

    def create(self, aerolinea):
        if not aerolinea: raise InvalidObject
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection
        cursor = connection.cursor()
        query = "INSERT INTO Aerolineas (nombre, codigo) VALUES (%s, %s)"
        valores = (aerolinea.getName(), aerolinea.getCode())
        cursor.execute(query, valores)
        connection.commit()
        self.log("Nuevo registro creado.")
        self.app.needUpdate(True)

    def edit(self, aerolineaVieja, aerolineaNueva):
        if not aerolineaVieja or not aerolineaNueva: raise InvalidObject
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection

        cursor = connection.cursor()

        query = "UPDATE Aerolineas SET nombre = %s, codigo = %s WHERE id = %s"
        values = (aerolineaNueva.getName(), aerolineaNueva.getCode(), aerolineaVieja.getId())

        cursor.execute(query, values)

        connection.commit()
        self.log(f"{cursor.rowcount} registro(s) afectados.")
        self.app.needUpdate(True)

    def findCodigo(self, code) -> list:
        self.app.updateData()
        return list(filter(lambda aerolinea: aerolinea.getCode().upper() == code.upper(), self.airlines))

    def buscar(self, tipo):
        if tipo == "ID":
            aerolineas = self.findId(int(input("Por favor ingresa un id").strip()))
            if len(aerolineas) > 0:
                for aerolinea in aerolineas:
                    aerolinea.printDetail()
            else:
                raise ZeroResults
        elif tipo == "CODIGO":
            aerolineas = self.findCodigo(str(input("Por favor ingresa un código").strip()))
            if len(aerolineas) > 0:
                for aerolinea in aerolineas:
                    aerolinea.printDetail()
            else:
                raise ZeroResults
        else:
            raise InvalidOption

    def delete(self, aerolinea):
        if not aerolinea: raise InvalidObject
        sure = str(input(f"¿Estas seguro que deseas eliminar la aerolinea [{aerolinea}]? (S/N) ").strip()).upper()
        if sure == "S":
            connection = self.initConnection()
            if not connection: raise FailedDatabaseConnection
            cursor = connection.cursor()
            query = f"DELETE FROM Aerolineas WHERE id='{aerolinea.getId()}'"
            cursor.execute(query)
            connection.commit()
            self.log(f"{cursor.rowcount} registro(s) afectados.")
            self.app.needUpdate(True)
        else:
            raise CancelledPayload

    def getAll(self):
        self.app.updateData()
        return self.airlines

    def clearData(self):
        self.airlines.clear()

    def end(self):
        super().end()
        self.clearData()
