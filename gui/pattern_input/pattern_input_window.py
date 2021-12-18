from logging import error
from tkinter import *
from typing import List
from gui.button import TkinterCustomButton
from gui.pattern_input.pattern_input_line import PatternInputLine


class PatternInputWindow:

    def __init__(self, root, args: List, patternName: str, onComplete):
        self.window = Toplevel(root)
        self.args = args
        print("args: " + str(args))
        self.patternName = patternName
        self.onComplete = onComplete

    def abort(self):
        self.deleteButtons()
        self.window.destroy()

    def deleteButtons(self):
        self.onComplete()
        self.buttonAccept.delete()
        self.buttonCancel.delete()
        self.nameInput.deleteButton()
        self.parameterInput.deleteButton()
        self.positionInput.deleteButton()
        self.rotationInput.deleteButton()

    def completed(self):
        result = {}
        result.update(self.nameInput.getValues())
        result.update(self.parameterInput.getValues())
        result.update(self.positionInput.getValues())
        result.update(self.rotationInput.getValues())
        print(result)

        self.deleteButtons()
        self.window.destroy()

    def openWindow(self):
        self.window.title("Place Pattern " + self.patternName)
        self.window.resizable(False, False)

        mainContainer = Frame(self.window, padx=20, pady=20)

        # Name row
        self.nameInput = PatternInputLine("Name/ID", ["name"], isNumeric=False)
        self.nameInput.build(mainContainer, 10, textWidth=10)
        self.nameInput.display()

        # Parameter row
        self.parameterInput = PatternInputLine("Parameters", self.args)
        self.parameterInput.build(mainContainer, 15)
        if len(self.args) > 0:
            self.parameterInput.display()

        # Position row
        self.positionInput = PatternInputLine("Position", ["x", "y"])
        self.positionInput.build(mainContainer, 15)
        self.positionInput.display()

        # Rotation row
        self.rotationInput = PatternInputLine("Rotation", ["degrees"])
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
