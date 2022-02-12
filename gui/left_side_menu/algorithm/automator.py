from functools import partial
from io import StringIO
from subprocess import run
from tkinter import *
import shutil

import numpy as np
from algorithms.algorithms import *
from algorithms.segmentation.segmentation import Segmenter
from algorithms.algorithms import *
from logger import log, Logger, Capturing, RedirectedStdout, capture2
from gui.canvas.plotting_options.plotting_option import PlottingOption
from gui.canvas.plotting_options.plotting_option_calculator import PlottingOptionCalculator
from util import doIntersect
import os
import igl
import sys
import io

class Automator:
    basicShapeThreshholdValue:int = 50
    basicShapeThreshholdPercentage:float = 0.95

    maxAllowedAngularDistortion = 0.005
    maxAllowedIsometricDistortion = 0.02

    angularDistLimitForMaxValue = 0.15
    isometricDistLimitForMaxValue = 1
    misometricDistLimitForMaxValue = 1.9

    facesThreshhold = 1800
    facesHardThreshhold = 400

    maxDistortionForChartAmountCalculation = 0.3
    maxChartCountPerSegmentation = 3
    additionalChartFactor = 1/8
    maxCharts = 3


    #Todo: integrate algoname


    def __init__(self, filename:str, folderPath:str="automation_results", totalFacesCount:int=None):
        log("Processing file " + filename)
        self.filename = filename
        self.folderPath = folderPath
        self.logger = Logger()
        self.isometricDist = None
        self.angularDist = None
        self.totalFacesCount = totalFacesCount

    def read(self):
        self.vertices, self.faces = igl.read_triangle_mesh(self.filename)
        if self.totalFacesCount is None: self.totalFacesCount = len(self.faces)
        self.segmenter = Segmenter()
        self.segmenter.parse(self.vertices, self.faces)
        
        
    def calcDistortions(self, pointsBefore, facesBefore, pointsAfter, facesAfter):
        angularDistVals, angularDist, _ = PlottingOption.LSCM.getOptionCalculator(pointsBefore,
            facesBefore, pointsAfter, facesAfter, "", 1).getDistortionValues()
        isometricDistVals, isometricDist, _ = PlottingOption.ARAP.getOptionCalculator(pointsBefore,
            facesBefore, pointsAfter, facesAfter, "", 1).getDistortionValues()
        misometricDistVals, misometricDist, _ = PlottingOption.MAX_ISOMETRIC.getOptionCalculator(pointsBefore,
            facesBefore, pointsAfter, facesAfter, "", 1).getDistortionValues()
        maxAngularDist = max(angularDistVals.values())
        maxIsometricDist = max(isometricDistVals.values())
        maxmIsometricDist = max(misometricDistVals.values())

        return angularDist, maxAngularDist, isometricDist, maxIsometricDist, misometricDist, maxmIsometricDist


    def calculate(self):
        self.read()
        if self.isBasicShape():
            #Todo: Optimize cone amount
            _, pointsBefore, facesBefore, pointsAfter, facesAfter = executeBFF(self.getOptimalConeCount(), self.filename)

            #Todo: Check distortion
#            if(dist bad):
#                return self.segmentAndProcess(True)

            return [], [(-1, pointsBefore, facesBefore, pointsAfter, facesAfter)]

        else:
            if self.isClosed():
                return self.segmentAndProcess(True)
            else:
                pointsBefore, facesBefore, pointsAfter, facesAfter = self.flatten()
#                self.calcDistortions(pointsBefore, facesBefore, pointsAfter, facesAfter)
                log("angularDist: " + str(self.angularDist))
                log("max angular dist: " + str(self.maxAngularDist))
                log("isometricDist: " + str(self.isometricDist))
                log("max isometric dist: " + str(self.maxIsometricDist))
                log("MisometricDist: " + str(self.misometricDist))
                log("max Misometric dist: " + str(self.maxmIsometricDist))
                #Todo: check overlapping
                if self.shouldSegment(pointsAfter, facesAfter):
                    return self.segmentAndProcess()
                else: 
                    return [], [(-1, pointsBefore, facesBefore, pointsAfter, facesAfter)]

    def getOptimalConeCount(self):
        return 18
        max = len(self.vertices)
        current = 30
        
        _, pB1, fB1, pA1, fA1 = executeBFF(current, self.filename)
        (aD1, mAD1,iD1, mID1, mmaxID1, mmmaxID1) = self.calcDistortions(pB1, fB1, pA1, fA1)


    def overlaps(self, pointsAfter, facesAfter):
        log("Checking overlaps")
        
        bnd = list(igl.boundary_loop(np.array(facesAfter)))
#        if len(bnd) > 0:
#            bnd.append(bnd[0])

        for index1 in range(0, len(bnd)-1):
            p1 = pointsAfter[bnd[index1]]
            p2 = pointsAfter[bnd[index1+1]]
            for index2 in range(index1+2, len(bnd)-1):
                p3 = pointsAfter[bnd[index2]]
                p4 = pointsAfter[bnd[index2+1]]

 #               log("doIntersect:")
 #               log("p1: " + str(p1) + ", p2: " + str(p2))
 #               log("p3: " + str(p3) + ", p4: " + str(p4))
                if doIntersect(p1, p2, p3, p4):
                    log("Overlaps returning True")
                    return True

        log("Overlaps returning False")
        return False
          
    def shouldSegment(self, pointsAfter, facesAfter):
#        if len(self.faces) < self.facesHardThreshhold:
#            return False

        if self.overlaps(pointsAfter, facesAfter): 
            log("shouldSegment returning True 1")
            return True

        if (self.maxIsometricDist > self.isometricDistLimitForMaxValue
         or self.maxAngularDist > self.angularDistLimitForMaxValue
         or self.maxmIsometricDist > self.misometricDistLimitForMaxValue):
            log("shouldSegment returning True 2")
            return True

        log("shouldSegment returning 3")
        return len(self.faces) >= self.facesThreshhold and (self.angularDist > self.maxAllowedAngularDistortion or
                 self.isometricDist > self.maxAllowedIsometricDistortion)

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

            f2C, data = seg_automator.SegmentationAutomator(self.folderPath, key, self.totalFacesCount).calculate()
#            dataList.extend(data)
            for d in data:
                k, pB, fB, pA, fA = d
                dataList.append((faceMapping[k], pB, fB, pA, fA))
            for index, x in enumerate(f2C):
                faceToChart[faceMapping[index]] = faceMapping[x]

        return faceToChart, dataList


    
    def getDistortionBasedChartCount(self):
        steps = self.maxChartCountPerSegmentation-1

        if self.isometricDist is None: return steps+1

        for i in range(1, steps+1):
            if self.isometricDist <= (self.maxDistortionForChartAmountCalculation/steps)*i: return i+1

        return steps

    def getOptimalChartCount(self, closed:bool=True):
        return 2
        distCharts = self.getDistortionBasedChartCount()
        additionalCharts = len(self.faces) // (self.totalFacesCount * self.additionalChartFactor)

        res = distCharts + additionalCharts
        if res > self.maxCharts: res = self.maxCharts
        return res

    def isClosed(self):
        bnd = list(igl.boundary_loop(np.array(self.faces)))
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
        _, pB1, fB1, pA1, fA1 = executeARAP(self.filename)
        _, pB2, fB2, pA2, fA2 = executeBFF(0, self.filename)

        (aD1, mAD1,iD1, mID1, mmaxID1, mmmaxID1) = self.calcDistortions(pB1, fB1, pA1, fA1)
        (aD2, mAD2,iD2, mID2, mmaxID2, mmmaxID2) = self.calcDistortions(pB2, fB2, pA2, fA2)

        if iD1 <= iD2:
            self.setDistortionValues(aD1, mAD1,iD1, mID1, mmaxID1, mmmaxID1)
            return pB1, fB1, pA1, fA1
        else:
            self.setDistortionValues(aD2, mAD2,iD2, mID2, mmaxID2, mmmaxID2)
            return pB2, fB2, pA2, fA2


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
        
    def setDistortionValues(self, angularDist, maxAngularDist,
      isometricDist, maxIsometricDist, misometricDist, maxmIsometricDist):
        self.angularDist = angularDist
        self.maxAngularDist = maxAngularDist
        self.isometricDist = isometricDist
        self.maxIsometricDist = maxIsometricDist
        self.misometricDist = misometricDist
        self.maxmIsometricDist = maxmIsometricDist


import gui.left_side_menu.algorithm.segmentation_automator as seg_automator