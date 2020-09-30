#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class ModuleFailedLoading(Exception):
    """
    Excepción

    Ocurre cuando algún módulo no inicia de manera correcta.
    """

    def __init__(self, message="[MODULO] Failed loading."):
        """
        Inicializa y llama la excepción.

        :param message: Mensaje que aparecerá en la consola.
        """
        self.message = message
        super().__init__(self.message)
