from tkinter import *
from typing import Pattern
from PIL.Image import init
import gui.canvas.translator as translator
from patterns.gcode_cmd import GCodeCmd
from gui.pattern_model import PatternModel
from gui.canvas.plotter.distortion_plotter import DistortionPlotter
from gui.canvas.plotter.pattern_plotter import PatternPlotter
from gui.canvas.plotter.object_plotter import ObjectPlotter

class CanvasManager:

    plotFaces:bool = False

    def __init__(self, master: Frame, initSize: int):
        self.size = initSize
        self.canvasFrame = Frame(master, height=self.size, width=self.size)
        self.canvas = Canvas(self.canvasFrame, height=self.size, width=self.size)
        self.distortionPlotter = DistortionPlotter(self)
        self.patternPlotter = PatternPlotter(self)
        self.objectPlotter = ObjectPlotter(self)
        self.placedPatternsMenu = None
        self.xmax = initSize
        self.ymax = initSize
        self.points = []
        self.faces = []
        self.flatObjectOnCanvas = []
        self.rulers = []

    def P(self, x,y):
        """
        Transform point from cartesian (x,y) to Canvas (X,Y)
        """
        M=4
        X = M + (x/self.xmax) * (self.size-2*M)
        Y = M + (1-(y/self.ymax)) * (self.size-2*M)
        return (X,Y)

    def plot(self, points, faces, areaDistortions, angularDistortions):
        self.faces = faces
        pointsNew = translator.moveToPositiveArea(points)
        self.points = pointsNew
        maxValue = 0
        for p in pointsNew:
            for x in p:
                if maxValue < x: maxValue = x
        self.xmax = self.ymax = round(maxValue, 2)

        for index, p in enumerate(self.points):
            self.points[index] = list(self.P(p[0], p[1]))

        self.distortionPlotter.plot(self.points, self.faces, areaDistortions, angularDistortions)
        self.objectPlotter.plot(self.points, self.faces)
        self.objectPlotter.plotFaces = False

        self.placedPatternsMenu.deleteAll()
        self.show()


    def createLine(self, x1, x2):
        self.flatObjectOnCanvas.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1]))

    def plotRulers(self):
        max = self.size - 4
        min = 4
        length = 820

        topLeft = self.size-length
        bottomRight = length
        diff = 10

        l1 = self.canvas.create_line(min, max, min, topLeft)
        l2 =self.canvas.create_line(min, max, length, max)

        l3 =self.canvas.create_line(4, topLeft, min+diff, topLeft+diff)
        l4 =self.canvas.create_line(bottomRight, max, bottomRight-diff, max-diff)

        l5 =self.canvas.create_text(min+20,topLeft-10,fill="darkblue",font=("Purisa", 10), text=str(self.ymax))
        l6 =self.canvas.create_text(bottomRight+25,max-5,fill="darkblue",font=("Purisa", 10), text=str(self.xmax))

        self.rulers.extend([l1, l2, l3, l4, l5, l6])

    def onFaces(self):
        self.objectPlotter.plotFaces = not self.objectPlotter.plotFaces
        self.clear(True, False, False)
        self.objectPlotter.show()
        
    def onDistortionPress(self, distortion:str = "none"):
        self.distortionPlotter.setDistortion(distortion)
        self.show()

    def show(self):
        self.clear(True, True)
        self.plotRulers()
        self.distortionPlotter.showDistortion()
        self.objectPlotter.show()

    def build(self):
        self.canvasFrame.pack(side=LEFT, anchor=N)
        self.canvas.pack(side=LEFT)
        self.plotRulers()

    def clear(self, object:bool, distortion:bool, rulers:bool=True):
        if distortion:
            self.distortionPlotter.clear()
        if object:
            self.objectPlotter.clear()
        if rulers:
            for point in self.rulers:
                self.canvas.delete(point)
            self.rulers.clear()

