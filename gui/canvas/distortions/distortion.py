from cmath import log
from typing import List, Mapping
import abc
import math 
import numpy as np


class Distortion:
    distortions:Mapping = {}

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

    def solveOne(self):
        pass

    def solveThree(self, p1:List[float], p2:List[float], p3:List[float], res:List[float]):
        #Test if objects are changed or copied

        A = np.array([p1, p2, p3])
        B = np.array(res)
        result = np.linalg.solve(A, B)
        log("A: " + str(A))
        log("B: " + str(B))
        log("result: " + str(result))


    def getTransformationMatrix(self, faceBefore:List[int], faceAfter=List[int]):
        """
        Returns the linear part of the tansformation matrix (2x2) with the first index being the row
        """
        x1, x2, x3 = self.getVerticesOfFace(faceBefore, self.verticesBefore)
        y1, y2, y3 = self.getVerticesOfFace(faceAfter, self.verticesAfter)


        #First row of matrix
        r1 = [y1[0], y2[0], y3[0]]
        r1Res = self.solveThree(x1, x2, x3, r1)

        #Second row of matrix
        r2 = [y1[1], y2[1], y3[1]]
        r2Res = self.solveThree(x1, x2, x3, r2)

        matrix = [r1Res[0:2], r2Res[0:2]]
        return matrix



    def getSingularValues(self, faceBefore:List[int], faceAfter=List[int]):
        matrix = self.getTransformationMatrix(faceBefore, faceAfter)

        a = matrix[0,0]
        b = matrix[0,1]
        c = matrix[1,0]
        d = matrix[1,1]

        firstArg = math.sqrt(math.pow(b+c , 2) + math.pow(a-d, 2))
        secondArg = math.sqrt(math.pow(b-c , 2) + math.pow(a+d, 2))

        o1 = 0.5 * (firstArg - secondArg)
        o2 = 0.5 * (firstArg + secondArg)

        return o1, o2


    def calculateDistortions(self):
        for index, faceAfter in enumerate(self.facesAfter):
            self.distortions[index] = self.getDistortion(self.facesBefore[index], faceAfter)

        return self.distortions


    @abc.abstractmethod
    def getDistortion(self, faceBefore:List[int], faceAfter=List[int]):
        """Implements the concrete formula of the distortion"""
        return
