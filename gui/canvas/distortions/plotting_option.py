from enum import Enum
from typing import List
from logger import log
from tkinter import *
from gui.canvas.distortions.lscm_calculator import LscmCalculator
from gui.canvas.distortions.default_calculator import DefaultCalculator
from gui.canvas.distortions.face_colors_calculator import FaceColorsCalculator
from gui.canvas.distortions.arap_calculator import ArapCalculator
from gui.canvas.distortions.maximal_isometric_calculator import MaximalIsometricCalculator

class PlottingOption(Enum):
     NO_DIST = 0
     COLORS = 1
     LSCM = 2
     ARAP = 3
     MAX_ISOMETRIC = 4

     def toString(self):
          switcher = {
               0: "Default",
               1: "Chart Colors",
               2: "LSCM Distortion",
               3: "Isometric Dist.",
               4: "Max. isom. Dist."
          }
          return switcher[self.value]

     def getOptionCalculator(self, verticesBefore:List[List[float]], facesBefore:List[List[int]],
        verticesAfter:List[List[float]], facesAfter:List[List[int]], color):

          switcher = {
               0: DefaultCalculator,
               1: FaceColorsCalculator,
               2: LscmCalculator,
               3: ArapCalculator,
               4: MaximalIsometricCalculator
          }

          calculator = switcher[self.value]
          log("calculator: " + str(calculator))

          return calculator(verticesBefore, facesBefore, verticesAfter, facesAfter, self, color)

     def getMinMax(self):
          switcher = {
               0: (None, None),
               1: (None, None),
               2: (0, 1),
               3: (0, 2),
               4: (1, 4)
          }
          return switcher[self.value]

     def getColor(self):
          switcher = {
               0: None,
               1: None,
               2: (255, 0, 0),
               3: (0, 0, 255),
               4: (255, 105, 36)
          }
          return switcher[self.value]
     

     def getColormap(self, canvas:Canvas, width:int, height:int):
          optionColor= self.getColor()
          if type(optionColor) is not tuple: return

          r, g, b = optionColor

          stepSizeR = (255-r)/width
          stepSizeG = (255-g)/width
          stepSizeB = (255-b)/width

          for x in range(width):
               for y in range(height):
                    
                    colorFacR = int(round(stepSizeR*x, 0))
                    colorFacG = int(round(stepSizeG*x, 0))
                    colorFacB = int(round(stepSizeB*x, 0))
                    

                    color = '#%02x%02x%02x' % (255-colorFacR, 255-colorFacG, 255-colorFacB)

                    canvas.create_oval(x, y, x, y, fill=color, width=0)
