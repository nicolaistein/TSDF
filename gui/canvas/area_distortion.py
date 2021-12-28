from tkinter import *
from typing import List
import numpy as np

def subtract(p1:List[float], p2:List[float]):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    z = p1[2] - p2[2] if len(p1) == 3 else 0
    return [x, y, z]

def triangleArea(a:List[float], b:List[float], c:List[float]):
    ab = subtract(a, b)
    ac = subtract(a, c)
    cross = np.cross(np.array(ab), np.array(ac))

    norm = np.linalg.norm(np.array(cross))
    return 0.5 * norm

def faceToArea(face, points):
    indexX = face[0]-1
    indexY = face[1]-1
    indexZ = face[2]-1
    return triangleArea(points[indexX], points[indexY], points[indexZ])

def computeDistortions(pointsBefore:List[List[float]], pointsAfter:List[List[float]], facesBefore:List[int], facesAfter:List[int]):
    print("computeDistortion: before=" + str(len(pointsBefore))
     + ", after=" + str(len(pointsAfter))
      + ", facesBefore=" + str(len(facesBefore))
       + ", facesAfter=" + str(len(facesAfter)))

    distortions = []
    maxDistortion = 0
    minDistortion = 10000
    for index, face in enumerate(facesAfter):
        areaBefore = faceToArea(facesBefore[index], pointsBefore)
        areaAfter = faceToArea(facesAfter[index], pointsAfter)

        dist = areaBefore / areaAfter if areaBefore >= areaAfter else areaAfter / areaBefore
        distortions.append(dist)
        if dist > maxDistortion:
            maxDistortion = dist
        if dist < minDistortion:
            minDistortion = dist

    return distortions