from tkinter import *
from PIL.Image import init
import gui.canvas.translator as translator
from patterns.gcode_cmd import GCodeCmd
from gui.pattern_model import PatternModel
from gui.canvas.plotter.distortions import DistortionPlotter

class PatternPlotter:

    def __init__(self, canvasManager):
        self.cv = canvasManager
        self.canvas = canvasManager.canvas
        self.placedPatternsMenu = None
        self.patterns = {}
        self.objectsOnCanvas = []
        self.selectedPattern = None


    def selectPattern(self, pattern: PatternModel):
        selected = self.selectedPattern
        if selected is None or not selected == pattern:
            self.selectedPattern = pattern

            if not selected is None:
                self.refreshPattern(selected)
        else:
            self.selectedPattern = None
        self.refreshPattern(pattern)
        

    def clear(self):
        for point in self.objectsOnCanvas:
            self.canvas.delete(point)
        self.objectsOnCanvas.clear()

    def deletePattern(self, pattern:PatternModel):
        self.removePatternFromCanvas(pattern)
        if self.selectedPattern == pattern:
            self.selectedPattern = None

    def removePatternFromCanvas(self, pattern:PatternModel):
        for shape in self.patterns[pattern]:
            self.canvas.delete(shape)
        self.patterns[pattern] = []

    def refreshPattern(self, pattern:PatternModel):
        self.removePatternFromCanvas(pattern)
        self.addPattern(pattern)

    def addPattern(self, pattern:PatternModel):
        result, commands = pattern.getGcode()
        color = "blue"
        #Change color to red if selected
        if not self.selectedPattern is None:
            color = "red" if self.selectedPattern == pattern else "blue"

        shapes = []
        for cmd in commands:
            s = []
            if(cmd.prefix == "G1"):
                p1x, p1y = self.cv.P(cmd.previousX, cmd.previousY)
                p2x, p2y = self.cv.P(cmd.x, cmd.y)
                s = self.canvas.create_line(p1x,p1y,p2x,p2y, fill=color, width=1)

            if cmd.prefix == "G02" or cmd.prefix == "G03":
                s = self.computeArc(cmd, color)

            shapes.append(s)

        self.patterns[pattern] = shapes

    def computeArc(self, cmd:GCodeCmd, color:str):
        points = [self.cv.P(cmd.previousX, cmd.previousY)]

        cornerPoints = self.getCornerPoints(cmd.prefix=="G02", cmd.arcDegrees, cmd.previousX, cmd.previousY, cmd.x, cmd.y)
        points.append(cornerPoints)

        points.append(self.cv.P(cmd.x, cmd.y))
        return self.canvas.create_line(points, smooth=True, fill=color, width=1)
        

    def getCornerPoints(self, clockwise:bool, degrees:float, x:float, y:float, x2:float, y2:float):
        #Compute orthogonal vector to v2-v vector
        xOrtho = halfY = (y2 - y) / 2
        yOrtho = halfX = (x2 - x) / 2

        if clockwise: xOrtho *= -1
        else: yOrtho *= -1

        if degrees == 180:
            return [self.cv.P(x + xOrtho, y + yOrtho), self.cv.P(x2 + xOrtho, y2 + yOrtho)]
        if degrees == 90:
            return [self.cv.P(x + + halfX + xOrtho, y + halfY + yOrtho)]

