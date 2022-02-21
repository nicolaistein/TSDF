import math
from typing import List
from gui.canvas.plotting_options.plotting_option_calculator import PlottingOptionCalculator
from logger import log

class EfficientIsometricCalculator(PlottingOptionCalculator):
 
    def getDistortion(self, faceBefore:List[int], faceAfter=List[int]):
        o1, o2 = self.getSingularValues(faceBefore, faceAfter)
        firstPart = 1 + math.pow(o1, -2) * math.pow(o2, -2)
        secondPart =  math.pow(o1, -2) + math.pow(o2, -2)
        return firstPart * secondPart