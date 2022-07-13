from util import subtract, angle_between
import numpy as np
import math
from logger import log


class GCodeCmd:
    arcLines: int = 5

    def __init__(
        self,
        prefix: str,
        x: float,
        y: float,
        z: float = None,
        i: float = None,
        j: float = None,
        e: float = None,
        f: float = None,
        p: int = None,
        arcDegrees: int = None,
        previousX: float = 0.0,
        previousY=0.0,
        isOverrun: bool = False,
        moving: bool = False,
        printing: bool = False,
    ):
        self.prefix = prefix
        self.isOverrun = isOverrun
        self.x = x
        self.y = y
        self.z = z
        self.i = i
        self.j = j
        self.p = p
        self.e = e
        self.f = f
        self.moving = moving
        self.printing = printing
        self.arcDegrees = arcDegrees
        self.previousX = previousX
        self.previousY = previousY

    def getCmdParam(self, label: str, val: float):
        return " " + label + str(round(val, 2)) if val is not None else ""

    def getDistance(
        self,
        prevX: float = None,
        prevY: float = None,
        x: float = None,
        y: float = None,
        i: float = None,
        j: float = None,
        arcDegrees: int = None,
    ):
        if arcDegrees is None:
            return np.linalg.norm([x - prevX, y - prevY])
        else:
            radius = np.linalg.norm([i, j])
            return (2 * math.pi * radius) * (arcDegrees / 360)

    def toGCode(self, eFactor, currentE, fValue):
        if self.f != None:
            fValue = self.f

        cmd = self.prefix
        if self.moving:
            cmd += self.getCmdParam("X", self.x)
            cmd += self.getCmdParam("Y", self.y)
            cmd += self.getCmdParam("Z", self.z)
            cmd += self.getCmdParam("I", self.i)
            cmd += self.getCmdParam("J", self.j)
        cmd += self.getCmdParam("P", self.p)

        if self.printing:
            if self.e is None:
                distance = self.getDistance(
                    prevX=self.previousX,
                    prevY=self.previousY,
                    x=self.x,
                    y=self.y,
                    i=self.i,
                    j=self.j,
                    arcDegrees=self.arcDegrees,
                )
                self.e = distance * eFactor

            currentE -= self.e
            cmd += self.getCmdParam("E", currentE)

        if self.moving:
            cmd += self.getCmdParam("F", fValue)

        return cmd, currentE

    def toPoints(self, shouldLog: bool = False):
        if shouldLog:
            log(
                "toPoints prevX: "
                + str(self.previousX)
                + ", prevY: "
                + str(self.previousY)
                + ", x: "
                + str(self.x)
                + ", y: "
                + str(self.y)
            )
        """Returns a list of lines represented with starting and ending points"""
        if self.prefix == "G1" or self.isOverrun:
            if self.previousX != self.x or self.previousY != self.y:
                if shouldLog:
                    log(
                        self.prefix
                        + ": "
                        + str([[self.previousX, self.previousY], [self.x, self.y]])
                    )
                return [[self.previousX, self.previousY], [self.x, self.y]]

        if self.prefix == "G02" or self.prefix == "G03":
            points = [[self.previousX, self.previousY]]

            xr = self.previousX + self.i
            yr = self.previousY + self.j

            v1 = subtract([self.previousX, self.previousY], [xr, yr])
            del v1[-1]
            v2 = subtract([self.x, self.y], [xr, yr])
            del v2[-1]
            angle = angle_between(v1, v2) / self.arcLines
            if math.isnan(angle):
                return []
            if self.prefix == "G02":
                angle *= -1

            for counter in range(self.arcLines + 1):
                rotation = angle * (counter)
                rotationMatrix = np.array(
                    [
                        [math.cos(rotation), math.sin(rotation) * -1],
                        [math.sin(rotation), math.cos(rotation)],
                    ]
                )
                result = rotationMatrix.dot(np.array(v1))

                xNew = xr + result[0]
                yNew = yr + result[1]
                points.append([xNew, yNew])

            if shouldLog:
                log(self.prefix + ": " + str(points))
            return points

        if shouldLog:
            log(self.prefix)
        return []

    def print(self):
        z = "nan" if self.z is None else str(self.z)
        print(
            "GCodeCMD "
            + self.prefix
            + ": x="
            + str(round(self.x, 2))
            + "  y="
            + str(round(self.y, 2))
            + " z="
            + z
            + "  prevX="
            + str(round(self.previousX, 2))
            + "  prevY="
            + str(round(self.previousY, 2))
        )
