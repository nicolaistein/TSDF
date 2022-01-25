import math
from typing import List
from gui.canvas.distortions.plotting_option_calculator import PlottingOptionCalculator

class FaceColors(PlottingOptionCalculator):

    def getDistortion(self, faceBefore:List[int], faceAfter=List[int]):
        o1, o2 = self.getSingularValues(faceBefore, faceAfter)
        return math.pow(o1-o2, 2)