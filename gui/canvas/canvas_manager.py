from tkinter import *
from typing import List
import gui.canvas.translator as translator
from gui.canvas.plotter.distortion_plotter import DistortionPlotter
from gui.canvas.plotter.pattern_plotter import PatternPlotter
from gui.canvas.plotter.object_plotter import ObjectPlotter
from gui.canvas.distortion import Distortion
from gui.canvas.packer import pack
from logger import log

class CanvasManager:
    plotFaces:bool = False
    plotDistortion:str = Distortion.NO_DIST
    objectPlotters:List[ObjectPlotter] = []
    rulers = []

    def __init__(self, master: Frame, initSize: int):
        self.size = initSize
        self.canvasFrame = Frame(master, height=self.size, width=self.size)
        self.canvas = Canvas(self.canvasFrame, height=self.size, width=self.size, bd=0, highlightthickness=0)
        self.patternPlotter = PatternPlotter(self)
        self.placedPatternsMenu = None
        self.xmax = initSize
        self.ymax = initSize

    def P(self, x,y):
        """
        Transform point from cartesian (x,y) to Canvas (X,Y)
        """
        M=1
        X = M + (x/self.xmax) * (self.size-2*M)
        Y = M + (1-(y/self.ymax)) * (self.size-2*M)
        return (X,Y)

    def reverseP(self, X,Y):
        """
        Transform point from Canvas (X,Y) to cartesian (x,y)
        """
        M=1
        x = (X-M) * self.xmax / (self.size-2*M)
        y = (Y-M-self.size+2*M) * self.ymax / (self.size-2*M) * -1
        return (x,y)

    def plot(self, list):
 #       pointsNew = translator.moveToPositiveArea(points)
 #       self.points = pointsNew

        self.list = list

        shapes = []
        for vertices, _, _, _ in list:
            shapes.append(translator.moveToPositiveArea(vertices))

        rects = pack(shapes)


        log("RECTS CALC FINISHED LENGTH: " + str(len(rects)))
        for index, rect in enumerate(rects):
            id, x, y, _, _, rid = rect
            shapes[index] = translator.moveToPosition(shapes[index], x, y)


        #Calculate max and adjust points

        maxValue = 0
        for shape in shapes:
            for point in shape:
                for x in point:
                    if maxValue < x: maxValue = x

        self.xmax = self.ymax = round(maxValue, 2)

        for index, shape in enumerate(shapes):
            for index2, point in enumerate(shape):
                shapes[index][index2] = self.P(point[0], point[1])


        #Reset everything plotted to this point

        self.placedPatternsMenu.deleteAll()

        for el in self.objectPlotters:
            el.delete()
        self.objectPlotters.clear()
        
        self.refreshRulers()




        for index, shape in enumerate(shapes):
            _, faces, areaDists, angleDists = list[index]
            op = ObjectPlotter(self, shape, faces, areaDists, angleDists)
            op.show()
            self.objectPlotters.append(op)

        self.patternPlotter.refresh()

       
#        for index, p in enumerate(self.points):
#            self.points[index] = list(self.P(p[0], p[1]))

#        for chart in list:    
#            points, faces, areaDistortions, angularDistortions = chart

    #        self.distortionPlotter.plot(self.points, faces, areaDistortions, angularDistortions)

    #        ObjectPlotter(self).plot(self.points, faces)



    def createLine(self, x1, x2):
        self.rulers.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1]))

    def onFaces(self):
        self.plotFaces = not self.plotFaces
        for op in self.objectPlotters: 
            op.setPlotFaces(self.plotFaces)
        self.patternPlotter.refresh()
        
    def onDistortionPress(self, distortion:Distortion):
        self.plotDistortion = distortion if distortion != self.plotDistortion else Distortion.NO_DIST
        for pl in self.objectPlotters:
            pl.setDistortion(self.plotDistortion)
        self.patternPlotter.refresh()

    def build(self):
        self.canvasFrame.pack(side=LEFT, anchor=N)
        self.canvas.pack(side=LEFT)
        self.refreshRulers()

    def refreshRulers(self):
        for point in self.rulers:
            self.canvas.delete(point)
        self.rulers.clear()

        max = self.size-1
        min = 0
        length = 820

        topLeft = self.size-length
        bottomRight = length
        diff = 10

        l1 = self.canvas.create_line(min, max, min, topLeft)
        l2 =self.canvas.create_line(min, max, length, max)

        l3 =self.canvas.create_line(min, topLeft, min+diff, topLeft+diff)
        l4 =self.canvas.create_line(bottomRight, max, bottomRight-diff, max-diff)

        l5 =self.canvas.create_text(min+5, topLeft-2, anchor="sw", fill="darkblue",font=("Purisa", 10), text=str(self.ymax))
        l6 =self.canvas.create_text(bottomRight+5, max, anchor="sw", fill="darkblue",font=("Purisa", 10), text=str(self.xmax))

        self.rulers.extend([l1, l2, l3, l4, l5, l6])