from typing import List, Mapping
import abc
import math 
import numpy as np
from patterns.gcode_cmd import GCodeCmd
from util import subtract
from logger import log

class PatternParent:
    def __init__(self, values: Mapping, workHeight:float, freeMoveHeight:float, 
                eFactor:float, eFactorStart:float, fValue:float, overrunStart:float, overrunEnd:float,
                printOverrun:float, 
                startX: float, startY: float, rotation:float):
        self.values = values
        self.workheight = workHeight
        self.freemoveHeight = freeMoveHeight
        self.eFactor = eFactor
        self.fValue = fValue
        self.startX = startX
        self.startY = startY
        self.overrunStart = overrunStart
        self.overrunEnd = overrunEnd
        self.printOverrun = printOverrun
        self.currentX = 0
        self.currentY = 0
        self.currentE = eFactorStart

        rotation = -1 * rotation * math.pi / 180
        self.rotationMatrix =   np.array(   [[math.cos(rotation), math.sin(rotation) * -1], 
                                            [math.sin(rotation), math.cos(rotation)]])
        self.reset()

    def getCmdParam(self, label: str, val: float):
        return " " + label + str(round(val, 2)) if val is not None else ""

    def getResult(self):
        res = ""
        for cmd in self.commands:
            cmdString, e = cmd.toGCode(self.eFactor, self.currentE, self.fValue)
            res += cmdString + "\n"
            self.currentE = e

        return res

    def reset(self):
        self.result = []
        self.commands = []


    def addCmd(self, prefix: str, x:float=None, y:float=None, z:float=None,
     i:float=None, j:float=None, arcDegrees:int=None, printing:bool=False, moving:bool=False):

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


        #Overrun start
        if printing and len(self.commands) != 0 and self.commands[-1].z is not None:
            if self.commands[-1].z == self.workheight and self.overrunStart != 0:
                startVector = subtract([xRot, yRot], [previousX, previousY])
                norm = np.linalg.norm(startVector)
                if norm != 0:
                    vec = (startVector / norm)

                    back = vec * (self.overrunStart + self.printOverrun)
                    forward1 = vec * self.printOverrun
                    
                    self.commands.insert(-1, GCodeCmd("G0", x=previousX-back[0], y=previousY-back[1],
                    previousX=previousX, previousY=previousY, isOverrun=False, moving=True))

                    self.commands.append(GCodeCmd("G0", x=previousX-forward1[0], y=previousY-forward1[1], previousX=previousX-back[0],
                    previousY=previousY-back[1], isOverrun=True, moving=True))

                    self.commands.append(GCodeCmd("G1", x=previousX, y=previousY, previousX=previousX-forward1[0],
                    previousY=previousY-forward1[1], isOverrun=True, moving=True, printing=True))

                    self.commands[-3].x -= back[0]
                    self.commands[-3].y -= back[1]
                    del self.commands[-5]
                    

        #Overrun end
        if z is not None and len(self.commands) != 0:
            if z == self.freemoveHeight and self.overrunEnd != 0:
                oldCmd = self.commands[-1]
                endVector = subtract([oldCmd.previousX, oldCmd.previousY], [oldCmd.x, oldCmd.y])
                norm = np.linalg.norm(endVector)
                if norm != 0:
                    vec = (endVector / norm) * self.overrunEnd
                    self.commands.append(GCodeCmd("G0", x=previousX-vec[0], y=previousY-vec[1], previousX=previousX, previousY=previousY, isOverrun=True))
                    xRot -= vec[0]
                    yRot -= vec[1]
                    previousX -= vec[0]
                    previousY -= vec[1]

        self.commands.append(GCodeCmd(prefix, x=xRot, y=yRot, z=z, i=i, j=j,
            arcDegrees=arcDegrees, previousX=previousX, previousY=previousY,
              printing=printing, moving=moving))

    #Set position in plane
    def setCurrentPosition(self, x=None, y=None):
        self.currentX = x
        self.currentY = y

    def moveTo(self, x=None, y=None, z=None):
        self.addCmd("G0", x, y, z, moving=True)

    def printTo(self, x=None, y=None, z=None):
        self.addCmd("G1", x, y, z, printing=True, moving=True)

    def clockArc(self, x=None, y=None, i=0.0, j=0.0, arcDegrees=180):
        self.addCmd("G02", x, y, i=i, j=j, arcDegrees=arcDegrees, printing=True, moving=True)

    def counterClockArc(self, x=None, y=None, i=0.0, j=0.0, arcDegrees=180):
        self.addCmd("G03", x, y, i=i, j=j, arcDegrees=arcDegrees, printing=True, moving=True)

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
