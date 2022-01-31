from tkinter import *
from gui.button import TkinterCustomButton
from algorithms.algorithms import *
from gui.left_side_menu.file_menu import FileMenu
from gui.left_side_menu.analyze.analyze_window import AnalyzeWindow
from gui.left_side_menu.mode.computation_mode import ComputationMode
from logger import log
import igl


class AnalyzeMenu:
    mode:ComputationMode = ComputationMode.default()
    mainFrame = None

    def __init__(self, master: Frame, fileMenu:FileMenu, defaultColor:str):
        self.fileMenu = fileMenu
        self.master = master
        self.defaultColor = defaultColor
        self.closed = IntVar()
        self.basicShape = IntVar()
        self.curves = IntVar()
        
    def setMode(self, mode:ComputationMode):
        self.mode = mode
        self.refreshView()

    def refreshView(self):
        if self.mainFrame is not None:
            for el in self.mainFrame.winfo_children():
                el.destroy()
            self.mainFrame.destroy()
            self.mainFrame = None
        
        self.build()

    def showResult(self):
        if self.fileMenu.getPath():
            self.error.configure(text="")
            timeLimiText =  self.timeLimit.get("1.0", END)[:-1]
            timeLimit = int(timeLimiText) if timeLimiText else 0
            timeLimit = timeLimit
            edgeCount =  self.edgeCount.get("1.0", END)[:-1]
            closed = self.closed.get() or len(igl.boundary_loop(self.fileMenu.triangles)) == 0
            AnalyzeWindow(self.content, len(self.fileMenu.triangles), closed,
             self.basicShape.get(), self.curves.get(), timeLimit, edgeCount).openWindow()
        else:
            self.error.configure(text="You have to select a file first!")

    def buildTextInput(self, label:str, val:str = ""):
        textInputFrame = Frame(self.content)
        Label(textInputFrame, text=label, wraplength=130).pack(side=LEFT, anchor=W)
        text = Text(textInputFrame, height=1, width=4)
        text.pack(side=LEFT, anchor=W, padx=10)
        text.insert(END, val)
        textInputFrame.pack(side="top", anchor="w", pady=(5, 0))
        return text

    def build(self):
        if self.mode == ComputationMode.AUTOMATIC: return
        self.mainFrame = Frame(self.master, bg=self.defaultColor)
        self.content = Frame(
            self.mainFrame, width=260, height=260, padx=20, pady=20)
        title = Label(self.content, text="Analyze")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP, pady=(0, 15))

        self.content.pack_propagate(0)
        Checkbutton(self.content, text="Object is closed and not segmented", variable=self.closed).pack(
            side="top", anchor="w")

        Checkbutton(self.content, text="Object is a basic shape", variable=self.basicShape).pack(
            side="top", anchor="w")

        Checkbutton(self.content, text="Object contains arcs/curves", variable=self.curves).pack(
            side="top", anchor="w")

        
        self.timeLimit = self.buildTextInput("Time limit in seconds:", "30")
        self.edgeCount = self.buildTextInput("Edge count(Leave empty if not obvious):")


        
        TkinterCustomButton(master=self.content, text="Show result", command=self.showResult,
                            corner_radius=60, height=25, width=140).pack(side=TOP, pady=(10, 0))

        self.error = Label(self.content, text="", fg="red")
        self.error.pack(side="top", pady=(4, 0))

        

        self.content.pack(side=TOP, pady=(2, 0))
        self.mainFrame.pack()

