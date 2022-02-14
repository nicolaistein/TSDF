import math
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
    indexX = face[0]
    indexY = face[1]
    indexZ = face[2]
    return triangleArea(points[indexX], points[indexY], points[indexZ])

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors v1 and v2"""
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0: return 0
    v1_u = v1 / norm1
    v2_u = v2 / norm2
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def doIntersect(p1:List[float], p2:List[float], p3:List[float], p4:List[float], shouldLog:bool=False):
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

    xVals1 = sorted([x1, x2])
    yVals1 = sorted([y1, y2])
    xVals2 = sorted([x3, x4])
    yVals2 = sorted([y3, y4])

    if bottom == 0: 
        if (x2-x1) == 0 and (x4-x3) == 0:
            b1 = yVals1[1] >= yVals2[0] and yVals1[1] <=yVals2[1]
            b2 = yVals1[0] >= yVals2[0] and yVals1[0] <=yVals2[1]
            b3 = yVals2[1] >= yVals1[0] and yVals2[1] <=yVals1[1]
            b4 = yVals2[0] >= yVals1[0] and yVals2[0] <=yVals1[1]

            if x1 == x3:
#                log("Error1 applicable")

                return (b1 or b2 or b3 or b4) and x1 == x3
        
        if (y4-y3) == 0 and (y2-y1) == 0:
            if y1 == y3:
#                log("Error2 applicable")
                b1 = xVals1[1] >= xVals2[0] and xVals1[1] <=xVals2[1]
                b2 = xVals1[0] >= xVals2[0] and xVals1[0] <=xVals2[1]
                b3 = xVals2[1] >= xVals1[0] and xVals2[1] <=xVals1[1]
                b4 = xVals2[0] >= xVals1[0] and xVals2[0] <=xVals1[1]
                return (b1 or b2 or b3 or b4) and y1 == y3

#        log("ERROR BOTTOM IS 0")
#        log("p1: " + str(p1) + ", p2: " + str(p2))
#        log("p3: " + str(p3) + ", p4: " + str(p4))
        return False

    xInter = round(xTop/bottom, 6)
    yInter = round(yTop/bottom, 6)


    insideFirstX = xInter >= round(xVals1[0], 6) and xInter <= round(xVals1[1], 6)
    insideFirstY = yInter >= round(yVals1[0], 6) and yInter <= round(yVals1[1], 6)
    insideSecX = xInter >= round(xVals2[0], 6) and xInter <= round(xVals2[1], 6)
    insideSecY = yInter >= round(yVals2[0], 6) and yInter <= round(yVals2[1], 6)

    res = insideFirstX and insideFirstY and insideSecX and insideSecY
 #   if not res and shouldLog:
 #       log("p1: " + str(p1) + ", p2: " + str(p2))
 #       log("p3: " + str(p3) + ", p4: " + str(p4))
 #       log("xInter: " + str(xInter) + ", yInter: " + str(yInter))
    return res



def getFlatTriangle(x1:List[float], x2:List[float], x3:List[float]):
    vector1 = np.array(x2)-np.array(x1)
    vector2 = np.array(x3)-np.array(x1)

    x1New = [0, 0, 1]

    length12 = np.linalg.norm(vector1)
    x2New = [length12, 0, 1]

    length23 = np.linalg.norm(vector2)
    angle = angle_between(vector1, vector2)

    x3New = [math.cos(angle) * length23, math.sin(angle) * length23, 1]
    return x1New, x2New, x3New
        