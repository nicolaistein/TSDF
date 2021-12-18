from functools import partial
from tkinter import *
from tkinter.filedialog import askopenfilename
from typing import Mapping
from gui.button import TkinterCustomButton
from PIL import ImageTk, Image
from gui.pattern_input.pattern_input_window import PatternInputWindow
from gui.pattern_list.placed_patterns_menu import PlacedPatternsMenu
import os


def parsePatternAttributes(pattern):
    mapping: Mapping = {}
    mapping["name"] = "NoName"
    mapping["author"] = "NoAuthor"
    mapping["params"] = ""
    for line in pattern:
        if(line.startswith("#")):
            while(line.startswith("#") or line.startswith(" ")):
                line = line[1:]
            if(line.endswith("\n")):
                line = line[:len(line)-1]
            split = line.split("=")
            if(len(split) == 2):
                mapping[split[0]] = split[1]
        else:
            break
    return mapping


class GCodeMenu:

    def __init__(self, master: Frame, mainColor: str, patternList: PlacedPatternsMenu):
        self.mainFrame = Frame(master, width=300, bg=mainColor)
        self.patternList = patternList
        self.content = Frame(self.mainFrame, width=300,
                             height=900, padx=20, pady=20)

    def place(self, pattern):
        params = pattern["params"].split(",")
        PatternInputWindow(self.mainFrame, [x for x in params if x],
                           pattern["name"], self.patternList.addPattern).openWindow()

    def buildPattern(self, folderName: str):
        patternFrame = Frame(self.content)
        pattern = open(folderName + "/pattern.py", "r")
        mapping = parsePatternAttributes(pattern)

        imgFile = Image.open(folderName + "/image.png")
        imgFile.thumbnail([120, 120], Image.ANTIALIAS)
        img = ImageTk.PhotoImage(imgFile)
        panel = Label(patternFrame, image=img, width=120, height=120)
        panel.image = img
        panel.pack(side=LEFT, fill="both", expand="yes")

        infoFrame = Frame(patternFrame)
        for (key, value) in mapping.items():
            keyVal = Frame(infoFrame)
            keyLabel = Label(keyVal, text=key, width=6, anchor=W)
            keyLabel.configure(font=("Helvetica", 10, "bold"))
            keyLabel.pack(side=LEFT)
            Label(keyVal, text=value if value else "-", anchor=S, justify=LEFT
                  ).pack(side=LEFT)

            keyLabel.configure(font=("Helvetica", 10, "bold"))
            keyLabel.pack(side=LEFT)

            keyVal.pack(side=TOP, anchor=W)

        TkinterCustomButton(master=infoFrame, text="Place", command=partial(self.place, mapping),
                            corner_radius=60, height=25, width=80).pack(side=LEFT, pady=(10, 0))

        infoFrame.pack(side=LEFT, anchor=N, padx=(10, 0))
        patternFrame.pack(side=TOP, pady=(20, 0), anchor=W)

    def build(self, side: str):
        self.content.pack_propagate(0)

        title = Label(self.content, text="All Patterns")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP)

        for file in os.listdir("patterns"):
            if os.path.isdir("patterns/" + file):
                self.buildPattern("patterns/" + file)

        self.content.pack(side=TOP)
        self.mainFrame.pack(side=side, padx=(20, 0), anchor=N)
