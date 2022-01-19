from re import X
from typing import List
from rectpack import *
import gui.canvas.translator as translator
import sys
from logger import log


def pack(shapes):
    rectangles = []
    for s in shapes:
        rectangles.append(shapeToRectangle(s))

    xTotal = yTotal = 0

    for x, y in rectangles:
        xTotal += x
        yTotal += y

    log("x total: " + str(xTotal))
    log("y total: " + str(yTotal))

    maxT = max([xTotal, yTotal])
    minT = min([xTotal, yTotal])
    log("min: " + str(minT) + ", max: " + str(maxT))

    bins = [(minT, maxT)]

    packer = newPacker(sort_algo=SORT_DIFF, rotation=False, pack_algo=SkylineBl)

    # Add the rectangles to packing queue
    for index, r in enumerate(rectangles):
        packer.add_rect(*r, rid=index)

    # Add the bins where the rectangles will be placed
    for b in bins:
        packer.add_bin(*b)

    # Start packing
    packer.pack()

    all_rects = packer.rect_list()
    log("All rects result: " + str(all_rects))
    return all_rects

def shapeToRectangle(vertices: List[List[float]]):
    maxX = maxY = 0
    minX = minY = sys.float_info.max
    for point in vertices:
        x = point[0]
        y = point[1]

        if x < minX:
            minX = x
        if y < minY:
            minY = y
        
        if x > maxX:
            maxX = x
        if y > maxY:
            maxY = y

    return (maxX-minX, maxY-minY)
