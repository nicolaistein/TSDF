from tkinter import Canvas
from logger import log
from typing import List, Mapping
import abc
import math 
import numpy as np
from gui.canvas.area_distortion import faceToArea


class PlottingOptionCalculator:

    def __init__(self, verticesBefore:List[List[float]], facesBefore:List[List[int]],
        verticesAfter:List[List[float]], facesAfter:List[List[int]], option, color:str):
        self.verticesBefore = verticesBefore
        self.facesBefore = facesBefore
        self.verticesAfter = verticesAfter
        self.facesAfter = facesAfter
        self.option = option
        self.color = color
        self.colors:Mapping = {}
        self.distortions:Mapping = {}
        self.totalDistortion = -1


    def getVerticesOfFace(self, face:List[int], vertices:List[List[float]]):
        v1 = vertices[face[0]]
        v2 = vertices[face[1]]
        v3 = vertices[face[2]]
        return v1, v2, v3


    def getDistortionValues(self):
        if self.totalDistortion == -1: self.calculateDistortions()
        return self.distortions, self.totalDistortion


    def solveThree(self, p1:List[float], p2:List[float], p3:List[float], res:List[float]):
        #Test if objects are changed or copied

        A = np.array([p1, p2, p3])
        B = np.array(res)
        
        try:
            result = np.linalg.solve(A, B)
#            log("linalg worked! result: " + str(result))
            return result
        except np.linalg.LinAlgError:
            log("Linalg ERROR!")
#            log("result: " + str([[1,0], [0,1]]))
            return [1, 1, 1]


    def angle_between(self, v1, v2):
        """ Returns the angle in radians between vectors v1 and v2"""

        v1_u = v1 / np.linalg.norm(v1)
        v2_u = v2 / np.linalg.norm(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))



    def getFlatTriangle(self, x1:List[float], x2:List[float], x3:List[float]):
        vector1 = np.array(x2)-np.array(x1)
        vector2 = np.array(x3)-np.array(x1)

        x1New = [0, 0, 1]

        length12 = np.linalg.norm(vector1)
        x2New = [length12, 0, 1]

        length23 = np.linalg.norm(vector2)

        angle = self.angle_between(vector1, vector2)
#        log("Angle: " + str(angle) + ", actual applied angle: " + str(math.cos(angle)))
    

        x3New = [math.cos(angle) * length23, math.sin(angle) * length23, 1]

#        log("x1: " + str(x1) + "x2: " + str(x2) + "x3: " + str(x3))
#        log("x1New: " + str(x1New) + "x2New: " + str(x2New) + "x3New: " + str(x3New))
        return x1New, x2New, x3New
        

    def getTransformationMatrix(self, faceBefore:List[int], faceAfter=List[int]):
        """Returns the linear part of the tansformation matrix (2x2)
         with the first index being the row"""
        t1, t2, t3 = self.getVerticesOfFace(faceBefore, self.verticesBefore)
        x1, x2, x3 = self.getFlatTriangle(t1, t2, t3)
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
#            log("faceBefore: " + str(faceBefore))
            allAreas[index] = faceToArea(faceBefore, self.verticesBefore)

        self.totalDistortion = 0
        totalArea = sum(list(allAreas.values()))

        for index, faceAfter in enumerate(self.facesAfter):
            self.distortions[index] = self.getDistortion(self.facesBefore[index], faceAfter)
            if index % 2000 == 0 and index > 0: log(str(round(100*index/len(self.facesAfter), 2))
                + "% (" + str(index) + "/" + str(len(self.facesAfter)) + ")")

            
            weight = allAreas[index] / totalArea
            self.totalDistortion += self.distortions[index] * weight

        log("maxDist: " + str(max(list(self.distortions.values()))))
        log("minDist: " + str(min(list(self.distortions.values()))))

#        log("distortions: " + str(self.distortions))
            
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
