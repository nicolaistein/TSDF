from functools import partial
from tkinter import *
from typing import Mapping
from PIL import ImageTk, Image
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


class Pattern:
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
            self.params[x] = ""

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
        print("Location(" + self.getPosition())
        print("Rotation: " + str(self.rotation))

    def getPosition(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
