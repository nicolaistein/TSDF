from tkinter import *
from typing import List

import numpy as np

from gui.canvas.plotter.options_plotter import OptionsPlotter
from util import faceToArea
from logger import log
import igl


class ObjectPlotter:
    def __init__(
        self,
        id: int,
        canvasManager,
        verticesToPlot: List[List[float]],
        verticesBefore: List[List[float]],
        facesBefore: List[List[int]],
        verticesAfter: List[List[float]],
        facesAfter: List[List[int]],
        color: str,
        totalArea: float,
        plotEdges: bool,
        verticesForExport: List[List[float]],
    ):
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
        self.bnd = igl.boundary_loop(np.array(self.faces))
        self.enabled = True
        self.optionsPlotter = OptionsPlotter(
            canvasManager,
            verticesToPlot,
            verticesBefore,
            facesBefore,
            verticesAfter,
            facesAfter,
            totalArea,
            color,
        )

    def createLine(self, x1, x2):
        self.objectsOnCanvas.append(self.canvas.create_line(x1[0], x1[1], x2[0], x2[1], fill="#828282"))

    def getDistortions(self, wholeObject: bool = False):
        return self.optionsPlotter.getDistortions(wholeObject)

    def show(self):
        if not self.enabled:
            return
        if self.plotEdges:

    #        print("Boundary loop")
    #        print(self.bnd)
            for face in self.faces:
                x = face[0]
                y = face[1]
                z = face[2]

                pX = list(self.points[x])
                pY = list(self.points[y])
                pZ = list(self.points[z])

    #            print("x: " + str(x) + ", y: " + str(y) + "z: " + str(z))

                # Edges
                if x in self.bnd and y in self.bnd:
                    self.createLine(pX, pY)
                if y in self.bnd and z in self.bnd:
                    self.createLine(pY, pZ)
                if x in self.bnd and z in self.bnd:
                    self.createLine(pZ, pX)

  #      else:
            for point in self.points:
                x = point[0]
                y = point[1]
                r = 0
                self.objectsOnCanvas.append(
                    self.canvas.create_oval(x - r, y - r, x + r, y + r)
                )

    def getArea(self):
        sum = 0
        for f in self.faces:
            sum += faceToArea(f, self.verticesAfter)
        return sum

    def getBoundary(self):
        return self.bnd

    def setEnabled(self, enabled: bool):
        self.enabled = enabled
        self.optionsPlotter.setEnabled(enabled)
        self.refresh()

    def setPlotEdges(self, plot: bool):
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
