from ctypes import pointer, string_at
from tkinter import *
from tkinter.filedialog import askopenfilename
from gui.button import TkinterCustomButton


class ScaleMenu:

    def __init__(self, master: Frame):
        self.mainFrame = Frame(master)
        self.content = Frame(self.mainFrame, width=300,
                             height=200, padx=20, pady=20)

    def build(self, side: str):
        self.content.pack_propagate(0)

        chooseFile = Label(self.content, text="Scale Points")
        chooseFile.configure(font=("Helvetica", 12, "bold"))
        chooseFile.pack(fill='both', side=TOP)

        self.content.pack(side=TOP)
        self.mainFrame.pack(side=side, pady=20, anchor=N)
