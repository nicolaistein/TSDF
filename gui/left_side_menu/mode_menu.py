from enum import Enum
from functools import partial
from pyclbr import Function
from tkinter import *
from gui.button import TkinterCustomButton
from algorithms.algorithms import *
from gui.canvas.canvas_manager import CanvasManager
from gui.left_side_menu.file_menu import FileMenu
from gui.left_side_menu.analyze.analyze_menu import AnalyzeMenu
from gui.left_side_menu.algorithm_menu import AlgorithmMenu
import os
from logger import log



class ModeMenu:

    automaticMode:bool = True
    button:TkinterCustomButton = None

    def __init__(self, master: Frame, analyzeMenu: AnalyzeMenu, algoMenu: AlgorithmMenu):
        self.mainFrame = Frame(master, width=260, height=140, padx=20, pady=20)
        self.analyzeMenu = analyzeMenu
        self.algoMenu = algoMenu


    def changeMode(self):
        self.automaticMode = not self.automaticMode
        self.refreshButton()
        #Todo: notify algoMenu and analyzeMenu

    def refreshButton(self):
        for el in self.buttonFrame.winfo_children():
            el.destroy()
        text = "Automatic Mode" if self.automaticMode else "Manual Mode"
        if self.button is not None: self.button.delete()
        self.button = TkinterCustomButton(master=self.buttonFrame, text=text, command=self.changeMode,
                            corner_radius=60, height=25, width=160)
        self.button.pack(side=TOP, pady=(10, 0))

    def build(self):

        title = Label(self.mainFrame, text="Select Mode")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP, pady=(0, 15))

        self.mainFrame.pack_propagate(0)

        self.buttonFrame = Frame(self.mainFrame)
        self.refreshButton()
        self.buttonFrame.pack(side=TOP)

        self.mainFrame.pack(side=TOP, pady=(2, 0))