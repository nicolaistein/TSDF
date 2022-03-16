from functools import partial
from tkinter import *

import numpy as np
from scipy.misc import face
from algorithms.algorithms import *
from algorithms.segmentation.segmentation import Segmenter
from algorithms.algorithms import *
from logger import log
from gui.canvas.plotting_options.plotting_option import PlottingOption
from util import doIntersect, subtract, angle_between, getFlatTriangle
import os
import igl
import sys
import io


class Automator:
    basicShapeThreshholdValue: int = 40
    basicShapeThreshholdPercentage: float = 0.95

    maxAllowedAngularDistortion = 0.005
    maxAllowedIsometricDistortion = 0.02

    angularDistLimitForMaxValue = 0.15
    isometricDistLimitForMaxValue = 1
    misometricDistLimitForMaxValue = 1.9

    facesThreshhold = 1800
    facesHardThreshhold = 500

    maxDistortionForChartAmountCalculation = 0.3
    maxChartCountPerSegmentation = 6
    additionalChartFactor = 1 / 6
    maxCharts = 2

    minSODForCornerDetection = 0
    maxConesForBFF = 500

    def __init__(
        self,
        filename: str,
        folderPath: str = "automation_results",
        totalFacesCount: int = None,
    ):
        log("Processing file " + filename)
        self.filename = filename
        self.folderPath = folderPath
        self.isometricDist = None
        self.angularDist = None
        self.totalFacesCount = totalFacesCount

    def read(self):
        self.vertices, self.faces = igl.read_triangle_mesh(self.filename)
        if self.totalFacesCount is None:
            self.totalFacesCount = len(self.faces)
        self.segmenter = Segmenter()
        if len(self.faces) > 0 and type(self.faces[0]) is not np.ndarray:
            self.faces = np.matrix([list(self.faces)]).tolist()
        else:
            self.segmenter.parse(self.vertices, self.faces)

    def calcDistortions(self, pointsBefore, facesBefore, pointsAfter, facesAfter):
        angularDistVals, angularDist, _ = PlottingOption.LSCM.getOptionCalculator(
            pointsBefore, facesBefore, pointsAfter, facesAfter, "", 1
        ).getDistortionValues()
        isometricDistVals, isometricDist, _ = PlottingOption.ARAP.getOptionCalculator(
            pointsBefore, facesBefore, pointsAfter, facesAfter, "", 1
        ).getDistortionValues()
        (
            misometricDistVals,
            misometricDist,
            _,
        ) = PlottingOption.MAX_ISOMETRIC.getOptionCalculator(
            pointsBefore, facesBefore, pointsAfter, facesAfter, "", 1
        ).getDistortionValues()
        (
            misometricDistVals,
            misometricDist,
            _,
        ) = PlottingOption.MAX_ISOMETRIC.getOptionCalculator(
            pointsBefore, facesBefore, pointsAfter, facesAfter, "", 1
        ).getDistortionValues()
        (
            fastisometricDistVals,
            fastisometricDist,
            _,
        ) = PlottingOption.EFFICIENT_ISOMETRIC.getOptionCalculator(
            pointsBefore, facesBefore, pointsAfter, facesAfter, "", 1
        ).getDistortionValues()
        maxAngularDist = max(angularDistVals.values())
        maxIsometricDist = max(isometricDistVals.values())
        maxmIsometricDist = max(misometricDistVals.values())
        maxfastIsometricDist = max(fastisometricDistVals.values())
        minfastIsometricDist = min(fastisometricDistVals.values())

        return (
            angularDist,
            maxAngularDist,
            isometricDist,
            maxIsometricDist,
            misometricDist,
            maxmIsometricDist,
            fastisometricDist,
            maxfastIsometricDist,
            minfastIsometricDist,
        )

    def calculate(self):
        self.read()
        if len(self.faces) == 1:
            return self.processSingleTriangle()

        if self.isBasicShape():
            log("Object is a basic shape")
            _, pB, fB, pA, fA = executeBFF(self.getOptimalConeCount(), self.filename)
            (
                aD1,
                mAD1,
                iD1,
                mID1,
                mmaxID1,
                mmmaxID1,
                fI,
                maxfI,
                minfi,
            ) = self.calcDistortions(pB, fB, pA, fA)
            self.setDistortionValues(
                aD1, mAD1, iD1, mID1, mmaxID1, mmmaxID1, fI, maxfI, minfi
            )
            if self.shouldSegment(pA, fA):
                return self.segmentAndProcess()
            else:
                log("Object is not a basic shape")
                return [], [(-1, pB, fB, pA, fA)]

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
                # Todo: check overlapping
                if self.shouldSegment(pointsAfter, facesAfter):
                    return self.segmentAndProcess()
                else:
                    return [], [
                        (-1, pointsBefore, facesBefore, pointsAfter, facesAfter)
                    ]

    def getEdgesOfVertex(self, vertex):
        edges = []
        for e in self.segmenter.parser.mesh.ve(
            self.segmenter.parser.vertexHandles[vertex]
        ):
            edges.append(e.idx())
        return edges

    def getAngleBetweenEdges(self, edge1, edge2, jointVertex):
        p1, p2 = self.segmenter.parser.edgeToVertices[edge1]
        p3, p4 = self.segmenter.parser.edgeToVertices[edge2]

        x1 = p1 if p2 == jointVertex else p2
        x2 = p3 if p4 == jointVertex else p4
        vector1 = subtract(self.vertices[x1], self.vertices[jointVertex])
        vector2 = subtract(self.vertices[x2], self.vertices[jointVertex])

        angle = np.rad2deg(angle_between(vector1, vector2))
        return angle

    def getOptimalConeCount(self):
        max = len(self.vertices)
        bnd = list(igl.boundary_loop(np.array(self.faces)))

        corners = 0
        for index, _ in enumerate(self.vertices):
            edges = self.getEdgesOfVertex(index)
            relevantEdges = 0
            bigAngleDetected = False
            for edge in edges:
                if bigAngleDetected:
                    continue
                if self.segmenter.parser.SOD[edge] > self.minSODForCornerDetection:
                    relevantEdges += 1
                for e2 in edges:
                    if edge != e2:
                        if self.getAngleBetweenEdges(edge, e2, index) > 175:
                            bigAngleDetected = True

            if relevantEdges >= 3 and not bigAngleDetected and index not in bnd:
                corners += 1

        log("Corners: " + str(corners))
        if corners > self.maxConesForBFF:
            corners = self.maxConesForBFF

        return corners

    def overlaps(self, pointsAfter, facesAfter):
        log("Checking overlaps")

        bnd = list(igl.boundary_loop(np.array(facesAfter)))
        if len(bnd) > 0:
            bnd.append(bnd[0])

        for index1 in range(0, len(bnd) - 1):
            p1 = pointsAfter[bnd[index1]]
            p2 = pointsAfter[bnd[index1 + 1]]
            for index2 in range(index1 + 2, len(bnd) - 1):
                p3 = pointsAfter[bnd[index2]]
                p4 = pointsAfter[bnd[index2 + 1]]

                if doIntersect(
                    p1, p2, p3, p4, neighboring=bnd[index1] == bnd[index2 + 1]
                ):
                    log("Overlaps returning True")
                    return True

        log("Overlaps returning False")
        return False

    def getOptimalChartCount(self, closed: bool = True):
        return 2
        distCharts = self.getDistortionBasedChartCount()
        additionalCharts = len(self.faces) // (
            self.totalFacesCount * self.additionalChartFactor
        )

        res = distCharts + additionalCharts
        if res > self.maxCharts:
            res = self.maxCharts
        log("Using " + str(res) + " charts")
        return res

    def shouldSegment(self, pointsAfter, facesAfter):
        log("shouldSeg faces length: " + str(len(self.faces)))
        if len(self.faces) <= 863:
            return False

        if self.overlaps(pointsAfter, facesAfter):
            log("shouldSegment returning True overlaps")
            return True

        if len(self.faces) < self.facesHardThreshhold:
            log("shouldSegment returning False faces threshold")
            return False

        log("fast isometric: " + str(self.fastIsometricDist))
        log("max fast isometric: " + str(self.maxFastIsometricDist))
        log("min fast isometric: " + str(self.minFastIsometricDist))

        if self.fastIsometricDist > 4.5 or self.fastIsometricDist < 3.5:
            log("shouldSegment returning True 1")
            return True

        #     if len(self.faces) >= self.facesThreshhold and (self.angularDist > self.maxAllowedAngularDistortion or
        #              self.isometricDist > self.maxAllowedIsometricDistortion):
        #             log("shouldSegment returning True 3")
        #             return True

        #    if (self.maxIsometricDist > self.isometricDistLimitForMaxValue
        #     or self.maxAngularDist > self.angularDistLimitForMaxValue
        #     or self.maxmIsometricDist > self.misometricDistLimitForMaxValue):
        #        log("shouldSegment returning True 2")
        #        return True

        log("shouldSegment returning False")
        return False

    def segmentAndProcess(self, closed: bool = False):
        faceToChart, chartKeys = self.segmenter.compute(
            self.vertices,
            self.faces,
            self.getOptimalChartCount(closed),
            self.folderPath,
        )
        dataList = []
        for key in chartKeys:
            faceMapping = {}
            counter = 0
            for face, chart in enumerate(faceToChart):
                if chart == key:
                    faceMapping[counter] = face
                    counter += 1

            f2C, data = seg_automator.SegmentationAutomator(
                self.folderPath, key, self.totalFacesCount
            ).calculate()
            for d in data:
                k, pB, fB, pA, fA = d
                dataList.append((faceMapping[k], pB, fB, pA, fA))
            for index, x in enumerate(f2C):
                faceToChart[faceMapping[index]] = faceMapping[x]

        return faceToChart, dataList

    def getDistortionBasedChartCount(self):
        steps = self.maxChartCountPerSegmentation - 1

        if self.isometricDist is None:
            return steps + 1

        for i in range(1, steps + 1):
            if (
                self.isometricDist
                <= (self.maxDistortionForChartAmountCalculation / steps) * i
            ):
                return i + 1

        return steps

    def isClosed(self):
        bnd = list(igl.boundary_loop(np.array(self.faces)))
        return len(bnd) == 0

    def isBasicShape(self):

        sodsToAnalyze = []
        for val in self.segmenter.parser.SOD.values():
            if val != 360 and val != 0:
                sodsToAnalyze.append(val)

        #    if len(self.faces) <= 100: return True
        underThresh = 0
        total = len(sodsToAnalyze)
        for val in sodsToAnalyze:
            if val <= self.basicShapeThreshholdValue:
                underThresh += 1

        log("underThresh: " + str(underThresh))
        log("total: " + str(total))
        if total == 0:
            return True
        log("underThresh / total: " + str(underThresh / total))
        return (underThresh / total) < self.basicShapeThreshholdPercentage

    def flatten(self):
        methods = [
            executeARAP,
            partial(executeLSCM),
            partial(executeBFF, 0)
            #        , partial(executeBFF, 1)
            #        , partial(executeBFF, 2)
        ]
        res = None
        for m in methods:
            _, pB, fB, pA, fA = m(self.filename)
            (
                aD,
                mAD,
                iD,
                mID,
                mmaxID,
                mmmaxID,
                fI,
                maxfI,
                minfi,
            ) = self.calcDistortions(pB, fB, pA, fA)

            if res is None:
                self.setDistortionValues(
                    aD, mAD, iD, mID, mmaxID, mmmaxID, fI, maxfI, minfi
                )
                res = pB, fB, pA, fA
                continue

            if not self.overlaps(pA, fA):
                if res is None or fI < self.fastIsometricDist:
                    self.setDistortionValues(
                        aD, mAD, iD, mID, mmaxID, mmmaxID, fI, maxfI, minfi
                    )
                    res = pB, fB, pA, fA
        return res

        # Use arap
        #        self.logger.start()
        # do what you have to do to create some output
        #        with capture2() as output:
        _, pB1, fB1, pA1, fA1 = executeARAP(self.filename)
        _, pB2, fB2, pA2, fA2 = executeBFF(0, self.filename)
        _, pB3, fB3, pA3, fA3 = executeBFF(1, self.filename)

        (aD1, mAD1, iD1, mID1, mmaxID1, mmmaxID1) = self.calcDistortions(
            pB1, fB1, pA1, fA1
        )
        (aD2, mAD2, iD2, mID2, mmaxID2, mmmaxID2) = self.calcDistortions(
            pB2, fB2, pA2, fA2
        )
        (aD3, mAD3, iD3, mID3, mmaxID3, mmmaxID3) = self.calcDistortions(
            pB3, fB3, pA3, fA3
        )

        if iD1 <= iD2 and iD1 <= iD3 and not self.overlaps(pA1, fA1):
            self.setDistortionValues(aD1, mAD1, iD1, mID1, mmaxID1, mmmaxID1)
            return pB1, fB1, pA1, fA1

        elif iD3 <= iD1 and iD3 <= iD1 and not self.overlaps(pA3, fA3):
            self.setDistortionValues(aD3, mAD3, iD3, mID3, mmaxID3, mmmaxID3)
            return pB3, fB3, pA3, fA3

        else:
            self.setDistortionValues(aD2, mAD2, iD2, mID2, mmaxID2, mmmaxID2)
            return pB2, fB2, pA2, fA2

    def setDistortionValues(
        self,
        angularDist,
        maxAngularDist,
        isometricDist,
        maxIsometricDist,
        misometricDist,
        maxmIsometricDist,
        fI,
        maxfI,
        minfi,
    ):
        self.angularDist = angularDist
        self.maxAngularDist = maxAngularDist
        self.isometricDist = isometricDist
        self.maxIsometricDist = maxIsometricDist
        self.misometricDist = misometricDist
        self.maxmIsometricDist = maxmIsometricDist
        self.fastIsometricDist = fI
        self.maxFastIsometricDist = maxfI
        self.minFastIsometricDist = minfi

    def processSingleTriangle(self):
        p1 = self.vertices[self.faces[0][0]]
        p2 = self.vertices[self.faces[0][1]]
        p3 = self.vertices[self.faces[0][2]]
        x1, x2, x3 = getFlatTriangle(p1, p2, p3)
        del x1[-1]
        del x2[-1]
        del x3[-1]
        log(
            "RETURNING AUTO "
            + str((0, self.vertices, self.faces, [x1, x2, x3], self.faces))
        )
        return [], [(0, self.vertices, self.faces, [x1, x2, x3], self.faces)]


import gui.left_side_menu.algorithm.segmentation_automator as seg_automator
