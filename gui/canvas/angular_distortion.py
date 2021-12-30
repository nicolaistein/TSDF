from tkinter import *
from typing import List
import numpy as np
import math


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)

    result = np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

    if result < 0:
        print("result negative: " + str(result))
        result = 180 + result
    
    if result > 90:
        result = 180-result

    return result

def subtract(p1:List[float], p2:List[float]):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    z = p1[2] - p2[2] if len(p1) == 3 else 0
    return [x, y, z]

def getAngles(a:List[float], b:List[float], c:List[float], debug:bool=False):
    ab = subtract(a, b)
    ac = subtract(a, c)
    bc = subtract(b, c)

    angle1 = angle_between(ab, ac)
    angle2 = angle_between(ac, bc)
    angle3 = angle_between(bc, ab)

    if debug:
        print("faceToAngles ab: " + str(ab) + ", ac: " + str(ac) + ", bc: " + str(bc))
        print("faceToAngles angle1: " + str(angle1) + ", angle2: " + str(angle2) + ", angle3: " + str(angle3))

    return angle1, angle2, angle3

def faceToAngles(face, points, debug:bool=False):
    indexX = face[0]-1
    indexY = face[1]-1
    indexZ = face[2]-1
    a1, a2, a3 = getAngles(points[indexX], points[indexY], points[indexZ], debug)
    if debug:
        print("face: " + str(face))
        print("faceToAngles a1: " + str(a1) + ", a2: " + str(a2) + ", a3: " + str(a3))
    return a1, a2, a3

def perm(a1, a2, a3, b1, b2, b3):
    return abs(b1-a1) + abs(b2-a2) + abs(b3-a3)

def compute(pointsBefore:List[List[float]], pointsAfter:List[List[float]], facesBefore:List[List[int]], facesAfter:List[List[int]]):
    print("compute angular distortion: before=" + str(len(pointsBefore))
     + ", after=" + str(len(pointsAfter))
      + ", facesBefore=" + str(len(facesBefore))
       + ", facesAfter=" + str(len(facesAfter)))

    distortions = {}
    maxDistortion = 0
    minDistortion = 1000000
    total = 0
    for index, face in enumerate(facesAfter):
        a1, a2, a3 = faceToAngles(facesBefore[index], pointsBefore)
        b1, b2, b3 = faceToAngles(facesAfter[index], pointsAfter, False)

        e11 = perm(a1, a2, a3, b1, b2, b3)
        e12 = perm(a1, a3, a2, b1, b2, b3)
        e21 = perm(a2, a1, a3, b1, b2, b3)
        e22 = perm(a2, a3, a1, b1, b2, b3)
        e31 = perm(a3, a1, a2, b1, b2, b3)
        e32 = perm(a3, a2, a1, b1, b2, b3)
        dist = e11 if len(pointsBefore) == len(pointsAfter) else min(e11, e12, e21, e21, e31, e32)
        dist = dist / 3

        if math.isnan(dist): continue
            
        distortions[index] = dist
        total += dist

        if dist > maxDistortion:
            maxDistortion = dist
        if dist < minDistortion:
            minDistortion = dist

    avg = total/len(list(distortions))


    print("min angular distortion: " + str(minDistortion))
    print("max angular distortion: " + str(maxDistortion))
    print("average angular distortion: " + str(avg))
    return distortions, avg