from typing import List
from rectpack import *
import gui.canvas.translator as translator
import sys
from logger import log


def calc(rects, size):
    packer = newPacker(rotation=False)

    bins = [(float2dec(r[0], 3), float2dec(r[1], 3)) for r in [(size, size)]]
    bins = [(size, size)]

    dec_rects = [(float2dec(r[0], 3), float2dec(r[1], 3)) for r in rects]
    dec_rects = rects
    # Add the rectangles to packing queue
    for index, r in enumerate(dec_rects):
        packer.add_rect(*r, rid=index)

    # Add the bins where the rectangles will be placed
    for b in bins:
        packer.add_bin(*b)

    # Start packing
    packer.pack()

    return packer.rect_list()


def pack(shapes):
    rectangles = []
    for s in shapes:
        rectangles.append(shapeToRectangle(s))

    xTotal = yTotal = 0
    allWidths = []
    allHeights = []

    for x, y in rectangles:
        xTotal += x
        allWidths.append(x)
        yTotal += y
        allHeights.append(y)

    allWidths.extend(allHeights)
    size = max(allWidths)
    step = size * 0.2

    result = []
    counter = 0
    while len(result) != len(rectangles):
        result = calc(rectangles, size)
        size += step
        counter += 1

    return result


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

    width = maxX - minX
    height = maxY - minY
    if width == 0:
        width = sys._float_info.min
    if height == 0:
        height = sys._float_info.min

    return (width, height)
