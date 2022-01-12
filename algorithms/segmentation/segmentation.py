from openmesh import *
import numpy as np
import time
from plotly import plot
from algorithms.segmentation.data_parser import SegmentationParser
from algorithms.segmentation.charts import Charts
from algorithms.segmentation.features import Features
from algorithms.segmentation.plotter import plotFeatures
import algorithms.segmentation.util

prefix = "[Segmenter] "

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
        log("Feature detection finished. Size: " + str(len(features)))

        return self.charts.computeCharts(features)
