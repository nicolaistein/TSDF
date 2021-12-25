from tkinter import *
from gui.button import TkinterCustomButton
from algorithms.algorithms import *
from gui.left_side_menu.file_menu import FileMenu
from gui.left_side_menu.analyze.analyze_window import AnalyzeWindow


class AnalyzeMenu:

    

    def __init__(self, master: Frame, fileMenu:FileMenu):
        self.mainFrame = Frame(
            master, width=220, height=280, padx=20, pady=20)
        self.fileMenu = fileMenu
        self.closed = IntVar()
        self.basicShape = IntVar()
        self.curves = IntVar()
        

    def showResult(self):
        print("show result")

    def buildTextInput(self, label:str):
        textInputFrame = Frame(self.mainFrame)
        Label(textInputFrame, text=label, wraplength=130).pack(side=LEFT, anchor=W)
        text = Text(textInputFrame, height=1, width=4)
        text.pack(side=LEFT, anchor=W, padx=10)
        textInputFrame.pack(side="top", anchor="w", pady=(5, 0))
        return text

    def build(self):
        title = Label(self.mainFrame, text="Analyze")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP, pady=(0, 20))

        self.mainFrame.pack_propagate(0)
        Checkbutton(self.mainFrame, text="Object is closed", variable=self.closed).pack(
            side="top", anchor="w")

        Checkbutton(self.mainFrame, text="Object is a basic shape", variable=self.basicShape).pack(
            side="top", anchor="w")

        Checkbutton(self.mainFrame, text="Object contains arcs/curves", variable=self.curves).pack(
            side="top", anchor="w")

        
        self.timeLimit = self.buildTextInput("Time limit in minutes:")
        self.edgeCount = self.buildTextInput("Edge count(Leave empty if not obvious):")


        
        TkinterCustomButton(master=self.mainFrame, text="Show result", command=self.showResult,
                            corner_radius=60, height=25, width=140).pack(side=TOP, pady=(20, 0))

        self.mainFrame.pack(side=TOP, pady=(20, 0))

