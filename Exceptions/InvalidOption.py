#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.

class InvalidOption(Exception):
    """
    Excepción

    Ocurre cuando la opción ingresada por el usuario no es correcta.
    """

    def __init__(self, message="[Error] Opción inválida"):
        """
        Inicializa y llama la excepción.

        :param message: Mensaje que aparecerá en la consola.
        """
        self.message = message
        super().__init__(self.message)
