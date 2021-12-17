from ctypes import pointer, string_at
from tkinter import *
from tkinter.filedialog import askopenfilename
from typing import Mapping
from gui.button import TkinterCustomButton
from PIL import ImageTk, Image
import os


def getPatternAttributes(pattern):
    mapping: Mapping = {}
    mapping["name"] = "NoName"
    mapping["author"] = "NoAuthor"
    mapping["params"] = ""
    for line in pattern:
        if(line.startswith("#")):
            while(line.startswith("#") or line.startswith(" ")):
                line = line[1:]
                split = line.split("=")
                if(len(split) == 2):
                    mapping[split[0]] = split[1]
        else:
            break
    return mapping


class GCodeMenu:

    def __init__(self, master: Frame, mainColor: str):
        self.mainFrame = Frame(master, width=400, bg=mainColor)
        self.content = Frame(self.mainFrame, width=400,
                             height=730, padx=20, pady=20)

    def buildPattern(self, folderName: str):
        patternFrame = Frame(self.content)
        pattern = open(folderName + "/pattern.py", "r")
        mapping = getPatternAttributes(pattern)

        print("Building pattern frame")
        imgFile = Image.open(folderName + "/image.png")
        imgFile.thumbnail([120, 120], Image.ANTIALIAS)
        img = ImageTk.PhotoImage(imgFile)
        panel = Label(patternFrame, image=img)
        panel.image = img
        panel.pack(side=LEFT, fill="both", expand="yes")

        Label(patternFrame, text=mapping["name"]).pack(side=TOP)
        patternFrame.pack(side=TOP, pady=(0, 10), anchor=W)

    def build(self, side: str):
        self.content.pack_propagate(0)

        title = Label(self.content, text="All Patterns")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP)

        for file in os.listdir("patterns"):
            if os.path.isdir("patterns/" + file):
                print("isDir: " + file)
                self.buildPattern("patterns/" + file)

        self.content.pack(side=TOP)
        TkinterCustomButton(master=self.mainFrame, text="Generate GCode",
                            corner_radius=60, height=25, width=160).pack(side=TOP, pady=20)

        self.mainFrame.pack(side=side, padx=(20, 0), anchor=N)
