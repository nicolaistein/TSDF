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
from algorithms.segmentation.parameters import *
import os
from logger import log

folder = "segmentation_results"

class Segmenter:

    
    def __init__(self):
        self.faces = []
        self.vertices = []
        self.parser = None
        self.computedFeatures = None

    def parse(self, vertices, faces):
            self.faces = faces
            self.vertices = vertices
            self.parser = SegmentationParser()
            self.parser.parse(self.vertices, self.faces, True)
            self.computedFeatures = None

    def compute(self, vertices, faces, chartCount:int, targetFolder:str=None):
        if self.faces is not faces and self.vertices is not vertices:
            self.parse(vertices, faces)

        if self.computedFeatures == None:
            self.computedFeatures = Features(self.parser).computeFeatures()
        
        self.charts = Charts(self.parser, chartCount)
        faceToChart, chartKeys = self.charts.computeCharts(self.computedFeatures)
        self.clearFolder(targetFolder)
        self.charts.plotCurrentCharts(targetFolder)
        for x in chartKeys:
            self.extract(faceToChart, x, targetFolder)
        
        return faceToChart, chartKeys
        

    def calc(self, targetFolder:str=None):
        self.parser.parse(self.vertices, self.faces, True)
        log("parsing finished")

        # features = edges to feature mapping
        self.computedFeatures = self.features.computeFeatures()
        self.features.saveResult()
        self.features.plotResult()

        faceToChart, chartKeys = self.charts.computeCharts(self.computedFeatures)
        self.clearFolder(targetFolder)
        for x in chartKeys:
            self.extract(faceToChart, x, targetFolder)
        
        return faceToChart, chartKeys

    def clearFolder(self, folderName:str=None):
        if folderName is None: folderName = os.getcwd() + "/" + folder
        if os.path.isdir(folderName):
            shutil.rmtree(folderName)

        os.mkdir(folderName)


    def extract(self, faceToChart, key, folderName:str=None):
        if folderName is None: folderName = os.getcwd() + "/" + folder
        usedVertices = {}
        counter = 1
        for index, ch in enumerate(faceToChart):
            if ch == key:
                for v in self.faces[index]:
                    if v not in usedVertices: 
                        usedVertices[v] = counter
                        counter += 1


        file = open(folderName + "/" + str(key) + ".obj", "w")
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


