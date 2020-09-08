#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.

class ZeroResults(Exception):

    def __init__(self, message="[Error] No se encontraron resultados."):
        self.message = message
        super().__init__(message)
