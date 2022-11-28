from typing import List
from gui.canvas.plotting_options.plotting_option_calculator import (
    PlottingOptionCalculator,
)
from logger import log


class DefaultCalculator(PlottingOptionCalculator):
    def getColors(self):
        return {}

    def getDistortion(self, faceBefore: List[int], faceAfter=List[int]):
        return 5

    def getDistortionValues(self):
        return self.distortions, self.totalDistortion

    def distortionToColor(self, distortion: float):
        color = "#%02x%02x%02x" % (100, 100, 100)
        return color
