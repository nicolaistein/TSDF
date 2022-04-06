import math
from typing import List
from gui.canvas.plotting_options.plotting_option_calculator import (
    PlottingOptionCalculator,
)
from logger import log


class EfficientIsometricCalculator(PlottingOptionCalculator):
    def getDistortion(self, faceBefore: List[int], faceAfter=List[int]):
        o1, o2 = self.getSingularValues(faceBefore, faceAfter)
        firstPart = 1 + math.pow(o1, -2) * math.pow(o2, -2)
        secondPart = math.pow(o1, -2) + math.pow(o2, -2)
        return firstPart * secondPart

    def distortionToColor(self, distortion: float):
        minD, optimalD, maxD = self.option.getMinMax()
        if distortion > maxD:
            distortion = maxD

        if distortion >= optimalD:
            dist = abs(distortion - optimalD) / abs(maxD - optimalD)
        else:
            dist = abs(distortion - optimalD) / abs(minD - optimalD)

        color = self.option.getColor()
        r, g, b = color

        stepSizeR = (255 - r) * dist
        stepSizeG = (255 - g) * dist
        stepSizeB = (255 - b) * dist

        colorFacR = int(round(stepSizeR, 0))
        colorFacG = int(round(stepSizeG, 0))
        colorFacB = int(round(stepSizeB, 0))

        color = "#%02x%02x%02x" % (255 - colorFacR, 255 - colorFacG, 255 - colorFacB)
        return color
