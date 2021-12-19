from tkinter import *
from PIL import ImageTk
from PIL import ImageTk, Image
from typing import Mapping
from gui.button import TkinterCustomButton
from gui.pattern import Pattern
import os


class PlacedPatternsItem:

    def __init__(self, master: Frame, pattern: Pattern, menu):
        self.pattern = pattern
        self.menu = menu
        self.master = master

    def delete(self):
        self.menu.delete(self)

    def edit(self):
        self.menu.edit(self.pattern)

    def getKeyValueFrame(self, parent: Frame, key: str, value: str, valueLength: float = 70):
        keyValFrame = Frame(parent)
        keyLabel = Label(keyValFrame, text=key, width=7,
                         anchor=W, justify=LEFT, wraplength=50)
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        Label(keyValFrame, text=value if value else "-", anchor=S, justify=LEFT, wraplength=valueLength
              ).pack(side=LEFT)

        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)

        return keyValFrame

    def deleteButtons(self):
        self.button1.delete()
        self.button2.delete()

    def build(self):

        container = Frame(self.master)

        topContent = Frame(container)

        importantValues = {}
        importantValues["name"] = self.pattern.name
        importantValues["id"] = self.pattern.id
        importantValues["position"] = self.pattern.getPosition()
        importantValues["rotation"] = str(self.pattern.rotation) + " degrees"

        leftFrame = Frame(topContent)
        self.getKeyValueFrame(leftFrame, "name", self.pattern.name).pack(
            side=TOP, anchor=W)
        self.getKeyValueFrame(leftFrame, "id", self.pattern.id).pack(
            side=TOP, anchor=W)
        leftFrame.pack(side=LEFT, anchor=N)

        rightFrame = Frame(topContent)
        self.getKeyValueFrame(rightFrame, "position", self.pattern.getPosition()).pack(
            side=TOP, anchor=W)
        self.getKeyValueFrame(rightFrame, "rotation", str(
            self.pattern.rotation) + " degrees").pack(side=TOP, anchor=W)
        rightFrame.pack(side=LEFT, anchor=N, padx=(10, 0))

        topContent.pack(side=TOP, anchor=W)

        paramsText = ""
        for key, val in self.pattern.params.items():
            paramsText += key + "=" + val + "   "
        if paramsText:
            paramsText = paramsText[:-2]

        if len(self.pattern.params) > 0:
            self.getKeyValueFrame(container, "params", paramsText, 200).pack(
                side=TOP, anchor=W, pady=(0, 0))

        buttonContainer = Frame(container)
        self.button1 = TkinterCustomButton(master=buttonContainer, text="Edit", command=self.edit,
                                           corner_radius=60, height=25, width=80)
        self.button1.pack(side=LEFT)

        self.button2 = TkinterCustomButton(master=buttonContainer, text="Delete", command=self.delete,
                                           fg_color="#a62828", hover_color="#c75454",
                                           corner_radius=60, height=25, width=80)
        self.button2.pack(side=RIGHT, padx=(10, 0))

        buttonContainer.pack(side=TOP, anchor=N, pady=(10, 0))

        container.pack(side=TOP, pady=(20, 0), anchor=N)
