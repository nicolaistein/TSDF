import math
from typing import List
import numpy as np
from logger import log


def subtract(p1: List[float], p2: List[float]):
    """Creates a vector out of two 2 or 3 dimensional points

    Args:
        p1 (List[float]): point 1
        p2 (List[float]): point 2

    Returns:
        List[float]: 3 dimensional vector
    """
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    z = p1[2] - p2[2] if len(p1) == 3 else 0
    return [x, y, z]


def triangleArea(a: List[float], b: List[float], c: List[float]):
    """Computes the area of a triangle

    Args:
        a (List[float]): corner point 1
        b (List[float]): corner point 2
        c (List[float]): corner point 3

    Returns:
        float: Triangle area
    """
    ab = subtract(a, b)
    ac = subtract(a, c)
    cross = np.cross(np.array(ab), np.array(ac))

    norm = np.linalg.norm(np.array(cross))
    return 0.5 * norm


def faceToArea(face: List[int], points: List[List[float]]):
    """Calculates the area of a given face

    Args:
        face (List[int]): list that contains the indices of the three corner points
        points (List[List[float]]): a list of points

    Returns:
        float: the face area
    """
    indexX = face[0]
    indexY = face[1]
    indexZ = face[2]
    return triangleArea(points[indexX], points[indexY], points[indexZ])


def angle_between(v1: List[float], v2: List[float]):
    """Returns the angle in radians between two vectors

    Args:
        v1 (List[float]): vector 1
        v2 (List[float]): vector 2

    Returns:
        float: resulting angle
    """
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0
    v1_u = v1 / norm1
    v2_u = v2 / norm2
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def isFirstBigger(val1: float, val2: float, neighboring: bool):
    if neighboring:
        return val1 > val2
    else:
        return val1 >= val2


def doIntersect(
    p1: List[float],
    p2: List[float],
    p3: List[float],
    p4: List[float],
    neighboring: bool = False,
):
    """Checks if two lines intersect

    Args:
        p1 (List[float]): Start point of line 1
        p2 (List[float]): End point of line 1
        p3 (List[float]): Start point of line 2
        p4 (List[float]): End point of line 2
        neighboring (bool, optional): True if the lines have one endpoint in common. Defaults to False.

    Returns:
        bool: intersection result
    """

    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    x3 = p3[0]
    y3 = p3[1]
    x4 = p4[0]
    y4 = p4[1]
    n = neighboring

    xTop = (x2 - x1) * (x3 * y4 - y3 * x4) - (x4 - x3) * (x1 * y2 - y1 * x2)
    yTop = (y2 - y1) * (x3 * y4 - y3 * x4) - (y4 - y3) * (x1 * y2 - y1 * x2)
    bottom = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)

    xVals1 = sorted([x1, x2])
    yVals1 = sorted([y1, y2])
    xVals2 = sorted([x3, x4])
    yVals2 = sorted([y3, y4])

    # At least one line is vertical or horizontal
    if bottom == 0:

        # Line is vertical
        if (x2 - x1) == 0 and (x4 - x3) == 0:
            b1 = isFirstBigger(yVals1[1], yVals2[0], n) and isFirstBigger(
                yVals2[1], yVals1[1], n
            )
            b2 = isFirstBigger(yVals1[0], yVals2[0], n) and isFirstBigger(
                yVals2[1], yVals1[0], n
            )
            b3 = isFirstBigger(yVals2[1], yVals1[0], n) and isFirstBigger(
                yVals1[1], yVals2[1], n
            )
            b4 = isFirstBigger(yVals2[0], yVals1[0], n) and isFirstBigger(
                yVals1[1], yVals2[0], n
            )

            if x1 == x3:
                return (b1 or b2 or b3 or b4) and x1 == x3

        # Line is horizontal
        if (y4 - y3) == 0 and (y2 - y1) == 0:
            if y1 == y3:
                b1 = isFirstBigger(xVals1[1], xVals2[0], n) and isFirstBigger(
                    xVals2[1], xVals1[1], n
                )
                b2 = isFirstBigger(xVals1[0], xVals2[0], n) and isFirstBigger(
                    xVals2[1], xVals1[0], n
                )
                b3 = isFirstBigger(xVals2[1], xVals1[0], n) and isFirstBigger(
                    xVals1[1], xVals2[1], n
                )
                b4 = isFirstBigger(xVals2[0], xVals1[0], n) and isFirstBigger(
                    xVals1[1], xVals2[0], n
                )
                return (b1 or b2 or b3 or b4) and y1 == y3

        return False

    xInter = round(xTop / bottom, 6)
    yInter = round(yTop / bottom, 6)

    insideFirstX = isFirstBigger(xInter, round(xVals1[0], 6), n) and isFirstBigger(
        round(xVals1[1], 6), xInter, n
    )
    insideFirstY = isFirstBigger(yInter, round(yVals1[0], 6), n) and isFirstBigger(
        round(yVals1[1], 6), yInter, n
    )
    insideSecX = isFirstBigger(xInter, round(xVals2[0], 6), n) and isFirstBigger(
        round(xVals2[1], 6), xInter, n
    )
    insideSecY = isFirstBigger(yInter, round(yVals2[0], 6), n) and isFirstBigger(
        round(yVals2[1], 6), yInter, n
    )

    res = insideFirstX and insideFirstY and insideSecX and insideSecY
    return res


def getFlatTriangle(x1: List[float], x2: List[float], x3: List[float]):
    """Flattens a single triangle

    Args:
        x1 (List[float]): corner point 1
        x2 (List[float]): corner point 2
        x3 (List[float]): corner point 3

    Returns:
        List[float], List[float], List[float]: corner points of flattened triangle
    """
    vector1 = np.array(x2) - np.array(x1)
    vector2 = np.array(x3) - np.array(x1)

    x1New = [0, 0, 1]

    length12 = np.linalg.norm(vector1)
    x2New = [length12, 0, 1]

    length23 = np.linalg.norm(vector2)
    angle = angle_between(vector1, vector2)

    x3New = [math.cos(angle) * length23, math.sin(angle) * length23, 1]
    return x1New, x2New, x3New
