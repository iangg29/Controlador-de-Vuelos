#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.

class FailedDatabaseConnection(Exception):

    def __init__(self, message="[Error] No se ha podido establecer conexión con la base de datos."):
        self.message = message
        super().__init__(self.message)
