from typing import List, Mapping
import abc
import math
import numpy as np
from patterns.gcode_cmd import GCodeCmd
from util import subtract
from logger import log

class PatternParent:
    def __init__(
        self,
        values: Mapping,
        workHeight: float,
        freeMoveHeight: float,
        eFactor: float,
        eFactorStart: float,
        fValueLine: float,
        fValueArc: float,
        overrunStart: float,
        overrunEnd: float,
        printOverrun: float,
        startX: float,
        startY: float,
        rotation: float,
        pause: float = 0,
        retract: float = 0,
        platformLength: float = 0,
        platformWidth: float = 0,
        platformLines: float = 0
    ):
        self.values = values
        self.workheight = workHeight
        self.freemoveHeight = freeMoveHeight
        self.eFactor = eFactor
        self.fValueLine = fValueLine
        self.fValueArc = fValueArc
        self.startX = startX
        self.startY = startY
        self.overrunStart = overrunStart
        self.overrunEnd = overrunEnd
        self.printOverrun = printOverrun
        self.pause = pause
        self.currentX = 0
        self.currentY = 0
        self.currentE = eFactorStart
        self.retract = retract
        self.platformLength = platformLength
        self.platformWidth = platformWidth
        self.platformLines = int(platformLines)

        rotation = -1 * rotation * math.pi / 180
        self.rotationMatrix = np.array(
            [
                [math.cos(rotation), math.sin(rotation) * -1],
                [math.sin(rotation), math.cos(rotation)],
            ]
        )
        self.reset()

    def getCmdParam(self, label: str, val: float):
        return " " + label + str(round(val, 2)) if val is not None else ""

    def getResult(self):
        res = ""
        for cmd in self.commands:
            fval = self.fValueArc if cmd.prefix == "G02" or cmd.prefix == "G03" else self.fValueLine 
            cmdString, e = cmd.toGCode(self.eFactor, self.currentE, fval)
            res += cmdString + "\n"
            self.currentE = e

        return res

    def reset(self):
        self.result = []
        self.commands = []

    def addCmd(
        self,
        prefix: str,
        x: float = None,
        y: float = None,
        z: float = None,
        i: float = None,
        j: float = None,
        e:float = None,
        p: int = None,
        arcDegrees: int = None,
        printing: bool = False,
        moving: bool = False,
    ):

        # x and y are both needed for rotation (even if one of them does not change)
        x = x if not x is None else self.currentX
        y = y if not y is None else self.currentY

        # Save current location
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

        # Rotate i and j (relative offset of the circle center)
        if i is not None and j is not None:
            iAbs = x + i
            jAbs = y + j

            iAbsNew, jAbsNew = self.rotate(iAbs, jAbs)

            iAbsNew += self.startX
            jAbsNew += self.startY

            i = iAbsNew - xRot
            j = jAbsNew - yRot

        # Overrun start
        if printing and len(self.commands) != 0 and self.commands[-1].z is not None:
            if (
                self.commands[-1].z == self.workheight
                and self.overrunStart + self.printOverrun != 0
            ):
                startVector = subtract([xRot, yRot], [previousX, previousY])
                norm = np.linalg.norm(startVector)
                if norm != 0:
                    vec = startVector / norm

                    back = vec * (self.overrunStart + self.printOverrun)
                    forward1 = vec * self.printOverrun

                    self.commands.insert(
                        -1,
                        GCodeCmd(
                            "G0",
                            x=previousX - back[0],
                            y=previousY - back[1],
                            previousX=previousX,
                            previousY=previousY,
                            isOverrun=False,
                            moving=True,
                        ),
                    )

                    self.commands.append(
                        GCodeCmd(
                            "G0",
                            x=previousX - forward1[0],
                            y=previousY - forward1[1],
                            previousX=previousX - back[0],
                            previousY=previousY - back[1],
                            isOverrun=True,
                            moving=True,
                        )
                    )

                    self.commands.append(
                        GCodeCmd(
                            "G1",
                            x=previousX,
                            y=previousY,
                            previousX=previousX - forward1[0],
                            previousY=previousY - forward1[1],
                            isOverrun=True,
                            moving=True,
                            printing=True,
                        )
                    )

                    self.commands[-3].x -= back[0]
                    self.commands[-3].y -= back[1]
                    del self.commands[-5]

        # Overrun end
        if z is not None and len(self.commands) != 0:
            if z == self.freemoveHeight and self.overrunEnd != 0:
                oldCmd = self.commands[-1]
                endVector = subtract(
                    [oldCmd.previousX, oldCmd.previousY], [oldCmd.x, oldCmd.y]
                )
                norm = np.linalg.norm(endVector)
                if norm != 0:
                    vec = (endVector / norm) * self.overrunEnd
                    self.commands.append(
                        GCodeCmd(
                            "G0",
                            x=previousX - vec[0],
                            y=previousY - vec[1],
                            previousX=previousX,
                            previousY=previousY,
                            isOverrun=True,
                            moving=True,
                        )
                    )
                    xRot -= vec[0]
                    yRot -= vec[1]
                    previousX -= vec[0]
                    previousY -= vec[1]

        self.commands.append(
            GCodeCmd(
                prefix,
                x=xRot,
                y=yRot,
                z=z,
                i=i,
                j=j,
                e=e,
                p=p,
                arcDegrees=arcDegrees,
                previousX=previousX,
                previousY=previousY,
                printing=printing,
                moving=moving,
            )
        )

    def setCurrentPosition(self, x=None, y=None):
        self.currentX = x
        self.currentY = y

    def moveTo(self, x: float = None, y: float = None, z: float = None):
        """Moves to the given location without releasing material

        Args:
            x (float, optional): relative difference in x direction. Defaults to None.
            y (float, optional): relative difference in y direction. Defaults to None.
            z (float, optional): absolute z coordinate. Defaults to None.
        """
        self.addCmd("G0", x, y, z,  moving=True)

    def printTo(self, x: float = None, y: float = None, z: float = None, e: float = None):
        """Moves to the given location while releasing material

        Args:
            x (float, optional): relative difference in x direction. Defaults to None.
            y (float, optional): relative difference in y direction. Defaults to None.
            z (float, optional): absolute z coordinate. Defaults to None.
        """
        self.addCmd("G1", x, y, z, e=e, printing=True, moving=True)

    def clockArc(
        self,
        x: float = None,
        y: float = None,
        i: float = 0.0,
        j: float = 0.0,
        arcDegrees=180,
    ):
        """Prints an arc clockwise. The center point offset as well as the location of the
         nozzle after printing the arc need to be defined. Again all coordinates are relative
          to the starting point of the arc (current location).

        Args:
            x (float, optional): Relative x coordinate of the nozzle after drawing the arc. Defaults to None.
            y (float, optional): Relative y coordinate of the nozzle after drawing the arc. Defaults to None.
            i (float, optional): Relative offset of the center point in x direction. Defaults to 0.0.
            j (float, optional): Relative offset of the center point in y direction. Defaults to 0.0.
            arcDegrees (int, optional): Number of degrees. Defaults to 180.
        """
        self.addCmd(
            "G02", x, y, i=i, j=j, arcDegrees=arcDegrees, printing=True, moving=True
        )

    def counterClockArc(
        self,
        x: float = None,
        y: float = None,
        i: float = 0.0,
        j: float = 0.0,
        arcDegrees=180,
    ):
        """Prints an arc counter-clockwise. The center point offset as well as the location of the
         nozzle after printing the arc need to be defined. Again all coordinate are relative
          to the starting point of the arc (current location).

        Args:
            x (float, optional): Relative x coordinate of the nozzle after drawing the arc. Defaults to None.
            y (float, optional): Relative y coordinate of the nozzle after drawing the arc. Defaults to None.
            i (float, optional): Relative offset of the center point in x direction. Defaults to 0.0.
            j (float, optional): Relative offset of the center point in y direction. Defaults to 0.0.
            arcDegrees (int, optional): Number of degrees. Defaults to 180.
        """
        self.addCmd(
            "G03", x, y, i=i, j=j, arcDegrees=arcDegrees, printing=True, moving=True
        )

    def workHeight(self):
        """Moves along the z-axis until work height is reached"""
        self.moveTo(z=self.workheight)

    def freeMoveHeight(self):
        """Moves along the z-axis until work free move height is reached"""
        if self.retract is not None and self.retract != 0:
            self.printTo(z=self.freemoveHeight, e=self.retract)
        else:
            self.moveTo(z=self.freemoveHeight)

    def rotate(self, x: float, y: float):
        result = self.rotationMatrix.dot(np.array([x, y]))
        return result[0], result[1]

    def onFinish(self):
        if self.pause != 0:
            self.addCmd("G4", p=self.pause)

    @abc.abstractmethod
    def gcode(self, startX: float, startY: float, workHeight: float):
        """Generates the gcode of the pattern"""
        
    def drawPlatformStart(self):
        """Draws a platform on the left side"""

        if self.platformLines == 0 or self.platformLength == 0 or self.platformWidth == 0:
            self.workHeight()
            return

        if self.platformLines % 2 != 0:
            self.platformLines += 1

        width = self.platformWidth / self.platformLines 
        y = self.currentY
        x = self.currentX

        self.moveTo(y=y - width*self.platformLines)
        self.workHeight()

        for num in range(self.platformLines, 0, -2):
            self.printTo(x=x + self.platformLength)
            self.printTo(y=y - width*(num-1))
            self.printTo(x=x)
            self.printTo(y=y - width*(num-2))


    def drawPlatformEnd(self):
        """Draws a platform on the left side"""

        if self.platformLines == 0 or self.platformLength == 0 or self.platformWidth == 0:
            return
            
        if self.platformLines % 2 != 0:
            self.platformLines += 1

        width = self.platformWidth / self.platformLines 
        y = self.currentY
        x = self.currentX

        for num in range(0, self.platformLines, 2):
            self.printTo(y=y+width*(num+1))
            self.printTo(x=x + self.platformLength)
            self.printTo(y=y+width*(num+2))
            self.printTo(x=x)