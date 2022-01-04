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
            x1 = int(split[1].split("/")[0])
            x2 = int(split[2].split("/")[0])
            x3 = int(split[3].split("/")[0])
            faces.append([x1, x2, x3])
    return faces

def executeBFF(file: str, coneCount: int):
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
    computeEnd = time.time()

    return computeEnd-computeStart, points, getPreviousVertices(algo.objPath), faces, facesBefore
