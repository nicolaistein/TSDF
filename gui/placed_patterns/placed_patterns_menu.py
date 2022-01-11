from tkinter import *
from tkinter.filedialog import askdirectory
from gui.button import TkinterCustomButton
from gui.canvas.canvas_manager import CanvasManager
from gui.pattern_model import PatternModel
from gui.pattern_input.pattern_input_window import PatternInputWindow
from gui.placed_patterns.placed_patterns_item import PlacedPatternsItem
from tkinter import ttk


class PlacedPatternsMenu:

    def __init__(self, master: Frame, canvasManager:CanvasManager, mainColor: str):
        self.mainFrame = Frame(master, bg=mainColor)
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

        file.write("G90\n")
        file.write("G0 Z30\n")
        for pattern in self.patterns:
            print("# menu generates code of " + pattern.name)
            result, commands = pattern.getGcode()
            file.write(result)
            file.write("\n")
        file.close()

    def build(self):
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        self.content = Frame(self.mainFrame, pady=20)

        title = Label(self.content, text="Placed Patterns")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP, pady=(0,15))


        self.canvas = Canvas(self.content, height=750, width=310)
        self.innerContent = Frame(self.canvas, padx=10)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # Add A Scrollbar To The Canvas
        my_scrollbar = ttk.Scrollbar(self.content, orient=VERTICAL, command=self.canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        self.canvas.configure(yscrollcommand=my_scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

        # Add that New frame To a Window In The Canvas
        self.canvas.create_window((0,0), window=self.innerContent, anchor="nw")

        for pattern in self.patterns:
            PlacedPatternsItem(self.innerContent, pattern, self).build()

        self.content.pack(side=TOP, anchor=N)

        TkinterCustomButton(master=self.mainFrame, text="Generate GCode", command=self.generateGCode,
                            corner_radius=60, height=25, width=160).pack(pady=(20, 0))

        self.mainFrame.pack(side=LEFT, padx=(20, 0), anchor=N)
