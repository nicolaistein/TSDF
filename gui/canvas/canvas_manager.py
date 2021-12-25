from sys import modules
from tkinter import *
from typing import List, Pattern
import gui.canvas.translator as translator
from patterns.gcode_cmd import GCodeCmd
from gui.pattern_model import PatternModel

M = 4  
W = 900
H = 900
xmin = 0
xmax = 900
ymin = 0
ymax = 900    

def P(x,y):
    """
    Transform point from cartesian (x,y) to Canvas (X,Y)
    """
    X = M + (x/xmax) * (W-2*M)
    Y = M + (1-(y/ymax)) * (H-2*M)
    return (X,Y)

class CanvasManager:

    def __init__(self, master: Frame, initSize: int):
        self.master = master
        self.size = initSize
        self.points = []
        self.patterns = {}
        self.selectedPattern = None

    def resize(self, newSize: int):
        self.show()

    def plot(self, points):
        self.points = points
        self.show()

    def selectPattern(self, pattern: PatternModel):
        selected = self.selectedPattern
        if selected is None or not selected == pattern:
            self.selectedPattern = pattern

            if not selected is None:
                self.refreshPattern(selected)
        else:
            self.selectedPattern = None
        self.refreshPattern(pattern)

    def show(self):
        points = translator.moveToPositiveArea(self.points)
        scale, points = translator.scale(points, self.size)
        self.clear()
        for point in points:
            x = point[0]
            y = point[1]
            r = 0
            self.canvas.create_oval(x - r, y - r, x + r, y + r)

    def build(self):
        canvasFrame = Frame(self.master, height=self.size, width=self.size)
        self.canvas = Canvas(canvasFrame, height=self.size, width=self.size)
        canvasFrame.pack(side=LEFT, anchor=N)
        self.canvas.pack(side=LEFT)

    def clear(self):
        self.canvas.delete("all")

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
                s = self.canvas.create_line(cmd.previousX, 900-cmd.previousY, cmd.x, 900-cmd.y, fill=color, width=1)

            if(cmd.prefix == "G02"):
                s = self.computeArc(cmd, color)

            if(cmd.prefix == "G03"):
                s = self.computeArc(cmd, color)
            shapes.append(s)

        self.patterns[pattern] = shapes

    def computeArc(self, cmd:GCodeCmd, color:str):
        points = [P(cmd.previousX, cmd.previousY)]

        cornerPoints = self.getCornerPoints(cmd.prefix=="G02", cmd.arcDegrees, cmd.previousX, cmd.previousY, cmd.x, cmd.y)
        points.append(cornerPoints)

        points.append(P(cmd.x, cmd.y))
        return self.canvas.create_line(points, smooth=True, fill=color, width=1)
        

    def getCornerPoints(self, clockwise:bool, degrees:float, x:float, y:float, x2:float, y2:float):
        #Compute orthogonal vector to v2-v vector
        xOrtho = halfY = (y2 - y) / 2
        yOrtho = halfX = (x2 - x) / 2

        if clockwise: xOrtho *= -1
        else: yOrtho *= -1

        if degrees == 180:
            return [P(x + xOrtho, y + yOrtho), P(x2 + xOrtho, y2 + yOrtho)]
        if degrees == 90:
            return [P(x + + halfX + xOrtho, y + halfY + yOrtho)]

