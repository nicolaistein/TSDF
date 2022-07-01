import enum
from tkinter import *
from gui.button import TkinterCustomButton
from gui.pattern_model import PatternModel
from gui.canvas.canvas_manager import CanvasManager
from gui.canvas.plotter.object_plotter import ObjectPlotter
from threading import Thread
from time import sleep
from util import doIntersect
from logger import log


class PlacedPatternsItem:

    colorBlue = "#cde3fa"
    colorGreen = "#b8dbbd"
    colorRed = "#f29696"

    def __init__(
        self, master: Frame, pattern: PatternModel, menu, canvasManager: CanvasManager
    ):
        self.pattern = pattern
        self.menu = menu
        self.master = master
        self.canvasManager = canvasManager
        self.color = self.colorBlue
        self.container = None
        self.toRefresh = []

    def delete(self):
        self.deleteButtons()
        self.container.destroy()
        self.menu.delete(self)

    def edit(self):
        self.menu.edit(self)

    def onEdit(self):
        pass

    def getKeyValueFrame(
        self, parent: Frame, key: str, value: str, valueLength: float = 80
    ):
        keyValFrame = Frame(
            parent,
            bg=self.color,
        )
        self.toRefresh.append(keyValFrame)
        keyLabel = Label(
            keyValFrame,
            text=key,
            width=7,
            bg=self.color,
            anchor=W,
            justify=LEFT,
            wraplength=50,
        )
        self.toRefresh.append(keyLabel)
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        label = Label(
            keyValFrame,
            text=value if value else "-",
            anchor=S,
            bg=self.color,
            justify=LEFT,
            wraplength=valueLength,
        )
        label.pack(side=LEFT)
        self.toRefresh.append(label)

        return keyValFrame, label

    def deleteButtons(self):
        self.button1.delete()
        self.button2.delete()
        self.button3.delete()

    def onShowClick(self):
        self.menu.onPlacedPatternItemClick(self.pattern)

    def toPoints(self):
#        overrunStart, overrunEnd, printOverrun = self.menu.getOverruns()
        overrunStart = self.menu.overrunStartText.getNumberInput()
        overrunEnd = self.menu.overrunEndText.getNumberInput()
        printOverrun = self.menu.printOverrunStartText.getNumberInput()
        
        platformLength = self.menu.platformLengthText.getNumberInput()
        platformWidth = self.menu.platformWidthText.getNumberInput()
        platformLines = self.menu.platformLinesText.getNumberInput()

        _, commands, _ = self.pattern.getGcode(
            overrunStart = overrunStart,
             overrunEnd = overrunEnd,
              printOverrun = printOverrun,
              platformLength = platformLength,
              platformWidth = platformWidth,
              platformLines = platformLines
        )
        result = []
        for index, c in enumerate(commands):
            result.extend(c.toPoints())

        #        log("result: " + str(result))
        #        counter = 1
        #        text = 'Execute[{'
        #        for index, r in enumerate(result):
        #            log("r: " + str(r))
        #            text += '"A' + str(counter) + ' = (' + str(r[0]) + ", " + str(r[1]) + ')"'
        #            if index != len(result)-1:
        #                text += ','
        #            counter += 1
        #        text += '}]'
        #        print(text)
        #        log("points: " + str(result))

        return result

    def resetColor(self):
        self.color = self.colorBlue
        self.refreshColor()

    def checkIfInsideAndRefreshColors(self):
        #        self.plotBoundaryLoop()
        self.resetColor()
        inside = self.isInsideBoundaries()
        intersects = self.intersectsWithBoundary()
        self.color = self.colorRed if intersects or not inside else self.colorGreen
        self.refreshColor()

    def checkBoundaries(self):
        thread = Thread(target=self.checkIfInsideAndRefreshColors)
        thread.start()

    #        thread.join()
    #        intersects = self.intersectsWithBoundary()

    #        log("Pattern " + self.pattern.name + " intersects: " + str(intersects))

    def refreshColor(self):
        for el in self.toRefresh:
            el.configure(bg=self.color)
        self.button1.configure_color(bg_color=self.color)
        self.button2.configure_color(bg_color=self.color)
        self.button3.configure_color(bg_color=self.color)

    def formatParams(self):
        paramsText = ""
        for key, val in self.pattern.params.items():
            paramsText += key + "=" + val + "   "
        if paramsText:
            paramsText = paramsText[:-2]
        return paramsText

    def refreshValues(self):
        self.nameLabel.configure(text=self.pattern.name)
        self.idLabel.configure(text=self.pattern.id)
        self.positionLabel.configure(text=self.pattern.getPosition())
        self.rotationLabel.configure(text=str(self.pattern.rotation) + "°")
        if len(self.pattern.params) > 0:
            self.paramsLabel.configure(text=self.formatParams())

    def sign(self, p1, p2, p3):

        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    def pointInTriangle(self, pt, v1, v2, v3):
        #        d1, d2, d3
        #        has_neg, has_pos

        d1 = self.sign(pt, v1, v2)
        d2 = self.sign(pt, v2, v3)
        d3 = self.sign(pt, v3, v1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def isInsideBoundaries(self):
        if len(self.canvasManager.objectPlotters) == 0:
            return True
        selfPoints = self.toPoints()
        pointInside = [False] * len(selfPoints)

        for obPlotter in self.canvasManager.objectPlotters:
            vertices = obPlotter.verticesForExport
            faces = obPlotter.faces
            for face in faces:
                for index, p in enumerate(selfPoints):
                    if self.pointInTriangle(
                        p, vertices[face[0]], vertices[face[1]], vertices[face[2]]
                    ):
                        pointInside[index] = True
                        if all(pointInside):
                            return True

        return False

    def plotBoundaryLoop(self):
        for obPlotter in self.canvasManager.objectPlotters:
            #           log("Checking plotter " + str(obPlotter.id))
            boundaryPoints = list(obPlotter.getBoundary())
            vertices = obPlotter.verticesForExport

            for index, p in enumerate(boundaryPoints):
                xP = vertices[p][0]
                yP = vertices[p][1]
                x, y = self.canvasManager.P(xP, yP)

                #               log("boundary x y: (" + str(x) + ", " + str(y) + ")")
                r = 3
                #
                self.canvasManager.canvas.create_oval(
                    x - r, y - r, x + r, y + r, fill="green"
                )
                self.canvasManager.canvas.create_text(
                    x, y, anchor="sw", fill="blue", font=("Purisa", 10), text=str(index)
                )

    def intersectsWithBoundary(self):
        selfPoints = self.toPoints()
        for obPlotter in self.canvasManager.objectPlotters:
            #           log("Checking plotter " + str(obPlotter.id))
            boundaryPoints = list(obPlotter.getBoundary())
            vertices = obPlotter.verticesForExport

            #           for index, p in enumerate(boundaryPoints):
            #               xP = vertices[p][0]
            #               yP = vertices[p][1]
            #               x, y = self.canvasManager.P(xP, yP)

            #               log("boundary x y: (" + str(x) + ", " + str(y) + ")")
            #               r = 3
            #
            #               self.canvasManager.canvas.create_oval(x - r, y - r, x + r, y + r, fill="green")
            #               self.canvasManager.canvas.create_text(x, y, anchor="sw", fill="blue",font=("Purisa", 10), text=str(index))

            boundaryPoints.append(boundaryPoints[0])
            for index1, point in enumerate(selfPoints):
                if index1 == len(selfPoints) - 1:
                    continue
                for index2, boundaryPoint in enumerate(boundaryPoints):
                    if index2 == len(boundaryPoints) - 1:
                        continue

                    shouldLog = index2 == 3 and index1 == 3
                    intersects = doIntersect(
                        selfPoints[index1],
                        selfPoints[index1 + 1],
                        vertices[boundaryPoints[index2]],
                        vertices[boundaryPoints[index2 + 1]],
                        shouldLog,
                    )
                    if intersects:
                        return True

        return False

    def build(self):
        self.toRefresh.clear()
        self.container = Frame(
            self.master, borderwidth=1, bg=self.color, padx=10, pady=10
        )
        self.toRefresh.append(self.container)
        topContent = Frame(self.container, bg=self.color)
        self.toRefresh.append(topContent)

        importantValues = {}
        importantValues["name"] = self.pattern.name
        importantValues["id"] = self.pattern.id
        importantValues["position"] = self.pattern.getPosition()
        importantValues["rotation"] = str(self.pattern.rotation) + " degrees"

        leftFrame = Frame(topContent, bg=self.color)
        self.toRefresh.append(leftFrame)
        frame, self.nameLabel = self.getKeyValueFrame(
            leftFrame, "name", self.pattern.name
        )
        frame.pack(side=TOP, anchor=W)

        frame, self.idLabel = self.getKeyValueFrame(leftFrame, "id", self.pattern.id)
        frame.pack(side=TOP, anchor=W)
        leftFrame.pack(side=LEFT, anchor=N)

        rightFrame = Frame(topContent, bg=self.color)
        self.toRefresh.append(rightFrame)
        frame, self.positionLabel = self.getKeyValueFrame(
            rightFrame, "position", self.pattern.getPosition()
        )
        frame.pack(side=TOP, anchor=W)
        frame, self.rotationLabel = self.getKeyValueFrame(
            rightFrame, "rotation", str(self.pattern.rotation) + "°"
        )
        frame.pack(side=TOP, anchor=W)
        rightFrame.pack(side=LEFT, anchor=N, padx=(10, 0))

        topContent.pack(side=TOP, anchor=W)

        paramsText = self.formatParams()
        if len(self.pattern.params) > 0:
            frame, self.paramsLabel = self.getKeyValueFrame(
                self.container, "params", paramsText, 200
            )
            frame.pack(side=TOP, anchor=W, pady=(0, 0))

        buttonContainer = Frame(self.container, bg=self.color, width=275, height=30)
        self.toRefresh.append(buttonContainer)
        self.button1 = TkinterCustomButton(
            master=buttonContainer,
            text="Edit",
            command=self.edit,
            fg_color="#28a63f",
            hover_color="#54c76d",
            corner_radius=60,
            height=25,
            width=70,
        )
        self.button1.pack(side=LEFT)

        self.button3 = TkinterCustomButton(
            master=buttonContainer,
            text="Show",
            command=self.onShowClick,
            corner_radius=60,
            height=25,
            width=70,
        )
        self.button3.pack(side=LEFT, padx=(10, 0))

        self.button2 = TkinterCustomButton(
            master=buttonContainer,
            text="Delete",
            command=self.delete,
            fg_color="#a62828",
            hover_color="#c75454",
            corner_radius=60,
            height=25,
            width=70,
        )
        self.button2.pack(side=LEFT, padx=(10, 0))

        buttonContainer.pack_propagate(0)
        buttonContainer.pack(side=TOP, anchor=N, pady=(10, 0))

        self.container.pack(side=TOP, pady=(10, 0), anchor=N)
