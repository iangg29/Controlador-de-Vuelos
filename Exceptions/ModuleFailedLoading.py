#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class ModuleFailedLoading(Exception):

    def __init__(self, message="[MODULO] Failed loading."):
        self.message = message
        super().__init__(self.message)
