from logger import log
from algorithms.bff.main import BFF
from algorithms.arap.arap import ARAP
from algorithms.lscm.lscm import LSCM
import time
import os
import igl

def getPreviousVertices(objPath:str):
    file = open(objPath)
    vertices = []
    for line in file:
        if line.startswith("v "):
            while "  " in line: 
                line = line.replace("  ", " ")
            split = line.split(" ")
            x1 = float(split[1])
            x2 = float(split[2])
            x3 = float(split[3])
            vertices.append([x1, x2, x3])
    return vertices

def getFaces(objPath:str):
    file = open(objPath)
    faces = []
    for line in file:
        if line.startswith("f"):
            while "  " in line: 
                line = line.replace("  ", " ")
            split = line.split(" ")
            x1 = int(split[1].split("/")[0])-1
            x2 = int(split[2].split("/")[0])-1
            x3 = int(split[3].split("/")[0])-1
            faces.append([x1, x2, x3])
    return faces

def executeBFF(coneCount: int, file: str):
    return executeAlgo(BFF(coneCount, file), False)

def executeLSCM(file: str):
    return executeAlgo(LSCM(file))

def executeARAP(file: str):
    return executeAlgo(ARAP(file))

def executeAlgo(algo, includeFaces:bool=True):

    faces = getFaces(algo.objPath)
    facesBefore = getFaces(algo.objPath)

    # execute algorithm
    computeStart = time.time()
    if includeFaces:
        points = algo.execute()
    else:
        points, faces = algo.execute()

        for index, f in enumerate(faces):
            for index2, f2 in enumerate(f):
                faces[index][index2] = f2-1

    computeEnd = time.time()

    return computeEnd-computeStart, points, getPreviousVertices(algo.objPath), faces, facesBefore
    
"""
    max = -300
    min = 100000000000000000000
    for f in faces:
        for f2 in f:
            if f2 < min: min = f2
            if f2 > max: max = f2 

    log("faces min: " + str(min) + ", max: " + str(max))


    max = -300
    min = 100000000000000000000
    for f in facesBefore:
        for f2 in f:
            if f2 < min: min = f2
            if f2 > max: max = f2 

    log("facesBefore min: " + str(min) + ", max: " + str(max))
"""

