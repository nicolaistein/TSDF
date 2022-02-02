from tkinter import *
from typing import List

from gui.canvas.plotter.options_plotter import OptionsPlotter
from gui.canvas.plotting_options.plotting_option import PlottingOption
from gui.canvas.util import faceToArea
from logger import log

class ObjectPlotter:

    def __init__(self, id, canvasManager, verticesToPlot:List[List[float]], verticesBefore:List[List[float]], facesBefore:List[List[int]],
        verticesAfter:List[List[float]], facesAfter:List[List[int]], color:str, totalArea:float, plotEdges:bool, verticesForExport:List[List[float]]):
        self.color = color
        self.id = id
        self.verticesForExport = verticesForExport
        self.canvas = canvasManager.canvas
        self.cv = canvasManager
        self.objectsOnCanvas = []
        self.points = verticesToPlot
        self.verticesAfter = verticesAfter
        self.faces = facesAfter
        self.plotEdges = plotEdges
        self.enabled = True
        self.optionsPlotter = OptionsPlotter(canvasManager, verticesToPlot, verticesBefore,
            facesBefore, verticesAfter, facesAfter, totalArea, color)

    def createLine(self, x1, x2):
        self.objectsOnCanvas.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1]))
            
    def getDistortions(self, wholeObject:bool=False):
        return self.optionsPlotter.getDistortions(wholeObject)

    def show(self):
        if not self.enabled: return
        if self.plotEdges:
            for face in self.faces:
                
                x = list(self.points[face[0]])
                y = list(self.points[face[1]])
                z = list(self.points[face[2]])

                #Edges
                if self.plotEdges:
                    self.createLine(x, y)
                    self.createLine(y, z)
                    self.createLine(z, x)

        else:
            for point in self.points:
                x = point[0]
                y = point[1]
                r = 0
                self.objectsOnCanvas.append(self.canvas.create_oval(x - r, y - r, x + r, y + r))

    def getArea(self):
        sum = 0
        for f in self.faces:
            sum += faceToArea(f, self.verticesAfter)
        return sum


    def setEnabled(self, enabled:bool):
        self.enabled = enabled
        self.optionsPlotter.setEnabled(enabled)
        self.refresh()

    def setPlotEdges(self, plot:bool):
        self.plotEdges = plot
        self.refresh()

    def setPlottingOption(self, opt):
        self.optionsPlotter.setOption(opt)
        self.refresh()

    def refresh(self):
        self.clear()
        self.show()

    def clear(self):
        for point in self.objectsOnCanvas:
            self.canvas.delete(point)
        self.objectsOnCanvas.clear()

    def delete(self):
        self.clear()
        self.optionsPlotter.clear()

