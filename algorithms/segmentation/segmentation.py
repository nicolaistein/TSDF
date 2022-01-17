import enum
from typing import List, Mapping
from openmesh import *
import numpy as np
import time
import shutil
from plotly import plot
from algorithms.segmentation.data_parser import SegmentationParser
from algorithms.segmentation.charts import Charts
from algorithms.segmentation.features import Features
from algorithms.segmentation.plotter import plotFeatures
import algorithms.segmentation.util
import os

prefix = "[Segmenter] "
folder = "algorithms/segmentation/result"

def log(msg:str):
    print(prefix + msg)

class Segmenter:

    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.parser = SegmentationParser()
        self.features = Features(self.parser)
        self.charts = Charts(self.parser)

    def calc(self):
        self.parser.parse(self.vertices, self.faces, True)
        log("parsing finished")
        features = self.features.computeFeatures()
        self.features.saveResult()
    #    self.features.plotResult()

        faceToChart, chartKeys = self.charts.computeCharts(features)
        self.clearFolder()
        for x in chartKeys:
            self.extract(faceToChart, x)
        
        return faceToChart, chartKeys

    def clearFolder(self):
        if os.path.isdir(os.getcwd() + "/" + folder):
            shutil.rmtree(folder)

        os.mkdir(folder)


    def extract(self, faceToChart, key):
        usedVertices = {}
        counter = 1
        for index, ch in enumerate(faceToChart):
            if ch == key:
                for v in self.faces[index]:
                    if v not in usedVertices: 
                        usedVertices[v] = counter
                        counter += 1


        file = open(folder + "/" + str(key) + ".obj", "w")
        for k, v in usedVertices.items():
            file.write(self.arrayToString("v", self.vertices[k]))

        for index, ch in enumerate(faceToChart):
            if ch == key:
                file.write(self.arrayToString("f", self.faces[index], usedVertices))
        file.close()


    def arrayToString(self, prefix:str, list:List[int], mapping:Mapping=None):
        s = prefix
        for num in list:
            s += " " + str(mapping[num] if mapping is not None else num)

        s += "\n"
        return s


