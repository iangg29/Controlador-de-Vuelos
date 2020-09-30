#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 29/9/2020.

from enum import Enum, unique


@unique
class RequestType(Enum):
    TODOS = "TODOS"
    CREAR = "CREAR"
    BUSCAR = "BUSCAR"
    EDITAR = "EDITAR"
    ELIMINAR = "ELIMINAR"
    INVALIDA = "INVALIDA"

    def __str__(self):
        return self.value
