from functools import partial
from tkinter import *
import gui.mesh3dplotter.mesh3dplotter as plotter
from gui.button import TkinterCustomButton
from algorithms.algorithms import *
from gui.canvas.canvas_manager import CanvasManager
from gui.left_side_menu.file_menu import FileMenu
from gui.left_side_menu.computation_info import ComputationInfo
from gui.numeric_text import NumericText
from algorithms.segmentation.segmentation import folder
from gui.left_side_menu.mode.computation_mode import ComputationMode
from gui.left_side_menu.algorithm.automator import Automator
from tkinter import messagebox
from gui.menu_heading.menu_heading import MenuHeading
import gui.menu_heading.info_texts as infotexts
import igl
import os
import time
from logger import log


class AlgorithmMenu:
    """The desired parameterization algorithm can be selected in this menu"""

    points = []
    mainFrame = None
    mode = ComputationMode.default()

    algorithms = [
        ("BFF", 0),
        ("ARAP", 1),
    ]

    def __init__(
        self,
        master: Frame,
        canvasManager: CanvasManager,
        fileMenu: FileMenu,
        compInfo: ComputationInfo,
        plotter: plotter.Mesh3DPlotter,
    ):
        self.master = master
        self.canvasManager = canvasManager
        self.fileMenu = fileMenu
        self.compInfo = compInfo
        self.plotter = plotter
        plotter.refreshChartDistortionInfo = self.onChartSelect
        canvasManager.refreshChartDistortionInfo = self.onChartSelect
        self.v = IntVar()
        self.v.set(0)

    def onChartSelect(self, chart):
        self.compInfo.setDistortionValues(
            self.canvasManager.getDistortionsOfChart(chart)
        )
        self.canvasManager.enableChart(chart)

    def setMode(self, mode: ComputationMode):
        self.mode = mode
        if self.mainFrame is not None:
            for el in self.mainFrame.winfo_children():
                el.destroy()
            self.mainFrame.destroy()
            self.mainFrame = None

        self.build()

    def calculateAutomatic(self, file: str):
        computeStart = time.time()
        automator = Automator(file)
        charts, data = automator.calculate()
        computeEnd = time.time()
        for shape in data:
            _, _, _, pointsAfter, _ = shape
            if not self.areVerticesValid(pointsAfter):
                return
        self.plotter.plotAutomaticMode(automator.vertices, automator.faces, charts)
        self.canvasManager.plot(data)
        self.compInfo.updateInfo("Automatic", computeEnd - computeStart)

    def areVerticesValid(self, vertices):
        for v in vertices:
            for x in v:
                if x != 0:
                    return True

        messagebox.showerror("Parameterization", "Too many cones")
        return False

    def calculate(self):
        file = self.fileMenu.getPath()
        if not file:
            return

        if self.mode == ComputationMode.AUTOMATIC:
            self.calculateAutomatic(file)
            return

        chosen = self.v.get()
        algoName, _ = self.algorithms[chosen]
        coneCount = 0

        if chosen == 0:
            coneCount = self.bffConeInput.getNumberInput()
            algorithmFunc = partial(executeBFF, coneCount)
            algoName = "BFF with " + str(coneCount) + " cones"
        if chosen == 1:
            algorithmFunc = executeARAP

        chartList = []
        if self.fileMenu.plotter.isSegmented():
            folderName = os.getcwd() + "/" + folder
            fileList = os.listdir(folderName)
            for file in fileList:
                chartKey = int(file.split(".")[0])
                chartList.append((chartKey, folderName + "/" + file))
        else:
            chartList = [(-1, file)]

        computeStart = time.time()
        results = []
        for key, ch in chartList:

            root_folder = os.getcwd()
            log("proccessing " + ch)
            v, f = igl.read_triangle_mesh(os.path.join(root_folder, ch))
            bnd = igl.boundary_loop(f)
            if len(bnd) == 0 and not (chosen == 0 and coneCount >= 3):
                if chosen == 0:
                    messagebox.showerror(
                        "Parameterization",
                        "BFF needs at least 3 cones in order to flatten a closed mesh",
                    )
                else:
                    messagebox.showerror(
                        "Parameterization", algoName + " cannot flatten a closed mesh"
                    )
                continue
            elif coneCount > len(v):
                messagebox.showerror(
                    "Parameterization",
                    "The number of cones for BFF must be lower or equal to the number of vertices of the mesh",
                )
                continue

            res = algorithmFunc(ch)
            results.append((key,) + res)
            log("file: " + file)
        computeEnd = time.time()

        for shape in results:
            _, _, _, pointsAfter, _ = shape
            if not self.areVerticesValid(pointsAfter):
                return

        if len(results) > 0:
            self.canvasManager.plot(results)
            self.compInfo.updateInfo(algoName, computeEnd - computeStart)

    def build(self):
        """Renders the corresponding widget"""
        height = 200 if self.mode == ComputationMode.MANUAL else 110
        self.mainFrame = Frame(self.master, width=260, height=height, padx=20, pady=20)
        MenuHeading("Flatten", infotexts.flatten).build(self.mainFrame)

        self.mainFrame.pack_propagate(0)

        if self.mode == ComputationMode.MANUAL:
            self.assembleAlgoChooserFrame()
        buttonPady = 10 if self.mode == ComputationMode.MANUAL else 0
        TkinterCustomButton(
            master=self.mainFrame,
            text="Calculate",
            command=self.calculate,
            corner_radius=60,
            height=25,
            width=140,
        ).pack(side=TOP, pady=(buttonPady, 0))
        self.mainFrame.pack(side=TOP, pady=(2, 0))

    def assembleAlgoChooserFrame(self):
        """Renders the Radiobutton frame where the algorithm can be selected"""
        selectAlgoFrame = Frame(self.mainFrame)

        for txt, val in self.algorithms:
            optionFrame = Frame(selectAlgoFrame)
            Radiobutton(
                optionFrame,
                text=txt,
                height=1,
                wrap=None,
                variable=self.v,
                value=val,
            ).pack(anchor=W, side=LEFT)

            # Needed because BFF is the only algorithm that takes other parameters as input
            if txt == "BFF":
                Label(optionFrame, text="with").pack(side=LEFT, anchor=W)
                self.bffConeInput = NumericText(
                    optionFrame, width=3, initialText="10", floatingPoint=False
                )
                self.bffConeInput.build().pack(side=LEFT, anchor=W, padx=10)
                Label(optionFrame, text="cones").pack(side=LEFT, anchor=W)
            optionFrame.pack(side=TOP, anchor=W)

        selectAlgoFrame.pack(side=TOP, anchor=W)
