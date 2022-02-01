from tkinter import *
import math
from scipy.spatial import distance
import numpy as np
from gui.button import TkinterCustomButton
from algorithms.algorithms import *
from gui.canvas.canvas_manager import CanvasManager
from gui.left_side_menu.file_menu import FileMenu
from gui.left_side_menu.computation_info import ComputationInfo
from gui.numeric_text import NumericText
from algorithms.segmentation.segmentation import folder
from gui.left_side_menu.mode.computation_mode import ComputationMode
import os
from logger import log


class MeasuringTool:
    length = -1
    angle = -1
    currentlyMeasuring:bool = False
    mainFrame:Frame = None
    button:TkinterCustomButton = None

    def __init__(self, master: Frame, canvasManager: CanvasManager):
        self.master = master
        self.canvasManager = canvasManager
        self.plotter = canvasManager.measurePlotter


    def getKeyValueFrame(self, parent: Frame, key: str, value:str):
        keyValFrame = Frame(parent)
        keyLabel = Label(keyValFrame, text=key, width=10,
                            anchor=W, justify=LEFT, wraplength=120)
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        valLabel = Label(keyValFrame, text=value, wraplength=100)
        valLabel.pack(side=LEFT)

        keyValFrame.pack(side="top", anchor="w")
        return valLabel

    def onChange(self, points):
        if len(points) >= 2:
            self.length = distance.euclidean(points[0], points[1])

        if len(points) >= 3:
            v1 = np.array(points[1])-np.array(points[0])
            v2 = np.array(points[1])-np.array(points[2])
            v1_u = v1 / np.linalg.norm(v1)
            v2_u = v2 / np.linalg.norm(v2)
            self.angle = math.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

        self.refreshValues()


    def buttonClick(self):
        if self.currentlyMeasuring: self.onAbort()
        else: 
            self.currentlyMeasuring = True
            self.refreshValues()
            self.refreshButton()
            self.plotter.performMeasure(self.onChange, self.onAbort)

    def refreshView(self):
        self.button.delete()
        for child in self.mainFrame.winfo_children():
            child.destroy()
        self.mainFrame.destroy()
        self.build()

    def onAbort(self):
        self.currentlyMeasuring = False
        self.length = -1
        self.angle = -1
        self.plotter.abort()
        self.refreshValues()
        self.refreshButton()


    def refreshButton(self):
        if self.button is not None:
            self.button.delete()
            self.button.destroy()
        text = "Abort" if self.currentlyMeasuring else "Measure"

        if not self.currentlyMeasuring:
            self.button = TkinterCustomButton(master=self.mainFrame, text=text, command=self.buttonClick,
                            corner_radius=60, height=25, width=140)
        else:
            self.button = TkinterCustomButton(master=self.mainFrame, text=text, command=self.buttonClick,
                            fg_color="#a62828", hover_color="#c75454", corner_radius=60, height=25, width=140)

        self.button.pack(side=TOP, pady=(10, 0))

    def refreshValues(self):
        lengthT = "-" if self.length == -1 else str(round(self.length, 2))
        self.lengthText.configure(text=lengthT)
        angleT = "-" if self.angle == -1 else str(round(self.angle, 2)) + "°"
        self.angleText.configure(text=angleT)


    def build(self):
        self.mainFrame = Frame(self.master, width=260, height=160, padx=20, pady=20)
        title = Label(self.mainFrame, text="Measure")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP, pady=(0, 15))

        self.mainFrame.pack_propagate(0)

        self.lengthText = self.getKeyValueFrame(self.mainFrame, "Length", "")
        self.lengthText.pack(side=TOP)
        self.angleText = self.getKeyValueFrame(self.mainFrame, "Angle", "")
        self.angleText.pack(side=TOP)

        self.refreshValues()
        self.refreshButton()
        self.mainFrame.pack(side=TOP, pady=(2, 0))
