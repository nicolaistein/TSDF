from algorithms.bff.main import *
import sys


def scale(points, targetSize):
    maxX = 0
    maxY = 0
    for point in points:
        x = point[0]
        y = point[1]
        if(maxX < x):
            maxX = x
        if(maxY < y):
            maxY = y

    scale = 1
    if(maxX > maxY):
        scale = targetSize / maxX
    else:
        scale = targetSize / maxY

    for point in points:
        point[0] *= scale
        point[1] *= scale

    return scale, points


def moveToPositiveArea(points):
    minX = sys.float_info.max
    minY = sys.float_info.max
    for point in points:
        x = point[0]
        y = point[1]
        if(minX > x):
            minX = x
        if(minY > y):
            minY = y

    if minX < 0:
        minX *= -1
        for point in points:
            point[0] += minX

    if minY < 0:
        minY *= -1
        for point in points:
            point[1] += minY

    return points
