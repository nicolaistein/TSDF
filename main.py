from tkinter import *
from gui.left_side_menu.computation_info import ComputationInfo
from gui.all_patterns.all_patterns import AllPatterns
from gui.left_side_menu.algorithm.algorithm_menu import AlgorithmMenu
from gui.left_side_menu.measuring_tool import MeasuringTool
from gui.left_side_menu.file_menu import FileMenu
from gui.placed_patterns.placed_patterns_menu import PlacedPatternsMenu
from gui.canvas.canvas_manager import CanvasManager
from gui.left_side_menu.analyze.analyze_menu import AnalyzeMenu
from gui.mesh3dplotter.mesh3dplotter import Mesh3DPlotter
from gui.left_side_menu.mode.mode_menu import ModeMenu
from gui.left_side_menu.export_menu import ExportMenu
from gui.listview import ListView

mainColor = "#cccccc"
root = Tk()
root.title("Tactile Sensing Development Framework")
root.iconbitmap("image.ico")
root.geometry("1920x900")
root.configure(bg=mainColor)
canvasSize = 900

allPatternsContainer = Frame(root, bg=mainColor)
leftContainerParent = Frame(root)
leftContainer = ListView(leftContainerParent, 255, 900, 0, mainColor).build()

plotter = Mesh3DPlotter(allPatternsContainer)
canvasManager = CanvasManager(root, canvasSize, plotter)
computationInfo = ComputationInfo(leftContainer, canvasManager)
measuringTool = MeasuringTool(leftContainer, canvasManager)
fileMenu = FileMenu(leftContainer, plotter, mainColor)
exportMenu = ExportMenu(leftContainer, canvasManager, fileMenu)
analyzeMenu = AnalyzeMenu(leftContainer, fileMenu, mainColor)
algorithmMenu = AlgorithmMenu(
    leftContainer, canvasManager, fileMenu, computationInfo, plotter
)
modeMenu = ModeMenu(
    leftContainer,
    analyzeMenu,
    algorithmMenu,
    computationInfo,
    measuringTool,
    exportMenu,
)
placedPatterns = PlacedPatternsMenu(root, canvasManager, mainColor)
allPatterns = AllPatterns(
    allPatternsContainer, mainColor, placedPatterns, canvasManager
)

fileMenu.build()
modeMenu.build()
analyzeMenu.build()
algorithmMenu.build()
computationInfo.build()
measuringTool.build()
exportMenu.build()
leftContainerParent.pack(side=LEFT, anchor=N, padx=(0, 20))
canvasManager.build()
allPatterns.build()
plotter.show()
allPatternsContainer.pack(side=LEFT, anchor=N, padx=(20, 0))
placedPatterns.build()


root.mainloop()
