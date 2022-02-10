from typing import Mapping
import os
from gui.canvas.plotting_options.plotting_option import PlottingOption
import gui.left_side_menu.algorithm.automator as automator

class SegmentationAutomator(automator.Automator):

    def __init__(self, parentFolder:str, faceMapping:Mapping, chartId:int):
        self.faceMapping = faceMapping
        name = parentFolder+"/"+str(chartId)
        super.__init__(os.getcwd() + "/" + name + ".obj", name)

    def calculate(self):
        self.read()
        pointsBefore, facesBefore, pointsAfter, facesAfter = self.flatten()
        _, self.angularDist, _ = PlottingOption.LSCM.getOptionCalculator(pointsBefore,
            facesBefore, pointsAfter, facesAfter, "", 1).getDistortionValues()
        _, self.isometricDist, _ = PlottingOption.ARAP.getOptionCalculator(pointsBefore,
            facesBefore, pointsAfter, facesAfter, "", 1).getDistortionValues()

        if (self.angularDist > self.maxAngularDistortion or
            self.isometricDist > self.maxIsometricDistortion):
            faceToChart = self.segmentAndProcess()
            return faceToChart, [(pointsBefore, facesBefore, pointsAfter, facesAfter)]
        else: 
            return [self.chartId]*len(self.faces), [(pointsBefore, facesBefore, pointsAfter, facesAfter)]
        #Todo: Map faces back
        #Todo: Return list of charts, chartKeys already mapped
