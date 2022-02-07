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
    indexX = face[0]
    indexY = face[1]
    indexZ = face[2]
    return triangleArea(points[indexX], points[indexY], points[indexZ])

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors v1 and v2"""

    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def doIntersect(p1:List[float], p2:List[float], p3:List[float], p4:List[float]):
    """Calculates whether the line from p1 to p2 intersects with the line from p3 to p4"""
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    x3 = p3[0]
    y3 = p3[1]
    x4 = p4[0]
    y4 = p4[1]

    xTop = (x2-x1)*(x3*y4-y3*x4)-(x4-x3)*(x1*y2-y1*x2)
    yTop = (y2-y1)*(x3*y4-y3*x4)-(y4-y3)*(x1*y2-y1*x2)
    bottom = (x2-x1)*(y4-y3)-(y2-y1)*(x4-x3)

    if bottom == 0: return False

    xInter = xTop/bottom
    yInter = yTop/bottom

    xVals1 = sorted([x1, x2])
    yVals1 = sorted([y1, y2])
    xVals2 = sorted([x3, x4])
    yVals2 = sorted([y3, y4])

    insideFirstX = xInter >= xVals1[0] and xInter <= xVals1[1]
    insideFirstY = yInter >= yVals1[0] and yInter <= yVals1[1]
    insideSecX = xInter >= xVals2[0] and xInter <= xVals2[1]
    insideSecY = yInter >= yVals2[0] and yInter <= yVals2[1]

    return insideFirstX and insideFirstY and insideSecX and insideSecY