#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.
from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Exceptions.InvalidObject import InvalidObject
from Exceptions.InvalidOption import InvalidOption
from Exceptions.ZeroResults import ZeroResults
from Objetos.Pasajero import Pasajero
from Utilidades.ModuleType import ModuleType
from modulo import Modulo


class PassengerManager(Modulo):

    def __init__(self, app, name):
        super().__init__(app, name, ModuleType.DATA)
        self.app = app
        self.passengers = []
        self.mysqlManager = app.getMySQLManager()
        self.configurationManager = app.getConfiguracion()

    def loadData(self):
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection
        cursor = connection.cursor()
        query = ("SELECT * FROM Pasajeros LEFT OUTER JOIN  Vuelos V on V.id = Pasajeros.vuelos")
        cursor.execute(query)

        for x in cursor:
            self.passengers.append(Pasajero(x))

        cursor.close()
        connection.close()

    def findId(self, id) -> Pasajero:
        self.app.updateData()
        for x in self.passengers:
            if x.getId() == id:
                return x

    def findNombre(self, nombre) -> Pasajero:
        self.app.updateData()
        for x in self.passengers:
            if x.getName().upper() == nombre.upper():
                return x

    def create(self, pasajero):
        if not pasajero: raise InvalidObject
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection
        cursor = connection.cursor()
        query = ("INSERT INTO Pasajeros (nombre, email, celular, edad, vuelos) VALUES (%s, %s, %s, %s, null)")
        valores = (pasajero.getName(), pasajero.getEmail(), pasajero.getCelular(), pasajero.getEdad())

        cursor.execute(query, valores)
        connection.commit()
        self.log("Nuevo registro creado.")
        self.app.needUpdate(True)

    def edit(self, oldPasajero, newPasajero):
        if not oldPasajero or not newPasajero: raise InvalidObject
        connection = self.initConnection()
        if not connection: raise FailedDatabaseConnection
        cursor = connection.cursor()

        query = ("UPDATE Pasajeros SET nombre = %s, email = %s, celular = %s, edad = %s, vuelos = %s WHERE id = %s")
        valores = (newPasajero.getName(), newPasajero.getEmail(), newPasajero.getCelular(), newPasajero.getEdad(),
                   oldPasajero.getId())
        cursor.execute(query, valores)
        connection.commit()
        self.log(f"{cursor.rowcount} registro afectado.")
        self.app.needUpdate(True)

    def buscar(self, tipo):
        if tipo == "ID":
            id = int(input("Por favor ingresa un id ").strip())
            pasajero = self.findId(id)
            if pasajero:
                print("---- PASAJERO ----")
                print(f"ID: {pasajero.getId()}")
                print(f"Nombre: {pasajero.getName()}")
                print(f"Email: {pasajero.getEmail()}")
                print(f"Celular: {pasajero.getCelular()}")
                print(f"Edad: {pasajero.getEdad()}")
                print(f"Vuelos: {pasajero.getVuelos()}")
                print("------------------")
            else:
                raise ZeroResults
        elif tipo == "NOMBRE":
            nombre = str(input("Por favor ingresa el nombre del pasajero: ").strip())
            pasajero = self.findNombre(nombre)
            if pasajero:
                print("---- PASAJERO ----")
                print(f"ID: {pasajero.getId()}")
                print(f"Nombre: {pasajero.getName()}")
                print(f"Email: {pasajero.getEmail()}")
                print(f"Celular: {pasajero.getCelular()}")
                print(f"Edad: {pasajero.getEdad()}")
                print(f"Vuelos: {pasajero.getVuelos()}")
                print("------------------")
            else:
                raise ZeroResults
        else:
            raise InvalidOption

    def delete(self, pasajero):
        if not pasajero: raise InvalidObject
        sure = str(input(f"¿Estas seguro que deseas eliminar la aerolinea [{aerolinea}]? (S/N) ").strip()).upper()
        if sure == "S":
            connection = self.initConnection()
            if not connection: raise FailedDatabaseConnection
            cursor = connection.cursor()
            query = f"DELETE FROM Pasajeros WHERE id='{pasajero.getId()}'"
            cursor.execute(query)
            connection.commit()
            self.log(f"{cursor.rowcount} registro(s) afectados.")
            self.app.needUpdate(True)
        else:
            raise CancelledPayload

    def getAll(self):
        self.app.updateData()
        return self.passengers

    def clearData(self):
        self.passengers.clear()

    def end(self):
        super().end()
        self.clearData()

    def initConnection(self):
        return self.mysqlManager.initConnection(self.configurationManager.getUser(),
                                                self.configurationManager.getPassword(),
                                                self.configurationManager.getHost(),
                                                self.configurationManager.getDB())
