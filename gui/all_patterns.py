from functools import partial
from tkinter import *
from gui.button import TkinterCustomButton
from PIL import ImageTk
from PIL import ImageTk, Image
from gui.pattern_model import PatternModel
from gui.pattern_input.pattern_input_window import PatternInputWindow
from gui.placed_patterns.placed_patterns_menu import PlacedPatternsMenu
import os


class AllPatterns:

    def __init__(self, master: Frame, mainColor: str, patternList: PlacedPatternsMenu):
        self.mainFrame = Frame(master, width=380, bg=mainColor)
        self.patternList = patternList
        self.content = Frame(self.mainFrame, width=380,
                             height=900, padx=20, pady=20)

    def place(self, patternFolderName):
        PatternInputWindow(self.mainFrame, PatternModel(patternFolderName),
                           self.patternList.addPattern).openWindow()

    def buildPattern(self, folderName: str):
        patternFrame = Frame(self.content)
        pattern = PatternModel(folderName)

        imgFile = pattern.img
        imgFile.thumbnail([200, 200], Image.ANTIALIAS)
        img = ImageTk.PhotoImage(imgFile)
        panel = Label(patternFrame, image=img, width=200, height=130)
        panel.image = img
        panel.pack(side=LEFT, fill="both", expand="yes", anchor=N)

        infoFrame = Frame(patternFrame)
        for (key, value) in pattern.attributes.items():
            keyVal = Frame(infoFrame)
            keyLabel = Label(keyVal, text=key, width=6,
                             anchor=W, justify=LEFT, wraplength=50)
            keyLabel.configure(font=("Helvetica", 10, "bold"))
            keyLabel.pack(side=LEFT)
            Label(keyVal, text=value if value else "-", anchor=S, justify=LEFT, wraplength=70
                  ).pack(side=LEFT)

            keyLabel.configure(font=("Helvetica", 10, "bold"))
            keyLabel.pack(side=LEFT)

            keyVal.pack(side=TOP, anchor=W)

        TkinterCustomButton(master=infoFrame, text="Place", command=partial(self.place, pattern.folderName),
                            corner_radius=60, height=25, width=80).pack(side=LEFT, pady=(10, 0))

        infoFrame.pack(side=LEFT, anchor=N, padx=(10, 0))
        patternFrame.pack(side=TOP, pady=(20, 0), anchor=W)

    def build(self, side: str):
        self.content.pack_propagate(0)

        title = Label(self.content, text="All Patterns")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP)

        for file in os.listdir("patterns"):
            if os.path.isdir("patterns/" + file) and file.startswith("pattern"):
                self.buildPattern("patterns/" + file)

        self.content.pack(side=TOP)
        self.mainFrame.pack(side=side, padx=(20, 0), anchor=N)