from pyclbr import Function
import sys
from tkinter import *
from typing import List, Mapping
import gui.canvas.translator as translator
from gui.canvas.plotter.pattern_plotter import PatternPlotter
from gui.canvas.plotter.object_plotter import ObjectPlotter
from gui.canvas.plotter.measure_plotter import MeasurePlotter
from gui.canvas.plotting_options.plotting_option import PlottingOption
from gui.mesh3dplotter.mesh3dplotter import Mesh3DPlotter
from gui.canvas.packer import pack
from gui.canvas.util import faceToArea
from logger import log

class CanvasManager:
    plotEdges:bool = False
    objectPlotters:List[ObjectPlotter] = []
    rulers = []
    borders = []

    def __init__(self, master: Frame, initSize: int, plotter:Mesh3DPlotter):
        self.size = initSize
        self.plotter = plotter
        self.canvasFrame = Frame(master, height=self.size, width=self.size)
        self.canvas = Canvas(self.canvasFrame, height=self.size, width=self.size, bd=0, highlightthickness=0)
        self.patternPlotter = PatternPlotter(self)
        self.measurePlotter = MeasurePlotter(self)
        self.placedPatternsMenu = None
        self.xmax = initSize
        self.ymax = initSize

    def P(self, x, y):
        """
        Transform point from cartesian (x,y) to Canvas (X,Y)
        """
        M=1
        X = M + (x/self.xmax) * (self.size-2*M)
        Y = M + (1-(y/self.ymax)) * (self.size-2*M)
        return (X,Y)

    def reverseP(self, X, Y):
        """
        Transform point from Canvas (X,Y) to cartesian (x,y)
        """
        M=1
        x = (X-M) * self.xmax / (self.size-2*M)
        y = (Y-M-self.size+2*M) * self.ymax / (self.size-2*M) * -1
        return (x,y)

    def plot(self, shapeList):
        self.plotter.deselectIfSelected()
        shapes = []
        verticesAfterInitial = []
        # copying a list
        for _, _, _, vertices, _ in shapeList:

            vnew = translator.moveToPositiveArea(vertices)
            vnew2 = []
            for x in vnew:
                vnew2.append(x.copy())

            shapes.append(vnew)
            verticesAfterInitial.append(vnew2)

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

        shapesOld = []
        for index, shape in enumerate(shapes):
            shapesOld.append([])
            for index2, point in enumerate(shape):
                shapesOld[index].append(point.copy())

        
        for index, shape in enumerate(shapes):
            for index2, point in enumerate(shape):
                for index3, v in enumerate(point):
                    if shapesOld[index][index2][index3] != shapes[index][index2][index3]: pass

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
        self.measurePlotter.delete()

        for el in self.objectPlotters:
            el.delete()
        self.objectPlotters.clear()
        

        #Calculate total area
        area = 0
        for sh in shapeList:
            chartKey, verticesBefore, facesBefore, verticesAfter, facesAfter = sh
            for f in facesBefore:
                area += faceToArea(f, verticesBefore)


        # Plot all again
        self.refreshRulers()
        self.plotEdges = True
        for index, shape in enumerate(shapes):
            chartKey, verticesBefore, facesBefore, verticesAfter, facesAfter = shapeList[index]

            color = "" if chartKey == -1 else self.plotter.getChartColor(chartKey)
            
            op = ObjectPlotter(chartKey, self, shape, verticesBefore, facesBefore, verticesAfterInitial[index], facesAfter,
            color, area, self.plotEdges, shapesOld[index])
            op.show()
            self.objectPlotters.append(op)


    def createLine(self, x1, x2):
        self.rulers.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1]))

    def onEdges(self):
        self.plotEdges = not self.plotEdges
        for op in self.objectPlotters: 
            op.setPlotEdges(self.plotEdges)
        self.refresh()
        
    def selectPlottingOption(self, option:PlottingOption):
        for pl in self.objectPlotters:
            pl.setPlottingOption(option)
        self.refresh()

        if len(self.objectPlotters) == 1:
            self.refreshChartDistortionInfo(self.objectPlotters[0].id)
            return
        
        selected = self.plotter.selectedChart
        self.refreshChartDistortionInfo(selected)

    def refresh(self):
        self.refreshRulers()
        self.patternPlotter.refresh()
        self.measurePlotter.refresh()

    def build(self):
        self.canvasFrame.pack(side=LEFT, anchor=N)
        self.canvas.pack(side=LEFT)
        self.refreshRulers()

    def getDistortionsOfChart(self, chart:int):
        for op in self.objectPlotters: 
            if op.id == chart: return op.getDistortions()
        
        dists = {}
        for pl in self.objectPlotters:
            d = pl.getDistortions(True)
            for key, val in d.items():
                if val == -1: continue
                if key not in dists: dists[key] = 0
                dists[key] += val

        return dists

    def enableChart(self, chart:int):
        """Enables all charts if chart is -1 (no chart is selected)"""
        for op in self.objectPlotters: 
            op.setEnabled(True if chart == -1 else op.id == chart)

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
