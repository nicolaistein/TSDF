from logging import error
from os import name
from tkinter import *
from typing import List
from gui.pattern_model import PatternModel
from gui.button import TkinterCustomButton


class AnalyzeWindow:

    def __init__(self, root):
        self.window = Toplevel(root)

    def abort(self):
        self.window.destroy()

  
    def openWindow(self):
        self.window.title("Analyzation results")
        self.window.resizable(False, False)

        mainContainer = Frame(self.window, padx=20, pady=20)
      
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
