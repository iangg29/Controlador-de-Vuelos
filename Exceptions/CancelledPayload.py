#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.

class CancelledPayload(Exception):
    """
    Excepción

    Ocurre cuando el usuario cancela el proceso.
    """

    def __init__(self, message="[Error] Se ha cancelado la solicitud."):
        """
        Inicializa y llama la excepción.

        :param message: Mensaje que aparecerá en la consola.
        """
        self.message = message
        super().__init__(self.message)
