from enum import Enum


class ComputationMode(Enum):
    """The different modi for unwrapping an object"""

    AUTOMATIC = 0
    MANUAL = 1

    def getOpposite(self):
        return (
            ComputationMode.AUTOMATIC
            if self == ComputationMode.MANUAL
            else ComputationMode.MANUAL
        )

    def default():
        return ComputationMode.AUTOMATIC
