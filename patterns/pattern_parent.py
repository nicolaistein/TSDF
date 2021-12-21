from typing import Mapping
import abc
import math 
import numpy as np


def getCmdParam(label: str, val: float):
    return " " + label + str(round(val, 2)) if val is not None else ""


class PatternParent:
    def __init__(self, values: Mapping, workHeight:float, freeMoveHeight:float, 
                startX: float, startY: float, rotation:float):
        self.values = values
        self.workHeight = workHeight
        self.freeMoveHeight = freeMoveHeight
        self.startX = startX
        self.startY = startY
        self.currentX = 0
        self.currentY = 0

        rotation = -1 * rotation * math.pi / 180
        self.rotationMatrix =   np.array(   [[math.cos(rotation), math.sin(rotation) * -1], 
                                            [math.sin(rotation), math.cos(rotation)]])
        self.result = ""

    def reset(self):
        self.result = ""

    def add(self, cmd: str):
        self.result += cmd + "\n"

    def addCmd(self, prefix: str, x=None, y=None, z=None, i=None, j=None):

        #x and y are both needed for rotation (even if one of them does not change)
        x = x if not x is None else self.currentX
        y = y if not y is None else self.currentY

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
        cmd += getCmdParam("X", xRot)
        cmd += getCmdParam("Y", yRot)
        cmd += getCmdParam("Z", z)
        cmd += getCmdParam("I", i)
        cmd += getCmdParam("J", j)
        if(cmd):
            self.add(prefix + cmd)

    #Set position in plane
    def setCurrentPosition(self, x=None, y=None):
        self.currentX = x
        self.currentY = y

    def moveTo(self, x=None, y=None, z=None):
        self.addCmd("G0", x, y, z)

    def printTo(self, x=None, y=None, z=None):
        self.addCmd("G1", x, y, z)

    def clockArc(self, x=None, y=None, i=0.0, j=0.0):
        self.addCmd("G02", x, y, i=i, j=j)

    def counterClockArc(self, x=None, y=None, i=0.0, j=0.0):
        self.addCmd("G03", x, y, i=i, j=j)

    def relativeMode(self):
        self.add("G91")

    def absoluteMode(self):
        self.add("G90")

    def rotate(self, x:float, y:float):
        result = self.rotationMatrix.dot(np.array([x, y]))
        return result[0], result[1]


    @abc.abstractmethod
    def gcode(self, startX: float, startY: float, workHeight: float):
        """Generates the gcode of the pattern"""
        return
