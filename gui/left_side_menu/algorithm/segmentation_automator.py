import os
from gui.canvas.plotting_options.plotting_option import PlottingOption
import gui.left_side_menu.algorithm.automator as automator
from util import getFlatTriangle
from logger import log

class SegmentationAutomator(automator.Automator):

    def __init__(self, parentFolder:str, chartId:int, totalFacesCount:int=None):
        self.chartId = chartId
        name = parentFolder + "/" + str(chartId)
        super().__init__(os.getcwd() + "/" + name + ".obj", name, totalFacesCount)

    def calculate(self):
        self.read()

        if len(self.faces) == 1:
            return self.processSingleTriangle()

        pointsBefore, facesBefore, pointsAfter, facesAfter = self.flatten()

        log("chart " + self.folderPath + " angularDist: " + str(self.angularDist))
        log("chart " + self.folderPath + " isometricDist: " + str(self.isometricDist))
        log("chart " + self.folderPath + " max angular dist: " + str(self.maxAngularDist))
        log("chart " + self.folderPath + " max isometric dist: " + str(self.maxIsometricDist))
        if self.shouldSegment(pointsAfter, facesAfter):
            faceToChart, data = self.segmentAndProcess()
            return faceToChart, data
        else: 
            return [1]*len(self.faces), [(1, pointsBefore, facesBefore, pointsAfter, facesAfter)]
