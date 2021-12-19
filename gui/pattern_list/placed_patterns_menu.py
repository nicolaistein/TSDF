from tkinter import *
from tkinter.filedialog import askdirectory
from gui.button import TkinterCustomButton
from gui.pattern import Pattern
from gui.pattern_input.pattern_input_window import PatternInputWindow
from gui.pattern_list.placed_patterns_item import PlacedPatternsItem
import os


class PlacedPatternsMenu:

    def __init__(self, master: Frame, mainColor: str):
        self.mainFrame = Frame(master, width=400, bg=mainColor)
        self.content = Frame(self.mainFrame, width=340,
                             height=835, padx=20, pady=20)
        self.patterns = []

    def delete(self, pattern):
        pattern.deleteButtons()
        self.patterns.remove(pattern.pattern)
        self.build()

    def onEditFinish(self, pattern):
        self.build()

    def edit(self, pattern: Pattern):
        PatternInputWindow(self.mainFrame, pattern,
                           self.onEditFinish).openWindow()

    def addPattern(self, pattern: Pattern):
        self.patterns.append(pattern)
        self.build()

    def generateGCode(self):
        filename = askdirectory()
        file = open(filename + "/result.gcode", "w")
        for pattern in self.patterns:
            file.write(pattern.getGcode())
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
