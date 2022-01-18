from tkinter import *
from gui.button import TkinterCustomButton
from algorithms.algorithms import *
from gui.canvas.canvas_manager import CanvasManager
from gui.left_side_menu.file_menu import FileMenu
from gui.left_side_menu.computation_info import ComputationInfo
import gui.canvas.area_distortion as AreaDistortion
import gui.canvas.angular_distortion as AngularDistortion
from logger import log


class AlgorithmMenu:

    points = []

    algorithms = [
        ("BFF", 0),
        ("LSCM", 1),
        ("ARAP", 2),
    ]

    def __init__(self, master: Frame, canvasManager: CanvasManager,
     fileMenu:FileMenu, compInfo:ComputationInfo):
        self.mainFrame = Frame(master, width=220, height=200, padx=20, pady=20)
        self.canvasManager = canvasManager
        self.fileMenu = fileMenu
        self.compInfo = compInfo
        self.v = IntVar()
        self.v.set(0)

    def calculate(self):
        file = self.fileMenu.getPath()
        if not file:
            return

        chosen = self.v.get()
        algo, id = self.algorithms[chosen]

        if(chosen == 0):
            coneCount = int(self.bffConeInput.get("1.0", END)[:-1])
            time, points, pointsBefore, faces, facesBefore = executeBFF(file, coneCount)
            algo = "BFF with " + str(coneCount) + " cones"
        if(chosen == 1):
            time, points, pointsBefore, faces, facesBefore = executeLSCM(file)
        if(chosen == 2):
            time, points, pointsBefore, faces, facesBefore = executeARAP(file)

        log("time: " + str(time) + ", points: " + str(len(points)))
        areaDistortions, avgAreaDistortion = AreaDistortion.compute(pointsBefore, points, facesBefore, faces)
        angularDistortions, avgAngularDistortion = AngularDistortion.compute(pointsBefore, points, facesBefore, faces, isBFF=chosen==0)

        self.canvasManager.plot(points, faces, areaDistortions, angularDistortions)
        self.compInfo.updateInfo(algo, time, avgAreaDistortion, avgAngularDistortion)


    def build(self):

        title = Label(self.mainFrame, text="Flatten")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP, pady=(0, 20))

        self.mainFrame.pack_propagate(0)
        self.assembleAlgoChooserFrame()

        TkinterCustomButton(master=self.mainFrame, text="Calculate", command=self.calculate,
                            corner_radius=60, height=25, width=140).pack(side=TOP, pady=(10, 0))

        self.mainFrame.pack(side=TOP, pady=(20, 0))

    def ShowChoice(self):
        pass

    def cancelInput(self, event):
        return "break"

    def allowInput(self, event):
        pass

    def onKeyPress(self, event):
        if not event.char in "1234567890":
            return "break"

    def assembleAlgoChooserFrame(self):
        selectAlgoFrame = Frame(self.mainFrame)

        for txt, val in self.algorithms:
            optionFrame = Frame(selectAlgoFrame)
            Radiobutton(optionFrame,
                        text=txt,
                        height=1,
                        wrap=None,
                        variable=self.v,
                        command=self.ShowChoice,
                        value=val).pack(anchor=W, side=LEFT)

            if(txt == "BFF"):
                Label(optionFrame, text="with").pack(side=LEFT, anchor=W)
                self.bffConeInput = Text(optionFrame, height=1, width=3)
                self.bffConeInput.bind('<Return>', self.cancelInput)
                self.bffConeInput.bind('<Tab>', self.cancelInput)
                self.bffConeInput.bind('<BackSpace>', self.allowInput)
                self.bffConeInput.bind('<KeyPress>', self.onKeyPress)
                self.bffConeInput.insert(END, "10")
                self.bffConeInput.pack(side=LEFT, anchor=W, padx=10)
                Label(optionFrame, text="cones").pack(side=LEFT, anchor=W)
            optionFrame.pack(side=TOP, anchor=W)

        selectAlgoFrame.pack(side=TOP, anchor=W)
