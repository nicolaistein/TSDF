from tkinter import *
from tkinter import messagebox
from gui.button import TkinterCustomButton
from gui.canvas.canvas_manager import CanvasManager
from gui.pattern_model import PatternModel
from gui.pattern_input.pattern_input_window import PatternInputWindow
from gui.placed_patterns.placed_patterns_item import PlacedPatternsItem
from gui.listview import ListView
from gui.numeric_text import NumericText
from gui.menu_heading.menu_heading import MenuHeading
import gui.menu_heading.info_texts as infotexts
from tkinter import filedialog
from logger import log
import os


class PlacedPatternsMenu:
    def __init__(self, master: Frame, canvasManager: CanvasManager, mainColor: str):
        self.mainFrame = Frame(master, bg=mainColor)
        self.canvasManager = canvasManager
        canvasManager.placedPatternsMenu = self
        self.placedPatternItems = {}

    def deleteAll(self):
        values = list(self.placedPatternItems.values())
        for p in values:
            p.delete()
        self.placedPatternItems.clear()
        self.build()

    def delete(self, placedPatternItem):
        self.canvasManager.patternPlotter.deletePattern(placedPatternItem.pattern)
        del self.placedPatternItems[placedPatternItem.pattern]

    def onCheckBoundaries(self):
        for p in self.placedPatternItems.values():
            p.resetColor()
        log("Checking boundaries")
        for p in self.placedPatternItems.values():
            p.checkBoundaries()

    def onPlacedPatternItemClick(self, pattern):
        self.canvasManager.patternPlotter.selectPattern(pattern)

    def onEditFinished(self, pattern: PatternModel):
        self.canvasManager.patternPlotter.refreshPattern(pattern)
        self.placedPatternItems[pattern].refreshValues()
        self.placedPatternItems[pattern].checkBoundaries()

    def edit(self, patternItem: PlacedPatternsItem):
        PatternInputWindow(
            self.mainFrame,
            patternItem.pattern,
            patternItem.onEdit,
            self.onEditFinished,
            self.canvasManager,
            True,
        ).openWindow()

    def addPattern(self, pattern: PatternModel):
        self.canvasManager.patternPlotter.addPattern(pattern)
        pat = PlacedPatternsItem(self.innerContent, pattern, self, self.canvasManager)
        self.placedPatternItems[pattern] = pat
        pat.build()
        pat.checkBoundaries()

    def getOverruns(self):
        overrunStart = self.overrunStartText.getNumberInput()
        overrunEnd = self.overrunEndText.getNumberInput()
        printOverrun = self.printOverrunStartText.getNumberInput()
        return overrunStart, overrunEnd, printOverrun

    def generateGCode(self):
        if len(self.placedPatternItems) == 0:
            return
        file = filedialog.asksaveasfile(
            mode="w", defaultextension=".gcode", filetypes=[("GCode file", ".gcode")]
        )
        if file is None:
            return
        workHeight = self.workHeightText.getNumberInput()
        freeMoveHeight = self.freeMoveHeightText.getNumberInput()
        eFactor = self.eFactorText.getNumberInput()
        fFactor = self.fFactorText.getNumberInput()
        overrunStart, overrunEnd, printOverrun = self.getOverruns()
        cleaningX = self.cleaningXText.getNumberInput()
        cleaningY = self.cleaningYText.getNumberInput()
        pause = self.pauseText.getNumberInput()

        file.write("G90\n")
        file.write("G0 Z" + str(freeMoveHeight) + " F" + str(fFactor) + "\n\n")
        currentE = 0
        alllPatterns = self.placedPatternItems.keys()
        for index, pattern in enumerate(alllPatterns):
            result, commands, e = pattern.getGcode(
                workHeight,
                freeMoveHeight,
                eFactor,
                currentE,
                fFactor,
                overrunStart,
                overrunEnd,
                printOverrun,
                pause,
                cleaningX,
                cleaningY,
            )
            currentE = e
            file.write(result)
            file.write("\n")
        file.write("G0 X0 Y0")
        file.close()

        length = len(self.placedPatternItems)
        text = "pattern" if length == 1 else "patterns"
        messagebox.showinfo(
            "Export",
            "Successfully exported " + str(length) + " " + text + " to " + file.name,
        )

    def getKeyValueFrame(
        self, parent: Frame, key: str, value: str, padx: bool = False, defaultValue=0
    ):
        keyValFrame = Frame(parent)
        keyLabel = Label(keyValFrame, text=key, width=12, anchor=W, justify=LEFT)
        keyLabel.pack(side=LEFT)
        valText = NumericText(
            keyValFrame,
            width=4,
            initialText=value,
            floatingPoint=True,
            defaultValue=defaultValue,
        )
        valText.build().pack(side=LEFT, padx=(2, 0))
        valText.bindOnChange(self.canvasManager.patternPlotter.refresh)

        keyValFrame.pack(side=LEFT, pady=(5, 0), padx=(26 if padx else 0, 0))
        return valText

    def build(self):
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        self.content = Frame(self.mainFrame, pady=20)

        MenuHeading("Placed Patterns", infotexts.palcedPatterns).build(self.content)

        self.innerContent = ListView(self.content, 310, 550).build()

        self.placedPatternItems.clear()
        self.content.pack(side=TOP, anchor=N)

        generationFrame = Frame(self.mainFrame, width=327, height=270, pady=20)
        generationFrame.pack_propagate(0)
        inputParentFrame = Frame(generationFrame)
        InputFrame1 = Frame(inputParentFrame)
        self.workHeightText = self.getKeyValueFrame(InputFrame1, "Print height", "2.3")
        self.freeMoveHeightText = self.getKeyValueFrame(
            InputFrame1, "Move height", "10", padx=True
        )
        InputFrame1.pack(side=TOP, anchor=W)

        InputFrame2 = Frame(inputParentFrame)
        self.eFactorText = self.getKeyValueFrame(InputFrame2, "E Factor", "4")
        self.fFactorText = self.getKeyValueFrame(
            InputFrame2, "mm per min", "250", padx=True
        )
        InputFrame2.pack(side=TOP, anchor=W, pady=(5, 0))

        InputFrame3 = Frame(inputParentFrame)
        self.overrunStartText = self.getKeyValueFrame(InputFrame3, "Overrun Start", "2")
        self.overrunEndText = self.getKeyValueFrame(
            InputFrame3, "Overrun End", "1", padx=True
        )
        InputFrame3.pack(side=TOP, anchor=W, pady=(5, 0))
        inputParentFrame.pack(side=TOP, padx=(20, 20))

        InputFrame4 = Frame(inputParentFrame)
        self.printOverrunStartText = self.getKeyValueFrame(
            InputFrame4, "Print-overrun", "1"
        )
        self.pauseText = self.getKeyValueFrame(
            InputFrame4, "Pause in ms", "1000", padx=True
        )
        InputFrame4.pack(side=TOP, anchor=W, pady=(5, 0))

        InputFrame5 = Frame(inputParentFrame)
        self.cleaningXText = self.getKeyValueFrame(
            InputFrame5, "Cleaning x", "", defaultValue=None
        )
        self.cleaningYText = self.getKeyValueFrame(
            InputFrame5, "Cleaning y", "", defaultValue=None, padx=True
        )
        InputFrame5.pack(side=TOP, anchor=W, pady=(5, 0))
        inputParentFrame.pack(side=TOP, padx=(20, 20))

        TkinterCustomButton(
            master=generationFrame,
            text="Generate GCode",
            command=self.generateGCode,
            corner_radius=60,
            height=25,
            width=160,
        ).pack(side=TOP, pady=(15, 0))

        TkinterCustomButton(
            master=generationFrame,
            text="Check Boundaries",
            command=self.onCheckBoundaries,
            corner_radius=60,
            height=25,
            width=160,
        ).pack(side=TOP, pady=(15, 0))

        generationFrame.pack(side=TOP)
        self.mainFrame.pack(side=LEFT, padx=(20, 0), anchor=N)
