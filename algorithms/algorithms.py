from algorithms.bff.main import BFF
from algorithms.arap.arap import ARAP
from algorithms.lscm.lscm import LSCM
import time

def getFaces(objPath:str):
    file = open(objPath)
    faces = []
    for line in file:
        if line.startswith("f"):
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

    # execute algorithm
    computeStart = time.time()
    if includeFaces:
        points = algo.execute()
        faces = getFaces(algo.objPath)
    else:
        points, faces = algo.execute()
    computeEnd = time.time()

    return computeEnd-computeStart, points, faces
