import sys
from tkinter import *
from gui.canvas.plotter.distortion_plotter import DistortionPlotter

class ObjectPlotter:
    plotFaces:bool = False

    def __init__(self, canvasManager, points, faces, areaDists, angleDists,
     plotFaces:bool=False, rect=None):
        self.canvas = canvasManager.canvas
        self.cv = canvasManager
        self.rect = rect
        self.points = points
        self.faces = faces
        self.plotFaces = plotFaces
        self.objectsOnCanvas = []
        self.distortionPlotter = DistortionPlotter(canvasManager, points, faces, areaDists, angleDists)

    def createLine(self, x1, x2, fill="black"):
        self.objectsOnCanvas.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1], fill=fill))
            

    def show(self):
        self.distortionPlotter.showDistortion()
        if self.plotFaces:
            for face in self.faces:
                x = list(self.points[face[0]-1])
                y = list(self.points[face[1]-1])
                z = list(self.points[face[2]-1])

                #Border
                self.createLine(x, y)
                self.createLine(y, z)
                self.createLine(z, x)

        else:
            for point in self.points:
                x = point[0]
                y = point[1]
                r = 0
                self.objectsOnCanvas.append(self.canvas.create_oval(x - r, y - r, x + r, y + r))

    def setPlotFaces(self, plot:bool):
        self.plotFaces = plot
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

