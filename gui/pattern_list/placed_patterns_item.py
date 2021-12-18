from tkinter import *
from tkinter.filedialog import askopenfilename
from typing import Mapping
from gui.button import TkinterCustomButton
import os


class PlacedPatternsItem:

    def __init__(self, master: Frame, pattern: Mapping):
        self.pattern = pattern
        self.master = master
        print("placed patterns pattern: " + str(pattern))

    def build(self):

        container = Frame(self.master)

        title = Label(container, text=self.pattern["name"])
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=LEFT)

        container.pack(side=TOP, padx=(0, 20), anchor=W)
