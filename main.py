from tkinter import *
from typing import List
from gui.left_side_menu.computation_info import ComputationInfo
from gui.all_patterns.all_patterns import AllPatterns
from gui.left_side_menu.algorithm_menu import AlgorithmMenu
from gui.left_side_menu.algorithm_menu import AlgorithmMenu
from gui.left_side_menu.file_menu import FileMenu
from gui.placed_patterns.placed_patterns_menu import PlacedPatternsMenu
from gui.canvas.canvas_manager import CanvasManager
from gui.left_side_menu.analyze.analyze_menu import AnalyzeMenu
from gui.mesh3dplotter.mesh3dplotter import Mesh3DPlotter
from gui.listview import getListview
import numpy as np

mainColor = "#cccccc"
root = Tk()
root.title("GCode Pattern Manager")
root.resizable(False, False)
# root.iconbitmap("Path/to/test.ico")
root.geometry("1920x940")
root.configure(bg=mainColor, padx=20, pady=20)

canvasSize = 900

allPatternsContainer = Frame(root, bg=mainColor)
plotter = Mesh3DPlotter(allPatternsContainer)

leftContainerParent = Frame(root, bg=mainColor)
leftContainer = getListview(leftContainerParent, 220, 900, 0, mainColor)
canvasManager = CanvasManager(root, canvasSize, plotter)
fileMenu = FileMenu(leftContainer, plotter)
computationInfo = ComputationInfo(leftContainer, canvasManager)

fileMenu.build()
AnalyzeMenu(leftContainer, fileMenu).build()
AlgorithmMenu(leftContainer, canvasManager, fileMenu, computationInfo).build()
computationInfo.build()
leftContainerParent.pack(side="left", anchor=N, padx=(0, 20))



canvasManager.build()
placedPatterns = PlacedPatternsMenu(root, canvasManager, mainColor)

AllPatterns(allPatternsContainer, mainColor, placedPatterns, canvasManager).build("top")
plotter.show()

allPatternsContainer.pack(side=LEFT, anchor=N, padx=(20,0))

placedPatterns.build()




#plotter.plotFile("algorithms/segmentation/plot.html")

#p1 = [2,3,1]
#p2 = [8,2,2]
#p3 = [1,4,2]
#res = [66,4,3]
#A = np.array([p1, p2, p3])
#B = np.array(res)
#print("A: " + str(A))
#print("B: " + str(B))
#try:
#    result = np.linalg.solve(A, B)
#    print("result: " + str(result))
#except np.linalg.LinAlgError:
#    print("Linalg ERROR!")
#            log("result: " + str([[1,0], [0,1]]))



root.mainloop()