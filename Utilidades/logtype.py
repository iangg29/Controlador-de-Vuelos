#  Copyright (c) 2020
#  Ian García González
#  A01706892
#  Archivo creado el 1/9/2020.
from enum import Enum


class LogType(Enum):
    NORMAL = "[\033[92mi\033[0m]"
    ERROR = "[\033[91mError\033[0m]"
    SEVERE = "[\033[91m\033[1mError\033[0m]"

    def __str__(self):
        return self.value
