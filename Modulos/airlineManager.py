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
from Objetos.Airline import Airline
from Utilidades.ModuleType import ModuleType
from Utilidades.RequestType import RequestType


class AirlineManager(Module):
    """
    Módulo controlador de aerolineas

    Gestiona y administra las solicitudes en torno a las aerolíneas.
    """

    def __init__(self, app, name):
        """
        Inicializa el módulo y crea una lista para almacenar las aerolineas.

        :param app: Instancia de la aplicación principal
        :param name: Nombre del módulo
        """
        super().__init__(app, name, ModuleType.DATA)
        self.app = app
        self.airlines = []

    def printAll(self):
        """
        Imprime los registros de las aerolineas.
        """
        print("Las aerolineas registradas son: ")
        for aerolinea in self.getAll():
            print(f"- {aerolinea}")

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
        else:
            raise InvalidOption

    def loadData(self):
        """
        Convierte los regitros de la base de datos en objetos (Airline.py) y los almacena en una lista.

        :raise FailedDatabaseConnection: En caso de que no se logre una conexión exitosa con la base de datos.
        """
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
        """
        Filtra la lista de todos los registros con el id ingresado por el usuario

        :param id: Input del ID a buscar ingresado por el usuario
        :return: Lista de resultados
        """
        self.app.updateData()
        return list(filter(lambda aerolinea: aerolinea.getId() == id, self.airlines))

    def create(self, connection):
        """
        Crea un nuevo objeto de Aerolinea con inputs del usuario y lo inserta en la base de datos.

        :param connection: Conexión del servidor

        :raise InvalidObject: En caso de que el usuario introduzca valor inválidos o los deje vacios.
        :raise CancelledPayload: En caso de que el usuario cancele la solicitud al servidor.
        """
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
        """
        Busca una aerolinea con ID, lo edita, cambia de información y después se actualiza en la base de
        datos

        :param connection: Conexión del servidor

        :raise CancelledPayload: En caso de que el usuario cancele la solicitud al servidor
        :raise ZeroResults: En caso de que el sistema no encuentre resultados a la búsqueda del usuario.
        :raise InvalidObject: En caso de que el usuario introduzca valor inválidos o los deje vacios.
        """
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
        """
        Filtra la lista de todos los registros con el código ingresado por el usuario

        :param code: Input del código a buscar ingresado por el usuario
        :return: Lista de resultados
        """
        self.app.updateData()
        return list(filter(lambda aerolinea: aerolinea.getCode().upper() == code.upper(), self.airlines))

    def buscar(self):
        """
        Imprime la lista de todos los registros con el id o código de la aerolínea ingresado por el usuario.
        """
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
        """
        Elimina una aerolínea de la base de datos previamente buscado por código o ID.

        :param connection: Conexión a la base de datos

        :raise CancelledPayload: En caso de que el usuario cancele la solicitud al servidor.
        :raise ZeroResults: En caso de no haber encontrado ningún resultado.
        """
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
        """
        :return: Manda una solicitud de actualización de datos y regresa la lista de registros.
        """
        self.app.updateData()
        return self.airlines

    def clearData(self):
        """
        Vacía la lista de registros de aerolineas.
        """
        self.airlines.clear()

    def end(self):
        """
         Finaliza el módulo y limpia los registros para evitar errores.
        """
        super().end()
        self.clearData()
