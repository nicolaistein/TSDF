from tkinter import *
from typing import Mapping
import gui.time_formatter as formatter
from gui.button import TkinterCustomButton
from gui.canvas.canvas_manager import CanvasManager
from gui.canvas.plotting_options.plotting_option import PlottingOption
from gui.menu_heading.menu_heading import MenuHeading
import gui.menu_heading.info_texts as infotexts
from logger import log


class PlottingOptionsMenu:
    distortionLabels = {}
    mainFrame = None
    algo = "-"
    time = "-"
    viewOptions = [(e, e.value) for e in PlottingOption]
    currentDistortions = {e.value: -1 for e in PlottingOption}
    """Contains all viewoptions (facecolor, distortions) displayed in the computation info widget"""

    def __init__(self, master: Frame, canvasManager: CanvasManager):
        self.canvasManager = canvasManager
        self.master = master
        self.selectedView = IntVar()
        self.selectedView.set(0)

    def updateInfo(self, algo: str, time: int):
        """Updates the info shown in the widget"""
        self.algo = algo
        self.time = formatter.formatTime(time)
        self.algorithmLabel.configure(text=self.algo)
        self.timeLabel.configure(text=self.time)
        self.selectedView.set(0)
        self.refreshButton()

        self.setDistortionValues({e.value: -1 for e in PlottingOption})

    def getKeyValueFrame(self, parent: Frame, key: str, value: str):
        keyValFrame = Frame(parent)
        keyLabel = Label(
            keyValFrame, text=key, width=10, anchor=W, justify=LEFT, wraplength=120
        )
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        valLabel = Label(keyValFrame, text=value, wraplength=100)
        valLabel.pack(side=LEFT)

        keyValFrame.pack(side="top", anchor="w")
        return valLabel

    def refreshView(self):
        self.edgeButton.delete()
        for child in self.mainFrame.winfo_children():
            child.destroy()
        self.mainFrame.destroy()
        self.build()

    def refreshButton(self):
        text = "Show Edges" if not self.canvasManager.plotEdges else "Hide Edges"
        self.edgeButton.set_text(text)

    def onEdgeClick(self):
        self.canvasManager.onEdges()
        self.refreshButton()

    def showChoice(self):
        selected = self.selectedView.get()
        self.canvasManager.selectPlottingOption(selected)

    def setDistortionValues(self, values: Mapping):
        for distortion, distVal in values.items():
            self.currentDistortions[distortion] = distVal
        self.refreshDistortionLabels()

    def refreshDistortionLabels(self):
        for distortion, distVal in self.currentDistortions.items():
            distText = str(round(distVal, 2)) if distVal != -1 else "-"
            if distortion not in self.distortionLabels:
                continue
            self.distortionLabels[distortion].configure(text=distText)

    def build(self):

        self.mainFrame = Frame(self.master)
        self.content = Frame(self.mainFrame, width=260, height=450, padx=20, pady=20)
        self.content.pack_propagate(0)

        MenuHeading("Plotting Options", infotexts.plottingOptions).build(self.content)

        self.algorithmLabel = self.getKeyValueFrame(
            self.content, "Algorithm", self.algo
        )
        self.timeLabel = self.getKeyValueFrame(self.content, "Time", self.time)

        self.edgeButton = TkinterCustomButton(
            master=self.content,
            text="",
            command=self.onEdgeClick,
            corner_radius=60,
            height=25,
            width=120,
        )
        self.edgeButton.pack(side=TOP, pady=(10, 8))
        self.refreshButton()

        bottomFrame = Frame(self.content)

        for distortion, distIndex in self.viewOptions:
            viewOptionFrame = Frame(bottomFrame)
            Radiobutton(
                viewOptionFrame,
                text="",
                height=1,
                wrap=None,
                variable=self.selectedView,
                command=self.showChoice,
                value=distIndex,
            ).pack(anchor=W, side=LEFT)

            rightFrame = Frame(viewOptionFrame)

            minDist, optimalDist, _ = distortion.getMinMax()

            innerTopFrame = Frame(rightFrame)
            opTitle = Label(innerTopFrame, text=distortion.toString())
            opTitle.configure(font=("Helvetica", 10, "bold"))
            opTitle.pack(side=LEFT, anchor=W)

            if optimalDist is not None:
                self.distortionLabels[distortion.value] = Label(
                    innerTopFrame, text="-", fg="blue"
                )
                self.distortionLabels[distortion.value].pack(
                    side=LEFT, padx=(0, 0), pady=(1, 0)
                )
            innerTopFrame.pack(side=TOP, anchor=W)

            if optimalDist is not None:
                innerBottomFrame = Frame(rightFrame)
                if minDist is None:
                    self.buildTwoValue(innerBottomFrame, distortion)
                else:
                    self.buildThreeValue(innerBottomFrame, distortion)
                innerBottomFrame.pack(side=TOP, anchor=NW)

            rightFrame.pack(side=LEFT, anchor=N)
            viewOptionFrame.pack(side=TOP, anchor=W, pady=(10, 0))

        self.refreshDistortionLabels()
        bottomFrame.pack(side=TOP, anchor=W, pady=(0, 0))

        self.content.pack(side=LEFT)
        self.mainFrame.pack(side=TOP, pady=(2, 0), anchor=N)

    def buildTwoValue(self, innerBottomFrame: Frame, distortion: PlottingOption):
        _, optimalDist, maxDist = distortion.getMinMax()
        Label(innerBottomFrame, text=str(round(optimalDist, 1))).pack(
            side=LEFT, anchor=W
        )

        canvas = Canvas(
            innerBottomFrame, width=100, height=5, bd=0, highlightthickness=0
        )
        canvas.pack(side=LEFT, padx=(5, 5))
        distortion.getColormap(canvas, 100, 5)
        Label(innerBottomFrame, text=str(round(maxDist, 1))).pack(side=LEFT, anchor=W)

    def buildThreeValue(self, innerBottomFrame: Frame, distortion: PlottingOption):
        minDist, optimalDist, maxDist = distortion.getMinMax()
        Label(innerBottomFrame, text=str(round(minDist, 1))).pack(side=LEFT, anchor=W)

        canvas = Canvas(
            innerBottomFrame, width=40, height=5, bd=0, highlightthickness=0
        )
        canvas.pack(side=LEFT, padx=(5, 5))
        distortion.getColormap(
            canvas, 40, 5, optionColor=distortion.getColor()[0], reverse=True
        )

        Label(innerBottomFrame, text=str(round(optimalDist, 1))).pack(
            side=LEFT, anchor=W
        )

        canvas = Canvas(
            innerBottomFrame, width=40, height=5, bd=0, highlightthickness=0
        )
        canvas.pack(side=LEFT, padx=(5, 5))
        distortion.getColormap(canvas, 40, 5, optionColor=distortion.getColor()[1])

        Label(innerBottomFrame, text=str(round(maxDist, 1))).pack(side=LEFT, anchor=W)
