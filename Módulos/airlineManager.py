#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.
from Exceptions.InvalidOption import InvalidOption
from Exceptions.ZeroResults import ZeroResults
from Objetos.Aerolinea import Aerolinea
from modulo import Modulo


class AirlineManager(Modulo):

    def __init__(self, app, name, mysql, configuracion):
        super().__init__(app, name)
        self.airlines = []
        self.mysqlModule = mysql
        self.configurationModule = configuracion

    def loadData(self):
        # self.log("[SQL] Cargando datos ...", LogType.NORMAL)
        connection = self.mysqlModule.initConnection(self.configurationModule.getUser(),
                                                     self.configurationModule.getPassword(),
                                                     self.configurationModule.getHost(),
                                                     self.configurationModule.getDB())
        if not connection: return
        # self.log("[SQL] La conexión con la base de datos fue exitosa.", LogType.NORMAL)
        cursor = connection.cursor()
        query = ("SELECT * FROM Aerolineas")

        cursor.execute(query)

        for x in cursor:
            newAirline = Aerolinea(x)
            if not x == newAirline:
                self.airlines.append(newAirline)

        # self.log("[SQL] Datos cargados correctamente.", LogType.NORMAL)
        cursor.close()
        connection.close()

    def findId(self, id) -> Aerolinea:
        self.loadData()
        for x in self.airlines:
            if x.getId() == id:
                return x

    def findCodigo(self, code) -> Aerolinea:
        self.loadData()
        for x in self.airlines:
            if x.getCode().upper() == code.upper():
                return x

    def buscar(self, tipo):
        if tipo == "ID":
            id = int(input("Por favor ingresa un id").strip())
            aerolinea = self.findId(id)
            if aerolinea:
                print(aerolinea)
            else:
                raise ZeroResults
        elif tipo == "CODIGO":
            codigo = str(input("Por favor ingresa un código").strip())
            aerolinea = self.findCodigo(codigo)
            if aerolinea:
                print(aerolinea)
            else:
                raise ZeroResults
        else:
            raise InvalidOption

    def getAll(self):
        self.loadData()
        return self.airlines

    def end(self):
        super().end()
        self.airlines.clear()
