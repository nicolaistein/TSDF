from tkinter import *
from gui.button import TkinterCustomButton
from algorithms.algorithms import *
from gui.left_side_menu.analyze.analyze_menu import AnalyzeMenu
from gui.left_side_menu.algorithm.algorithm_menu import AlgorithmMenu
from gui.left_side_menu.computation_info import ComputationInfo
from gui.left_side_menu.mode.computation_mode import ComputationMode
from gui.left_side_menu.measuring_tool import MeasuringTool
from gui.left_side_menu.export_menu import ExportMenu
from gui.menu_heading.menu_heading import MenuHeading
import gui.menu_heading.info_texts as infotexts
from logger import log


class ModeMenu:

    currentMode: ComputationMode = ComputationMode.default()
    button: TkinterCustomButton = None

    def __init__(
        self,
        master: Frame,
        analyzeMenu: AnalyzeMenu,
        algoMenu: AlgorithmMenu,
        compInfo: ComputationInfo,
        measuringTool: MeasuringTool,
        exportMenu: ExportMenu,
    ):
        self.mainFrame = Frame(master, width=260, height=110, padx=20, pady=20)
        self.analyzeMenu = analyzeMenu
        self.algoMenu = algoMenu
        self.measuringTool = measuringTool
        self.compInfo = compInfo
        self.exportMenu = exportMenu

    def changeMode(self):
        self.currentMode = self.currentMode.getOpposite()
        self.refreshButton()
        self.analyzeMenu.setMode(self.currentMode)
        self.algoMenu.setMode(self.currentMode)
        self.compInfo.refreshView()
        self.measuringTool.refreshView()
        self.exportMenu.refreshView()

    def refreshButton(self):
        for el in self.buttonFrame.winfo_children():
            el.destroy()
        text = (
            "Automatic Mode"
            if not self.currentMode == ComputationMode.AUTOMATIC
            else "Manual Mode"
        )
        if self.button is not None:
            self.button.delete()
        self.button = TkinterCustomButton(
            master=self.buttonFrame,
            text=text,
            command=self.changeMode,
            corner_radius=60,
            height=25,
            width=160,
        )
        self.button.pack(side=TOP)

    def build(self):
        MenuHeading("Select Mode", infotexts.selectMode).build(self.mainFrame)

        self.mainFrame.pack_propagate(0)

        self.buttonFrame = Frame(self.mainFrame)
        self.refreshButton()
        self.buttonFrame.pack(side=TOP)

        self.mainFrame.pack(side=TOP, pady=(2, 0))
