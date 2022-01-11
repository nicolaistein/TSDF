from tkinter import *
from gui.left_side_menu.computation_info import ComputationInfo
from gui.all_patterns.all_patterns import AllPatterns
from gui.left_side_menu.algorithm_menu import AlgorithmMenu
from gui.left_side_menu.algorithm_menu import AlgorithmMenu
from gui.left_side_menu.file_menu import FileMenu
from gui.placed_patterns.placed_patterns_menu import PlacedPatternsMenu
from gui.canvas.canvas_manager import CanvasManager
from gui.left_side_menu.analyze.analyze_menu import AnalyzeMenu
from gui.canvas.mesh3dplotter import Mesh3DPlotter

mainColor = "#cccccc"
root = Tk()
root.title("GCode Pattern Manager")
root.resizable(False, False)
# root.iconbitmap("Path/to/test.ico")
root.geometry("1920x940")
root.configure(bg=mainColor, padx=20, pady=20)

canvasSize = 900

leftContainer = Frame(root, bg=mainColor)
canvasManager = CanvasManager(root, canvasSize)
fileMenu = FileMenu(leftContainer)
computationInfo = ComputationInfo(leftContainer, canvasManager)

fileMenu.build()
AnalyzeMenu(leftContainer, fileMenu).build()
AlgorithmMenu(leftContainer, canvasManager, fileMenu, computationInfo).build()
computationInfo.build("top")
leftContainer.pack(side="left", anchor=N, padx=(0, 20))

canvasManager.build()
placedPatterns = PlacedPatternsMenu(root, canvasManager, mainColor)

allPatternsContainer = Frame(root, bg=mainColor)
AllPatterns(allPatternsContainer, mainColor, placedPatterns).build("top")
plotter = Mesh3DPlotter(allPatternsContainer)
plotter.build()
plotter.draw2()

allPatternsContainer.pack(side=LEFT, anchor=N)

placedPatterns.build()


root.mainloop()


#plotter.plotFile("algorithms/segmentation/plot.html")