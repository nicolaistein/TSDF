from tkinter import *
from tkinter.filedialog import askdirectory
from gui.scale_menu import ScaleMenu
from gui.gcode_menu import GCodeMenu
from gui.algorithm_menu import AlgorithmMenu
from gui.algorithm_menu import AlgorithmMenu
from gui.file_menu import FileMenu
from gui.pattern_list.placed_patterns_menu import PlacedPatternsMenu
from gui.plotting.canvas_manager import CanvasManager

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
fileMenu.build()
AlgorithmMenu(leftContainer, canvasManager, fileMenu).build()
ScaleMenu(leftContainer, canvasManager, canvasSize).build("top")

leftContainer.pack(side="left", padx=(0, 20), anchor=N)
canvasManager.build()
placedPatterns = PlacedPatternsMenu(root, canvasManager, mainColor)
patternList = GCodeMenu(root, mainColor, placedPatterns)
patternList.build("left")
placedPatterns.build()


root.mainloop()
