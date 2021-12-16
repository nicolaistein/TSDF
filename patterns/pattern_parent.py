from typing import Mapping
import abc


def getCmdParam(label: str, val: float):
    return " " + label + str(val) if val is not None else ""


class PatternParent:
    def __init__(self, values: Mapping):
        self.values = values
        self.result = ""

    def reset(self):
        self.result = ""

    def add(self, cmd: str):
        self.result += cmd + "\n"

    def addCmd(self, prefix: str, x=None, y=None, z=None, i=None, j=None):
        cmd: str = ""
        cmd += getCmdParam("X" + x)
        cmd += getCmdParam("Y" + y)
        cmd += getCmdParam("Z" + z)
        cmd += getCmdParam("I" + i)
        cmd += getCmdParam("J" + j)
        if(cmd):
            self.add(prefix + cmd)

    def moveTo(self, x=None, y=None, z=None):
        self.addCmd("G0", x, y, z)

    def printTo(self, x=None, y=None, z=None):
        self.addCmd("G1", x, y, z)

    def clockArc(self, x=None, y=None, i=None, j=None):
        self.addCmd("G02", x, y, i=i, j=j)

    def counterClockArc(self, x=None, y=None, i=None, j=None):
        self.addCmd("G03", x, y, i=i, j=j)

    def relativeMode(self):
        self.add("G91")

    def absoluteMode(self):
        self.add("G90")

    @abc.abstractmethod
    def gcode(self, startX: float, startY: float, workHeight: float):
        """Generates the gcode of the pattern"""
        return
