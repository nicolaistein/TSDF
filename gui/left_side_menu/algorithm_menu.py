from functools import partial
from pyclbr import Function
from tkinter import *
from gui.button import TkinterCustomButton
from algorithms.algorithms import *
from gui.canvas.canvas_manager import CanvasManager
from gui.left_side_menu.file_menu import FileMenu
from gui.left_side_menu.computation_info import ComputationInfo
from algorithms.segmentation.segmentation import folder
import os
from logger import log


class AlgorithmMenu:

    points = []

    algorithms = [
        ("BFF", 0),
        ("LSCM", 1),
        ("ARAP", 2),
    ]

    def __init__(self, master: Frame, canvasManager: CanvasManager,
     fileMenu:FileMenu, compInfo:ComputationInfo, plotter):
        self.mainFrame = Frame(master, width=260, height=200, padx=20, pady=20)
        self.canvasManager = canvasManager
        self.fileMenu = fileMenu
        self.compInfo = compInfo
        plotter.refreshChartDistortionInfo = self.onChartSelect
        canvasManager.refreshChartDistortionInfo = self.onChartSelect
        self.v = IntVar()
        self.v.set(0)

    def onChartSelect(self, chart):
        self.compInfo.setDistortionValues(self.canvasManager.getDistortionsOfChart(chart))
        self.canvasManager.enableChart(chart)

    def calculate(self):
        file = self.fileMenu.getPath()
        if not file:
            return

        chosen = self.v.get()
        algoName, id = self.algorithms[chosen]

        if(chosen == 0):
            coneCount = int(self.bffConeInput.get("1.0", END)[:-1])
            algorithmFunc = partial(executeBFF, coneCount)
            algoName = "BFF with " + str(coneCount) + " cones"
        if(chosen == 1):
            algorithmFunc = executeLSCM
        if(chosen == 2):
            algorithmFunc = executeARAP

        chartList = []
        if self.fileMenu.plotter.isSegmented():
            folderName = os.getcwd() + "/" + folder
            fileList = os.listdir(folderName)
            for file in fileList:
                chartKey = int(file.split(".")[0])
                chartList.append((chartKey, folderName + "/" + file))
        else:
            chartList = [(-1, file)]

        #Todo: map charts to 1-n

        computeStart = time.time()
        results = []
        for key, ch in chartList:
            res = self.calculateSingleFile(ch, algorithmFunc, chosen==0)
            results.append((key,) + res)
        computeEnd = time.time()

        self.canvasManager.plot(results)
        self.compInfo.updateInfo(algoName, computeEnd-computeStart)


    def calculateSingleFile(self, file, algorithm:Function, isBFF):
        time, pointsBefore, facesBefore, pointsAfter, facesAfter = algorithm(file)
        log("file: " + file + ", time: " + str(time) + ", points: " + str(len(pointsAfter)))
        return (pointsBefore, facesBefore, pointsAfter, facesAfter)


    def build(self):

        title = Label(self.mainFrame, text="Flatten")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP, pady=(0, 15))

        self.mainFrame.pack_propagate(0)
        self.assembleAlgoChooserFrame()

        TkinterCustomButton(master=self.mainFrame, text="Calculate", command=self.calculate,
                            corner_radius=60, height=25, width=140).pack(side=TOP, pady=(10, 0))

        self.mainFrame.pack(side=TOP, pady=(2, 0))

    def ShowChoice(self):
        pass

    def cancelInput(self, event):
        return "break"

    def allowInput(self, event):
        pass

    def onKeyPress(self, event):
        if not event.char in "1234567890":
            return "break"

    def assembleAlgoChooserFrame(self):
        selectAlgoFrame = Frame(self.mainFrame)

        for txt, val in self.algorithms:
            optionFrame = Frame(selectAlgoFrame)
            Radiobutton(optionFrame,
                        text=txt,
                        height=1,
                        wrap=None,
                        variable=self.v,
                        command=self.ShowChoice,
                        value=val).pack(anchor=W, side=LEFT)

            if(txt == "BFF"):
                Label(optionFrame, text="with").pack(side=LEFT, anchor=W)
                self.bffConeInput = Text(optionFrame, height=1, width=3)
                self.bffConeInput.bind('<Return>', self.cancelInput)
                self.bffConeInput.bind('<Tab>', self.cancelInput)
                self.bffConeInput.bind('<BackSpace>', self.allowInput)
                self.bffConeInput.bind('<KeyPress>', self.onKeyPress)
                self.bffConeInput.insert(END, "10")
                self.bffConeInput.pack(side=LEFT, anchor=W, padx=10)
                Label(optionFrame, text="cones").pack(side=LEFT, anchor=W)
            optionFrame.pack(side=TOP, anchor=W)

        selectAlgoFrame.pack(side=TOP, anchor=W)
