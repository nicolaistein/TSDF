from sys import modules
from tkinter import *
from typing import List, Pattern
import gui.plotting.translator as translator
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
    For convenience only.
    Transform point in cartesian (x,y) to Canvas (X,Y)
    As both system has difference y direction:
    Cartesian y-axis from bottom-left - up 
    Canvas Y-axis from top-left - down 
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

    def resize(self, newSize: int):
        print("resize: size: " + str(newSize))
        self.show()

    def plot(self, points):
        self.points = points
        self.show()

    def show(self):
        points = translator.moveToPositiveArea(self.points)
        scale, points = translator.scale(points, self.size)
        self.clear()
        for point in points:
            x = point[0]
            y = point[1]
            r = 1
            self.canvas.create_oval(x - r, y - r, x + r, y + r)

    def build(self):
        canvasFrame = Frame(self.master, height=self.size, width=self.size)
        self.canvas = Canvas(canvasFrame, height=self.size, width=self.size)
        canvasFrame.pack(side=LEFT, anchor=N)
        self.canvas.pack(side=LEFT)

    def clear(self):
        self.canvas.delete("all")

    def deletePattern(self, pattern:PatternModel):
        for shape in self.patterns[pattern]:
            self.canvas.delete(shape)
        self.patterns[pattern] = []

    def refreshPattern(self, pattern:PatternModel):
        self.deletePattern(pattern)
        self.addPattern(pattern)

    def addPattern(self, pattern:PatternModel):
        result, commands = pattern.getGcode()
        shapes = []
        for cmd in commands:
            cmd.print()
            s = []
            if(cmd.prefix == "G1"):
                s = self.canvas.create_line(cmd.previousX, 900-cmd.previousY, cmd.x, 900-cmd.y, fill="red", width=2)

            if(cmd.prefix == "G02"):
                s = self.computeArc(cmd)

            if(cmd.prefix == "G03"):
                s = self.computeArc(cmd)
            shapes.append(s)

        self.patterns[pattern] = shapes

    def computeArc(self, cmd:GCodeCmd):
        points = [P(cmd.previousX, cmd.previousY)]
        if cmd.arcDegrees == 180:
            ortho1, ortho2 = self.get2Corners(cmd.prefix=="G02", cmd.previousX, cmd.previousY, cmd.x, cmd.y)
            points.append([ortho1, ortho2])

        points.append(P(cmd.x, cmd.y))
        return self.canvas.create_line(points, smooth=True, fill="red", width=2)
        

    def get2Corners(self, clockwise:bool, x:float, y:float, x2:float, y2:float):
        #Compute orthogonal vector to v2-v vector
        xOrtho = (y2 - y) / 2
        yOrtho = (x2 - x) / 2

        if clockwise: xOrtho *= -1
        else: yOrtho *= -1

        return P(x + xOrtho, y + yOrtho), P(x2 + xOrtho, y2 + yOrtho)

