from enum import Enum
from typing import List
from logger import log
from tkinter import *
from gui.canvas.distortions.lscm_distortion import LscmDistortion

class PlottingOption(Enum):
     NO_DIST = 0
     COLORS = 1
     LSCM = 2

     def toString(self):
          switcher = {
               0: "Default",
               1: "Face Colors",
               2: "LSCM Distortion",
          }
          return switcher[self.value]

     def getOptionCalculator(self, verticesBefore:List[List[float]], facesBefore:List[List[int]],
        verticesAfter:List[List[float]], facesAfter:List[List[int]]):
          if self == PlottingOption.LSCM:
               log("distortion is LSCM")
               return LscmDistortion(verticesBefore, facesBefore, verticesAfter, facesAfter)

     def getMinMax(self):
          switcher = {
               0: (-1, -1),
               1: (-1, -1),
               2: (1, 2),
          }
          return switcher[self.value]
     
     def getColormap(self, canvas:Canvas, width:int, height:int):
          width = canvas.winfo_width()
          height = canvas.winfo_height()
          width = 100
          height = 5
#          log("width: " + str(width) + ", height: " + str(height))

          if self == PlottingOption.LSCM:
               stepSize = 255/width

               for x in range(width):
                    for y in range(height):
                         
                         colorFac = int(round(stepSize*x, 0))
               #          log("colorFac: " + str(colorFac))
                         color = '#%02x%02x%02x' % (255, 255-colorFac, 255-colorFac)

                         canvas.create_oval(x, y, x, y, fill=color, width=0)

