from typing import List

filename = "features.txt"
separator = "#"

def saveMarkedFeatures(features:List[int]):
    file = open(filename, "w")
    for k1, k2 in features:
        file.write(str(k1) + separator + str(k2) + "\n")

    file.close()

def getMarkedFeatures():
    file = open(filename, "r")
    vertices = []
    for line in file:
        split = line.split(separator)
        vertices.append([int(split[0]), int(split[1])])

