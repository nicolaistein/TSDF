from tkinter import *
from typing import Mapping
from PIL import ImageTk, Image
from patterns.pattern1.pattern import Pattern as Pattern1
from patterns.pattern2.pattern import Pattern as Pattern2
from patterns.pattern3.pattern import Pattern as Pattern3
import os


def parsePatternAttributes(folderName: str):
    pattern = open(folderName + "/pattern.py", "r")
    mapping: Mapping = {}
    mapping["id"] = "NoID"
    mapping["author"] = "NoAuthor"
    mapping["params"] = ""
    for line in pattern:
        if(line.startswith("#")):
            while(line.startswith("#") or line.startswith(" ")):
                line = line[1:]
            if(line.endswith("\n")):
                line = line[:len(line)-1]
            split = line.split("=")
            if(len(split) == 2):
                mapping[split[0]] = split[1]
        else:
            break
    return mapping


class PatternModel:
    def __init__(self, folderName: str):
        self.folderName = folderName
        self.attributes = parsePatternAttributes(folderName)
        self.img = Image.open(folderName + "/image.png")
        self.name = ""
        self.id = self.attributes["id"]
        if(self.attributes["id"] == "NoID"):
            raise "Pattern " + self.name + " does not have an ID"
        self.location = {}
        self.x = 0.0
        self.y = 0.0
        self.rotation = 0.0
        self.params = {}
        for x in [i for i in self.attributes["params"].split(",") if i]:
            self.params[x] = "0.0"

    def getGcode(self):
        print("# Pattern " + self.name + " generate gcode")
        print("# x: " + str(self.x) + ", y: " + str(self.y))
        print("# rotation: " + str(self.rotation) + " degrees")
        values = {}
        for key, val in self.params.items():
            values[key] = float(val)

        print("folder: " + self.folderName)
        
        if self.folderName.endswith("pattern1"):
            result, commands = Pattern1(values, 2.8, 30, self.x, self.y, self.rotation).gcode()
        if self.folderName.endswith("pattern2"):
            result, commands = Pattern2(values, 2.8, 30, self.x, self.y, self.rotation).gcode()
        if self.folderName.endswith("pattern3"):
            result, commands = Pattern3(values, 2.8, 30, self.x, self.y, self.rotation).gcode()

        return result, commands

    def setName(self, newName: str):
        self.name = newName if newName else "NoName"

    def setLocation(self, x: float, y: float):
        self.x = x
        self.y = y

    def updateParams(self, mapping: Mapping):
        self.params.update(mapping)

    def print(self):
        print("Pattern " + self.name)
        print("Params: " + str(self.params))
        print("Location" + self.getPosition())
        print("Rotation: " + str(self.rotation))

    def getPosition(self):
        return str(self.x) + ", " + str(self.y)
