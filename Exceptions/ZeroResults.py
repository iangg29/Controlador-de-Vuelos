#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.

class ZeroResults(Exception):
    """
    Excepción

    Ocurre cuando no se encuentran resultados en alguna búsqueda.
    """

    def __init__(self, message="[Error] No se encontraron resultados."):
        """
        Inicializa y llama la excepción.

        :param message: Mensaje que aparecerá en la consola.
        """
        self.message = message
        super().__init__(message)
