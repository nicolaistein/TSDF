import sys
from tkinter import *
from typing import List, Mapping
import gui.canvas.translator as translator
from gui.canvas.plotter.distortion_plotter import DistortionPlotter
from gui.canvas.plotter.pattern_plotter import PatternPlotter
from gui.canvas.plotter.object_plotter import ObjectPlotter
from gui.canvas.distortion import Distortion
from gui.mesh3dplotter.mesh3dplotter import Mesh3DPlotter
from gui.canvas.packer import pack
from logger import log

class CanvasManager:
    plotColors:bool = False
    plotEdges:bool = False
    plotDistortion:str = Distortion.NO_DIST
    objectPlotters:List[ObjectPlotter] = []
    rulers = []
    borders = []

    def __init__(self, master: Frame, initSize: int, plotter:Mesh3DPlotter):
        self.size = initSize
        self.plotter = plotter
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

    def plot(self, shapeList):
        shapes = []
        for _, vertices, _, _, _ in shapeList:
            shapes.append(translator.moveToPositiveArea(vertices))

        # Calculate packing
        rects = pack(shapes)

        idToRect = {}
        for rect in rects:
            _, _, _, _, _, id = rect
            idToRect[id] = rect

        # Move shapes according to rectangle results
        for index, rect in enumerate(rects):
            id, x, y, _, _, rid = rect
            shapes[rid] = translator.moveToPosition(shapes[rid], x, y)


        # Calculate max needed for canvas coordinate transformation
        maxValue = 0
        for shape in shapes:
            for point in shape:
                for x in point:
                    if maxValue < x: maxValue = x
        self.xmax = self.ymax = round(maxValue, 2)


#        self.drawBorders(shapes, idToRect)

        # Transform to canvas coordinates
        for index, shape in enumerate(shapes):
            for index2, point in enumerate(shape):
                shapes[index][index2] = self.P(point[0], point[1])


        # Delete everything plotted to this point
        self.placedPatternsMenu.deleteAll()

        for el in self.objectPlotters:
            el.delete()
        self.objectPlotters.clear()
        

        # Plot all again
        self.refreshRulers()
        self.plotColors = True
        self.plotEdges = True
        for index, shape in enumerate(shapes):
            chartKey, _, faces, areaDists, angleDists = shapeList[index]

            color = "" if chartKey == -1 else self.plotter.getChartColor(chartKey)

            op = ObjectPlotter(self, shape, faces, areaDists, angleDists,
            color, self.plotColors)
            op.show()
            self.objectPlotters.append(op)

        self.patternPlotter.refresh()


    def createLine(self, x1, x2):
        self.rulers.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1]))

    def onFaces(self):
        self.plotColors = not self.plotColors
        for op in self.objectPlotters: 
            op.setPlotColors(self.plotColors)
        self.patternPlotter.refresh()

    def onEdges(self):
        self.plotEdges = not self.plotEdges
        for op in self.objectPlotters: 
            op.ssetPlotEdges(self.plotEdges)
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
        l2 = self.canvas.create_line(min, max, length, max)

        l3 = self.canvas.create_line(min, topLeft, min+diff, topLeft+diff)
        l4 = self.canvas.create_line(bottomRight, max, bottomRight-diff, max-diff)

        l5 = self.canvas.create_text(min+5, topLeft-2, anchor="sw", fill="blue",font=("Purisa", 10), text=str(self.ymax))
        l6 = self.canvas.create_text(bottomRight+5, max, anchor="sw", fill="blue",font=("Purisa", 10), text=str(self.xmax))

        self.rulers = [l1, l2, l3, l4, l5, l6]


    def drawBorders(self, shapes, idToRect:Mapping):
         # Delete old borders
        for point in self.borders:
            self.canvas.delete(point)
        self.borders.clear()

        # Draw new borders
        for index, shape in enumerate(shapes):
            _, x, y, w, h, id = idToRect[index]

            minX  = sys.float_info.max
            minY  = sys.float_info.max
            for p in shape:
                if p[0] < minX: minX = p[0]
                if p[1] < minY: minY = p[1]

            xR = minX
            yR = minY
            upper = yR+h
            right = xR+w

            self.borders.append(self.canvas.create_line(self.P(xR,yR), self.P(right, yR), fill="red"))
            self.borders.append(self.canvas.create_line(self.P(xR,yR), self.P(xR, upper), fill="red"))
            
            self.borders.append(self.canvas.create_line(self.P(right, upper), self.P(right, yR), fill="red"))
            self.borders.append(self.canvas.create_line(self.P(right, upper), self.P(xR, upper), fill="red"))
