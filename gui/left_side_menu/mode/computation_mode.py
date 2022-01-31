from enum import Enum

class ComputationMode(Enum):
    AUTOMATIC = 0
    MANUAL = 1

    def getOpposite(self):
         return ComputationMode.AUTOMATIC if self==ComputationMode.MANUAL else ComputationMode.MANUAL
    
    def default(): return ComputationMode.AUTOMATIC
     

