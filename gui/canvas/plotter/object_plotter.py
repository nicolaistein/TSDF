import sys
from tkinter import *
from gui.canvas.plotter.distortion_plotter import DistortionPlotter
from gui.canvas.distortion import Distortion
from logger import log

class ObjectPlotter:

    plotEdges:bool = False
    plotColors:bool = False

    def __init__(self, canvasManager, points, faces, areaDists,
     angleDists, color:str, plotColors:bool=False):
        self.color = color
        self.canvas = canvasManager.canvas
        self.cv = canvasManager
        self.points = points
        self.faces = faces
        self.plotColors = plotColors
        self.plotEdges = plotColors
        self.objectsOnCanvas = []
        self.distortionPlotter = DistortionPlotter(canvasManager, points, faces, areaDists, angleDists)

    def createLine(self, x1, x2):
        self.objectsOnCanvas.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1]))
            

    def show(self):
        self.distortionPlotter.showDistortion()
        if self.plotEdges or self.plotColors:
            for face in self.faces:
                
                x = list(self.points[face[0]])
                y = list(self.points[face[1]])
                z = list(self.points[face[2]])

                if self.plotColors:
                    self.objectsOnCanvas.append(
                        self.canvas.create_polygon(x, y, z, fill=self.color))

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

    def setPlotColors(self, plot:bool):
        if plot:
            self.setDistortion(Distortion.NO_DIST)
        self.plotColors = plot
        self.refresh()

    def ssetPlotEdges(self, plot:bool):
        self.plotEdges = plot
        self.refresh()

    def setDistortion(self, dist):
        self.distortionPlotter.setDistortion(dist)
        self.distortionPlotter.refresh()
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
        self.distortionPlotter.clear()

