from tkinter import *
from typing import List
import numpy as np
from logger import log

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