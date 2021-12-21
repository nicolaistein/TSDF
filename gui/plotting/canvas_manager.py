from tkinter import *
import gui.plotting.translator as translator


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
        print("scale: " + str(scale))
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
