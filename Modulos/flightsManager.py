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
from Objetos.Flight import Flight
from Utilidades.ModuleType import ModuleType
from Utilidades.RequestType import RequestType


class FlightManager(Module):
    """
    Módulo controlador de vuelos

    Gestiona y administra las solicitudes en torno a los vuelos.
    """

    def __init__(self, app, name):
        """
        Inicializa el módulo y crea una lista para almacenar los vuelos.

        :param app: Instancia de la aplicación principal
        :param name: Nombre del módulo
        """
        super().__init__(app, name, ModuleType.DATA)
        self.app = app
        self.flights = []

    def printAll(self):
        """
        Imprime los registros de los vuelos.
        """
        print("Los vuelos registrados son: ")
        for vuelo in self.flights:
            print(f"- {vuelo}")

    def loadData(self):
        """
        Convierte los regitros de la base de datos en objetos (Flights.py) y los almacena en una lista.

        :raise FailedDatabaseConnection: En caso de que no se logre una conexión exitosa con la base de datos.
        """
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
        """
        Gestiona la solicitud del usuario para modificar la información, ya sea para crear, buscar, editar, eliminar
        o imprimir todos los registro.

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
        elif request == RequestType.PASAJEROS:
            self.pasajeros(connection)
        else:
            raise InvalidOption

    def menu(self):
        super().menu()
        print("- Pasajeros")

    def pasajeros(self, connection):
        """
        :return: Muestra los pasajeros del vuelo seleccionado.

        :raise ZeroResults: En caso de no encontrar el vuelo
        """
        accion = str(input("¿Qué deseas hacer? (Vuelo, Agregar, Eliminar) "))
        if accion.lower() == "vuelo":
            id = int(input("Ingresa el ID del vuelo a mostrar: ").strip())
            vuelos = self.find(id)
            if len(vuelos) <= 0: raise ZeroResults
            vuelo = vuelos[0]
            vuelo.printDetail()
            resultados = self.allPasajeros(vuelo)
            if len(resultados) <= 0: return
            for pasajero in resultados:
                print(pasajero)
        elif accion.lower() == "añadir" or accion.lower() == "agregar":
            vuelos = self.find(int(input("Ingresa el ID del vuelo para agregar el pasajero: ").strip()))
            if len(vuelos) <= 0: raise ZeroResults
            vuelo = vuelos[0]
            pasajeros = self.app.getPassengerManager().findId(
                int(input("Ingresa el ID del pasajero para agregar al vuelo: ").strip()))
            if len(pasajeros) <= 0: raise ZeroResults
            pasajero = pasajeros[0]
            self.agregarPasajero(vuelo, pasajero, connection)
        elif accion.lower() == "eliminar" or accion.lower() == "borrar":
            pasajeros = self.app.getPassengerManager().findId(
                int(input("Ingresa el ID del pasajero para borrar del vuelo: ").strip()))
            if len(pasajeros) <= 0: raise ZeroResults
            pasajero = pasajeros[0]
            vuelos = self.find(
                int(input("Ingresa el ID del vuelo para borrar el pasajero: ").strip()))
            if len(vuelos) <= 0: raise ZeroResults
            vuelo = vuelos[0]
            self.eliminarPasajero(vuelo, pasajero, connection)
        else:
            raise InvalidOption

    def allPasajeros(self, vuelo) -> list:
        """
        :param vuelo: Objeto del vuelo a mostrar pasajeros
        :return: Lista de los pasajeros de un vuelo
        """
        if vuelo.getPasajeros() == "-1": raise ZeroResults
        pasajerosID = vuelo.getPasajeros().split("-")
        pasajeros = []
        for pasajeroID in pasajerosID:
            busqueda = self.app.getPassengerManager().findId(int(pasajeroID))
            if len(busqueda) <= 0: continue
            pasajeros.append(busqueda[0])
        return pasajeros

    def find(self, id) -> list:
        """
        Filtra la lista de todos los registros con el id ingresado por el usuario

        :param id: Input del ID a buscar ingresado por el usuario
        :return: Lista de resultados
        """
        self.app.updateData()
        return list(filter(lambda vuelo: vuelo.getId() == id, self.flights))

    def buscar(self):
        """
        Filtra la lista de todos los registros con el id del vuelo ingresado por el usuario.

        :param nombre: Input del usuar
        :return: Lista de resultados
        """
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
        """
        Crea un nuevo objeto de Vuelo con inputs del usuario y lo inserta en la base de datos.

        :param connection: Conexión del servidor

        :raise InvalidObject: En caso de que el usuario introduzca valor inválidos o los deje vacios.
        :raise CancelledPayload: En caso de que el usuario cancele la solicitud al servidor.
        """
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
        pasajeros = "-1"

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
        """
        Busca un vuelo con ID, lo edita, cambia de información y después se actualiza en la base de
        datos

        :param connection: Conexión del servidor

        :raise CancelledPayload: En caso de que el usuario cancele la solicitud al servidor
        :raise ZeroResults: En caso de que el sistema no encuentre resultados a la búsqueda del usuario.
        :raise InvalidObject: En caso de que el usuario introduzca valor inválidos o los deje vacios.
        """
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

                if capacidad <= 0 or duracion <= 0:
                    raise InvalidObject

                nuevoVuelo = Flight(vueloAEditar.getId(), origen, destino, capacidad, duracion, tipo, aerolinea,
                                    vueloAEditar.getPasajeros())

                self.log("El vuelo actualizado es: ")
                nuevoVuelo.printDetail()
                if not self.app.getUtilities().confirm():
                    raise CancelledPayload

                cursor = connection.cursor()
                query = (
                    "UPDATE Vuelos SET origen = %s, destino = %s, capacidad = %s, duracion = %s, tipo = %s, aerolinea = %s, pasajeros = %s WHERE id = %s")
                valores = (
                    origen.getId(), destino.getId(), capacidad, duracion, tipo, aerolinea.getId(),
                    vueloAEditar.getPasajeros(), vueloAEditar.getId())

                cursor.execute(query, valores)
                connection.commit()
                self.log("El vuelo ha sido editado!")
                self.app.needUpdate(True)
            else:
                raise ZeroResults

    def delete(self, connection):
        """
        Elimina un vuelo de la base de datos previamente buscado por ID.

        :param connection: Conexión a la base de datos

        :raise CancelledPayload: En caso de que el usuario cancele la solicitud al servidor.
        :raise ZeroResults: En caso de no haber encontrado ningún resultado.
        """
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
        """
        :return: Manda una solicitud de actualización de datos y regresa la lista de registros.
        """
        self.app.updateData()
        return self.flights

    def clearData(self):
        """
        Vacía la lista de registros de vuelos.
        """
        self.flights.clear()

    def end(self):
        """
         Finaliza el módulo y limpia los registros para evitar errores.
        """
        super().end()
        self.clearData()
