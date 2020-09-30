#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 29/9/2020.

from enum import Enum, unique


@unique
class RequestType(Enum):
    """
    Tipo de solicitud del programa

    Cada módulo tendrá acceso a estos tipos de solicitud para afectar la información en la base de datos.
    """

    TODOS = "TODOS"
    CREAR = "CREAR"
    BUSCAR = "BUSCAR"
    EDITAR = "EDITAR"
    ELIMINAR = "ELIMINAR"
    INVALIDA = "INVALIDA"

    def __str__(self):
        """
        :return: Regresa el valor del tipo de solicitud.
        """
        return self.value
