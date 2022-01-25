from tkinter import Canvas
from logger import log
from typing import List, Mapping
import abc
import math 
import numpy as np
from gui.canvas.area_distortion import faceToArea


class PlottingOptionCalculator:
    distortions:Mapping = {}
    totalDistortion = -1

    def __init__(self, verticesBefore:List[List[float]], facesBefore:List[List[int]],
        verticesAfter:List[List[float]], facesAfter:List[List[int]]):
        self.verticesBefore = verticesBefore
        self.facesBefore = facesBefore
        self.verticesAfter = verticesAfter
        self.facesAfter = facesAfter


    def getVerticesOfFace(self, face:List[int], vertices:List[List[float]]):
        v1 = vertices[face[0]]
        v2 = vertices[face[1]]
        v3 = vertices[face[2]]
        return v1, v2, v3


    def getDistortionValues(self):
        if self.totalDistortion == -1: self.calculateDistortions()
        return self.distortions, self.totalDistortion

    def solveSix(self, p1:List[float], p2:List[float], p3:List[float], p4:List[float], p5:List[float], p6:List[float], res:List[float]):
        #Test if objects are changed or copied

        A = np.array([p1, p2, p3, p4, p5, p6])
        B = np.array(res)
        log("A: " + str(A))
        log("B: " + str(B))
        try:
            result = np.linalg.solve(A, B)
            log("result: " + str(result))
            return result
        except np.linalg.LinAlgError:
            log("Linalg ERROR!")
#            log("result: " + str([[1,0], [0,1]]))
            return [1, 1, 1]



    def solveThree(self, p1:List[float], p2:List[float], p3:List[float], res:List[float]):
        #Test if objects are changed or copied

        A = np.array([p1, p2, p3])
        B = np.array(res)
        log("A: " + str(A))
        log("B: " + str(B))
        try:
            result = np.linalg.solve(A, B)
            log("result: " + str(result))
            return result
        except np.linalg.LinAlgError:
            log("Linalg ERROR!")
#            log("result: " + str([[1,0], [0,1]]))
            return [1, 1, 1]


    def getTransformationMatrix(self, faceBefore:List[int], faceAfter=List[int]):
        """Returns the linear part of the tansformation matrix (2x2)
         with the first index being the row"""
        x1, x2, x3 = self.getVerticesOfFace(faceBefore, self.verticesBefore)
        y1, y2, y3 = self.getVerticesOfFace(faceAfter, self.verticesAfter)

        log("vertices after: " + str(self.verticesAfter))


        #First row of matrix
        r1 = [y1[0], y2[0], y3[0]]
        r1Res = self.solveThree(x1, x2, x3, r1)

        #Second row of matrix
        r2 = [y1[1], y2[1], y3[1]]
        r2Res = self.solveThree(x1, x2, x3, r2)
        


        #-----------------------Tests

#        r3 = [y1[2], y2[2], y3[2]]
#        r3Res = self.solveThree(x1, x2, x3, r3)

#        q1 = list(r1Res)
#        q2 = list(r2Res)
#        q3 = list(r3Res)
#        wholeTMatrix = [q1, q2, q3]
#        log("MATRIX: " + str(wholeTMatrix))

        #-----------------------Tests




        part1 = list(r1Res[0:2])
        part2 = list(r2Res[0:2])

        log("part1: " + str(part1))
        log("part2: " + str(part2))

        matrix = [part1, part2]
        log("result matrix: " + str(matrix))
        return matrix


    def getSingularValues(self, faceBefore:List[int], faceAfter=List[int]):
        matrix = self.getTransformationMatrix(faceBefore, faceAfter)
        log("matrix: " + str(matrix))

        a = matrix[0][0]
        b = matrix[0][1]
        c = matrix[1][0]
        d = matrix[1][1]

        log("a: " + str(a))
        log("b: " + str(b))
        log("c: " + str(c))
        log("d: " + str(d))

        firstArg = math.sqrt(math.pow(b+c , 2) + math.pow(a-d, 2))
        secondArg = math.sqrt(math.pow(b-c , 2) + math.pow(a+d, 2))

        o1 = 0.5 * (firstArg - secondArg)
        o2 = 0.5 * (firstArg + secondArg)

        return o1, o2


    def calculateDistortions(self):
        """Calculates the distortion of the whole object and for every triangle"""

        allAreas = {}
        totalArea = sum(list(allAreas.values()))
            
        log("verticesBefore length: " + str(len(self.verticesBefore)))

        for index, faceBefore in enumerate(self.facesBefore):
            log("faceBefore: " + str(faceBefore))
            allAreas[index] = faceToArea(faceBefore, self.verticesBefore)

        self.totalDistortion = 0

        for index, faceAfter in enumerate(self.facesAfter):
            self.distortions[index] = self.getDistortion(self.facesBefore[index], faceAfter)
            weight = allAreas[index] / totalArea
            self.totalDistortion += self.distortions[index] * weight

        log("maxDist: " + str(max(list(self.distortions.values()))))
        log("minDist: " + str(min(list(self.distortions.values()))))

        log("distortions: " + str(self.distortions))
            
        return self.distortions, self.totalDistortion

    def getColors(self):
        """Returns a list of colors where the indexes correspond to the indexes in the faces list"""
        return []

    @abc.abstractmethod
    def getDistortion(self, faceBefore:List[int], faceAfter=List[int]):
        """Implements the concrete formula of the distortion"""
        return
