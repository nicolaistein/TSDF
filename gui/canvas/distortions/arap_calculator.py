import math
from typing import List
from gui.canvas.distortions.plotting_option_calculator import PlottingOptionCalculator
from logger import log

class ArapCalculator(PlottingOptionCalculator):
 
    def getDistortion(self, faceBefore:List[int], faceAfter=List[int]):
        o1, o2 = self.getSingularValues(faceBefore, faceAfter)
        return math.pow(o1-1, 2) + math.pow(o2-1, 2)