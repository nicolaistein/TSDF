from openmesh import *
import numpy as np
import time
from plotly import plot
from algorithms.segmentation.data_parser import SegmentationParser
from algorithms.segmentation.charts import Charts
from algorithms.segmentation.features import Features
from algorithms.segmentation.plotter import plot
import algorithms.segmentation.util

prefix = "[Segmenter] "

def log(msg:str):
    print(prefix + msg)

class Segmenter:

    def __init__(self, objPath:str):
        self.objPath = objPath
        self.parser = SegmentationParser()
        self.features = Features(self.parser)
        self.charts = Charts(self.parser)

    def calc(self):
        self.parser.parse(self.objPath, True)
        log("parsing finished")
        features = self.features.computeFeatures()
        self.features.saveResult()
        self.features.plotResult()
  #      features = util.loadMarkedFeatures()
        log("Feature detection finished. Size: " + str(len(features)))

        return self.charts.computeCharts(features)



#print("init")
#s = Segmenter("Body_2.obj")
#computeStart = time.time()
#s.calc()
#computeEnd = time.time()
#print("time: " + str(computeEnd-computeStart))


#print("ALL")
#s.printAll()
#print("SOD")
#print(s.parser.SOD)
#print("CUSTOM DATA")
#print(s.parser.edgeToFaces)