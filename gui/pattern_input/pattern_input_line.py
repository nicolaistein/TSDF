from functools import partial
from tkinter import *
from typing import List, Mapping
from gui.button import TkinterCustomButton


class PatternInputLine:

    def __init__(self, title: str, values: List, isNumeric: bool = True):
        self.values = values
        self.title = title
        self.isNumeric = isNumeric

    def getValues(self):
        if len(self.values) == 0:
            return {}
        result = {}
        for key, text in self.texts.items():
            # Remove the /n at the end
            result[key] = text.get("1.0", END)[:-1]
        return result

    def reset(self):
        for key, textField in self.texts.items():
            textField.delete(1.0, END)
            textField.insert(END, "")

    def deleteButton(self):
        if not self.button is None:
            self.button.delete()

    def cancelInput(self, event):
        return "break"

    def allowInput(self, event):
        pass

    def onKeyPress(self, event):
        if not event.char in "1234567890." and self.isNumeric:
            return "break"

    def build(self, master: Frame, pady: float, textWidth=4):
        self.pady = pady
        self.mainContainer = Frame(master)

        title = Label(self.mainContainer, text=self.title, width=10, anchor=W)
        title.configure(font=("Helvetica", 10, "bold"))
        title.pack(side=LEFT, padx=(0, 20))

        self.texts = {}

        for ele in self.values:
            Label(self.mainContainer, text=ele + "=").pack(side=LEFT)
            text = Text(self.mainContainer, width=textWidth, height=1)
            text.bind('<Return>', self.cancelInput)
            text.bind('<Tab>', self.cancelInput)
            text.bind('<BackSpace>', self.allowInput)
            text.bind('<KeyPress>', self.onKeyPress)
            if self.isNumeric:
                text.insert(END, "0.0")
            self.texts[ele] = text
            text.pack(side=LEFT, padx=(0, 10))

        self.button = TkinterCustomButton(master=self.mainContainer, text="Reset", command=self.reset,
                                          corner_radius=60, height=25, width=80)
        self.button.pack(side=LEFT, padx=(10, 0))

    def display(self):
        self.mainContainer.pack(side=TOP, anchor=W, pady=(self.pady, 0))
