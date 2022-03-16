from tkinter import *
from gui.custom_text import CustomText
from logger import log


class NumericText:
    def __init__(
        self,
        parent: Frame,
        width=3,
        initialText: str = "",
        floatingPoint: bool = False,
        defaultValue=0,
    ):
        self.parent = parent
        self.width = width
        self.initialText = initialText
        self.floatingPoint = floatingPoint
        self.defaultValue = defaultValue
        self.onChange = None

    def bindOnChange(self, onChange):
        self.onChange = onChange

    def onInputChange(self, _):
        if self.onChange is None:
            return
        self.onChange()

    def cancelInput(self, event):
        return "break"

    def allowInput(self, event):
        pass

    def onKeyPress(self, event):
        allowed = "1234567890"
        if self.floatingPoint:
            allowed += "."
        if not event.char in allowed:
            return "break"

    def getNumberInput(self):
        text = self.input.get("1.0", END)[:-1]
        if len(text) == 0 or text == ".":
            return self.defaultValue
        return float(text) if self.floatingPoint else int(text)

    def build(self):
        self.input = CustomText(self.parent, height=1, width=self.width)
        self.input.bind("<Return>", self.cancelInput)
        self.input.bind("<Tab>", self.cancelInput)
        self.input.bind("<BackSpace>", self.allowInput)
        self.input.bind("<KeyPress>", self.onKeyPress)
        self.input.bind("<<TextModified>>", self.onInputChange)
        self.input.insert(END, self.initialText)
        return self.input
