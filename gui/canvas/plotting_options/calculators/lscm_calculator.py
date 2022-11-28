import math
from typing import List
from gui.canvas.plotting_options.plotting_option_calculator import (
    PlottingOptionCalculator,
)
from logger import log


class LscmCalculator(PlottingOptionCalculator):
    def getDistortion(self, faceBefore: List[int], faceAfter=List[int]):
        o1, o2 = self.getSingularValues(faceBefore, faceAfter)
        return 0.08
