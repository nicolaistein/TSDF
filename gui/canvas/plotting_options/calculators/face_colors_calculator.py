from typing import List
from gui.canvas.plotting_options.plotting_option_calculator import (
    PlottingOptionCalculator,
)
from logger import log


class FaceColorsCalculator(PlottingOptionCalculator):
    def getColors(self):
        return {index: self.color for index, _ in enumerate(self.facesAfter)}

    def getDistortionValues(self):
        return self.distortions, self.totalDistortion
