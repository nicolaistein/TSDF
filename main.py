from tkinter import *
from tkinter.filedialog import askdirectory
from gui.left_side_menu.scale_menu import ScaleMenu
from gui.all_patterns import AllPatterns
from gui.left_side_menu.algorithm_menu import AlgorithmMenu
from gui.left_side_menu.algorithm_menu import AlgorithmMenu
from gui.left_side_menu.file_menu import FileMenu
from gui.placed_patterns.placed_patterns_menu import PlacedPatternsMenu
from gui.canvas.canvas_manager import CanvasManager

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
patternList = AllPatterns(root, mainColor, placedPatterns)
patternList.build("left")
placedPatterns.build()


root.mainloop()
