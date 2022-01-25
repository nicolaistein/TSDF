import math
from typing import List
from gui.canvas.distortions.plotting_option_calculator import PlottingOptionCalculator
from logger import log

class LscmDistortion(PlottingOptionCalculator):

    def getDistortion(self, faceBefore:List[int], faceAfter=List[int]):
        o1, o2 = self.getSingularValues(faceBefore, faceAfter)
        log("o1: " + str(o1) + ", o2: " + str(o2))
        return o1/o2
#        return math.pow(o1-o2, 2)