from tkinter import *

class NumericText:

    def __init__(self, parent:Frame, width=3, initialText:str="", floatingPoint:bool=False):
        self.parent = parent
        self.width = width
        self.initialText = initialText
        self.floatingPoint = floatingPoint

    def cancelInput(self, event):
        return "break"

    def allowInput(self, event):
        pass

    def onKeyPress(self, event):
        allowed = "1234567890"
        if self.floatingPoint: allowed += "."
        if not event.char in allowed:
            return "break"

    def getNumberInput(self):
        text = self.input.get("1.0", END)[:-1]
        return float(text) if self.floatingPoint else int(text)

    def build(self):
        self.input = Text(self.parent, height=1, width=self.width)
        self.input.bind('<Return>', self.cancelInput)
        self.input.bind('<Tab>', self.cancelInput)
        self.input.bind('<BackSpace>', self.allowInput)
        self.input.bind('<KeyPress>', self.onKeyPress)
        self.input.insert(END, self.initialText)
        return self.input
