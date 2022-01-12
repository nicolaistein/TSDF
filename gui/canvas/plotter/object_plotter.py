from tkinter import *

class ObjectPlotter:
    plotFaces:bool = False

    def __init__(self, canvasManager):
        self.canvas = canvasManager.canvas
        self.cv = canvasManager
        self.points = []
        self.faces = []
        self.objectsOnCanvas = []

    def plot(self, points, faces):
        self.points = points
        self.faces = faces

    def createLine(self, x1, x2):
        self.objectsOnCanvas.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1]))
            
    def show(self):
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

    def clear(self):
        for point in self.objectsOnCanvas:
            self.canvas.delete(point)
        self.objectsOnCanvas.clear()


