from tkinter import *
from gui.left_side_menu.computation_info import ComputationInfo
from gui.all_patterns import AllPatterns
from gui.left_side_menu.algorithm_menu import AlgorithmMenu
from gui.left_side_menu.algorithm_menu import AlgorithmMenu
from gui.left_side_menu.file_menu import FileMenu
from gui.placed_patterns.placed_patterns_menu import PlacedPatternsMenu
from gui.canvas.canvas_manager import CanvasManager
from gui.left_side_menu.analyze.analyze_menu import AnalyzeMenu

mainColor = "#cccccc"
root = Tk()
root.title("GCode Pattern Manager")
root.resizable(False, False)
# root.iconbitmap("Path/to/test.ico")
root.geometry("1920x940")
root.configure(bg=mainColor, padx=20, pady=20)

canvasSize = 900

leftContainer = Frame(root, bg=mainColor)
leftSubContainer = Frame(leftContainer, bg=mainColor)

canvasManager = CanvasManager(root, canvasSize)
fileMenu = FileMenu(leftSubContainer)
computationInfo = ComputationInfo(leftSubContainer)
fileMenu.build()
AnalyzeMenu(leftSubContainer, fileMenu).build()
AlgorithmMenu(leftSubContainer, canvasManager, fileMenu, computationInfo).build()
leftSubContainer.pack(side="top", anchor=N, padx=(0, 20))

computationInfo.build("top")
leftContainer.pack(side="left", anchor=N)
canvasManager.build()
placedPatterns = PlacedPatternsMenu(root, canvasManager, mainColor)
patternList = AllPatterns(root, mainColor, placedPatterns)
patternList.build("left")
placedPatterns.build()


root.mainloop()
