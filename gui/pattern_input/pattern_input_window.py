from logging import error
from os import name
from tkinter import *
from typing import List
from copy import copy
from gui.pattern_model import PatternModel
from gui.button import TkinterCustomButton
from gui.pattern_input.pattern_input_line import PatternInputLine
from gui.pattern_input.pattern_slider_input import PatternSliderInput
from gui.canvas.canvas_manager import CanvasManager


class PatternInputWindow:

    def __init__(self, root, pattern: PatternModel, onComplete, canvasManager:CanvasManager, isEditMode:bool):
        self.window = Toplevel(root)
        self.oldObject = copy(pattern)
        self.isEditMode = isEditMode
        self.pattern = pattern
        self.onComplete = onComplete
        self.canvasManager = canvasManager
        self.initialized = False

    def abort(self):
        if not self.isEditMode:
            self.canvasManager.patternPlotter.deletePattern(self.pattern)

        #Reset values
        self.pattern.name = self.oldObject.name
        self.pattern.params = self.oldObject.params
        self.pattern.x = self.oldObject.x
        self.pattern.y = self.oldObject.y
        self.pattern.rotation = self.oldObject.rotation
        self.deleteButtons()
        self.window.destroy()
        self.onComplete(self.pattern)

    def deleteButtons(self):
        self.buttonAccept.delete()
        self.buttonCancel.delete()
        self.nameInput.deleteButton()
        self.parameterInput.deleteButton()
        self.positionInput.deleteButton()
        self.rotationInput.deleteButton()

    def onValueChange(self):
        self.collectValues()
        self.canvasManager.patternPlotter.refreshPattern(self.pattern)


    def completed(self):
        self.collectValues()
        self.deleteButtons()
        self.window.destroy()
        self.onComplete(self.pattern)

    def collectValues(self):
        if self.initialized:
            self.pattern.updateParams(self.parameterInput.getValues())

            self.pattern.setName(self.nameInput.getValues()["name"])
            self.pattern.rotation = round(float(self.rotationInput.getValue()), 2)

            loc = self.positionInput.getValues()
            self.pattern.setLocation(float(loc["x"]), float(loc["y"]))


    def openWindow(self):
        self.window.title(
            "Place Pattern " + self.pattern.id if not self.pattern.name
            else "Edit Pattern " + self.pattern.name)
        self.window.resizable(False, False)

        mainContainer = Frame(self.window, padx=20, pady=20)

        pattern = self.pattern
        # Name row
        self.nameInput = PatternInputLine(self,
            "Name", {"name": pattern.name}, isNumeric=False)
        self.nameInput.build(mainContainer, 10, textWidth=10)
        self.nameInput.display()

        # Parameter row
        self.parameterInput = PatternInputLine(self,
            "Parameters", self.pattern.params)
        self.parameterInput.build(mainContainer, 15)
        if len(self.pattern.params) > 0:
            self.parameterInput.display()

        # Rotation row
        self.rotationInput = PatternSliderInput(self,"Rotation", "degrees", pattern.rotation, 360)
        self.rotationInput.build(mainContainer, 15)
        self.rotationInput.display()

        # Position row
        self.positionInput = PatternInputLine(self,
            "Position", {"x": pattern.x, "y": pattern.y})
        self.positionInput.build(mainContainer, 15)
        self.positionInput.display()

        self.initialized = True

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
