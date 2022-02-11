from functools import partial
from io import StringIO
from subprocess import run
from tkinter import *
import shutil
from algorithms.algorithms import *
from algorithms.segmentation.segmentation import Segmenter
from algorithms.algorithms import *
from logger import log, Logger, Capturing, RedirectedStdout, capture2
from gui.canvas.plotting_options.plotting_option import PlottingOption
from gui.canvas.plotting_options.plotting_option_calculator import PlottingOptionCalculator
import os
import igl
import sys
import io

class Automator:
    basicShapeThreshholdValue:int = 50
    basicShapeThreshholdPercentage:float = 0.95
    maxAngularDistortion = 0.005
    maxIsometricDistortion = 0.01
    facesThreshhold = 1800
    facesHardThreshhold = 1200
    angularDistLimitForMaxValue = 5000
    isometricDistLimitForMaxValue = 5000


    def __init__(self, filename:str, folderPath:str="automation_results"):
        log("Processing file " + filename)
        self.filename = filename
        self.folderPath = folderPath
        self.logger = Logger()
        self.isometricDist = None
        self.angularDist = None

    def read(self):
        self.vertices, self.faces = igl.read_triangle_mesh(self.filename)
        self.segmenter = Segmenter()
        self.segmenter.parse(self.vertices, self.faces)
        
        
    def calcDistortions(self, pointsBefore, facesBefore, pointsAfter, facesAfter):
        angularDistVals, self.angularDist, _ = PlottingOption.LSCM.getOptionCalculator(pointsBefore,
            facesBefore, pointsAfter, facesAfter, "", 1).getDistortionValues()
        isometricDistVals, self.isometricDist, _ = PlottingOption.ARAP.getOptionCalculator(pointsBefore,
            facesBefore, pointsAfter, facesAfter, "", 1).getDistortionValues()
        self.maxAngularDist = max(angularDistVals)
        self.maxIsometricDist = max(isometricDistVals)


    def calculate(self):
        self.read()
        if self.isBasicShape():
            #Todo: Optimize cone amount
            _, pointsBefore, facesBefore, pointsAfter, facesAfter = executeBFF(3, self.filename)
            return [], [(-1, pointsBefore, facesBefore, pointsAfter, facesAfter)]

        else:
            if self.isClosed():
                faceToChart, data = self.segmentAndProcess(True)
                return faceToChart, data
            else:
                pointsBefore, facesBefore, pointsAfter, facesAfter = self.flatten()
                self.calcDistortions(pointsBefore, facesBefore, pointsAfter, facesAfter)
                log("angularDist: " + str(self.angularDist))
                log("isometricDist: " + str(self.isometricDist))
                log("max angular dist: " + str(self.maxAngularDist))
                log("max isometric dist: " + str(self.maxIsometricDist))
                #Todo: check overlapping
                if self.shouldSegment():
                    faceToChart, data = self.segmentAndProcess()
                    return faceToChart, data
                else: 
                    return [], [(-1, pointsBefore, facesBefore, pointsAfter, facesAfter)]
                    
    def shouldSegment(self):
        if len(self.faces) < self.facesHardThreshhold:
            return False
        if self.maxIsometricDist > self.isometricDistLimitForMaxValue or self.maxAngularDist > self.angularDistLimitForMaxValue:
            return True

        return len(self.faces) >= self.facesThreshhold and (self.angularDist > self.maxAngularDistortion or
                 self.isometricDist > self.maxIsometricDistortion)

    def segmentAndProcess(self, closed:bool=False):
#        self.createFolder()
        faceToChart, chartKeys = self.segmenter.compute(self.vertices,
          self.faces, self.getOptimalChartCount(closed), self.folderPath)
        dataList = []
        for key in chartKeys:
            faceMapping = {}
            counter = 0
            for face, chart in enumerate(faceToChart):
                if chart == key:
                    faceMapping[counter] = face
                    counter += 1

            f2C, data = seg_automator.SegmentationAutomator(self.folderPath, key).calculate()
#            dataList.extend(data)
            for d in data:
                k, pB, fB, pA, fA = d
                dataList.append((faceMapping[k], pB, fB, pA, fA))
            for index, x in enumerate(f2C):
                faceToChart[faceMapping[index]] = faceMapping[x]

        return faceToChart, dataList



    def getOptimalChartCount(self, closed:bool=True):
        #Todo: zwischen 2 und 5
        #Todo: Je höher der error, desto mehr
        end = 0.2
        steps = 3
        if self.isometricDist is None: return steps+1
        for i in range(1, steps+1):
            if self.isometricDist <= (end/steps)*i: return i+1
        #from 0 to 0.2
        return steps

    def isClosed(self):
        bnd = igl.boundary_loop(self.faces)
        return len(bnd) == 0

    def isBasicShape(self):
        if len(self.faces) <= 100: return True
        underThresh = 0
        total = len(self.segmenter.parser.SOD.values())
        for val in self.segmenter.parser.SOD.values():
            if val <= self.basicShapeThreshholdValue: underThresh += 1

        log("underThresh: " + str(underThresh))
        log("total: " + str(total))
        log("underThresh / total: " + str(underThresh / total))
        return (underThresh / total) < self.basicShapeThreshholdPercentage

    def flatten(self):
        #Use arap
#        self.logger.start()
        print("Testmsg")
            # do what you have to do to create some output
#        with capture2() as output:
        _, pB, fB, pA, fA = executeARAP(self.filename)
        self.calcDistortions(pB, fB, pA, fA)

        if self.angularDist > 0.4 or self.isometricDist > 0.4:
        
    # do what you want with the output_string
#        output = run("pwd", capture_output=True).stdout
#        print("Testmsg 2")
#        self.logger.stop()

#        log("custom output: " + str(output))

#        if output[-1].endswith("Error: Numerical issue."):
#        if False:
            log("Switching to BFF")
            _, pB, fB, pA, fA = executeBFF(0, self.filename)

        return pB, fB, pA, fA
        


import gui.left_side_menu.algorithm.segmentation_automator as seg_automator