import math
from typing import List
from gui.canvas.distortions.plotting_option_calculator import PlottingOptionCalculator
from logger import log

class DefaultCalculator(PlottingOptionCalculator):
 
    def getColors(self):
        return {}

    def getDistortionValues(self):
        return self.distortions, self.totalDistortion