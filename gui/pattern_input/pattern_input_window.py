from logging import error
from os import name
from tkinter import *
from typing import List
from gui.pattern_model import PatternModel
from gui.button import TkinterCustomButton
from gui.pattern_input.pattern_input_line import PatternInputLine


class PatternInputWindow:

    def __init__(self, root, pattern: PatternModel, onComplete):
        self.window = Toplevel(root)
        self.pattern = pattern
        self.onComplete = onComplete

    def abort(self):
        self.deleteButtons()
        self.window.destroy()

    def deleteButtons(self):
        self.buttonAccept.delete()
        self.buttonCancel.delete()
        self.nameInput.deleteButton()
        self.parameterInput.deleteButton()
        self.positionInput.deleteButton()
        self.rotationInput.deleteButton()

    def completed(self):
        self.pattern.updateParams(self.parameterInput.getValues())

        self.pattern.setName(self.nameInput.getValues()["name"])
        self.pattern.rotation = float(
            self.rotationInput.getValues()["degrees"])

        loc = self.positionInput.getValues()
        self.pattern.setLocation(float(loc["x"]), float(loc["y"]))

        self.deleteButtons()
        self.window.destroy()

        self.onComplete(self.pattern)

    def openWindow(self):
        self.window.title(
            "Place Pattern " + self.pattern.id if not self.pattern.name
            else "Edit Pattern " + self.pattern.name)
        self.window.resizable(False, False)

        mainContainer = Frame(self.window, padx=20, pady=20)

        pattern = self.pattern
        # Name row
        self.nameInput = PatternInputLine(
            "Name", {"name": pattern.name}, isNumeric=False)
        self.nameInput.build(mainContainer, 10, textWidth=10)
        self.nameInput.display()

        # Parameter row
        self.parameterInput = PatternInputLine(
            "Parameters", self.pattern.params)
        self.parameterInput.build(mainContainer, 15)
        if len(self.pattern.params) > 0:
            self.parameterInput.display()

        # Position row
        self.positionInput = PatternInputLine(
            "Position", {"x": pattern.x, "y": pattern.y})
        self.positionInput.build(mainContainer, 15)
        self.positionInput.display()

        # Rotation row
        self.rotationInput = PatternInputLine(
            "Rotation", {"degrees": pattern.rotation})
        self.rotationInput.build(mainContainer, 15)
        self.rotationInput.display()

        # buttons
        buttonFrame = Frame(mainContainer)
        self.buttonAccept = TkinterCustomButton(master=buttonFrame, text="Accept", command=self.completed,
                                                fg_color="#28a63f", hover_color="#54c76d",
                                                corner_radius=60, height=25, width=80)
        self.buttonAccept.pack(side=LEFT)

        self.buttonCancel = TkinterCustomButton(master=buttonFrame, text="Cancel", command=self.abort,
                                                fg_color="#a62828", hover_color="#c75454",
                                                corner_radius=60, height=25, width=80)
        self.buttonCancel.pack(side=LEFT, padx=(10, 0))

        buttonFrame.pack(side=TOP, anchor=W, pady=(30, 0))

        mainContainer.pack(anchor=N)
        self.window.mainloop()
