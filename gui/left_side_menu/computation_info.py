from tkinter import *
from typing import List

from matplotlib.pyplot import text
import gui.time_formatter as formatter
from gui.button import TkinterCustomButton
from gui.canvas.canvas_manager import CanvasManager
from gui.canvas.distortions.plotting_option import PlottingOption
from logger import log


class ComputationInfo:
    viewOptions = [(e, e.value) for e in PlottingOption]
    currentDistortions = {e.value: -1 for e in PlottingOption}
    """Contains all viewoptions (facecolor, distortions) displayed in the computation info widget"""

    def __init__(self, master: Frame, canvasManager:CanvasManager):
        self.canvasManager = canvasManager
        self.mainFrame = Frame(master)
 #       log("view options: " + str(self.viewOptions))
        self.selectedView = IntVar()
        self.selectedView.set(0)

    def updateInfo(self, algo:str, time:int, verticesBefore:List[List[float]], facesBefore:List[List[int]],
        verticesAfter:List[List[float]], facesAfter:List[List[int]]):
        """Updates the info shown in the widget"""
   #     self.verticesBefore = verticesBefore
   #     self.facesBefore = facesBefore
   #     self.verticesAfter = verticesAfter
   #     self.facesAfter = facesAfter
        self.algorithm.configure(text=algo)
        self.time.configure(text=formatter.formatTime(time))
    
    def getKeyValueFrame(self, parent: Frame, key: str, keyWidth:float=14):
        keyValFrame = Frame(parent)
        keyLabel = Label(keyValFrame, text=key, width=keyWidth,
                            anchor=W, justify=LEFT, wraplength=120)
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        valLabel = Label(keyValFrame, text="-", wraplength=100)
        valLabel.pack(side=LEFT)

        keyValFrame.pack(side="top", anchor="w")
        return valLabel

    def refreshView(self):
        self.edgeButton.delete()
        for child in self.mainFrame.winfo_children():
            child.destroy()
        self.build()

    def onEdgeClick(self):
        self.canvasManager.onEdges()
        self.refreshView()

    def showChoice(self):
        selected = self.selectedView.get()
        log("currently selected: " + str(selected))

        self.canvasManager.selectPlottingOption(selected)
        self.refreshView()

    def setDistortionValues(self, values):
        for distortion, distVal in values.items():
            self.currentDistortions[distortion] = distVal
        self.refreshView()

    def build(self):

        self.content = Frame(self.mainFrame, width=220,
                             height=280, padx=20, pady=20)
        self.content.pack_propagate(0)

        chooseFile = Label(self.content, text="Computation Info")
        chooseFile.configure(font=("Helvetica", 12, "bold"))

        self.algorithm = self.getKeyValueFrame(self.content, "Algorithm", 10)
        self.time = self.getKeyValueFrame(self.content, "Time", 10)
#        self.areaDist = self.getKeyValueFrame(self.content, "Area Distortion")
#        self.angleDist = self.getKeyValueFrame(self.content, "Angle Distortion")

        edgeText = "Show Edges" if not self.canvasManager.plotEdges else "Hide Edges"
        self.edgeButton = TkinterCustomButton(master=self.content, text=edgeText, command=self.onEdgeClick,
                        corner_radius=60, height=25, width=120)
        self.edgeButton.pack(side=TOP, pady=(10,8))

        bottomFrame = Frame(self.content)

        for distortion, distIndex in self.viewOptions:
            viewOptionFrame = Frame(bottomFrame)
            Radiobutton(viewOptionFrame,
                            text="",
                            height=1,
                            wrap=None,
                            variable=self.selectedView,
                            command=self.showChoice,
                            value=distIndex).pack(anchor=W, side=LEFT)

            rightFrame = Frame(viewOptionFrame)

            minDist, maxDist = distortion.getMinMax()


            innerTopFrame = Frame(rightFrame)
            opTitle = Label(innerTopFrame, text=distortion.toString())
            opTitle.configure(font=("Helvetica", 10, "bold"))
            opTitle.pack(side=LEFT, anchor=W)

            distortionValue = self.currentDistortions[distortion.value]
            if distortionValue != -1:
                Label(innerTopFrame, text=str(distortionValue)).pack(side=LEFT, padx=(10,0))
            innerTopFrame.pack(side=TOP, anchor=W)




            if minDist != -1:
                innerBottomFrame=Frame(rightFrame)
                minValue = round(minDist,1)
                Label(innerBottomFrame, text=str(minValue)).pack(side=LEFT, anchor=W)

                canvas = Canvas(innerBottomFrame, width=100, height=5, bd=0, highlightthickness=0)
                canvas.pack(side=LEFT, padx=(5,5))
                distortion.getColormap(canvas, 100, 5)

                maxValue = round(maxDist,1)
                Label(innerBottomFrame, text=str(maxValue)).pack(side=LEFT, anchor=W)
                innerBottomFrame.pack(side=TOP, anchor=NW)



            rightFrame.pack(side=LEFT, anchor=N)
            viewOptionFrame.pack(side=TOP, anchor=W, pady=(10,0))

        bottomFrame.pack(side=TOP, anchor=W, pady=(0,0))

        self.content.pack(side=LEFT)
        self.mainFrame.pack(side=TOP, pady=(2, 0), anchor=N)
