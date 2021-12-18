from tkinter import *
from tkinter.filedialog import askopenfilename
from gui.button import TkinterCustomButton
from gui.pattern_list.placed_patterns_item import PlacedPatternsItem
import os


class PlacedPatternsMenu:

    def __init__(self, master: Frame, mainColor: str):
        self.mainFrame = Frame(master, width=400, bg=mainColor)
        self.content = Frame(self.mainFrame, width=340,
                             height=900, padx=20, pady=20)
        self.patterns = []

    def addPattern(self, pattern):
        print("add pattern " + str(pattern))
        self.patterns.append(pattern)
        self.build()

    def build(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self.content.pack_propagate(0)

        title = Label(self.content, text="Placed Patterns")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP)

        patternContainer = Frame(self.content)
        for pattern in self.patterns:
            PlacedPatternsItem(patternContainer, pattern).build()

        patternContainer.pack(side=TOP, anchor=N)
        self.content.pack(side=TOP, anchor=N)
        self.mainFrame.pack(side=LEFT, padx=(20, 0), anchor=N)
