#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.
from Exceptions.CancelledPayload import CancelledPayload
from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Exceptions.InvalidObject import InvalidObject
from Exceptions.InvalidOption import InvalidOption
from Exceptions.ZeroResults import ZeroResults
from Objetos.Flight import Flight
from Utilidades.ModuleType import ModuleType
from Utilidades.RequestType import RequestType
from Module import Modulo


class FlightManager(Modulo):

    def __init__(self, app, name):
        super().__init__(app, name, ModuleType.DATA)
        self.app = app
        self.flights = []

    def printAll(self):
        print("Los vuelos registrados son: ")
        for vuelo in self.flights:
            print(f"- {vuelo}")

    def loadData(self):
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection
        cursor = connection.cursor()
        query = (
            "SELECT * FROM Vuelos")
        cursor.execute(query)
        self.app.needUpdate(False)
        for x in cursor:
            self.flights.append(
                Flight(x[0], self.app.getAirportManager().findID(x[1])[0], self.app.getAirportManager().findID(x[2])[0],
                       x[3], x[4], x[5], self.app.getAirlineManager().findId(x[6])[0], x[7]))
        self.app.needUpdate(True)
        cursor.close()
        connection.close()

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

    def find(self, id) -> list:
        self.app.updateData()
        return list(filter(lambda vuelo: vuelo.getId() == id, self.flights))

    def buscar(self):
        super().handleRequest()
        query = input("Por favor ingresa un id ")
        if query.upper() == "CANCELAR":
            raise CancelledPayload
        else:
            vuelos = self.find(int(query))
            if len(vuelos) > 0:
                for vuelo in vuelos:
                    vuelo.printDetail()
            else:
                raise ZeroResults

    def create(self, connection):
        super().handleRequest()
        sub = str(input("Ingresa el codigo del aeropuerto de origen").strip()).upper()
        if sub == "CANCELAR":
            raise CancelledPayload
        origenes = self.app.airportManager.findCodigo(sub)
        destinos = self.app.airportManager.findCodigo(
            str(input("Ingresa el codigo del aeropuerto de destino").strip()).upper())
        aerolineas = self.app.airlineManager.findCodigo(
            str(input("Ingresa el codigo de la aerolinea ").strip()).upper())

        if len(origenes) <= 0 or len(destinos) <= 0 or len(aerolineas) <= 0:
            raise ZeroResults

        origen = origenes[0]
        destino = destinos[0]
        aerolinea = aerolineas[0]

        capacidad = int(input("Ingresa la capacidad que tendrá el vuelo ").strip())
        duracion = int(input("Ingrea la duración del vuelo en minutos ").strip())
        tipo = ("INT", "NAC")[origen.getPais() == destino.getPais()]
        pasajeros = "[]"

        if capacidad <= 0 or duracion <= 0:
            raise InvalidObject

        nuevoVuelo = Flight(0, origen, destino, capacidad, duracion, tipo, aerolinea, pasajeros)

        self.log("El vuelo a crear es: ")
        nuevoVuelo.printDetail()
        if not self.app.getUtilities().confirm():
            raise CancelledPayload

        cursor = connection.cursor()
        query = (
            "INSERT INTO Vuelos (origen, destino, capacidad, duracion, tipo, aerolinea, pasajeros) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        valores = (
            origen.getId(), destino.getId(), capacidad, duracion, tipo, aerolinea.getId(),
            pasajeros)

        cursor.execute(query, valores)
        connection.commit()
        self.log("Nuevo vuelo creado!")
        self.app.needUpdate(True)

    def edit(self, connection):
        super().handleRequest()
        query = input("Por favor ingresa un id ")
        if query.upper() == "CANCELAR":
            raise CancelledPayload
        else:
            vuelos = self.find(int(query))
            if len(vuelos) > 0:
                vueloAEditar = vuelos[0]
                self.log("El vuelo a editar es: ")
                vueloAEditar.printDetail()
                origenes = self.app.getAirportManager().findCodigo(
                    str(input("Introduce el nuevo origen: ").strip()).upper())
                destinos = self.app.getAirportManager().findCodigo(
                    str(input("Introduce el nuevo destino: ").strip()).upper())
                aerolineas = self.app.getAirlineManager().findCodigo(
                    str(input("Introduce la nueva aerolinea: ").strip()).upper())

                if len(origenes) <= 0 or len(destinos) <= 0 or len(aerolineas) <= 0:
                    raise ZeroResults

                origen = origenes[0]
                destino = destinos[0]
                aerolinea = aerolineas[0]

                capacidad = int(input("Ingresa la capacidad que tendrá el vuelo ").strip())
                duracion = int(input("Ingrea la duración del vuelo en minutos ").strip())
                tipo = ("INT", "NAC")[origen.getPais() == destino.getPais()]
                pasajeros = "[]"

                if capacidad <= 0 or duracion <= 0:
                    raise InvalidObject

                nuevoVuelo = Flight(vueloAEditar.getId(), origen, destino, capacidad, duracion, tipo, aerolinea,
                                    pasajeros)

                self.log("El vuelo actualizado es: ")
                nuevoVuelo.printDetail()
                if not self.app.getUtilities().confirm():
                    raise CancelledPayload

                cursor = connection.cursor()
                query = (
                    "UPDATE Vuelos SET origen = %s, destino = %s, capacidad = %s, duracion = %s, tipo = %s, aerolinea = %s, pasajeros = %s WHERE id = %s")
                valores = (
                    origen.getId(), destino.getId(), capacidad, duracion, tipo, aerolinea.getId(),
                    pasajeros, vueloAEditar.getId())

                cursor.execute(query, valores)
                connection.commit()
                self.log("El vuelo ha sido editado!")
                self.app.needUpdate(True)
            else:
                raise ZeroResults

    def delete(self, connection):
        super().handleRequest()
        id = input("Ingresa el ID del vuelo a eliminar").strip()
        if id.upper() == "CANCELAR":
            raise CancelledPayload
        vuelos = self.find(int(id))
        if not len(vuelos) > 0: raise ZeroResults
        vuelo = vuelos[0]
        self.log("El vuelo a eliminar es:")
        vuelo.printDetail()

        if not self.app.getUtilities().confirm():
            raise CancelledPayload

        cursor = connection.cursor()
        query = f"DELETE FROM Vuelos WHERE id='{vuelo.getId()}'"
        cursor.execute(query)
        connection.commit()
        self.log("El vuelo ha sido eliminado")
        self.app.needUpdate(True)

    def getAll(self):
        self.app.updateData()
        return self.flights

    def clearData(self):
        self.flights.clear()

    def end(self):
        super().end()
        self.clearData()
