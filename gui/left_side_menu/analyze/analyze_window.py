from tkinter import *
from gui.pattern_model import PatternModel
from gui.button import TkinterCustomButton
import gui.left_side_menu.analyze.runtimes as runtimes
import gui.time_formatter as formatter


class AnalyzeWindow:

    def __init__(self, root, triangleCount:int, closed:bool, basicShape:bool, curves:bool,
     timeLimit:int, edgeCount:str):
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

    def getSuggestion(self):
        return "BFF"

    def getMaxConeCount(self):
        time = runtimes.bffTime(self.triangleCount, self.basicShape)
        cones = 1
        while time * (cones+1) <= self.timeLimit:
            cones += 1

        return cones

    def openWindow(self):
        self.window.title("Analyzation results")
        self.window.resizable(False, False)

        mainContainer = Frame(self.window, padx=20, pady=20)
        self.buildHeading(mainContainer, "Estimated Runtimes", 0)
        self.getKeyValueFrame(mainContainer, "BFF", formatter.formatTime(runtimes.bffTime(self.triangleCount, self.basicShape)) + " per cone")
        self.getKeyValueFrame(mainContainer, "LSCM", formatter.formatTime(runtimes.lscmTime(self.triangleCount)))
        self.getKeyValueFrame(mainContainer, "ARAP", formatter.formatTime(runtimes.arapTime(self.triangleCount)))

        self.buildHeading(mainContainer, "Possibilities")
        
        if runtimes.bffTime(self.triangleCount, self.basicShape) <= self.timeLimit:
            self.getKeyValueFrame(mainContainer, "BFF with max. " + str(self.getMaxConeCount()) + " cones", "")
        if not self.closed:
            if runtimes.lscmTime(self.triangleCount) <= self.timeLimit:
                self.getKeyValueFrame(mainContainer, "LSCM", "")
            if runtimes.arapTime(self.triangleCount) <= self.timeLimit:
                self.getKeyValueFrame(mainContainer, "ARAP", "")

        self.buildHeading(mainContainer, "Suggestion")
        self.getKeyValueFrame(mainContainer, self.getSuggestion(), "")
      
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
