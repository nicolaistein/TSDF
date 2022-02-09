from typing import List, Mapping
import abc
import math 
import numpy as np
from patterns.gcode_cmd import GCodeCmd
from util import subtract
from logger import log

class PatternParent:
    def __init__(self, values: Mapping, workHeight:float, freeMoveHeight:float, 
                eFactor:float, fValue:float, overrunStart:float, overrunEnd:float,
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
        self.currentX = 0
        self.currentY = 0
        self.currentE = 0

        rotation = -1 * rotation * math.pi / 180
        self.rotationMatrix =   np.array(   [[math.cos(rotation), math.sin(rotation) * -1], 
                                            [math.sin(rotation), math.cos(rotation)]])
        self.reset()

    def getCmdParam(self, label: str, val: float):
        return " " + label + str(round(val, 2)) if val is not None else ""

    def reset(self):
        self.result = []
        self.commands = []

    def add(self, cmd: str):
        self.result.append(cmd)

    def getDistance(self, prevX:float=None, prevY:float=None, x:float=None, y:float=None,
      i:float=None, j:float=None, arcDegrees:int=None):
      if arcDegrees is None:
          return np.linalg.norm([x-prevX, y-prevY])
      else:
          radius = np.linalg.norm([i, j])
          return (2*math.pi*radius) * (arcDegrees/360)


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
        




        if printing and len(self.commands) != 0 and self.commands[-1].z is not None:
#            log("start overrun check1")
#            log("overrunStart: " + str(self.overrunStart))
#            log("last z: " + str(self.commands[-1].z))
#            log("workheight: " + str(self.commands[-1].z))
            if self.commands[-1].z == self.workheight and self.overrunStart != 0:
 #               log("adding start overrun")
                startVector = subtract([xRot, yRot], [previousX, previousY])
 #               log("[x, y]: " + str([xRot, yRot]))
 #               log("[previousX, previousY]: " + str([previousX, previousY]))
 #               log("startVector: " + str(startVector))
                vec = (startVector / np.linalg.norm(startVector)) * self.overrunStart
 #               log("vec: " + str(vec))
                self.result.insert(-1,"G0 X" + str(previousX-vec[0]) + " Y" + str(previousY-vec[1]) + " F250.0")
                self.result.append("G0 X" + str(previousX) + " Y" + str(previousY) + " F250.0")
                self.commands.insert(-1, GCodeCmd("G0", x=previousX-vec[0], y=previousY-vec[1], previousX=previousX, previousY=previousY))
                self.commands.append(GCodeCmd("G0", x=previousX, y=previousY, previousX=previousX-vec[0], previousY=previousY-vec[1]))
                self.commands[-2].x -= vec[0]
                self.commands[-2].y -= vec[1]
                split = self.result[-2].split(" ")
                self.result[-2] = ""
                for x in split:
                    if x.startswith("X"):
                        self.result[-2] += "X" + str(self.commands[-2].x) + " "
                    elif x.startswith("Y"):
                        self.result[-2] += "Y" + str(self.commands[-2].y) + " "
                    else:
                        self.result[-2] += x + " "
                self.result[-2] += "\n"


        if z is not None and len(self.commands) != 0:
            if z == self.freemoveHeight and self.overrunEnd != 0:
#                log("adding end overrun")
                oldCmd = self.commands[-1]
                endVector = subtract([oldCmd.previousX, oldCmd.previousY], [oldCmd.x, oldCmd.y])
                vec = (endVector / np.linalg.norm(endVector)) * self.overrunEnd
                self.add("G0 X" + str(previousX-vec[0]) + " Y" + str(previousY-vec[1]) + " F250.0")
#                log("vec: " + str(vec))
                self.commands.append(GCodeCmd("G0", x=previousX-vec[0], y=previousY-vec[1], previousX=previousX, previousY=previousY))
                xRot -= vec[0]
                yRot -= vec[1]
                previousX -= vec[0]
                previousY -= vec[1]

        cmd: str = ""
        cmd += self.getCmdParam("X", xRot)
        cmd += self.getCmdParam("Y", yRot)
        cmd += self.getCmdParam("Z", z)
        cmd += self.getCmdParam("I", i)
        cmd += self.getCmdParam("J", j)
        if printing:
            distance = self.getDistance(prevX=previousX, prevY=previousY, x=xRot, y=yRot, i=i, j=j, arcDegrees=arcDegrees)
            self.currentE -= distance * self.eFactor
            cmd += self.getCmdParam("E", self.currentE)

        if moving:
            cmd += self.getCmdParam("F", self.fValue)


        if(cmd):
            self.add(prefix + cmd)
            self.commands.append(GCodeCmd(prefix, x=xRot, y=yRot, z=z, i=i, j=j,
                arcDegrees=arcDegrees, previousX=previousX, previousY=previousY))

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
