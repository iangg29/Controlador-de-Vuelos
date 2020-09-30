#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.
from Exceptions.CancelledPayload import CancelledPayload
from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Exceptions.InvalidObject import InvalidObject
from Exceptions.InvalidOption import InvalidOption
from Exceptions.ZeroResults import ZeroResults
from Objetos.Passenger import Passenger
from Utilidades.ModuleType import ModuleType
from Utilidades.RequestType import RequestType
from Module import Modulo


class PassengerManager(Modulo):

    def __init__(self, app, name):
        super().__init__(app, name, ModuleType.DATA)
        self.app = app
        self.passengers = []

    def printAll(self):
        print("Los pasajeros registrados son: ")
        for pasajero in self.getAll():
            print(f"{pasajero.getId()}- {pasajero}")

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
        query = ("SELECT * FROM Pasajeros")
        cursor.execute(query)

        for x in cursor:
            self.passengers.append(Passenger(x[0], x[1], x[2], x[3], x[4], x[5]))

        cursor.close()
        connection.close()

    def findId(self, id) -> list:
        self.app.updateData()
        return list(filter(lambda passenger: passenger.getId() == id, self.passengers))

    def findNombre(self, nombre) -> Passenger:
        self.app.updateData()
        return list(filter(lambda passenger: nombre.upper() in passenger.getName().upper(), self.passengers))

    def create(self, connection):
        super().handleRequest()
        nombre = str(input("Ingresa el name del pasajero").capitalize())
        if nombre.upper() == "CANCELAR":
            raise CancelledPayload
        email = str(input("Ingresa el email del pasajero").strip()).lower()
        celular = int(input("Ingresa el celular del pasajero").strip())
        edad = int(input("Ingresa la edad del pasajero").strip())
        vuelos = "[]"

        if not nombre or not email or not celular or edad < 0:
            raise InvalidObject

        pasajero = Passenger(0, nombre, email, celular, edad, vuelos)

        self.log("El pasajero a crear es:")
        pasajero.printDetail()

        if not self.app.getUtilities().confirm():
            raise CancelledPayload

        cursor = connection.cursor()
        query = ("INSERT INTO Pasajeros (name, email, celular, edad, vuelos) VALUES (%s, %s, %s, %s, %s)")
        valores = (
            pasajero.getName(), pasajero.getEmail(), pasajero.getCelular(), pasajero.getEdad(), pasajero.getVuelos())

        cursor.execute(query, valores)
        connection.commit()
        self.log("El pasajero ha sido creado.")
        self.app.needUpdate(True)

    def edit(self, connection):
        super().handleRequest()

        query = input("Por favor ingresa un name/ID: ").strip()
        if query.upper() == "CANCELAR":
            raise CancelledPayload
        else:
            pasajeros = self.findNombre(query.upper())
            if len(pasajeros) <= 0:
                pasajeros = self.findId(int(query))
                if len(pasajeros) > 0:
                    pasajero = pasajeros[0]
                else:
                    raise ZeroResults
            else:
                pasajero = pasajeros[0]

        if not pasajero:
            raise ZeroResults

        self.log("El pasajero a editar es:")
        pasajero.printDetail()

        nombre = str(input("Ingresa el nuevo name del pasajero").capitalize())
        email = str(input("Ingresa el nuevo email del pasajero").strip()).lower()
        celular = int(input("Ingresa el nuevo celular del pasajero").strip())
        edad = int(input("Ingresa la nueva edad del pasajero").strip())
        vuelos = "[]"

        if not nombre or not email or not celular or edad < 0:
            raise InvalidObject

        nuevoPasajero = Passenger(pasajero.getId(), nombre, email, celular, edad, vuelos)

        self.log("El pasajero actualizado es: ")
        nuevoPasajero.printDetail()

        if not self.app.getUtilities().confirm():
            raise CancelledPayload

        cursor = connection.cursor()
        query = ("UPDATE Pasajeros SET name = %s, email = %s, celular = %s, edad = %s, vuelos = %s WHERE id = %s")
        valores = (
            nuevoPasajero.getName(), nuevoPasajero.getEmail(), nuevoPasajero.getCelular(), nuevoPasajero.getEdad(),
            pasajero.getId())
        cursor.execute(query, valores)
        connection.commit()
        self.log("El pasajero ha sido editado.")
        self.app.needUpdate(True)

    def buscar(self):
        super().handleRequest()
        query = input("Por favor ingresa un name/ID: ").strip()
        if query.upper() == "CANCELAR":
            raise CancelledPayload
        else:
            pasajeros = self.findNombre(query.upper())
            if len(pasajeros) <= 0:
                pasajeros = self.findId(int(query))
                if len(pasajeros) > 0:
                    for pasajero in pasajeros:
                        pasajero.printDetail()
                else:
                    raise ZeroResults
            else:
                for pasajero in pasajeros:
                    pasajero.printDetail()

    def delete(self, connection):
        super().handleRequest()

        query = input("Por favor ingresa un name/ID: ").strip()
        if query.upper() == "CANCELAR":
            raise CancelledPayload
        else:
            pasajeros = self.findNombre(query.upper())
            if len(pasajeros) <= 0:
                pasajeros = self.findId(int(query))
                if len(pasajeros) > 0:
                    pasajero = pasajeros[0]
                else:
                    raise ZeroResults
            else:
                pasajero = pasajeros[0]

        if not pasajero:
            raise ZeroResults

        self.log("El pasajero a eliminar es:")
        pasajero.printDetail()

        if not self.app.getUtilities().confirm():
            raise CancelledPayload

        cursor = connection.cursor()
        query = f"DELETE FROM Pasajeros WHERE id='{pasajero.getId()}'"
        cursor.execute(query)
        connection.commit()
        self.log("El pasajero ha sido eliminado")
        self.app.needUpdate(True)

    def getAll(self):
        self.app.updateData()
        return self.passengers

    def clearData(self):
        self.passengers.clear()

    def end(self):
        super().end()
        self.clearData()
