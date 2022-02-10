from functools import partial
from subprocess import run
from tkinter import *
import shutil
from algorithms.algorithms import *
from algorithms.segmentation.segmentation import Segmenter
from algorithms.algorithms import *
from logger import log
from gui.canvas.plotting_options.plotting_option import PlottingOption
from gui.canvas.plotting_options.plotting_option_calculator import PlottingOptionCalculator
from gui.left_side_menu.algorithm.segmentation_automator import SegmentationAutomator
import os
import igl

class Automator:
    basicShapeThreshholdValue:int = 40
    basicShapeThreshholdPercentage:float = 0.95
    maxAngularDistortion = 0.01
    maxIsometricDistortion = 0.02

    def __init__(self, filename:str, folderPath:str="automation_results"):
        log("Processing file " + filename)
        self.filename = filename
        self.folderPath = folderPath

    def read(self):
        self.vertices, self.faces = igl.read_triangle_mesh(self.filename)
        self.segmenter = Segmenter()
        self.segmenter.parse(self.vertices, self.faces)
        
        
    def calculate(self):
        self.read()
        if self.isBasicShape():
            #Todo: use BFF with x cones
            return None, [(pointsBefore, facesBefore, pointsAfter, facesAfter)]

        else:
            if self.isClosed():
                faceToChart, data = self.segmentAndProcess(True)
            else:
                pointsBefore, facesBefore, pointsAfter, facesAfter = self.flatten()
                _, self.angularDist, _ = PlottingOption.LSCM.getOptionCalculator(pointsBefore,
                 facesBefore, pointsAfter, facesAfter, "", 1).getDistortionValues()
                _, self.isometricDist, _ = PlottingOption.ARAP.getOptionCalculator(pointsBefore,
                 facesBefore, pointsAfter, facesAfter, "", 1).getDistortionValues()

                #Todo: check overlapping
                if (self.angularDist > self.maxAngularDistortion or
                 self.isometricDist > self.maxIsometricDistortion):
                    faceToChart, data = self.segmentAndProcess()
                    return faceToChart, data
                else: 
                    return None, [(pointsBefore, facesBefore, pointsAfter, facesAfter)]
                    

    def segmentAndProcess(self, closed:bool=False):
#        self.createFolder()
        faceToChart, chartKeys = self.segmenter.compute(self.vertices, self.faces, self.getOptimalChartCount(closed))
        dataMapping = {}
        for key in chartKeys:
            faceMapping = {}
            counter = 0
            for face, chart in enumerate(faceToChart):
                if chart == key:
                    faceMapping[counter] = face
                    counter += 1

            #Todo: make keys unique
            f2C, data = SegmentationAutomator(faceMapping, key).calculate()
            dataMapping.update(data)
            for index, x in enumerate(f2C):
                faceToChart[faceMapping[index]] = x

        return faceToChart, data



    def getOptimalChartCount(self, closed:bool=True):
        #Todo: zwischen 2 und 5
        #Todo: Je höher der error, desto mehr
        return 4

    def isClosed(self):
        bnd = igl.boundary_loop(self.faces)
        return len(bnd) == 0

    def isBasicShape(self):
        underThresh = 0
        total = len(self.segmenter.parser.SOD.values())
        for val in self.segmenter.parser.SOD.values():
            if val <= self.basicShapeThreshholdValue: underThresh += 1

        return (underThresh / total) >= self.basicShapeThreshholdPercentage

    def flatten(self):
        #Use arap
        result = executeARAP(self.filename)
        output = run("pwd", capture_output=True).stdout
        log("cusomt output: " + output)

        if output.endswith("Error: Numerical issue."):
            log("Switching to BFF")
            result = executeBFF(0, self.filename)

        _, pointsBefore, facesBefore, pointsAfter, facesAfter = result
        return pointsBefore, facesBefore, pointsAfter, facesAfter
        
#    def createFolder(self):
#        if os.path.isdir(os.getcwd() + "/" + self.folderPath):
#            shutil.rmtree(self.folderPath)
#        os.mkdir(self.folderPath)