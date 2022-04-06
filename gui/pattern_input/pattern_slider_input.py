from __future__ import print_function
from tkinter import *
import tkinter.ttk as ttk
from gui.button import TkinterCustomButton
from gui.custom_text import CustomText


class PatternSliderInput:
    def __init__(self, window, title: str, key: str, currentVal: float, maxVal: int):
        self.window = window
        self.currentVal = currentVal
        self.slider_val = DoubleVar()
        if currentVal is not None:
            self.slider_val.set(currentVal)
        self.maxVal = maxVal
        self.key = key
        self.title = title

    def getValue(self):
        current = self.text.get("1.0", END)[:-1]
        return current if current else "0.0"

    def reset(self):
        self.text.delete(1.0, END)
        self.text.insert(END, "0.0")

    def deleteButton(self):
        if not self.button is None:
            self.button.delete()

    def slider_changed(self, event):
        self.currentVal = round(self.slider.get(), 2)
        self.text.delete(1.0, END)
        self.text.insert(END, str(self.currentVal))

    def build(self, master: Frame, pady: float):
        self.pady = pady
        self.mainContainer = Frame(master)

        title = Label(self.mainContainer, text=self.title, width=10, anchor=W)
        title.configure(font=("Helvetica", 10, "bold"))
        title.pack(side=LEFT, padx=(0, 20))

        Label(self.mainContainer, text=self.key + "=").pack(side=LEFT)
        self.text = CustomText(self.mainContainer, width=6, height=1)
        self.text.bind("<Return>", self.cancelInput)
        self.text.bind("<Tab>", self.cancelInput)
        self.text.bind("<BackSpace>", self.allowInput)
        self.text.bind("<KeyPress>", self.onKeyPress)
        self.text.bind("<<TextModified>>", self.refreshSlider)
        self.text.insert(END, str(self.currentVal))
        self.text.pack(side=LEFT, padx=(0, 10))

        self.slider = ttk.Scale(
            self.mainContainer,
            from_=0,
            to=self.maxVal,
            orient="horizontal",
            variable=self.slider_val,
            command=self.slider_changed,
        )
        self.slider.pack(side=LEFT, padx=(10, 0))

        self.button = TkinterCustomButton(
            master=self.mainContainer,
            text="Reset",
            command=self.reset,
            corner_radius=60,
            height=25,
            width=80,
        )
        self.button.pack(side=LEFT, padx=(10, 0))

    def display(self):
        self.mainContainer.pack(side=TOP, anchor=W, pady=(self.pady, 0))

    def cancelInput(self, event):
        return "break"

    def allowInput(self, event):
        pass

    def refreshSlider(self, event):
        try:
            num = float(self.text.get("1.0", END)[:-1])
            self.slider_val.set(round(num, 2))
            self.window.onValueChange()
        except ValueError:
            pass

    def onKeyPress(self, event):
        if not event.char in "1234567890.":
            return "break"
