#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.
from Exceptions.CancelledPayload import CancelledPayload
from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Exceptions.InvalidObject import InvalidObject
from Exceptions.ZeroResults import ZeroResults
from Objetos.Vuelo import Vuelo
from Utilidades.ModuleType import ModuleType
from modulo import Modulo


class FlightManager(Modulo):

    def __init__(self, app, name):
        super().__init__(app, name, ModuleType.DATA)
        self.app = app
        self.flights = []

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
                Vuelo(x[0], self.app.getAirportManager().findID(x[1])[0], self.app.getAirportManager().findID(x[2])[0],
                      x[3], x[4], x[5], self.app.getAirlineManager().findId(x[6])[0], x[7]))
        self.app.needUpdate(True)
        cursor.close()
        connection.close()

    def find(self, id) -> list:
        self.app.updateData()
        return list(filter(lambda vuelo: vuelo.getId() == id, self.flights))

    def buscar(self):
        vuelos = self.find(int(input("Por favor ingresa un id ").strip()))
        if len(vuelos) > 0:
            for vuelo in vuelos:
                vuelo.printDetail()
        else:
            raise ZeroResults

    def create(self, vuelo):
        if not vuelo: raise InvalidObject
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection
        cursor = connection.cursor()
        query = (
            "INSERT INTO Vuelos (origen, destino, capacidad, duracion, tipo, aerolinea, pasajeros) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        valores = (vuelo.getOrigen(), vuelo.getDestino(), vuelo.getCapacidad(), vuelo.getDuracion(), vuelo.getTipo(),
                   vuelo.getAerolinea(), vuelo.getPasajeros())

        cursor.execute(query, valores)
        connection.commit()
        self.log("Nuevo vuelo creado!")
        self.app.needUpdate(True)

    def edit(self, oldFlight, newFlight):
        if not oldFlight or not newFlight: raise InvalidObject
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection
        cursor = connection.cursor()

        query = (
            "UPDATE Vuelos SET origen = %s, destino = %s, capacidad = %s, duracion = %s, tipo = %s, aerolinea = %s, pasajeros = %s WHERE id = %s")
        valores = (newFlight.getOrigen(), newFlight.getDestino(), newFlight.getCapacidad(), newFlight.getDuracion(),
                   newFlight.getTipo(), newFlight.getAerolinea(), newFlight.getPasajeros(), oldFlight.getId())
        cursor.execute(query, valores)
        connection.commit()
        self.log(f"{cursor.rowcount} registro afectado.")
        self.app.needUpdate(True)

    def delete(self, vuelo):
        if not vuelo: raise InvalidObject
        sure = str(input(f"¿Estas seguro que deseas eliminar el vuelo [{vuelo}]? (S/N) ").strip()).upper()
        if sure == "S":
            connection = self.initConnection()
            if not connection: raise FailedDatabaseConnection
            cursor = connection.cursor()
            query = f"DELETE FROM Vuelos WHERE id='{vuelo.getId()}'"
            cursor.execute(query)
            connection.commit()
            self.log(f"{cursor.rowcount} registro(s) afectados.")
            self.app.needUpdate(True)
        else:
            raise CancelledPayload

    def getAll(self):
        self.app.updateData()
        return self.flights

    def clearData(self):
        self.flights.clear()

    def end(self):
        super().end()
        self.clearData()
