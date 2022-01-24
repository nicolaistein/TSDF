from enum import Enum
from typing import List
from logger import log
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

     def getDistortion(self, verticesBefore:List[List[float]], facesBefore:List[List[int]],
        verticesAfter:List[List[float]], facesAfter:List[List[int]]):
          if self == PlottingOption.LSCM:
               log("distortion is LSCM")
               return LscmDistortion(verticesBefore, facesBefore, verticesAfter, facesAfter)