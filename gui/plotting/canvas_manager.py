from tkinter import *
from typing import List
import gui.plotting.translator as translator
from patterns.gcode_cmd import GCodeCmd

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

    def resize(self, newSize: int):
        print("resize: size: " + str(newSize))
        self.show()

    def plot(self, points):
        self.points = points
        self.show()

    def show(self):
        points = translator.moveToPositiveArea(self.points)
        scale, points = translator.scale(points, self.size)
        self.canvas.delete("all")
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
        self.canvas.create_line(0,800,800,800, fill="red", width=6)
    #    points = P(120.56,20), P(90,50), P(50,100), P(10,50), P(40,20)
    #    fracture = self.canvas.create_line(points, fill='red')
    #    smooth = self.canvas.create_line(points, smooth=True)
        
        points2 = P(60,20), P(90,20), P(90,80), P(60,80)
        smooth2 = self.canvas.create_line(points2, smooth=True)

    def clear(self):
        self.canvas.delete("all")

    def addPattern(self, commands:List[GCodeCmd]):
        print("CanvasManager received pattern size: " + str(len(commands)))
        for cmd in commands:
            cmd.print()
            if(cmd.prefix == "G1"):
                self.canvas.create_line(cmd.previousX, 900-cmd.previousY, cmd.x, 900-cmd.y, fill="red", width=2)

            if(cmd.prefix == "G02"):
                points = [P(cmd.previousX, cmd.previousY)]
                if cmd.arcDegrees == 180:
                    ortho1, ortho2 = self.get2Corners(True, cmd.previousX, cmd.previousY, cmd.x, cmd.y)
                    points.append([ortho1, ortho2])

                points.append(P(cmd.x, cmd.y))
                self.canvas.create_line(points, smooth=True, fill="red", width=2)

            if(cmd.prefix == "G03"):
                points = [P(cmd.previousX, cmd.previousY)]
                if cmd.arcDegrees == 180:
                    ortho1, ortho2 = self.get2Corners(False, cmd.previousX, cmd.previousY, cmd.x, cmd.y)
                    points.append([ortho1, ortho2])

                points.append(P(cmd.x, cmd.y))
                self.canvas.create_line(points, smooth=True, fill="blue", width=2)


    def get2Corners(self, forwards:bool, x:float, y:float, x2:float, y2:float):
        #Compute orthogonal vector to v2-v vector
        xOrtho = (y2 - y) / 2
        yOrtho = (x2 - x) / 2

        if forwards: xOrtho *= -1
        else: yOrtho *= -1

        return P(x + xOrtho, y + yOrtho), P(x2 + xOrtho, y2 + yOrtho)

