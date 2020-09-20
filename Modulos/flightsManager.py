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
            "SELECT * FROM Vuelos INNER JOIN Aerolineas ON Vuelos.`aerolinea` = Aerolineas.`id` INNER JOIN Aeropuertos AS Aeropuerto1 ON Vuelos.`origen` = Aeropuerto1.`id` INNER JOIN Aeropuertos AS Aeropuerto2 ON  Vuelos.`destino` = Aeropuerto2.`id` INNER JOIN Pasajeros ON Vuelos.`pasajeros`= Pasajeros.`id`")
        cursor.execute(query)

        for x in cursor:
            print(x)
            self.flights.append(Vuelo(x))

        cursor.close()
        connection.close()

    def find(self, id) -> Vuelo:
        self.app.updateData()
        for x in self.flights:
            if x.getId() == id:
                return x

    def buscar(self):
        id = int(input("Por favor ingresa un id ").strip())
        vuelo = self.find(id)
        if vuelo:
            print("---- VUELO ----")
            print(f"ID: {vuelo.getId()}")
            print(f"Origen: {vuelo.getOrigen()}")
            print(f"Destino: {vuelo.getDestino()}")
            print(f"Capacidad: {vuelo.getCapacidad()}")
            print(f"Duración: {vuelo.getDuracion()}")
            print(f"Tipo: {('NACIONAL', 'INTERNACIONAL')[vuelo.getTipo() == 'INT']}")
            print(f"Aerolinea: {vuelo.getAerolinea()}")
            print(f"Pasajeros: {vuelo.getPasajeros()}")
            print("------------------")
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
