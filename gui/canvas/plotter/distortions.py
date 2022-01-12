from tkinter import *

from PIL.Image import init
import gui.canvas.translator as translator
from patterns.gcode_cmd import GCodeCmd
from gui.pattern_model import PatternModel

class DistortionPlotter:
    plotDistortion:str = "none"

    def __init__(self,canvasManager):
        self.cv = canvasManager
        self.canvas = canvasManager.canvas
        self.distortionOnCanvas = []

    def createLine(self, x1, x2):
        self.distortionOnCanvas.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1]))

    def setDistortion(self, distortion:str = "none"):
        if self.plotDistortion == distortion: 
            self.plotDistortion = "none"
        else:
            self.plotDistortion = distortion

    def plot(self, points, faces, areaDistortions, angularDistortions):
        self.areaDistortions = areaDistortions
        self.angularDistortions = angularDistortions
        self.faces = faces    
        self.points = points

    def refresh(self):
        self.clear()
        self.showDistortion()
        
    def showDistortion(self):
        if self.plotDistortion == "area": self.showAreaDistortion()
        if self.plotDistortion == "angle": self.showAngleDistortion()
            

    def showAreaDistortion(self):
        for index, face in enumerate(self.faces):
            if index not in self.areaDistortions: continue

            x = list(self.points[face[0]-1])
            y = list(self.points[face[1]-1])
            z = list(self.points[face[2]-1])

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

            x = list(self.points[face[0]-1])
            y = list(self.points[face[1]-1])
            z = list(self.points[face[2]-1])
            
            distortion = self.angularDistortions[index]/30
            if distortion > 1:
                distortion = 1

            distFac = 1-distortion
            colorFac = int(round(distFac * 255, 0))
            color = '#%02x%02x%02x' % (colorFac, 255, colorFac)
            
            self.distortionOnCanvas.append(
                self.canvas.create_polygon(x, y, z, fill=color))


    def clear(self):
        for point in self.distortionOnCanvas:
            self.canvas.delete(point)
        self.distortionOnCanvas.clear()

