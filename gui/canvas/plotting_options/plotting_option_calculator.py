from tkinter import Canvas
from logger import log
from typing import List, Mapping
import abc
import math 
import numpy as np
from util import faceToArea, angle_between, getFlatTriangle


class PlottingOptionCalculator:

    def __init__(self, verticesBefore:List[List[float]], facesBefore:List[List[int]],
        verticesAfter:List[List[float]], facesAfter:List[List[int]], option, color:str,
        wholeObjectArea:float):
        self.verticesBefore = verticesBefore
        self.facesBefore = facesBefore
        self.verticesAfter = verticesAfter
        self.facesAfter = facesAfter
        self.option = option
        self.color = color
        self.wholeObjectArea:float = wholeObjectArea
        self.colors:Mapping = {}
        self.distortions:Mapping = {}
        self.totalDistortion = -1
        self.totalDistortionWholeObject = -1


    def getVerticesOfFace(self, face:List[int], vertices:List[List[float]]):
        v1 = vertices[face[0]]
        v2 = vertices[face[1]]
        v3 = vertices[face[2]]
        return v1, v2, v3


    def getDistortionValues(self):
        if self.totalDistortion == -1: self.calculateDistortions()
        return self.distortions, self.totalDistortion, self.totalDistortionWholeObject


    def solveThree(self, p1:List[float], p2:List[float], p3:List[float], res:List[float]):

        A = np.array([p1, p2, p3])
        B = np.array(res)
        
        try:
            result = np.linalg.solve(A, B)
            return result
        except np.linalg.LinAlgError:
            log("Linalg ERROR!")
            return [1, 1, 1]


    def getTransformationMatrix(self, faceBefore:List[int], faceAfter=List[int]):
        """Returns the linear part of the tansformation matrix (2x2)
         with the first index being the row"""
        t1, t2, t3 = self.getVerticesOfFace(faceBefore, self.verticesBefore)
        x1, x2, x3 = getFlatTriangle(t1, t2, t3)
        y1, y2, y3 = self.getVerticesOfFace(faceAfter, self.verticesAfter)


        #First row of matrix
        r1 = [y1[0], y2[0], y3[0]]
        r1Res = self.solveThree(x1, x2, x3, r1)

        #Second row of matrix
        r2 = [y1[1], y2[1], y3[1]]
        r2Res = self.solveThree(x1, x2, x3, r2)
        
        part1 = list(r1Res[0:2])
        part2 = list(r2Res[0:2])


        matrix = [part1, part2]
        return matrix


    def getSingularValues(self, faceBefore:List[int], faceAfter=List[int]):
        matrix = self.getTransformationMatrix(faceBefore, faceAfter)

        a = matrix[0][0]
        b = matrix[0][1]
        c = matrix[1][0]
        d = matrix[1][1]

        firstArg = math.sqrt(math.pow(b+c , 2) + math.pow(a-d, 2))
        secondArg = math.sqrt(math.pow(b-c , 2) + math.pow(a+d, 2))

        o1 = 0.5 * abs(firstArg - secondArg)
        o2 = 0.5 * abs(firstArg + secondArg)

        return o1, o2


    def calculateDistortions(self):
        """Calculates the distortion of the whole object and for every triangle"""

        allAreas = {}

        for index, faceBefore in enumerate(self.facesBefore):
            allAreas[index] = faceToArea(faceBefore, self.verticesBefore)

        self.totalDistortion = 0
        self.totalDistortionWholeObject = 0
        totalArea = sum(list(allAreas.values()))

        for index, faceAfter in enumerate(self.facesAfter):
            
            try:
                dist = self.getDistortion(self.facesBefore[index], faceAfter)
                if math.isnan(dist) or math.isinf(dist):
                    dist = 1000
            except Exception as e:
                dist = 1000

            self.distortions[index] = dist

            if index % 2000 == 0 and index > 0: log(str(round(100*index/len(self.facesAfter), 2))
                + "% (" + str(index) + "/" + str(len(self.facesAfter)) + ")")


            weight = allAreas[index] / totalArea
            dist1 = self.distortions[index] * weight
            self.totalDistortion += dist1

            weight2 = allAreas[index] / self.wholeObjectArea
            dist2 = self.distortions[index] * weight2
            self.totalDistortionWholeObject += dist2

        log(str(self.option) + " avg dist: " + str(self.totalDistortion))
        log(str(self.option) + " avg dist rounded: " + str(round(self.totalDistortion, 4)))
        log(str(self.option) + " min dist: " + str(min(self.distortions.values())))
        log(str(self.option) + " max dist: " + str(max(self.distortions.values())))

        return self.distortions, self.totalDistortion

    
    def distortionToColor(self, distortion:float):
        minD, maxD = self.option.getMinMax()
        if distortion > maxD: distortion = maxD
        dist = abs(distortion-minD) / abs(maxD-minD)

        color = self.option.getColor()
        r, g, b = color

        stepSizeR = (255-r) * dist
        stepSizeG = (255-g) * dist
        stepSizeB = (255-b) * dist
        
        colorFacR = int(round(stepSizeR, 0))
        colorFacG = int(round(stepSizeG, 0))
        colorFacB = int(round(stepSizeB, 0))
            
        color = '#%02x%02x%02x' % (255-colorFacR, 255-colorFacG, 255-colorFacB)
        return color

    def getColors(self):
        """Returns a list of colors where the indexes correspond to the indexes in the faces list"""
        if not self.colors:
            for index, _ in enumerate(self.facesAfter):
                self.colors[index] = self.distortionToColor(self.distortions[index])

        return self.colors

    def getDistortion(self, faceBefore:List[int], faceAfter=List[int]):
        """Implements the concrete formula of the distortion"""
        return -1
