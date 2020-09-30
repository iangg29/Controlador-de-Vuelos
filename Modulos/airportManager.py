#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.
from Exceptions.CancelledPayload import CancelledPayload
from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Exceptions.InvalidObject import InvalidObject
from Exceptions.InvalidOption import InvalidOption
from Exceptions.ZeroResults import ZeroResults
from Objetos.Airport import Airport
from Utilidades.ModuleType import ModuleType
from Utilidades.RequestType import RequestType
from Module import Modulo


class AirportManager(Modulo):

    def __init__(self, app, name):
        super().__init__(app, name, ModuleType.DATA)
        self.app = app
        self.airports = []
        self.mysqlModule = app.getMySQLManager()
        self.configurationModule = app.getConfiguracion()

    def printAll(self):
        print("Los aeropuertos registrados son: ")
        for aeropuerto in self.getAll():
            print(f"{aeropuerto.getId()}- {aeropuerto}")

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
        query = ("SELECT * FROM Aeropuertos")

        cursor.execute(query)

        for x in cursor:
            self.airports.append(Airport(x[0], x[1], x[2], x[3]))
        cursor.close()
        connection.close()

    def findID(self, id) -> list:
        self.app.updateData()
        return list(filter(lambda airport: airport.getId() == id, self.airports))

    def findCodigo(self, code) -> list:
        self.app.updateData()
        return list(filter(lambda airport: airport.getCode().upper() == code.upper(), self.airports))

    def create(self, connection):
        super().handleRequest()
        ciudad = str(input("Introduce la ciudad del aeropuerto: ").strip()).capitalize()
        if ciudad.upper() == "CANCELAR":
            raise CancelledPayload
        pais = str(input("Introduce el país del aeropuertos: ").strip()).capitalize()
        codigo = str(input("Introduce el código del aeropuerto: ").strip()).upper()

        if not ciudad or not pais or not codigo:
            raise InvalidObject

        nuevoAeropuerto = Airport(0, ciudad, pais, codigo)

        self.log("El aeropuerto a crear es:")
        nuevoAeropuerto.printDetail()

        if not self.app.getUtilities().confirm():
            raise CancelledPayload

        cursor = connection.cursor()
        query = ("INSERT INTO Aeropuertos (ciudad, pais, codigo) VALUES (%s, %s, %s)")
        valores = (ciudad, pais, codigo)
        cursor.execute(query, valores)
        connection.commit()
        self.log("El aeropuerto ha sido creado.")
        self.app.needUpdate(True)

    def buscar(self):
        super().handleRequest()
        query = input("Por favor ingresa un código/ID: ").strip()
        if query.upper() == "CANCELAR":
            raise CancelledPayload
        else:
            aeropuertos = self.findCodigo(query.upper())
            if len(aeropuertos) <= 0:
                aeropuertos = self.findID(int(query))
                if len(aeropuertos) > 0:
                    for aeropuerto in aeropuertos:
                        aeropuerto.printDetail()
                else:
                    raise ZeroResults
            else:
                for aeropuerto in aeropuertos:
                    aeropuerto.printDetail()

    def edit(self, connection):
        super().handleRequest()
        query = input("Por favor ingresa un código/ID: ").strip()
        if query.upper() == "CANCELAR":
            raise CancelledPayload
        else:
            aeropuertos = self.findCodigo(query.upper())
            if len(aeropuertos) <= 0:
                aeropuertos = self.findID(int(query))
                if len(aeropuertos) > 0:
                    aeropuerto = aeropuertos[0]
                else:
                    raise ZeroResults
            else:
                aeropuerto = aeropuertos[0]

        if not aeropuerto:
            raise ZeroResults

        self.log("El aeropuerto a editar es:")
        aeropuerto.printDetail()

        ciudad = str(input("Introduce la nueva ciudad del aeropuerto: ").strip()).capitalize()
        pais = str(input("Introduce el nuevo país del aeropuertos: ").strip()).capitalize()
        codigo = str(input("Introduce el nuevo código del aeropuerto: ").strip()).upper()

        if not ciudad or not pais or not codigo:
            raise InvalidObject

        nuevoAeropuerto = Airport(aeropuerto.getId(), ciudad, pais, codigo)

        self.log("El aeropuerto actualizado es: ")
        nuevoAeropuerto.printDetail()

        if not self.app.getUtilities().confirm():
            raise CancelledPayload

        cursor = connection.cursor()
        query = ("UPDATE Aeropuertos SET ciudad = %s, pais = %s, codigo = %s WHERE id = %s")
        valores = (
            nuevoAeropuerto.getCiudad(), nuevoAeropuerto.getPais(), nuevoAeropuerto.getCode(), aeropuerto.getId())
        cursor.execute(query, valores)
        connection.commit()
        self.log("El aeropuerto ha sido editado!")
        self.app.needUpdate(True)

    def delete(self, connection):
        super().handleRequest()

        query = input("Por favor ingresa un código/ID: ").strip()
        if query.upper() == "CANCELAR":
            raise CancelledPayload
        else:
            aeropuertos = self.findCodigo(query.upper())
            if len(aeropuertos) <= 0:
                aeropuertos = self.findID(int(query))
                if len(aeropuertos) > 0:
                    aeropuerto = aeropuertos[0]
                else:
                    raise ZeroResults
            else:
                aeropuerto = aeropuertos[0]

        if not aeropuerto:
            raise ZeroResults

        self.log("El aeropuerto a eliminar es:")
        aeropuerto.printDetail()

        if not self.app.getUtilities().confirm():
            raise CancelledPayload

        cursor = connection.cursor()
        query = f"DELETE FROM Aeropuertos WHERE id='{aeropuerto.getId()}'"
        cursor.execute(query)
        connection.commit()
        self.log("El aeropuerto ha sido eliminado")
        self.app.needUpdate(True)

    def getAll(self):
        self.app.updateData()
        return self.airports

    def clearData(self):
        self.airports.clear()

    def end(self):
        super().end()
        self.clearData()
