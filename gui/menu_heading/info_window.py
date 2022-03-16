from tkinter import *
from typing import Mapping
from gui.pattern_model import PatternModel
from gui.button import TkinterCustomButton
import gui.left_side_menu.analyze.runtimes as runtimes
import gui.time_formatter as formatter


class InfoWindow:
    def __init__(self, root, title: str, keyVals: Mapping):
        self.window = Toplevel(root)
        self.window.iconbitmap("image.ico")
        self.title = title
        self.keyVals = keyVals

    def abort(self):
        self.buttonCancel.delete()
        self.window.destroy()

    def getKeyValueFrame(self, parent: Frame, key: str, value: str):
        keyValFrame = Frame(parent)
        keyLabel = Label(
            keyValFrame, text=key, anchor=W, justify=LEFT, width=12, wraplength=90
        )
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        valLabel = Label(
            keyValFrame, text=value, anchor=W, justify=LEFT, wraplength=300
        )
        valLabel.pack(side=LEFT)

        keyValFrame.pack(side="top", anchor=NW, pady=(10, 0))
        return valLabel

    def openWindow(self):
        self.window.title(self.title)
        mainContainer = Frame(self.window, padx=20, pady=20)

        label = Label(mainContainer, text=self.title + " Info")
        label.configure(font=("Helvetica", 12, "bold"))
        label.pack(side=TOP, anchor=W, pady=(0, 10))
        for key, val in self.keyVals.items():
            self.getKeyValueFrame(mainContainer, key, val)

        # buttons
        buttonFrame = Frame(mainContainer)

        self.buttonCancel = TkinterCustomButton(
            master=buttonFrame,
            text="Close",
            command=self.abort,
            fg_color="#a62828",
            hover_color="#c75454",
            corner_radius=60,
            height=25,
            width=80,
        )
        self.buttonCancel.pack(side=LEFT)

        buttonFrame.pack(side=TOP, anchor=W, pady=(30, 0))

        mainContainer.pack(anchor=N)
        self.window.mainloop()
