from pyclbr import Function
from tkinter import *

from logger import log

class MeasurePlotter:
    active:bool = False
    onAbort = None
    points = []
    currentX = -1
    currentY = -1

    def __init__(self, canvasManager):
        self.canvas = canvasManager.canvas
        self.cv = canvasManager
        self.objectsOnCanvas = []
        self.enabled = True

    def performMeasure(self, onChange:Function, onAbort:Function):
        self.canvas.bind("<Motion>", self.onMouseMoved)
        self.canvas.bind("<Button-1>", self.onCanvasClickLeft)
        self.canvas.bind("<Button-2>", self.onCanvasClickRight)
        self.canvas.bind("<Button-3>", self.onCanvasClickRight)
        self.onChange = onChange
        self.onAbort = onAbort
        self.active = True
        self.points = [(-1, -1)]

    def createLine(self, p1, p2):
        x1, y1 = self.cv.P(p1[0], p1[1])
        x2, y2 = self.cv.P(p2[0], p2[1])
        self.objectsOnCanvas.append(
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=1))
            
    def show(self):
        log("Show called")
        for index, p in enumerate(self.points):
            if index >= len(self.points)-1: break
            if index >= 2: break
            self.createLine(p, self.points[index+1])


    def onCanvasClickLeft(self, event):
        if not self.active: return
        if len(self.points) >= 4: return
        self.points.append(self.cv.reverseP(event.x, event.y))
        self.refresh()
        self.onChange(self.points)

    def onCanvasClickRight(self, event):
        if not self.active: return
        self.onAbort()

    def abort(self):
        self.active = False
        self.clear()

    def onMouseMoved(self, event):
        if not self.active: return
        x, y = self.cv.reverseP(event.x, event.y)
        if len(self.points) == 0: return
        self.points[-1] = (x, y)
        self.refresh()
        self.onChange(self.points)

    def refresh(self):
        log("Measure show called")
        self.clear()
        if self.active: self.show()

    def delete(self):
        if self.onAbort is not None: self.onAbort()

    def clear(self):
        for point in self.objectsOnCanvas:
            self.canvas.delete(point)
        self.objectsOnCanvas.clear()


