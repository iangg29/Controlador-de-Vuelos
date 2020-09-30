#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.
from Exceptions.CancelledPayload import CancelledPayload
from Exceptions.FailedDatabaseConnection import FailedDatabaseConnection
from Exceptions.InvalidObject import InvalidObject
from Exceptions.InvalidOption import InvalidOption
from Exceptions.ZeroResults import ZeroResults
from Module import Module
from Objetos.Passenger import Passenger
from Utilidades.ModuleType import ModuleType
from Utilidades.RequestType import RequestType


class PassengerManager(Module):
    """
    Módulo controlador de pasajeros

    Gestiona y administra las solicitudes en torno a los pasajeros.

    """

    def __init__(self, app, name):
        """
        Inicializa el módulo y crea una lista para almacenar los pasajeros.

        :param app: Instancia de la aplicación principal.
        :param name: Nombre del módulo
        """
        super().__init__(app, name, ModuleType.DATA)
        self.app = app
        self.passengers = []

    def printAll(self):
        """
        Imprime los registros de los pasajeros.
        """
        print("Los pasajeros registrados son: ")
        for pasajero in self.getAll():
            print(f"{pasajero.getId()}- {pasajero}")

    def handleRequest(self, request):
        """
        Gestiona la solicitud del usuario para modificar la información, ya sea para crear, buscar, editar, eliminar
        o imprimir todos los registros.

        :param request: Input del usuario

        :raise FailedDatabaseConnection: En caso de que no se logre una conexión exitosa con la base de datos.
        :raise InvalidOption: En caso de que el usuario introduzca una opción inválida
        """
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
        """
        Convierte los registros de la base de datose en objetos (Passenger.py) y los almacena en una lista.

        :raise FailedDatabaseConnection: En caso de que no se logre una conexión exitosa con la base de datos.
        """
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
        """
        Filtra la lista de todos los registros con el id del pasajero ingresado por el usuario.

        :param id: Input del ID a buscar ingresado por el usuario
        :return: Lista de resultados
        """
        self.app.updateData()
        return list(filter(lambda passenger: passenger.getId() == id, self.passengers))

    def findNombre(self, nombre) -> Passenger:
        """
        Filtra la lista de todos los registros con el nombre del pasajero ingresado por el usuario.

        :param nombre: Input del usuario
        :return: Lista de resultados
        """
        self.app.updateData()
        return list(filter(lambda passenger: nombre.upper() in passenger.getName().upper(), self.passengers))

    def create(self, connection):
        """
        Crea un nuevo objeto de Pasajero con inputs del usuario y lo inserta en la base de datos.

        :param connection: Conexión del servidor

        :raise InvalidObject: En caso de que el usuario introduzca valor inválidos o los deje vacios.
        :raise CancelledPayload: En caso de que el usuario cancele la solicitud al servidor.
        """
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
        """
        Busca un pasajero con nombre o ID, lo edita, cambia de información y después se actualiza en la base de
        datos

        :param connection: Conexión del servidor

        :raise CancelledPayload: En caso de que el usuario cancele la solicitud al servidor
        :raise ZeroResults: En caso de que el sistema no encuentre resultados a la búsqueda del usuario.
        :raise InvalidObject: En caso de que el usuario introduzca valor inválidos o los deje vacios.
        """
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
        """
        Método para buscar pasajeros, ya sea por su nombre o por ID, una vez encontrado los posibles resultados imprime
        los detalles de cada pasajero encontrado.

        :raise CancelledPayload: En caso de que el usuario cancele la solicitud.
        :raise ZeroResults: En caso de no haber encontrado ningún resultado.
        """
        super().handleRequest()
        query = input("Por favor ingresa un nombre/ID: ").strip()
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
        """
        Elimina un pasajero de la base de datos previamente buscado por nombre o con ID.

        :param connection: Conexión a la base de datos

        :raise CancelledPayload: En caso de que el usuario cancele la solicitud al servidor.
        :raise ZeroResults: En caso de no haber encontrado ningún resultado.
        """
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
        """
        :return: Manda una solicitud de actualización de datos y regresa la lista de registros.
        """
        self.app.updateData()
        return self.passengers

    def clearData(self):
        """
        Vacía la lista de registros de pasajeros.
        """
        self.passengers.clear()

    def end(self):
        """
        Finaliza el módulo y limpia los registros para evitar errores.
        """
        super().end()
        self.clearData()
