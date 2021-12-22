from tkinter import *
from tkinter.filedialog import askdirectory
from gui.button import TkinterCustomButton
from gui.plotting.canvas_manager import CanvasManager
from gui.pattern_model import PatternModel
from gui.pattern_input.pattern_input_window import PatternInputWindow
from gui.pattern_list.placed_patterns_item import PlacedPatternsItem
import os


class PlacedPatternsMenu:

    def __init__(self, master: Frame, canvasManager:CanvasManager, mainColor: str):
        self.mainFrame = Frame(master, bg=mainColor)
        self.content = Frame(self.mainFrame, width=320,
                             height=835, padx=20, pady=20)
        self.canvasManager = canvasManager
        self.patterns = []

    def delete(self, placedPatternItem):
        placedPatternItem.deleteButtons()
        self.patterns.remove(placedPatternItem.pattern)
        self.canvasManager.deletePattern(placedPatternItem.pattern)
        self.build()

    def onPlacedPatternItemClick(self, pattern):
        self.canvasManager.selectPattern(pattern)

    def onEditFinished(self, pattern:PatternModel):
        self.canvasManager.refreshPattern(pattern)
        self.build()

    def edit(self, pattern: PatternModel):
        PatternInputWindow(self.mainFrame, pattern,
                           self.onEditFinished).openWindow()

    def addPattern(self, pattern: PatternModel):
        self.patterns.append(pattern)
        self.canvasManager.addPattern(pattern)
        self.build()

    def generateGCode(self):
        filename = askdirectory()
        print("pattern count: " + str(len(self.patterns)))
        file = open(filename + "/result.gcode", "w")
        print("G90")
        print("G0 Z30")

        file.write("G90\n")
        file.write("G0 Z30\n")
        for pattern in self.patterns:
            print("# menu generates code of " + pattern.name)
            result, commands = pattern.getGcode()
            file.write(result)
            file.write("\n")
        file.close()

    def build(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self.content.pack_propagate(0)

        title = Label(self.content, text="Placed Patterns")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP)

        patternContainer = Frame(self.content)
        for pattern in self.patterns:
            PlacedPatternsItem(patternContainer, pattern, self).build()

        patternContainer.pack(side=TOP, anchor=N)
        self.content.pack(side=TOP, anchor=N)

        TkinterCustomButton(master=self.mainFrame, text="Generate GCode", command=self.generateGCode,
                            corner_radius=60, height=25, width=160).pack(pady=(20, 0))

        self.mainFrame.pack(side=LEFT, padx=(20, 0), anchor=N)
