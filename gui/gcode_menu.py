from ctypes import pointer, string_at
from tkinter import *
from tkinter.filedialog import askopenfilename
from gui.button import TkinterCustomButton


class GCodeMenu:
    file = "[filename]"

    points = []

    def __init__(self, master: Frame):
        self.mainFrame = Frame(master, width=400, bg="#cccccc")
        self.content = Frame(self.mainFrame, width=400, height=730, padx=20, pady=20)


    def build(self, side: str):
        self.content.pack_propagate(0)
        
        chooseFile = Label(self.content, text="All Patterns")
        chooseFile.configure(font=("Helvetica", 12, "bold"))
        chooseFile.pack(fill='both', side=TOP)

        
        self.content.pack(side=TOP)
        TkinterCustomButton(master=self.mainFrame, text="Generate GCode",
                            corner_radius=60, height=25, width=160).pack(side=TOP, pady=20)

        self.mainFrame.pack(side=side, padx=20, anchor=N)
