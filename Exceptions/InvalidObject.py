#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.

class InvalidObject(Exception):

    def __init__(self, message="[Error] Objeto inválido."):
        self.message = message
        super().__init__(self.message)
