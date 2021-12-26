from logging import error
from os import name
from tkinter import *
from typing import List
from gui.pattern_model import PatternModel
from gui.button import TkinterCustomButton
import gui.left_side_menu.analyze.runtimes as runtimes


class AnalyzeWindow:

    def __init__(self, root, triangleCount:int, closed:bool, basicShape:bool, curves:bool,
     timeLimit:str, edgeCount:str):
        self.window = Toplevel(root)
        self.closed = closed
        self.basicShape = basicShape
        self.curves = curves
        self.timeLimit = timeLimit
        self.edgeCount = edgeCount
        self.triangleCount = triangleCount

    def abort(self):
        self.window.destroy()

    def buildHeading(self, master:Frame, text:str, pady=20):
        label = Label(master, text=text)
        label.configure(font=("Helvetica", 12, "bold"))
        label.pack(side=TOP, anchor=W, pady=(pady, 0))
  
    def getKeyValueFrame(self, parent: Frame, key: str, value:str):
        keyValFrame = Frame(parent)
        keyLabel = Label(keyValFrame, text=key, anchor=W, justify=LEFT, width=8)
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        valLabel = Label(keyValFrame, text=value, wraplength=200)
        valLabel.pack(side=LEFT)

        keyValFrame.pack(side="top", anchor="w")
        return valLabel

    def formatTime(self, time:int):
        minutes = int(time//60)
        seconds = int(round(time%60, 0))
        val = str(seconds) + "s"
        if minutes > 0:
            val = str(minutes) + "m " + val
        return val

    def getSuggestion(self):
        return "BFF"

    

    def openWindow(self):
        self.window.title("Analyzation results")
        self.window.resizable(False, False)

        mainContainer = Frame(self.window, padx=20, pady=20)
        self.buildHeading(mainContainer, "Estimated Runtimes", 0)
        self.getKeyValueFrame(mainContainer, "BFF", self.formatTime(runtimes.bffTime(self.triangleCount, self.basicShape)) + " per cone")
        self.getKeyValueFrame(mainContainer, "LSCM", self.formatTime(runtimes.lscmTime(self.triangleCount)))
        self.getKeyValueFrame(mainContainer, "ARAP", self.formatTime(runtimes.arapTime(self.triangleCount)))
        self.buildHeading(mainContainer, "Possibilities")
        self.buildHeading(mainContainer, "Suggestion")
      
        # buttons
        buttonFrame = Frame(mainContainer)
        self.buttonAccept = TkinterCustomButton(master=buttonFrame, text="Apply suggestion", command=self.abort,
                                                fg_color="#28a63f", hover_color="#54c76d",
                                                corner_radius=60, height=25, width=160)
        self.buttonAccept.pack(side=LEFT)

        self.buttonCancel = TkinterCustomButton(master=buttonFrame, text="Close", command=self.abort,
                                                fg_color="#a62828", hover_color="#c75454",
                                                corner_radius=60, height=25, width=80)
        self.buttonCancel.pack(side=LEFT, padx=(10, 0))

        buttonFrame.pack(side=TOP, anchor=W, pady=(30, 0))

        mainContainer.pack(anchor=N)
        self.window.mainloop()
