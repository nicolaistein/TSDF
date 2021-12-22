from algorithms.bff.main import BFF
#from algorithms.arap.arap import ARAP
#from algorithms.lscm.lscm import LSCM
import time


def executeBFF(file: str, coneCount: int):
    return executeAlgo(BFF(coneCount, file))


def executeLSCM(file: str):
    return executeAlgo(LSCM(file))


def executeARAP(file: str):
    return executeAlgo(ARAP(file))


def executeAlgo(algo):

    # execute algorithm
    computeStart = time.time()
    points = algo.execute()
    computeEnd = time.time()

    return computeEnd-computeStart, points
