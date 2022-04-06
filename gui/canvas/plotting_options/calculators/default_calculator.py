from gui.canvas.plotting_options.plotting_option_calculator import (
    PlottingOptionCalculator,
)
from logger import log


class DefaultCalculator(PlottingOptionCalculator):
    def getColors(self):
        return {}

    def getDistortionValues(self):
        return self.distortions, self.totalDistortion
