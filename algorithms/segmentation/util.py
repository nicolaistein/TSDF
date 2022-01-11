from typing import List
from algorithms.segmentation.data_parser import SegmentationParser

filename = "features.txt"
separator = "#"

def saveMarkedFeatures(features:List[int], parser:SegmentationParser):
    file = open(filename, "w")
    for edge in features:
        v = parser.edgeToVertices[edge]
        file.write(str(edge) + "#" + str(v[0]) + "#" + str(v[1]) + "\n")

    file.close()

def loadMarkedFeatures():
    file = open("features.txt", "r")
    vertices = []
    for line in file:
        vertices.append(int(line.split("#")[0]))
    return vertices

# def saveMarkedFeatures(features:List[int]):
    file = open(filename, "w")
    for k1, k2 in features:
        file.write(str(k1) + separator + str(k2) + "\n")

    file.close()

# def loadMarkedFeatures():
    file = open(filename, "r")
    vertices = []
    for line in file:
        split = line.split(separator)
        vertices.append([int(split[0]), int(split[1])])
    return vertices


