import enum
from tkinter import *
from gui.button import TkinterCustomButton
from gui.pattern_model import PatternModel
from gui.canvas.canvas_manager import CanvasManager
from gui.canvas.plotter.object_plotter import ObjectPlotter
from util import doIntersect
from logger import log


class PlacedPatternsItem:

    #cde3fa
    # #d1d1d1
    color = "#cde3fa"

    def __init__(self, master: Frame, pattern: PatternModel, menu, canvasManager:CanvasManager):
        self.pattern = pattern
        self.menu = menu
        self.master = master
        self.canvasManager = canvasManager

    def delete(self):
        self.menu.delete(self)

    def edit(self):
        self.menu.edit(self.pattern)

    def getKeyValueFrame(self, parent: Frame, key: str, value: str, valueLength: float = 80):
        keyValFrame = Frame(parent, bg=self.color,)
        keyLabel = Label(keyValFrame, text=key, width=7, bg=self.color,
                         anchor=W, justify=LEFT, wraplength=50)
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        Label(keyValFrame, text=value if value else "-", anchor=S,
         bg=self.color, justify=LEFT, wraplength=valueLength).pack(side=LEFT)

        return keyValFrame

    def deleteButtons(self):
        self.button1.delete()
        self.button2.delete()
        self.button3.delete()

    def onShowClick(self):
        self.menu.onPlacedPatternItemClick(self.pattern)

    def toPoints(self):
        _, commands = self.pattern.getGcode(0,1)
        result = []
        for c in commands:
            result.extend(c.toPoints())

#        Execute[{"A = (1, 2)"," B = (3, 4)"," C = (5, 6)"}]

        log("result: " + str(result))
        counter = 1
        text = 'Execute[{'
        for index, r in enumerate(result):
            log("r: " + str(r))
            text += '"A' + str(counter) + ' = (' + str(r[0]) + ", " + str(r[1]) + ')"'
            if index != len(result)-1:
                text += ','

            counter += 1


        text += '}]'
        print(text)
        log("points: " + str(result))
        return result

    def checkBoundaries(self):
        intersects = self.intersectsWithBoundary()
        log("Pattern " + self.pattern.name + " intersects: " + str(intersects))

    def intersectsWithBoundary(self):
        selfPoints = self.toPoints()
        for obPlotter in self.canvasManager.objectPlotters:
            boundaryPoints = obPlotter.getBoundary()
            vertices = obPlotter.verticesAfter
            for index1, point in enumerate(selfPoints):
                if index1 == len(selfPoints)-1: continue
                for index2, boundaryPoint in enumerate(boundaryPoints):
                    if index2 == len(boundaryPoints)-1: continue
                    intersects = doIntersect(selfPoints[index1], selfPoints[index1+1],
                      vertices[boundaryPoints[index2]], vertices[boundaryPoints[index2+1]])
                    if intersects: return True

        return False
            

    def build(self):

        container = Frame(self.master, borderwidth=1, bg=self.color, padx=10, pady=10)
        topContent = Frame(container, bg=self.color)

    #    container.pack_propagate(0)
        importantValues = {}
        importantValues["name"] = self.pattern.name
        importantValues["id"] = self.pattern.id
        importantValues["position"] = self.pattern.getPosition()
        importantValues["rotation"] = str(self.pattern.rotation) + " degrees"

        leftFrame = Frame(topContent, bg=self.color)
        self.getKeyValueFrame(leftFrame, "name", self.pattern.name).pack(
            side=TOP, anchor=W)
        self.getKeyValueFrame(leftFrame, "id", self.pattern.id).pack(
            side=TOP, anchor=W)
        leftFrame.pack(side=LEFT, anchor=N)

        rightFrame = Frame(topContent, bg=self.color)
        self.getKeyValueFrame(rightFrame, "position", self.pattern.getPosition()).pack(
            side=TOP, anchor=W)
        self.getKeyValueFrame(rightFrame, "rotation", str(
            self.pattern.rotation) + "°").pack(side=TOP, anchor=W)
        rightFrame.pack(side=LEFT, anchor=N, padx=(10, 0))

        topContent.pack(side=TOP, anchor=W)

        paramsText = ""
        for key, val in self.pattern.params.items():
            paramsText += key + "=" + val + "   "
        if paramsText:
            paramsText = paramsText[:-2]

        if len(self.pattern.params) > 0:
            self.getKeyValueFrame(container, "params", paramsText, 200).pack(
                side=TOP, anchor=W, pady=(0, 0))

        buttonContainer = Frame(container, bg=self.color, width=275, height=30)
        self.button1 = TkinterCustomButton(master=buttonContainer, text="Edit", command=self.edit,
                                            fg_color="#28a63f", hover_color="#54c76d",
                                           corner_radius=60, height=25, width=70)
        self.button1.pack(side=LEFT)

        self.button3 = TkinterCustomButton(master=buttonContainer, text="Show", command=self.onShowClick,
                                           corner_radius=60, height=25, width=70)
        self.button3.pack(side=LEFT, padx=(10, 0))

        self.button2 = TkinterCustomButton(master=buttonContainer, text="Delete", command=self.delete,
                                           fg_color="#a62828", hover_color="#c75454",
                                           corner_radius=60, height=25, width=70)
        self.button2.pack(side=LEFT, padx=(10, 0))

        buttonContainer.pack_propagate(0)
        buttonContainer.pack(side=TOP, anchor=N, pady=(10, 0))

        container.pack(side=TOP, pady=(10, 0), anchor=N)
