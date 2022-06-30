from tkinter import *
from tkinter import messagebox
from turtle import left
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
        fFactorLine = self.fFactorLineText.getNumberInput()
        fFactorArc = self.fFactorArcText.getNumberInput()
        overrunStart, overrunEnd, printOverrun = self.getOverruns()
        pause = self.pauseText.getNumberInput()
        retract = self.retractText.getNumberInput()
        extrude = self.extrudeText.getNumberInput()

        file.write("G90\n")
        file.write("G28 X Y\n")
        file.write("G28 Z\n")
        file.write("G0 X0 Y0 Z" + str(freeMoveHeight) + " F" + str(fFactorLine) + "\n")
        
        if extrude != 0:
            file.write("G0 X0 Y0 Z" + str(freeMoveHeight) + " E" + str(extrude) + " F" + str(fFactorLine) + "\n")

        file.write("\n")
        currentE = extrude
        alllPatterns = self.placedPatternItems.keys()
        for index, pattern in enumerate(alllPatterns):
            result, commands, e = pattern.getGcode(
                workHeight= workHeight,
                freeMoveHeight = freeMoveHeight,
                eFactor = eFactor,
                eFactorStart = currentE,
                fFactorLine = fFactorLine,
                fFactorArc = fFactorArc,
                overrunStart = overrunStart,
                overrunEnd = overrunEnd,
                printOverrun = printOverrun,
                pause = pause,
                retract = retract
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

    def buildParamLine(self, parent:Frame, name1:str, val1:str, name2:str=None, val2:str=None):
        InputFrame = Frame(parent)
        leftText = self.getKeyValueFrame(
            InputFrame, name1, val1
        )
        rightText = None
        if name2 != None:
            rightText = self.getKeyValueFrame(
                InputFrame, name2, val2, padx=True
                )
        InputFrame.pack(side=TOP, anchor=W, pady=(5, 0))
        return leftText, rightText


    def build(self):
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        self.content = Frame(self.mainFrame, pady=20)

        MenuHeading("Placed Patterns", infotexts.palcedPatterns).build(self.content)

        self.innerContent = ListView(self.content, 310, 510).build()

        self.placedPatternItems.clear()
        self.content.pack(side=TOP, anchor=N)

        generationFrame = Frame(self.mainFrame, width=327, height=310, pady=20)
        generationFrame.pack_propagate(0)
        inputParentFrame = Frame(generationFrame)

        self.workHeightText, self.freeMoveHeightText = self.buildParamLine(
            inputParentFrame, "Print height", "2.3", "Move height", "10")

        self.fFactorLineText, self.fFactorArcText = self.buildParamLine(
            inputParentFrame, "mm/min (Line)", "250", "mm/min (Arcs)", "250")

        self.overrunStartText, self.overrunEndText = self.buildParamLine(
            inputParentFrame, "Overrun Start", "2", "Overrun End", "1")

        self.printOverrunStartText, self.pauseText = self.buildParamLine(
            inputParentFrame, "Print-overrun", "1", "Pause in ms", "1000")

        self.retractText, self.extrudeText = self.buildParamLine(
            inputParentFrame, "Retract", "0", "Extrude", "0")
        
        self.eFactorText, _ = self.buildParamLine(
            inputParentFrame, "E Factor", "4")

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
