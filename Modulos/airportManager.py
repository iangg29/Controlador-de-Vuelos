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
from Objetos.Airport import Airport
from Utilidades.ModuleType import ModuleType
from Utilidades.RequestType import RequestType


class AirportManager(Module):
    """
    Módulo controlador de vuelos

    Gestiona y administra las solicitudes en torno a los aeropuertos.
    """

    def __init__(self, app, name):
        """
        Inicializa el módulo y crea una lista para almacenar los aeropuertos.

        :param app: Instancia de la aplicación principal
        :param name: Nombre del módulo
        """
        super().__init__(app, name, ModuleType.DATA)
        self.app = app
        self.airports = []
        self.mysqlModule = app.getMySQLManager()
        self.configurationModule = app.getConfiguracion()

    def printAll(self):
        """
        Imprime los registros de los aeropuertos.
        """
        print("Los aeropuertos registrados son: ")
        for aeropuerto in self.getAll():
            print(f"{aeropuerto.getId()}- {aeropuerto}")

    def handleRequest(self, request):
        """
        Gestiona la solicitud del usuario para modificar la información, ya sea para crear, buscar, editar, eliminar
        o impriir todos los registro.

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
        Convierte los regitros de la base de datos en objetos (Airport.py) y los almacena en una lista.

        :raise FailedDatabaseConnection: En caso de que no se logre una conexión exitosa con la base de datos.
        """
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
        """
        Filtra la lista de todos los registros con el id ingresado por el usuario

        :param id: Input del ID a buscar ingresado por el usuario
        :return: Lista de resultados
        """
        self.app.updateData()
        return list(filter(lambda airport: airport.getId() == id, self.airports))

    def findCodigo(self, code) -> list:
        """
        Filtra la lista de todos los registros con el código ingresado por el usuario

        :param code: Input del código a buscar ingresado por el usuario
        :return: Lista de resultados
        """
        self.app.updateData()
        return list(filter(lambda airport: airport.getCode().upper() == code.upper(), self.airports))

    def create(self, connection):
        """
        Crea un nuevo objeto de Aeropuerto con inputs del usuario y lo inserta en la base de datos.

        :param connection: Conexión del servidor

        :raise InvalidObject: En caso de que el usuario introduzca valor inválidos o los deje vacios.
        :raise CancelledPayload: En caso de que el usuario cancele la solicitud al servidor.
        """
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
        """
        Imprime la lista de todos los registros con el código o ID del vuelo ingresado por el usuario.
        """
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
        """
        Busca un aeropuerto con código o ID, lo edita, cambia de información y después se actualiza en la base de
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
        """
        Elimina un aeropuerto de la base de datos previamente buscado por código o ID.

        :param connection: Conexión a la base de datos

        :raise CancelledPayload: En caso de que el usuario cancele la solicitud al servidor.
        :raise ZeroResults: En caso de no haber encontrado ningún resultado.
        """
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
        """
        :return: Manda una solicitud de actualización de datos y regresa la lista de registros.
        """
        self.app.updateData()
        return self.airports

    def clearData(self):
        """
        Vacía la lista de registros de pasajeros.
        """
        self.airports.clear()

    def end(self):
        """
         Finaliza el módulo y limpia los registros para evitar errores.
         """
        super().end()
        self.clearData()
