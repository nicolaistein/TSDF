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

    def buildHeading(self, master:Frame, text:str):
        label = Label(master, text=text, anchor=W, justify=LEFT)
        label.configure(font=("Helvetica", 12, "bold"))
        label.pack(side=TOP)
  
    def getKeyValueFrame(self, parent: Frame, key: str, value:str):
        keyValFrame = Frame(parent)
        keyLabel = Label(keyValFrame, text=key, anchor=W, justify=LEFT)
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        valLabel = Label(keyValFrame, text=value, wraplength=200)
        valLabel.pack(side=LEFT)

        keyValFrame.pack(side="top", anchor="w")
        return valLabel


    def getSuggestion(self):
        return "BFF"

    

    def openWindow(self):
        self.window.title("Analyzation results")
        self.window.resizable(False, False)

        mainContainer = Frame(self.window, padx=20, pady=20)
        self.buildHeading(mainContainer, "Estimated Runtimes")
        self.getKeyValueFrame(mainContainer, "BFF", str(runtimes.bffTime(self.triangleCount, self.basicShape)))
        self.getKeyValueFrame(mainContainer, "LSCM", str(runtimes.bffTime(self.triangleCount)))
        self.getKeyValueFrame(mainContainer, "ARAP", str(runtimes.bffTime(self.triangleCount)))
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
