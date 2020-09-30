#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.

class InvalidObject(Exception):
    """
    Excepción

    Ocurre cuando el objeto generado no es válido.
    """

    def __init__(self, message="[Error] Objeto inválido."):
        """
        Inicializa y llama la excepción.

        :param message: Mensaje que aparecerá en la consola.
        """
        self.message = message
        super().__init__(self.message)
