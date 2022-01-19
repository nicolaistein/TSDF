from tkinter import *
import gui.time_formatter as formatter
from gui.button import TkinterCustomButton
from gui.canvas.canvas_manager import CanvasManager
from gui.canvas.distortion import Distortion


class ComputationInfo:

    def __init__(self, master: Frame, canvasManager:CanvasManager):
        self.canvasManager = canvasManager
        self.mainFrame = Frame(master)
        self.content = Frame(self.mainFrame, width=220,
                             height=200, padx=20, pady=20)

    def updateInfo(self, algo:str, time:int, areaDist:float, angleDist:float):
        self.algorithm.configure(text=algo)
        self.time.configure(text=formatter.formatTime(time))
        self.areaDist.configure(text=str(round(areaDist, 2)))
        self.angleDist.configure(text=str(round(angleDist, 2)))

    
    def getKeyValueFrame(self, parent: Frame, key: str, keyWidth:float=14):
        keyValFrame = Frame(parent)
        keyLabel = Label(keyValFrame, text=key, width=keyWidth,
                            anchor=W, justify=LEFT, wraplength=120)
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        valLabel = Label(keyValFrame, text="-", wraplength=100)
        valLabel.pack(side=LEFT)

        keyValFrame.pack(side="top", anchor="w")
        return valLabel

    def showAreaDistortion(self):
        self.canvasManager.onDistortionPress(Distortion.AREA)
        
    def showAngleDistortion(self):
        self.canvasManager.onDistortionPress(Distortion.ANGLE)


    def build(self, side: str):
        self.content.pack_propagate(0)

        chooseFile = Label(self.content, text="Computation Info")
        chooseFile.configure(font=("Helvetica", 12, "bold"))

        self.algorithm = self.getKeyValueFrame(self.content, "Algorithm", 10)
        self.time = self.getKeyValueFrame(self.content, "Time", 10)
        self.areaDist = self.getKeyValueFrame(self.content, "Area Distortion")
        self.angleDist = self.getKeyValueFrame(self.content, "Angle Distortion")

        buttons = Frame(self.content)
        TkinterCustomButton(master=buttons, text="Area Dist.",
                        command=self.showAreaDistortion,
                        corner_radius=60, height=25, width=95).pack(side=LEFT)
        
        TkinterCustomButton(master=buttons, text="Faces", command=self.canvasManager.onFaces,
                        corner_radius=60, height=25, width=70).pack(side=LEFT, padx=(10,0))
                        
                        
        
        buttons.pack(side=TOP, anchor=W, pady=(10,0))

        TkinterCustomButton(master=self.content, text="Angle Dist.",
                        command=self.showAngleDistortion,
                        corner_radius=60, height=25, width=95).pack(side=LEFT, pady=(10,0))

        self.content.pack(side=LEFT)
        self.mainFrame.pack(side=side, pady=(20, 0), anchor=N)
