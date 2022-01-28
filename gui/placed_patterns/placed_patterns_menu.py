from tkinter import *
from tkinter.filedialog import askdirectory
from gui.button import TkinterCustomButton
from gui.canvas.canvas_manager import CanvasManager
from gui.pattern_model import PatternModel
from gui.pattern_input.pattern_input_window import PatternInputWindow
from gui.placed_patterns.placed_patterns_item import PlacedPatternsItem
from gui.listview import ListView
from gui.numeric_text import NumericText


class PlacedPatternsMenu:

    def __init__(self, master: Frame, canvasManager:CanvasManager, mainColor: str):
        self.mainFrame = Frame(master, bg=mainColor)
        self.canvasManager = canvasManager
        canvasManager.placedPatternsMenu = self
        self.patterns = []
        self.placedPatternItems = []

    def deleteAll(self):
        for p in self.placedPatternItems:
            self.delete(p, False)
        self.placedPatternItems.clear()
        self.build()

    def delete(self, placedPatternItem, rebuild:bool=True):
        placedPatternItem.deleteButtons()
        self.patterns.remove(placedPatternItem.pattern)
        self.canvasManager.patternPlotter.deletePattern(placedPatternItem.pattern)
        if rebuild:
            self.build()

    def onPlacedPatternItemClick(self, pattern):
        self.canvasManager.patternPlotter.selectPattern(pattern)

    def onEditFinished(self, pattern:PatternModel):
        self.canvasManager.patternPlotter.refreshPattern(pattern)
        self.build()

    def edit(self, pattern: PatternModel):
        PatternInputWindow(self.mainFrame, pattern,
                           self.onEditFinished, self.canvasManager, True).openWindow()

    def addPattern(self, pattern: PatternModel):
        self.patterns.append(pattern)
        self.canvasManager.patternPlotter.addPattern(pattern)
        self.build()

    def generateGCode(self):
        filename = askdirectory()
        file = open(filename + "/result.gcode", "w")
        workHeight = self.workHeightText.getNumberInput()
        freeMoveHeight = self.freeMoveHeightText.getNumberInput()

        file.write("G90\n")
        file.write("G0 Z" + str(freeMoveHeight) + "\n\n")
        for pattern in self.patterns:
            result, commands = pattern.getGcode(workHeight,freeMoveHeight)
            file.write(result)
            file.write("\n")
        file.close()

    def getKeyValueFrame(self, parent: Frame, key: str, value:str):
        keyValFrame = Frame(parent)
        keyLabel = Label(keyValFrame, text=key, width=15,
                            anchor=W, justify=LEFT, wraplength=120)
        keyLabel.pack(side=LEFT)
        valText = NumericText(keyValFrame, width=4, initialText=value, floatingPoint=True)
        valText.build().pack(side=LEFT)

        keyValFrame.pack(side=TOP, pady=(5,0))
        return valText

    def build(self):
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        self.content = Frame(self.mainFrame)

        title = Label(self.content, text="Placed Patterns")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP, pady=(20,15))

        self.innerContent = ListView(self.content, 310, 710).build()

        self.placedPatternItems.clear()
        for pattern in self.patterns:
            pat = PlacedPatternsItem(self.innerContent, pattern, self)
            self.placedPatternItems.append(pat)
            pat.build()

        self.content.pack(side=TOP, anchor=N)

        generationFrame = Frame(self.mainFrame, width=323, height=130, pady=20)
        generationFrame.pack_propagate(0)
        self.workHeightText = self.getKeyValueFrame(generationFrame, "Work height", "2.3")
        self.freeMoveHeightText = self.getKeyValueFrame(generationFrame, "Free-Move height", "10")
        TkinterCustomButton(master=generationFrame, text="Generate GCode", command=self.generateGCode,
                            corner_radius=60, height=25, width=160).pack(side=TOP, pady=(10, 0))

        generationFrame.pack(side=TOP)
        self.mainFrame.pack(side=LEFT, padx=(20, 0), anchor=N)
