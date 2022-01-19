from typing import Mapping
import abc
import math 
import numpy as np
from patterns.gcode_cmd import GCodeCmd


class PatternParent:
    def __init__(self, values: Mapping, workHeight:float, freeMoveHeight:float, 
                startX: float, startY: float, rotation:float):
        self.values = values
        self.workheight = workHeight
        self.freemoveHeight = freeMoveHeight
        self.startX = startX
        self.startY = startY
        self.currentX = 0
        self.currentY = 0

        rotation = -1 * rotation * math.pi / 180
        self.rotationMatrix =   np.array(   [[math.cos(rotation), math.sin(rotation) * -1], 
                                            [math.sin(rotation), math.cos(rotation)]])
        self.reset()

    def getCmdParam(self, label: str, val: float):
        return " " + label + str(round(val, 2)) if val is not None else ""

    def reset(self):
        self.result = ""
        self.commands = []

    def add(self, cmd: str):
        self.result += cmd + "\n"

    def addCmd(self, prefix: str, x:float=None, y:float=None, z:float=None,
     i:float=None, j:float=None, arcDegrees:int=None):

        #x and y are both needed for rotation (even if one of them does not change)
        x = x if not x is None else self.currentX
        y = y if not y is None else self.currentY

        #Save current location
        previousX, previousY = self.rotate(self.currentX, self.currentY)
        previousX += self.startX
        previousY += self.startY

        # Refresh current x and y as if translation and rotation were 0
        self.currentX = x
        self.currentY = y

        # Rotate x and y
        xRot, yRot = self.rotate(x, y)
        xRot += self.startX
        yRot += self.startY
        
        #Rotate i and j (relative offset of the circle center)
        if i is not None and j is not None:
            iAbs = x + i
            jAbs = y + j

            iAbsNew, jAbsNew = self.rotate(iAbs, jAbs)

            iAbsNew += self.startX
            jAbsNew += self.startY

            i = iAbsNew - xRot
            j = jAbsNew - yRot

        cmd: str = ""
        cmd += self.getCmdParam("X", xRot)
        cmd += self.getCmdParam("Y", yRot)
        cmd += self.getCmdParam("Z", z)
        cmd += self.getCmdParam("I", i)
        cmd += self.getCmdParam("J", j)
        if(cmd):
            self.add(prefix + cmd)
            self.commands.append(GCodeCmd(prefix, x=xRot, y=yRot, z=z, i=i, j=j,
                arcDegrees=arcDegrees, previousX=previousX, previousY=previousY))

    #Set position in plane
    def setCurrentPosition(self, x=None, y=None):
        self.currentX = x
        self.currentY = y

    def moveTo(self, x=None, y=None, z=None):
        self.addCmd("G0", x, y, z)

    def printTo(self, x=None, y=None, z=None):
        self.addCmd("G1", x, y, z)

    def clockArc(self, x=None, y=None, i=0.0, j=0.0, arcDegrees=180):
        self.addCmd("G02", x, y, i=i, j=j, arcDegrees=arcDegrees)

    def counterClockArc(self, x=None, y=None, i=0.0, j=0.0, arcDegrees=180):
        self.addCmd("G03", x, y, i=i, j=j, arcDegrees=arcDegrees)

    def relativeMode(self):
        self.add("G91")

    def absoluteMode(self):
        self.add("G90")

    def workHeight(self):
        self.moveTo(z=self.workheight)

    def freeMoveHeight(self):
        self.moveTo(z=self.freemoveHeight)

    def rotate(self, x:float, y:float):
        result = self.rotationMatrix.dot(np.array([x, y]))
        return result[0], result[1]


    @abc.abstractmethod
    def gcode(self, startX: float, startY: float, workHeight: float):
        """Generates the gcode of the pattern"""
        return
