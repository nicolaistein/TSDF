from typing import List
from algorithms.segmentation.data_parser import SegmentationParser

filename = "features.txt"

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



