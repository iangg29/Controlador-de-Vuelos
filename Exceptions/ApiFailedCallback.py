#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.

class ApiFailedCallback(Exception):
    """
    Excepción

    Ocurre cuando el servidor regresa un error.
    """

    def __init__(self, app, message="[API] Failed retrieving data [500]", code=500):
        """
        Inicializa y llama la excepción.

        :param message: Mensaje que aparecerá en la consola.
        """
        self.app = app
        self.code = code
        self.message = f"{message} [{code}]."
        super().__init__(self.message, self.code)
