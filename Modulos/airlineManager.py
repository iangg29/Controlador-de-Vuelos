#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.
from Exceptions.CancelledPayload import CancelledPayload
from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Exceptions.InvalidObject import InvalidObject
from Exceptions.InvalidOption import InvalidOption
from Exceptions.ZeroResults import ZeroResults
from Objetos.Airline import Airline
from Utilidades.ModuleType import ModuleType
from Utilidades.RequestType import RequestType
from Module import Modulo


class AirlineManager(Modulo):

    def __init__(self, app, name):
        super().__init__(app, name, ModuleType.DATA)
        self.app = app
        self.airlines = []
        self.mysqlModule = app.getMySQLManager()
        self.configurationModule = app.getConfiguracion()

    def printAll(self):
        print("Las aerolineas registradas son: ")
        for aerolinea in self.getAll():
            print(f"- {aerolinea}")

    def handleRequest(self, request):
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection
        if request == RequestType.TODOS:
            self.printAll()
        elif request == RequestType.CREAR:
            self.create(connection)
        elif request == RequestType.BUSCAR:
            self.buscar()
        elif request == RequestType.EDITAR:
            self.edit(connection)
        elif request == RequestType.ELIMINAR:
            self.delete(connection)
        else:
            raise InvalidOption

    def loadData(self):
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection
        cursor = connection.cursor()
        query = ("SELECT * FROM Aerolineas")

        cursor.execute(query)

        for x in cursor:
            self.airlines.append(Airline(x[0], x[1], x[2]))
        cursor.close()
        connection.close()

    def findId(self, id) -> list:
        self.app.updateData()
        return list(filter(lambda aerolinea: aerolinea.getId() == id, self.airlines))

    def create(self, connection):
        super().handleRequest()
        nombre = str(input("Introduce el name de la aerolinea: ").strip()).capitalize()
        if nombre.upper() == "CANCElAR":
            raise CancelledPayload
        codigo = str(input("Introduce el código de la aerolinea: ").strip()).upper()

        if not nombre or not codigo:
            raise InvalidObject

        nuevaAerolinea = Airline(0, nombre, codigo)

        self.log("La aerolínea a crear es:")
        nuevaAerolinea.printDetail()

        if not self.app.getUtilities().confirm():
            raise CancelledPayload

        cursor = connection.cursor()
        query = "INSERT INTO Aerolineas (name, codigo) VALUES (%s, %s)"
        valores = (nombre, codigo)
        cursor.execute(query, valores)
        connection.commit()
        self.log("La aerolinea ha sido creada.")
        self.app.needUpdate(True)

    def edit(self, connection):
        super().handleRequest()
        query = input("Por favor ingresa un código/ID: ").strip()
        if query.upper() == "CANCELAR":
            raise CancelledPayload
        else:
            aerolineas = self.findCodigo(query.upper())
            if len(aerolineas) <= 0:
                aerolineas = self.findId(int(query))
                if len(aerolineas) > 0:
                    aerolineaAEditar = aerolineas[0]
                else:
                    raise ZeroResults
            else:
                aerolineaAEditar = aerolineas[0]

        if not aerolineaAEditar:
            raise ZeroResults

        self.log("La aerolínea a editar es:")
        aerolineaAEditar.printDetail()
        nombre = str(input("Introduce el nuevo name de la aerolínea: ").strip()).capitalize()
        codigo = str(input("Introduce el nuevo código de la aerolínea: ").strip()).upper()

        if not nombre or not codigo:
            raise InvalidObject

        nuevaAerolinea = Airline(aerolineaAEditar.getId(), nombre, codigo)

        self.log("La aerolínea actualizada es: ")
        nuevaAerolinea.printDetail()

        if not self.app.getUtilities().confirm():
            raise CancelledPayload

        cursor = connection.cursor()

        query = "UPDATE Aerolineas SET name = %s, codigo = %s WHERE id = %s"
        values = (nombre, codigo, aerolineaAEditar.getId())

        cursor.execute(query, values)

        connection.commit()
        self.log("La aerolínea a editar ha sido editada!")
        self.app.needUpdate(True)

    def findCodigo(self, code) -> list:
        self.app.updateData()
        return list(filter(lambda aerolinea: aerolinea.getCode().upper() == code.upper(), self.airlines))

    def buscar(self):
        super().handleRequest()
        query = input("Por favor ingresa un código/ID: ").strip()
        if query.upper() == "CANCELAR":
            raise CancelledPayload
        else:
            aerolineas = self.findCodigo(query.upper())
            if len(aerolineas) <= 0:
                aerolineas = self.findId(int(query))
                if len(aerolineas) > 0:
                    for aerolinea in aerolineas:
                        aerolinea.printDetail()
                else:
                    raise ZeroResults
            else:
                for aerolinea in aerolineas:
                    aerolinea.printDetail()

    def delete(self, connection):
        super().handleRequest()
        query = input("Por favor ingresa un código/ID: ").strip()
        if query.upper() == "CANCELAR":
            raise CancelledPayload
        else:
            aerolineas = self.findCodigo(query.upper())
            if len(aerolineas) <= 0:
                aerolineas = self.findId(int(query))
                if len(aerolineas) > 0:
                    aerolinea = aerolineas[0]
                else:
                    raise ZeroResults
            else:
                aerolinea = aerolineas[0]

        if not aerolinea:
            raise ZeroResults

        self.log("La aerolínea a eliminar es:")
        aerolinea.printDetail()

        if not self.app.getUtilities().confirm():
            raise CancelledPayload

        cursor = connection.cursor()
        query = f"DELETE FROM Aerolineas WHERE id='{aerolinea.getId()}'"
        cursor.execute(query)
        connection.commit()
        self.log("La aerolínea ha sido eliminada")
        self.app.needUpdate(True)

    def getAll(self):
        self.app.updateData()
        return self.airlines

    def clearData(self):
        self.airlines.clear()

    def end(self):
        super().end()
        self.clearData()
