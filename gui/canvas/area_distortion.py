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

def compute(pointsBefore:List[List[float]], pointsAfter:List[List[float]], facesBefore:List[List[int]], facesAfter:List[List[int]]):
    print("compute area distortion: before=" + str(len(pointsBefore))
     + ", after=" + str(len(pointsAfter))
      + ", facesBefore=" + str(len(facesBefore))
       + ", facesAfter=" + str(len(facesAfter)))

    distortions = []
    distortionsAVG = []
    maxDistortion = 0
    minDistortion = 1000000
    total = 0
    totalAVG = 0
    for index, face in enumerate(facesAfter):
        areaBefore = faceToArea(facesBefore[index], pointsBefore)
        areaAfter = faceToArea(facesAfter[index], pointsAfter)

        dist = areaBefore / areaAfter if areaBefore >= areaAfter else areaAfter / areaBefore
        distAVG = areaAfter / areaBefore

        distortions.append(dist)
        total += dist
        
        distortionsAVG.append(distAVG)
        totalAVG += distAVG

        if dist > maxDistortion:
            maxDistortion = dist
        if dist < minDistortion:
            minDistortion = dist

    avg = totalAVG/len(distortionsAVG)

    print("min area distortion: " + str(minDistortion))
    print("max area distortion: " + str(maxDistortion))
    print("average area distortion: " + str(avg))
    print("TRUE average area distortion: " + str(totalAVG / len(distortionsAVG)))
    return distortions, distortionsAVG, avg