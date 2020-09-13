#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 12/9/2020.
from enum import Enum, unique


@unique
class ModuleType(Enum):
    UTILITY = "UTILITY"
    DATA = "DATA"

    def __str__(self):
        return self.value
