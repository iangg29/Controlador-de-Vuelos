#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 12/9/2020.
from enum import Enum, unique


@unique
class ModuleType(Enum):
    """
    Tipo de módulo

    Clase para definir los tipos de módulo existentes, para poder ejecutar funciones en base a estos.
    """

    UTILITY = "UTILITY"
    DATA = "DATA"

    def __str__(self):
        """
        :return: Regresa el valor del tipo de módulo.
        """
        return self.value
