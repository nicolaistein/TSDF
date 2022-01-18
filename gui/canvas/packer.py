from typing import List
from rectpack import newPacker
import gui.canvas.translator as translator
import sys

def pack(shapes):
    rectangles = []
    for s in shapes:
        rectangles.append(shapeToRectangle(s))

    bins = [(110, 110)]

    packer = newPacker()

    # Add the rectangles to packing queue
    for index, r in enumerate(rectangles):
        packer.add_rect(*r, rid=index)

    # Add the bins where the rectangles will be placed
    for b in bins:
        packer.add_bin(*b)

    # Start packing
    packer.pack()

    all_rects = packer.rect_list()
    print("All result: " + str(all_rects))
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
