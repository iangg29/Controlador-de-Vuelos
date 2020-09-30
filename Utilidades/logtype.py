#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
from enum import Enum, unique


@unique
class LogType(Enum):
    """
    Tipo de mensaje

    Clase para definir el tipo de mensaje que se imprimirá en la consola. Dependiendo de estos variará el prefijo
    que tenga dicho mensaje.
    """
    NORMAL = "[\033[92mi\033[0m]"
    ERROR = "[\033[91mError\033[0m]"
    SEVERE = "[\033[91m\033[1mError\033[0m]"

    def __str__(self):
        """
        :return: Regresa el valor del tipo de mensaje.
        """
        return self.value
