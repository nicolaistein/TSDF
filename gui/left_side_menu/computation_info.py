from sqlite3 import PARSE_DECLTYPES
from tkinter import *

from matplotlib.pyplot import text
import gui.time_formatter as formatter
from gui.button import TkinterCustomButton
from gui.canvas.canvas_manager import CanvasManager
from gui.canvas.distortions.distortion_type import PlottingOption
from logger import log


class ComputationInfo:

    def __init__(self, master: Frame, canvasManager:CanvasManager):
        self.canvasManager = canvasManager
        self.mainFrame = Frame(master)
        self.viewOptions = [(e, e.value) for e in PlottingOption]
        log("view options: " + str(self.viewOptions))
        self.selectedView = IntVar()
        self.selectedView.set(0)
        self.mainFrame.pack(side=TOP, pady=(2, 0), anchor=N)

    def updateInfo(self, algo:str, time:int, areaDist:float, angleDist:float):
        self.algorithm.configure(text=algo)
        self.time.configure(text=formatter.formatTime(time))
        self.areaDist.configure(text=str(round(areaDist, 2)))
        self.angleDist.configure(text=str(round(angleDist, 2)))

    
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
        for child in self.mainFrame.winfo_children():
            child.destroy()
        self.build()

    def onEdgeClick(self):
        self.canvasManager.onEdges()
        self.refreshView()

    def showChoice(self):
        log("currently selected: " + str(self.selectedView.get()))

    def build(self):

        self.content = Frame(self.mainFrame, width=220,
                             height=280, padx=20, pady=20)
        self.content.pack_propagate(0)

        chooseFile = Label(self.content, text="Computation Info")
        chooseFile.configure(font=("Helvetica", 12, "bold"))

        self.algorithm = self.getKeyValueFrame(self.content, "Algorithm", 10)
        self.time = self.getKeyValueFrame(self.content, "Time", 10)
        self.areaDist = self.getKeyValueFrame(self.content, "Area Distortion")
        self.angleDist = self.getKeyValueFrame(self.content, "Angle Distortion")

        edgeText = "Show Edges" if not self.canvasManager.plotEdges else "Hide Edges"
        TkinterCustomButton(master=self.content, text=edgeText, command=self.onEdgeClick,
                        corner_radius=60, height=25, width=120).pack(side=LEFT)

        bottomFrame = Frame(self.content)

        for key, val in self.viewOptions:
            viewOptionFrame = Frame(bottomFrame)
            Radiobutton(viewOptionFrame,
                            text="",
                            height=2,
                            wrap=None,
                            variable=self.selectedView,
                            command=self.showChoice,
                            value=val).pack(anchor=W, side=LEFT)

            rightFrame = Frame(viewOptionFrame)

            topFrame = Frame(rightFrame)
            opTitle = Label(topFrame, text=key.toString())
            opTitle.configure(font=("Helvetica", 10, "bold"))
            opTitle.pack(side=LEFT, anchor=W)
            Label(topFrame, text="Distortion single value").pack(side=LEFT, padx=(10,0))
            topFrame.pack(side=TOP, anchor=W)

    #        bottomFrame=Frame(rightFrame)
            canvas = Canvas(rightFrame, width=120, height=2)
            #ToDo: make distortion object fill canvas with colorbar 
            self.canvas.pack(side=TOP, pady=(2,0))
    #        bottomFrame.pack(side=TOP, anchor=NW)


            rightFrame.pack(side=LEFT, anchor=N)
            viewOptionFrame.pack(side=TOP, anchor=W, pady=(10,0))

        bottomFrame.pack(side=TOP, anchor=W, pady=(0,0))

        self.content.pack(side=LEFT)
