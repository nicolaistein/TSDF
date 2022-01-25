from typing import List

from pyparsing import col
from logger import log
from tkinter import *
from gui.canvas.distortions.plotting_option import PlottingOption
from gui.canvas.distortions.plotting_option_calculator import PlottingOptionCalculator

class OptionsPlotter:

    calculators:List[PlottingOptionCalculator] = []
    currentOption:PlottingOption = PlottingOption.NO_DIST

    def __init__(self,canvasManager, verticesToPlot, verticesBefore:List[List[float]], facesBefore:List[List[int]],
        verticesAfter:List[List[float]], facesAfter:List[List[int]], color):
        self.cv = canvasManager
        self.canvas = canvasManager.canvas
        self.verticesToPlot = verticesToPlot
        self.color = color
        self.faces = facesAfter   

        log("verticesToPlot: " + str(verticesToPlot))
        log("verticesAfter: " + str(verticesAfter))

        self.distortionOnCanvas = []
        self.calculators = {e.value:e.getOptionCalculator(verticesBefore, facesBefore,
            verticesAfter, facesAfter) for e in PlottingOption if e.hasCalculator()}

    def createLine(self, x1, x2):
        self.distortionOnCanvas.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1]))

    def setOption(self, distortion:PlottingOption = PlottingOption.NO_DIST):
        self.currentOption = distortion
        self.refresh()


    def refresh(self):
        self.clear()
        self.show()
        
    def show(self):
    #    log("show called current: " + str(self.currentOption) + ", " + str(self.calculators))
        if self.currentOption not in self.calculators: return

        calculator = self.calculators[self.currentOption]
        calculator.getDistortionValues()
        colors = calculator.getColors()
        
        log("colors: " + str(colors))

        if not colors: return
        for index, face in enumerate(self.faces):

            x = list(self.verticesToPlot[face[0]])
            y = list(self.verticesToPlot[face[1]])
            z = list(self.verticesToPlot[face[2]])

            self.distortionOnCanvas.append(
                self.canvas.create_polygon(x, y, z, fill=colors[index]))

    def clear(self):
        for point in self.distortionOnCanvas:
            self.canvas.delete(point)
        self.distortionOnCanvas.clear()




    def showAreaDistortion(self):
        for index, face in enumerate(self.faces):
            if index not in self.areaDistortions: continue

            x = list(self.verticesToPlot[face[0]])
            y = list(self.verticesToPlot[face[1]])
            z = list(self.verticesToPlot[face[2]])

            maxDistort = 20
            distortion = self.areaDistortions[index]

            if distortion > 1:
                distFac = distortion
                if distFac > maxDistort:
                    distFac = maxDistort
                if distFac < 1:
                    distFac = 1

                distFac = distFac-1
                distFac = distFac/(maxDistort-1)
                distFac = 1-distFac

                colorFac = int(round(distFac * 255, 0))
                color = '#%02x%02x%02x' % (255, colorFac, colorFac)

            else:
                blueFac = distortion
                colorFac = int(round(blueFac * 255, 0))
                color = '#%02x%02x%02x' % (colorFac, colorFac, 255)
            
            self.distortionOnCanvas.append(
            self.canvas.create_polygon(x, y, z, fill=color))


    def showAngleDistortion(self):
        for index, face in enumerate(self.faces):
            if index not in self.angularDistortions: continue

            x = list(self.vertices[face[0]])
            y = list(self.vertices[face[1]])
            z = list(self.vertices[face[2]])
            
            distortion = self.angularDistortions[index]/30
            if distortion > 1:
                distortion = 1

            distFac = 1-distortion
            colorFac = int(round(distFac * 255, 0))
            color = '#%02x%02x%02x' % (colorFac, 255, colorFac)
            
            self.distortionOnCanvas.append(
                self.canvas.create_polygon(x, y, z, fill=color))


