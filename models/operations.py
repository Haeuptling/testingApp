from enum import Enum

class Operations(Enum):
    NONE = 0
    PRESSURE_SELF_TEST = 1
    PRESSURE_TEST = 2

    @staticmethod
    def toString(operation):
        if operation == Operations.PRESSURE_SELF_TEST:
            return "PRESSURE_SELF_TEST"
        elif operation == Operations.PRESSURE_TEST:
            return "PRESSURE_TEST"
        else:
            return "NONE"