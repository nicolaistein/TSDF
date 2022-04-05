import os
from gui.canvas.plotting_options.plotting_option import PlottingOption
import gui.left_side_menu.algorithm.automator as automator
from algorithms.algorithms import *
from util import getFlatTriangle
from logger import log


class SegmentationAutomator(automator.Automator):
    def __init__(self, parentFolder: str, chartId: int, totalFacesCount: int = None):
        self.chartId = chartId
        name = parentFolder + "/" + str(chartId)
        super().__init__(os.getcwd() + "/" + name + ".obj", name, totalFacesCount)

    def calculate(self):
        self.read()
        if len(self.faces) == 1:
            return self.processSingleTriangle()

        if self.isBasicShape():
            log("Object is a basic shape")
            pB, fB, pA, fA = executeBFF(self.getOptimalConeCount(), self.filename)
            (
                fI,
                maxfI,
                minfi,
            ) = self.calcDistortions(pB, fB, pA, fA)
            self.setDistortionValues(fI, maxfI, minfi)
            if self.shouldSegment(pA, fA):
                return self.segmentAndProcess()
            else:
                log("Object is not a basic shape")
                return [1] * len(self.faces), [(1, pB, fB, pA, fA)]

        pointsBefore, facesBefore, pointsAfter, facesAfter = self.flatten()
        if self.shouldSegment(pointsAfter, facesAfter):
            faceToChart, data = self.segmentAndProcess()
            return faceToChart, data
        else:
            return [1] * len(self.faces), [
                (1, pointsBefore, facesBefore, pointsAfter, facesAfter)
            ]
