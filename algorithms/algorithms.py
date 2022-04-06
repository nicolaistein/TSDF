from functools import partial
from logger import log
from algorithms.bff.main import BFF
from algorithms.arap.arap import ARAP


def getPreviousVertices(objPath: str):
    """Extracts the vertices before the parameterization

    Args:
        objPath (str): path to mesh

    Returns:
        List[List[float]]: List of vertices
    """
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


def getFaces(objPath: str):
    """Extracts the faces before the parameterization

    Args:
        objPath (str): path to mesh

    Returns:
        List[List[int]]: List of faces
    """
    file = open(objPath)
    faces = []
    for line in file:
        if line.startswith("f"):
            while "  " in line:
                line = line.replace("  ", " ")
            split = line.split(" ")
            x1 = int(split[1].split("/")[0]) - 1
            x2 = int(split[2].split("/")[0]) - 1
            x3 = int(split[3].split("/")[0]) - 1
            faces.append([x1, x2, x3])
    return faces


def executeBFF(coneCount: int, file: str):
    return executeAlgo(BFF(coneCount, file), True)


def executeARAP(file: str):
    return executeAlgo(ARAP(file))


def executeAlgo(algo: partial, replacesFaces: bool = False):
    """executes the selected parameterization algorithm

    Args:
        algo (partial): partial of the selected algorithm
        replacesFaces (bool, optional): True if the algorithm
          also replaces the faces and not just the vertices. Defaults to True.

    Returns:
        List[List[float]]: vertices before flattening
        List[List[int]]: faces before flattening
        List[List[float]]: vertices after flattening
        List[List[int]]: faces after flattening
    """
    faces = getFaces(algo.objPath)
    facesBefore = getFaces(algo.objPath)

    # execute algorithm
    if not replacesFaces:
        points = algo.execute()
    else:
        points, faces = algo.execute()

        for index, f in enumerate(faces):
            for index2, f2 in enumerate(f):
                faces[index][index2] = f2 - 1

    return (
        getPreviousVertices(algo.objPath),
        facesBefore,
        points,
        faces,
    )
