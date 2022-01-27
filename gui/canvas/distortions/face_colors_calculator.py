import math
from typing import List
from gui.canvas.distortions.plotting_option_calculator import PlottingOptionCalculator
from logger import log

class FaceColorsCalculator(PlottingOptionCalculator):
    
    def getColors(self):
        return {index:self.color for index, _ in enumerate(self.facesAfter)}