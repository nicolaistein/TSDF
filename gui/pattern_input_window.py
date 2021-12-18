from tkinter import *
from typing import List
from gui.button import TkinterCustomButton


class PatternInputWindow:

    def __init__(self, root, args: List, patternName: str, onComplete):
        self.window = Toplevel(root)
        self.args = args
        self.patternName = patternName
        self.onComplete = onComplete

    def abort(self):
        self.window.destroy()

    def completed(self):
        result = {}
        for key, val in self.texts.items():
            result[key] = val.get("1.0", END)
        self.onComplete()
        self.window.destroy()

    def openWindow(self):
        self.window.title("Place Pattern " + self.patternName)
        self.window.resizable(False, False)
   #     self.window.geometry("300x200")

        mainContainer = Frame(self.window, padx=20, pady=20)
        inputFrame = Frame(mainContainer)
        buttonFrame = Frame(mainContainer)

        self.texts = {}

        for ele in self.args:
            Label(inputFrame, text=ele + "=").pack(side=LEFT)
            text = Text(inputFrame, width=4, height=1)
            self.texts[ele] = text
            text.pack(side=LEFT, padx=(0, 10))

        TkinterCustomButton(master=buttonFrame, text="Accept", command=self.completed,
                            corner_radius=60, height=25, width=80).pack(side=LEFT)

        TkinterCustomButton(master=buttonFrame, text="Cancel", command=self.abort,
                            corner_radius=60, height=25, width=80).pack(side=LEFT, padx=(10, 0))

        inputFrame.pack(side=TOP, anchor=W)
        buttonFrame.pack(side=TOP, anchor=W, pady=(10, 0))
        mainContainer.pack(anchor=N)
        self.window.mainloop()

        # get results
