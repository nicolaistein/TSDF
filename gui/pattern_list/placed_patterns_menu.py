from tkinter import *
from tkinter.filedialog import askopenfilename
from gui.button import TkinterCustomButton
import os


class PlacedPatternsMenu:

    def __init__(self, master: Frame, mainColor: str):
        self.mainFrame = Frame(master, width=400, bg=mainColor)
        self.content = Frame(self.mainFrame, width=340,
                             height=900, padx=20, pady=20)
        self.patterns = []

    def addPattern(pattern):
        print("add pattern " + str(pattern))

    def build(self, side: str):
        self.content.pack_propagate(0)

        title = Label(self.content, text="Placed Patterns")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP)

        self.content.pack(side=TOP)
        self.mainFrame.pack(side=side, padx=(20, 0), anchor=N)
