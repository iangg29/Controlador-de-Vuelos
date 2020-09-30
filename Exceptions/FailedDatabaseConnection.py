#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 8/9/2020.

class FailedDatabaseConnection(Exception):
    """
    Excepción

    Ocurre cuando la conexión a la base de datos no es exitosa.
    """

    def __init__(self, message="[Error] No se ha podido establecer conexión con la base de datos."):
        """
        Inicializa y llama la excepción.

        :param message: Mensaje que aparecerá en la consola.
        """
        self.message = message
        super().__init__(self.message)
