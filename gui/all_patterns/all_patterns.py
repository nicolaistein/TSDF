from functools import partial
from tkinter import *
from tkinter import ttk
from gui.button import TkinterCustomButton
from PIL import ImageTk
from PIL import ImageTk, Image
from gui.pattern_model import PatternModel
from gui.pattern_input.pattern_input_window import PatternInputWindow
from gui.placed_patterns.placed_patterns_menu import PlacedPatternsMenu
from gui.menu_heading.menu_heading import MenuHeading
from gui.canvas.canvas_manager import CanvasManager
import gui.menu_heading.info_texts as infotexts
import os
from gui.listview import ListView


class AllPatterns:
    def __init__(
        self,
        master: Frame,
        mainColor: str,
        patternList: PlacedPatternsMenu,
        canvasManager: CanvasManager,
    ):
        self.canvasManager = canvasManager
        self.mainFrame = Frame(master, bg=mainColor)
        self.patternList = patternList
        self.content = Frame(self.mainFrame, padx=0, pady=20)

    def onEdit(self):
        pass

    def place(self, patternFolderName):
        PatternInputWindow(
            self.mainFrame,
            PatternModel(patternFolderName),
            self.onEdit,
            self.patternList.addPattern,
            self.canvasManager,
            False,
        ).openWindow()

    def buildPattern(self, folderName: str):
        patternFrame = Frame(self.innerContent)
        pattern = PatternModel(folderName)

        imgFile = pattern.img
        imgFile.thumbnail([200, 200], Image.ANTIALIAS)
        img = ImageTk.PhotoImage(imgFile)
        panel = Label(patternFrame, image=img, width=200, height=200)
        panel.image = img
        panel.pack(side=LEFT, fill="both", expand="yes")

        infoFrame = Frame(patternFrame)
        for (key, value) in pattern.attributes.items():
            keyVal = Frame(infoFrame)
            keyLabel = Label(
                keyVal, text=key, width=6, anchor=W, justify=LEFT, wraplength=50
            )
            keyLabel.configure(font=("Helvetica", 10, "bold"))
            keyLabel.pack(side=LEFT)
            Label(
                keyVal,
                text=value if value else "-",
                anchor=S,
                justify=LEFT,
                wraplength=70,
            ).pack(side=LEFT)

            keyLabel.configure(font=("Helvetica", 10, "bold"))
            keyLabel.pack(side=LEFT)

            keyVal.pack(side=TOP, anchor=W)

        TkinterCustomButton(
            master=infoFrame,
            text="Place",
            command=partial(self.place, pattern.folderName),
            corner_radius=60,
            height=25,
            width=80,
        ).pack(side=LEFT, pady=(10, 0))

        infoFrame.pack(side=LEFT, padx=(10, 0))
        patternFrame.pack(side=TOP, pady=(0, 0))

    def build(self):

        MenuHeading("All Patterns", infotexts.allPatterns).build(self.content)

        self.innerContent = ListView(
            self.content, width=340, height=320, padx=0
        ).build()

        for file in os.listdir("patterns"):
            if os.path.isdir("patterns/" + file) and file.startswith("pattern"):
                self.buildPattern("patterns/" + file)

        self.content.pack(side=TOP)
        self.mainFrame.pack(side=TOP, anchor=N)
