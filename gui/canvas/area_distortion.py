from tkinter import *
from typing import List
import numpy as np
from logger import log

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

def compute(pointsBefore:List[List[float]], pointsAfter:List[List[float]], facesBefore:List[List[int]], facesAfter:List[List[int]]):
    log("compute area distortion: before=" + str(len(pointsBefore))
     + ", after=" + str(len(pointsAfter))
      + ", facesBefore=" + str(len(facesBefore))
       + ", facesAfter=" + str(len(facesAfter)))

    distortionsAVG = {}
    maxDistortion = 0
    minDistortion = 1000000
    totalAVG = 0
    for index, face in enumerate(facesAfter):
        areaBefore = faceToArea(facesBefore[index], pointsBefore)
        areaAfter = faceToArea(facesAfter[index], pointsAfter)
        
        if areaBefore == 0: continue

        distAVG = areaAfter / areaBefore
        distortionsAVG[index] = distAVG
        totalAVG += distAVG

        if totalAVG > maxDistortion:
            maxDistortion = totalAVG
        if totalAVG < minDistortion:
            minDistortion = totalAVG

    avg = totalAVG/len(distortionsAVG)

    log("min area distortion: " + str(minDistortion))
    log("max area distortion: " + str(maxDistortion))
    log("average area distortion: " + str(avg))
    return distortionsAVG, avg