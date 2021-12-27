from tkinter import *
import gui.time_formatter as formatter


class ComputationInfo:

    def __init__(self, master: Frame):
        self.mainFrame = Frame(master)
        self.content = Frame(self.mainFrame, width=220,
                             height=150, padx=20, pady=20)

    def updateInfo(self, algo:str, time:int):
        self.algorithm.configure(text=algo)
        self.time.configure(text=formatter.formatTime(time))
    
    def getKeyValueFrame(self, parent: Frame, key: str):
        keyValFrame = Frame(parent)
        keyLabel = Label(keyValFrame, text=key, width=9,
                            anchor=W, justify=LEFT, wraplength=70)
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        valLabel = Label(keyValFrame, text="-", wraplength=100)
        valLabel.pack(side=LEFT)

        keyValFrame.pack(side="top", anchor="w")
        return valLabel


    def build(self, side: str):
        self.content.pack_propagate(0)

        chooseFile = Label(self.content, text="Computation Info")
        chooseFile.configure(font=("Helvetica", 12, "bold"))
        chooseFile.pack(side="top", pady=(0, 20))

        self.algorithm = self.getKeyValueFrame(self.content, "Algorithm")
        self.time = self.getKeyValueFrame(self.content, "Time")

        self.content.pack(side=TOP)
        self.mainFrame.pack(side=side, pady=(20, 0), anchor=N)
