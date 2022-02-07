from util import subtract, angle_between
import numpy as np
import math
from logger import log

class GCodeCmd:
    arcLines:int = 5

    def __init__(self, prefix:str, x:float, y:float,
         z:float=None, i:float=None, j:float=None, e:float=None, f:float=None,
          arcDegrees:int=None, previousX:float=0.0, previousY=0.0):
        self.prefix = prefix
        self.x = x
        self.y = y
        self.z = z
        self.i = i
        self.j = j
        self.e = e
        self.f = f
        self.arcDegrees = arcDegrees
        self.previousX = previousX
        self.previousY = previousY

    def toPoints(self):
        log("toPoints prevX: " + str(self.previousX) + ", prevY: " + str(self.previousY) + ", x: " + str(self.x) + ", y: " + str(self.y))
        """Returns a list of lines represented with starting and ending points"""
        if self.prefix == "G1": 
            if self.previousX != self.x and self.previousY != self.y:
                log(self.prefix + ": " + str([[self.previousX, self.previousY], [self.x, self.y]]))
                return [[self.previousX, self.previousY], [self.x, self.y]]

        if self.prefix == "G02" or self.prefix == "G03":
            points = [[self.previousX, self.previousY]]

            xr = self.previousX + self.i
            yr = self.previousY + self.j

            v1 = subtract([self.previousX, self.previousY], [xr, yr])
            del v1[-1]
            v2 = subtract([self.x, self.y], [xr, yr])
            del v2[-1]
            angle = angle_between(v1, v2)/self.arcLines
            if math.isnan(angle): return []
            if self.prefix == "G02": angle *= -1

            for counter in range(self.arcLines+1):
                rotation = angle * (counter)
                rotationMatrix =   np.array([[math.cos(rotation), math.sin(rotation) * -1], 
                                            [math.sin(rotation), math.cos(rotation)]])
                result = rotationMatrix.dot(np.array(v1))

                xNew = xr + result[0]
                yNew = yr + result[1]
                points.append([xNew, yNew])

            log(self.prefix + ": " + str(points))
            return points

        return []

    def print(self):
        print("GCodeCMD " + self.prefix + ": x=" + str(self.x) + "  y=" + str(self.y)
        + "  prevX=" + str(self.previousX) + "  prevY=" + str(self.previousY))
