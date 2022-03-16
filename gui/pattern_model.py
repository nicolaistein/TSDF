from tkinter import *
from typing import Mapping
from PIL import ImageTk, Image
from patterns.pattern1.pattern import Pattern as Pattern1
from patterns.pattern2.pattern import Pattern as Pattern2
from patterns.pattern3.pattern import Pattern as Pattern3
from logger import log


class PatternModel:
    def __init__(self, folderName: str):
        self.folderName = folderName
        self.attributes = self.parsePatternAttributes()
        self.img = Image.open(folderName + "/image.png")
        self.name = ""
        self.id = self.attributes["id"]
        if self.attributes["id"] == "NoID":
            raise "Pattern " + self.name + " does not have an ID"
        self.location = {}
        self.x = 0.0
        self.y = 0.0
        self.rotation = 0.0
        self.params = {}
        for x in [i for i in self.attributes["params"].split(",") if i]:
            self.params[x] = "0.0"

    def getGcode(
        self,
        workHeight: float = 0,
        freeMoveHeight: float = 1,
        eFactor: float = 0,
        eFactorStart: float = 0,
        fFactor: float = 0,
        overrunStart: float = 0,
        overrunEnd: float = 0,
        printOverrun: float = 0,
        pause: float = 0,
        cleaningX: float = None,
        cleaningY: float = None,
    ):
        values = {}
        for key, val in self.params.items():
            values[key] = float(val)

        if self.folderName.endswith("pattern1"):
            patternCalc = Pattern1
        if self.folderName.endswith("pattern2"):
            patternCalc = Pattern2
        if self.folderName.endswith("pattern3"):
            patternCalc = Pattern3

        return patternCalc(
            values,
            workHeight,
            freeMoveHeight,
            eFactor,
            eFactorStart,
            fFactor,
            overrunStart,
            overrunEnd,
            printOverrun,
            self.x,
            self.y,
            self.rotation,
            pause,
            cleaningX,
            cleaningY,
        ).gcode()

    def setName(self, newName: str):
        self.name = newName if newName else "NoName"

    def setLocation(self, x: float, y: float):
        self.x = x
        self.y = y

    def updateParams(self, mapping: Mapping):
        self.params.update(mapping)

    def print(self):
        log("Pattern " + self.name)
        log("Params: " + str(self.params))
        log("Location" + self.getPosition())
        log("Rotation: " + str(self.rotation))

    def getPosition(self):
        return str(self.x) + ", " + str(self.y)

    def parsePatternAttributes(self):
        pattern = open(self.folderName + "/pattern.py", "r")
        mapping: Mapping = {}
        mapping["id"] = "NoID"
        mapping["author"] = "NoAuthor"
        mapping["params"] = ""
        for line in pattern:
            if line.startswith("#"):
                while line.startswith("#") or line.startswith(" "):
                    line = line[1:]
                if line.endswith("\n"):
                    line = line[: len(line) - 1]
                split = line.split("=")
                if len(split) == 2:
                    mapping[split[0]] = split[1]
            else:
                break
        return mapping
